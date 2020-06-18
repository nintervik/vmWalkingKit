from maya import cmds
import os
import json
from collections import OrderedDict
import logging

# Set up logger
logger = logging.getLogger('WalkLibraryUI')
logger.setLevel(logging.INFO)
logging.basicConfig()

# Query C:\Users\userName\Documents\maya
USER_APP_DIR = cmds.internalVar(userAppDir=True)

# Generate presets path C:\Users\userName\Documents\maya\vmWalkingKitPresets
PARENT_DIRECTORY = os.path.join(USER_APP_DIR, 'vmWalkingKitData')
DIRECTORY = os.path.join(PARENT_DIRECTORY, 'vmWalkingKitPresets')
TEXT_DIR = os.path.join(PARENT_DIRECTORY, 'vmWalkingKitTextFiles')

# Set the name for the default preset JSON file and UI text data files
DEFAULT_PRESET_NAME = 'defaultPreset.json'
PARAM_TEXT_NAME = 'paramText.json'
TAB_TEXT_NAME = 'tabText.json'

# Set the default preset file path
FILE_PATH = os.path.join(DIRECTORY, DEFAULT_PRESET_NAME)
USER_PREFS_PATH = os.path.join(PARENT_DIRECTORY, 'vmWKUserPrefs.json')
IMG_DIR = os.path.join(PARENT_DIRECTORY, 'startupImg.png')


class WalkLibrary(object):
    """
    This class manages all the stuff related to animation layers and presets.
    """

    def __init__(self, createDefaultPreset=False):

        """
        Init method. Here we create the directory to save the presets and reset everything to
        default by reading from the 'defaultPreset.json' file.
        """

        self.createDirectory()

        # Only call this to generate the defaultPreset.json the first time
        if createDefaultPreset:
            self.savePreset()

        # Setting playback range to the max frames needed
        self.setPlaybackOptions(24)

    # ANIMATION LAYERS METHODS

    def changeLayerMuteState(self, layerNameToChange, mute):
        """
        Change the muted state of the given animation layer if this exists
        Args:
            layerNameToChange(str): the animation layer name to change
            mute(bool): mute state that will be applied to the given layer
        """

        # If the queried animation layer exists it will be muted
        if cmds.animLayer(layerNameToChange, query=True, exists=True):

            wasPlaying = False

            # Stop playback before doing any animation layer operation
            if cmds.play(query=True, state=True):
                cmds.play(state=False)
                wasPlaying = True

            # Change layer mute state
            cmds.animLayer(layerNameToChange, edit=True, mute=mute)

            if layerNameToChange == 'UpDown_1' and cmds.animLayer('UpDown_1', query=True, lock=True):
                cmds.animLayer('UpDown_1', edit=True, lock=False)

            # Once the operations have finished begin playback (only if it was playing before)
            if wasPlaying:
                cmds.play(state=True)
        else:
            logger.debug(layerNameToChange + " not found!")

    def changeLayerWeight(self, layerNameToChange, weight):
        """
        Change the weight of the given animation layer if this exists
        Args:
            layerNameToChange(str): the animation layer name to change
            weight(float): weight that will be set to the given layer
        """

        # If the queried animation layer exists it will be muted
        if cmds.animLayer(layerNameToChange, query=True, exists=True):

            wasPlaying = False

            # Stop playback before doing any animation layer operation
            if cmds.play(query=True, state=True):
                cmds.play(state=False)
                wasPlaying = True

            # Change layer weight
            cmds.animLayer(layerNameToChange, edit=True, weight=weight)

            # Once the operations have finished begin playback (only if it was playing before)
            if wasPlaying:
                cmds.play(state=True)
        else:
            logger.debug(layerNameToChange + " not found!")

    def getCurrentAnimationLayers(self):
        """
        Finds all the current existing animation layers in the scene.

        Returns: returns two lists. One with all the current existing layers names in the
        scene (except the base animation layer) and the other one with their weights.
        """

        # Query animation layers in the scene
        baseAnimationLayer = cmds.animLayer(query=True, root=True)
        childLayers = cmds.animLayer(baseAnimationLayer, query=True, children=True)

        weights = []
        layersToRemove = []

        # Store the weights if the layers are not corrective (they are just used to correct animations not as parameters)
        for i in range(0, len(childLayers)):
            if "Corrective" not in childLayers[i]:
                weights.append(cmds.animLayer(childLayers[i], query=True, weight=True))
            else:
                layersToRemove.append(childLayers[i])

        sizeToRemove = len(layersToRemove)

        # Remove layers that are corrective from the childLayers list
        for i in range(0, sizeToRemove):
            childLayers.remove(layersToRemove[i])

        return childLayers, weights

    def getActiveAnimationLayers(self):
        """
        Finds all the active animation layers in the scene.

        Returns: returns a two lists. One with all the active layers names in the
        scene (except the base animation layer) and the other one with their weights.
        """

        # Query animation layers in the scene
        baseAnimationLayer = cmds.animLayer(query=True, root=True)
        childLayers = cmds.animLayer(baseAnimationLayer, query=True, children=True)

        activeLayers = []
        weights = []

        # Store the all the layer's names and their weights (except the corrective ones)
        for i in range(0, len(childLayers)):
            if not cmds.animLayer(childLayers[i], query=True, mute=True) and "Corrective" not in childLayers[i]:
                activeLayers.append(childLayers[i])
                weights.append(cmds.animLayer(childLayers[i], query=True, weight=True))

        return activeLayers, weights

    # KEYFRAMES METHODS

    def offsetKeyframes(self, attrFull, layerName, prevIndex, currIndex):
        """
        Offset the keyframes of the given animation curve to match the current body or arms beat.
        Args:
            attrFull(str): the name of the attribute to select (controllerName.attribute)
            layerName(str): the name of the layer where the keyframes to offset live.
            prevIndex(int): the index that represents the beat that we are coming from.
            currIndex(int): the index that represents the current beat.
        """

        offset = 0

        # Calculate the offset of the keyframes that need to be moved according to the current and previous index
        # of the BodyBeat parameter
        if (prevIndex == 1 and currIndex == 2) or (prevIndex == 2 and currIndex == 3):
            offset = 1
        elif (prevIndex == 2 and currIndex == 1) or (prevIndex == 3 and currIndex == 2):
            offset = -1
        elif prevIndex == 1 and currIndex == 3:
            offset = 2
        elif prevIndex == 3 and currIndex == 1:
            offset = -2

        # Select the keyframes from the animation curve of the attribute the given layer
        layerPlug = cmds.animLayer(layerName, e=True, findCurveForPlug=attrFull)
        keyframes = cmds.keyframe(layerPlug[0], q=True)

        # Select the controller
        cmds.select(attrFull.split('.')[0], r=True)
        cmds.animLayer(layerName, edit=True, selected=True, preferred=True)
        cmds.animLayer(uir=True)

        # For each of the current keyframes move them the 'offset' amount. Except for the frame 1 that will always
        # be at the same position
        for i in range(0, len(keyframes)):
            if i != 0:
                # Every time before moving, query again the current keyframes as they are now moved
                keyframes = cmds.keyframe(layerPlug[0], query=True)
                # Move the keyframes the 'offset' amount in the range from the current one to the last one
                cmds.keyframe(attrFull, edit=True, relative=True,
                              timeChange=offset, time=(keyframes[i],
                              keyframes[len(keyframes)-1]))

        # Clear the active list
        cmds.select(clear=True)

        # Deselect the layer and make it not preferred
        cmds.animLayer(layerName, edit=True, selected=False, preferred=False)

    def calculatePlaybackRange(self, indices):
        """
        Calculates and sets the playback range according to body and arms beat.
        Args:
            indices(list(int)): the indices that represent the current option selected in the drop-down for the beats
            body and arms beats.
        """

        playBackEndRange = 0

        # Find the LCM (Least Common Multiple) to set the playback range based on the body and arms beats
        if indices[0] == 1 and indices[1] == 1:
            playBackEndRange = 16
        elif (indices[0] == 1 and indices[1] == 2) or (indices[0] == 2 and indices[1] == 1):
            playBackEndRange = 48
        elif ((indices[0] == 1 and indices[1] == 3) or (indices[0] == 3 and indices[1] == 1))\
                or (indices[0] == 3 and indices[1] == 3):
            playBackEndRange = 32
        elif indices[0] == 2 and indices[1] == 2:
            playBackEndRange = 24
        elif (indices[0] == 2 and indices[1] == 3) or (indices[0] == 3 and indices[1] == 2):
            playBackEndRange = 96

        # Set de new calculated playback range
        self.setPlaybackOptions(playBackEndRange)

    def setPlaybackOptions(self, playBackEndRange):
        """
        Sets the playback end range to the given number.
        Args:
            playBackEndRange (int): the desired playback end range.
        """

        cmds.playbackOptions(animationEndTime=96)
        cmds.playbackOptions(minTime=1)
        cmds.playbackOptions(maxTime=playBackEndRange)
        cmds.playbackOptions(animationStartTime=1)

    # DATA METHODS

    def importPreset(self, filePath=FILE_PATH):
        """
        Imports the given preset into the tool.
        Args:
            filePath(str): the path from where the preset file will be loaded. If
            not specified, it will be loaded from the default path.
        """

        self.activeLayersInfo = OrderedDict()
        layers = None
        weights = None

        # Load JSON content into 'activeLayersInfo' dict
        with open(filePath, 'r') as f:
            self.activeLayersInfo = json.load(f, object_pairs_hook=OrderedDict)

        # Make sure the preset file is not empty and exists
        if self.activeLayersInfo is not None:

            # These two list will store the layers and weight from the default preset
            layers = self.activeLayersInfo.keys()
            weights = self.activeLayersInfo.values()

            # Get the all the animation layers in the scene
            childLayers, sceneWeights = self.getCurrentAnimationLayers()

            # Iterate over all the animation layers in the scene
            for i in range(0, len(childLayers)):
                # If a layer is in the default preset file it will be unmuted
                if childLayers[i] in layers:
                    self.changeLayerMuteState(childLayers[i], False)
                # If the layer is not in the default preset file it will be muted
                else:
                    self.changeLayerMuteState(childLayers[i], True)

                # For now all weights will be 0.5. Just in case the user has manually changed it
                if "ArmsBeat" in childLayers[i]:
                    self.changeLayerWeight(childLayers[i], 0.5)

            # Iterate over the layers in the default preset and set their respective weight
            for i in range(0, len(layers)):
                self.changeLayerWeight(layers[i], weights[i])
        # If the preset default file is empty or does not exist we raise a warning
        else:
            logger.error(DEFAULT_PRESET_NAME + "not found or empty.")

        return layers, weights

    def savePreset(self, filePath=DIRECTORY):
        """
        Saves the current parameters in a preset JSON file.
        Args:
            filePath(str): the path where the preset file will be stored. If
            not specified, it will be saved in the default path.
        """

        # Find all the active animation layers in the scene
        activeLayers, weights = self.getActiveAnimationLayers()

        # Create an ordered dict to store the data
        dataToWrite = OrderedDict()

        # Populate the data dictionary with the active layers and their weights
        for i in range(0, len(activeLayers)):
            dataToWrite[activeLayers[i]] = weights[i]

        # Save all the active animation layers and their weights in the JSON preset file
        with open(filePath, 'w') as f:
            json.dump(dataToWrite, f, indent=4)

    def createDirectory(self, directory=DIRECTORY):
        """
        Creates the given directory if it doesn't exist already.
        Args:
            directory(str): the directory to create.
        Returns:
            directory(str): the created directory.
        """

        if not os.path.exists(directory):
            os.mkdir(directory)

        return directory

    def getUIText(self, element):
        """
        Gets the text data for the UI.
        Args:
            element(str): type of data to be queried ("param" or "tab").
        Returns:
            textDict(dict): dictionary of the text data.
        """

        # Get the file path of the json containing the queried data type
        if element == "param":
            filePath = os.path.join(TEXT_DIR, PARAM_TEXT_NAME)
        else:
            filePath = os.path.join(TEXT_DIR, TAB_TEXT_NAME)

        textDict = OrderedDict()

        # Read the json and store the data inside textDict
        with open(filePath, 'r') as f:
            textDict = json.load(f, object_pairs_hook=OrderedDict)

        return textDict

    def getStartupWinPref(self):
        """
        Gets the current startup window preferences set by the user.
        Returns:
            startupFlag(bool): indicates whether or not the user wants the startup window at startup.
        """

        # Set the flag to false by default
        startupFlag = False

        # Read the user preferences json and store the result in startupFlag
        with open(USER_PREFS_PATH, 'r') as f:
            startupFlag = json.load(f)["SHOW_STARTUP_WIN"]

        return startupFlag

    def setStartupWinPref(self, state):
        """
        Sets the startup window user preferences.
        Args:
            state(int): indicates whether or not the user wants the startup window at startup.
        Returns:

        """

        # Workaround to compensate for Maya related problem with bools
        if state == 2:
            state = 1

        # Create an ordered dictionary with the state value
        dataToWrite = OrderedDict()
        dataToWrite["SHOW_STARTUP_WIN"] = state

        # Open the user preferences json and store dataToWrite
        with open(USER_PREFS_PATH, 'w') as f:
            json.dump(dataToWrite, f, indent=4)
