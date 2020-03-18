from maya import cmds
import os
import json

USER_APP_DIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USER_APP_DIR, 'walkLibrary')

def createDirectory(directory=DIRECTORY):
    """
    Creates the given directory if it doesn't exist already.
    Args:
        directory(str): the directory to create
    """
    if not os.path.exists(directory):
        os.mkdir(directory)

class WalkLibrary(dict):

    def __init__(self):
        createDirectory()

    # ANIMATION LAYERS METHODS

    def muteLayer(self, layerNameToMute):
        """
        Mutes the given animation layer if this exists
        Args:
            layerNameToMute(str): the animation layer name to mute
        """

        # Stop playback before doing any animation layer operation
        cmds.play(state=False)

        # If the queried animation layer exists it will be muted
        if cmds.animLayer(layerNameToMute, query=True, exists=True):
            cmds.animLayer(layerNameToMute, edit=True, mute=True, lock=True)
        else:
            print(layerNameToMute + " not found!")

    def unmuteLayer(self, layerNameToUnmute):
        """
        Unmutes the given animation layer if this exists
        Args:
            layerNameToUnmute(str): the animation layer name to unmute
        """

        # Stop playback before doing any animation layers operation
        cmds.play(state=False)

        # If the queried animation layer exists it will be unmuted.
        # The other animation layers will be muted (for now)
        if cmds.animLayer(layerNameToUnmute, query=True, exists=True):
            baseAnimationLayer = cmds.animLayer(query=True, root=True)
            childLayers = cmds.animLayer(baseAnimationLayer, query=True, children=True)

            for child in childLayers:
                if child != layerNameToUnmute:
                    cmds.animLayer(child, edit=True, mute=True, lock=True)

            cmds.animLayer(layerNameToUnmute, edit=True, mute=False, lock=False)
        else:
            print(layerNameToUnmute + " not found!")

    def getCurrentAnimationLayers(self):
        """
        Finds all the current existing animation layers in the scene.

        Returns: returns a list with all the current existing layers
        in the scene (except the base animation layer).
        """

        baseAnimationLayer = cmds.animLayer(query=True, root=True)
        childLayers = cmds.animLayer(baseAnimationLayer, query=True, children=True)

        return childLayers

    # PARAMETERS METHODS

    def setBeat(self, index):
        """
        Sets the selected beat by the user
        Args:
            index(int): the index of the chosen beat option
        """
        beatLayerName = None

        if index == 0:
            beatLayerName = 'beat_8f'
        elif index == 1:
            beatLayerName = 'beat_12f'
        else:
            beatLayerName = 'beat_16f'

        self.unmuteLayer(beatLayerName)

    # PRESETS METHODS

    def savePreset(self, name='defaultPreset', directory=DIRECTORY):
        """
        Saves the current parameters in a preset JSON file.
        Args:
            name(str): the name of the JSON preset file. If not specified,
            it will be called 'defaultPreset' and will overwrite the default
            one.
            directory(str): the path where the preset file will be stored. If
            not specified, it will be save in the default path.
        """

        # Create directory for the JSON preset file
        infoFile = os.path.join(directory, '%s.json' % name)

        # Find all the animation layers in the scene
        childLayers = self.getCurrentAnimationLayers()
        activeLayers = []

        # Store all the active (not muted) animation layers in the 'activeLayers' list
        for i in range(0, len(childLayers)):
            if not cmds.animLayer(childLayers[i], query=True, mute=True):
                activeLayers.append(childLayers[i])

        # Save all the active animation layers in the JSON preset file
        with open(infoFile, 'w') as f:
            json.dump(activeLayers, f, indent=4)

    def importPreset(self, name='defaultPreset', directory=DIRECTORY):
        """
        Imports the given preset into the tool.
        Args:
            name(str): the name of the JSON preset file. If not specified,
            the default preset will be imported.
            directory(str): the path from where the preset file will be loaded. If
            not specified, it will be loaded from the default path.
        """

        # Create directory for the JSON preset file
        infoFile = os.path.join(directory, '%s.json' % name)

        activeLayers = []

        # Load JSON content into 'activeLayers' list
        with open(infoFile, 'r') as f:
            activeLayers = json.load(f)

        # Find all the animation layers in the scene
        childLayers = self.getCurrentAnimationLayers()

        for i in range(0, len(childLayers)):
            if childLayers[i] in activeLayers:
                cmds.animLayer(childLayers[i], edit=True, mute=False)
            else:
                cmds.animLayer(childLayers[i], edit=True, mute=True)
