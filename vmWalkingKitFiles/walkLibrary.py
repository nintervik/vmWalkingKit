from maya import cmds
import os
import json
from collections import OrderedDict
import logging

# Set up logger
logger = logging.getLogger('WalkLibraryUI')
logger.setLevel(logging.DEBUG) # TODO: change to logging.INFO when shipping
logging.basicConfig()

# Query C:\Users\userName\Documents\maya
USER_APP_DIR = cmds.internalVar(userAppDir=True)

# Generate presets path C:\Users\userName\Documents\maya\vmWalkingKitPresets
DIRECTORY = os.path.join(USER_APP_DIR, 'vmWalkKitPresets')

# Set the name for the default preset JSON file
DEFAULT_PRESET_NAME = 'defaultPreset'

def createDirectory(directory=DIRECTORY):
    """
    Creates the given directory if it doesn't exist already.
    Args:
        directory(str): the directory to create
    """

    if not os.path.exists(directory):
        os.mkdir(directory)

class WalkLibrary(object):
    """
    This class manages all the stuff related to animation layers and presets
    """

    def __init__(self, createDefaultPreset=False):

        """
        Init method. Here we create the directory to save the presets and reset everything to
        default by reading from the 'defaultPreset.json' file.
        """
        createDirectory()

        # Only call this to generate the defaultPreset.json the first time
        if createDefaultPreset:
            self.savePreset()

        # Setting playback range to the max frames needed
        cmds.playbackOptions(animationEndTime=96)
        cmds.playbackOptions(minTime=1)
        cmds.playbackOptions(maxTime=24)
        cmds.playbackOptions(animationStartTime=1)

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

            # Once the operations have finished begin playback (only if it was playing before)
            if wasPlaying:
                cmds.play(state=True)
        else:
            print(layerNameToChange + " not found!")

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
            print(layerNameToChange + " not found!")

    def getCurrentAnimationLayers(self):
        """
        Finds all the current existing animation layers in the scene.

        Returns: returns a two lists. One with all the current existing layers in the
        scene (except the base animation layer) and the other one with their weights.
        """

        baseAnimationLayer = cmds.animLayer(query=True, root=True)
        childLayers = cmds.animLayer(baseAnimationLayer, query=True, children=True)

        weights = []

        for i in range(0, len(childLayers)):
            weights.append(cmds.animLayer(childLayers[i], query=True, weight=True))

        return childLayers, weights

    def getActiveAnimationLayers(self):
        """
        Finds all the active animation layers in the scene.

        Returns: returns a two lists. One with all the active layers in the
        scene (except the base animation layer) and the other one with their weights.
        """

        baseAnimationLayer = cmds.animLayer(query=True, root=True)
        childLayers = cmds.animLayer(baseAnimationLayer, query=True, children=True)

        activeLayers = []
        weights = []

        for i in range(0, len(childLayers)):
            if not cmds.animLayer(childLayers[i], query=True, mute=True):
                activeLayers.append(childLayers[i])
                weights.append(cmds.animLayer(childLayers[i], query=True, weight=True))

        return activeLayers, weights

    # PRESETS METHODS

    def importPreset(self, name=DEFAULT_PRESET_NAME, directory=DIRECTORY):
        """
        Imports the given preset into the tool.
        Args:
            name(str): the name of the JSON preset file. If not specified,
            the default preset will be imported.
            directory(str): the path from where the preset file will be loaded. If
            not specified, it will be loaded from the default path.
        """

        # TODO: take into account playback range settings when importing preset (as inDropDownChanged)

        # Generate directory name for the JSON preset file
        infoFile = os.path.join(directory, '%s.json' % name)

        self.activeLayersInfo = OrderedDict()

        # Load JSON content into 'activeLayersInfo' dict
        with open(infoFile, 'r') as f:
            self.activeLayersInfo = json.load(f, object_pairs_hook=OrderedDict)

        # Make sure the preset file is not empty and exists
        if self.activeLayersInfo is not None:

            # These two list will store the layers and weight from the default preset
            defaultLayers = self.activeLayersInfo.keys()
            defaultWeights = self.activeLayersInfo.values()

            # Get the all the animation layers in the scene
            childLayers, weights = self.getCurrentAnimationLayers()

            # Iterate over all the animation layers in the scene
            for i in range(0, len(childLayers)):
                # If a layer is in the default preset file it will be unmuted
                if childLayers[i] in defaultLayers:
                    self.changeLayerMuteState(childLayers[i], False)
                # If the layer is not in the default preset file it will be muted
                else:
                    self.changeLayerMuteState(childLayers[i], True)

                # For now all weights will be 1.0. Just in case the user has manually changed it
                self.changeLayerWeight(childLayers[i], 1.0)

            # Iterate over the layers in the default preset and set their respective weight
            for i in range(0, len(defaultLayers)):
                self.changeLayerWeight(defaultLayers[i], defaultWeights[i])
        # If the preset default file is empty or does not exist we raise a warning
        else:
            logger.error(DEFAULT_PRESET_NAME + "not found or empty.")

        return defaultLayers, defaultWeights

    def savePreset(self, name='defaultPreset', directory=DIRECTORY):
        """
        Saves the current parameters in a preset JSON file.
        Args:
            name(str): the name of the JSON preset file. If not specified,
            it will be called 'defaultPreset' and will overwrite the default
            one.
            directory(str): the path where the preset file will be stored. If
            not specified, it will be saved in the default path.
        """

        # Create directory for the JSON preset file
        infoFile = os.path.join(directory, '%s.json' % name)

        # Find all the active animation layers in the scene
        activeLayers, weights = self.getActiveAnimationLayers()

        # Create an ordered dict to store the data
        dataToWrite = OrderedDict()

        # Populate the data dic with the active layers and their weights
        for i in range(0, len(activeLayers)):
            dataToWrite[activeLayers[i]] = weights[i]

        # Save all the active animation layers and their weights in the JSON preset file
        with open(infoFile, 'w') as f:
            json.dump(dataToWrite, f, indent=4) # TODO: check for errors here
