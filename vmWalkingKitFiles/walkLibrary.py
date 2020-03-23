from maya import cmds
import os
import json
from collections import OrderedDict

USER_APP_DIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USER_APP_DIR, 'vmWalkKitPresets')
DEFAULT_PRESET_NAME = 'defaultPreset'

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
        self.savePreset()
        self.resetPreset()

    # ANIMATION LAYERS METHODS

    def changeLayerStateDropDown(self, layerToChange, mute):
        """
        Change the muted state of the given animation layer if this exists
        Args:
            layerNameToChange(str): the animation layer change
        """

        wasPlaying = False

        # Stop playback before doing any animation layer operation
        if cmds.play(query=True, state=True):
            cmds.play(state=False)
            wasPlaying = True

        # If the queried animation layer exists it will be muted
        if cmds.animLayer(layerToChange, query=True, exists=True):
            cmds.animLayer(layerToChange, edit=True, mute=mute)

            # Once the operations have finished begin playback (only if it was playing before)
            if wasPlaying:
                cmds.play(state=True)
        else:
            print(layerToChange + " not found!")

    def changeLayerStateSlider(self, layerToChange, weight):
        """
        Change the weight of the given animation layer if this exists
        Args:
            layerNameToChange(str): the animation layer change
        """

        wasPlaying = False

        # Stop playback before doing any animation layer operation
        if cmds.play(query=True, state=True):
            cmds.play(state=False)
            wasPlaying = True

        # If the queried animation layer exists it will be muted
        if cmds.animLayer(layerToChange, query=True, exists=True):
            cmds.animLayer(layerToChange, edit=True, weight=weight)

            # Once the operations have finished begin playback (only if it was playing before)
            if wasPlaying:
                cmds.play(state=True)
        else:
            print(layerToChange + " not found!")

    def getCurrentAnimationLayers(self):
        """
        Finds all the current existing animation layers in the scene.

        Returns: returns a dict with all the current existing layers
        in the scene (except the base animation layer) and their weights.
        """

        baseAnimationLayer = cmds.animLayer(query=True, root=True)
        childLayers = cmds.animLayer(baseAnimationLayer, query=True, children=True)

        weights = OrderedDict()

        for i in range(0, len(childLayers)):
            weights[i] = cmds.animLayer(childLayers[i], query=True, weight=True)

        return childLayers, weights

    # PRESETS METHODS

    def resetPreset(self):
        """
        Imports the given preset into the tool.
        Args:
            name(str): the name of the JSON preset file. If not specified,
            the default preset will be imported.
            directory(str): the path from where the preset file will be loaded. If
            not specified, it will be loaded from the default path.
        """

        # Create directory for the JSON preset file
        infoFile = os.path.join(DIRECTORY, '%s.json' % DEFAULT_PRESET_NAME)

        # Load JSON content into 'activeLayers' list
        with open(infoFile, 'r') as f:
            activeLayersInfo = json.load(f)

        if activeLayersInfo is not None:

            # Find all the animation layers in the scene
            activeLayers = activeLayersInfo.keys()
            childLayers, weights = self.getCurrentAnimationLayers()

            for i in range(0, len(childLayers)):
                if childLayers[i] in activeLayers:
                    cmds.animLayer(childLayers[i], edit=True, mute=False)
                else:
                    cmds.animLayer(childLayers[i], edit=True, mute=True)
        else:
            print DEFAULT_PRESET_NAME + "not found."

        return activeLayers

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
        childLayers, weights = self.getCurrentAnimationLayers()
        activeLayers = []

        # Store all the active (not muted) animation layers in the 'activeLayers' list
        for i in range(0, len(childLayers)):
            if not cmds.animLayer(childLayers[i], query=True, mute=True):
                activeLayers.append(childLayers[i])

        dataToWrite = OrderedDict()

        for i in range(0, len(activeLayers)):
            dataToWrite[activeLayers[i]] = weights[i]

        # Save all the active animation layers and their weights in the JSON preset file
        with open(infoFile, 'w') as f:
            json.dump(dataToWrite, f, indent=4)

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
