from maya import cmds
from collections import OrderedDict

# This is not done like this when shipping the tool.
# Watch from 5:30 of video 57
import walkLibrary
reload(walkLibrary)  # TODO: delete this when shipping.

# TODO: Substitute 'PySide2' with 'Qt' when shipping the tool.
# This is only for developing purposes
from Qt import QtWidgets, QtCore, QtGui
from functools import partial
import Qt
import logging
from maya import OpenMayaUI as omui

# Setting up logger
logger = logging.getLogger('WalkLibraryUI')
logger.setLevel(logging.DEBUG) # TODO: change to logging.INFO when shipping
logging.basicConfig()

# This makes sure that all import statements work regardless of what Python library it's been used for Qt

if Qt.__binding__ == 'PySide': # If we are using PySide
    logger.debug('Using PySide with shiboken')
    from shiboken import wrapInstance
elif Qt.__binding__.startswith('PyQt'): # If we are using PyQt4 or PyQt5
    logger.debug('Using PyQt with sip')
    from sip import wrapInstance as wrapInstance
else: # If we are using PySide2 (Maya 2017 and above)
    logger.debug('Using PySide2 with shiboken2')
    from shiboken2 import wrapInstance


class WalkLibraryUI(QtWidgets.QWidget):
    """
    The WalkLibraryUI is a dialog that lets us control all the walkTool parameters.
    """

    # Saving initial BodyBeat index for adapting UpDown parameter accordingly
    prevBodyIndex = 2

    def __init__(self, dock=True):

        # Delete UI if it already exists
        try:
            cmds.deleteUI('walktool')
        except:
            logger.debug('No previous UI exists.')

        # If dock mode is queried the parent will be the docked window
        # If not, the parent will be the main Maya window
        # TODO: explain this dock(bool) option in the documentation of the tool
        if dock:
            parent = getWindowDock()
        else:
            deleteWindowDock()
            parent = QtWidgets.QDialog(parent=getMayaMainWindow())
            parent.setObjectName('walktool')
            parent.setWindowTitle('Walk Tool')
            layout = QtWidgets.QVBoxLayout(parent)

        # Now that our parent is set we can initialize it
        super(WalkLibraryUI, self).__init__(parent=parent)

        # Set default size of the window
        self.resize(400, 350)

        # The Library variable points to an instance of our controller library
        self.library = walkLibrary.WalkLibrary()

        # Dropdown options list
        self.frameOptions = ["8f", "12f", "16f"]
        self.rangeOptions = ["Low", "Mid", "High"]
        self.paramWidgets = OrderedDict()

        # Prefixes
        self.prefixes = ["BodyBeat", "ArmsBeat", "UpDown", "BodyTilt", "HeadUpDown", "HeadPigeon",
                         "HeadEgoist", "HeadNodding", "HeadTilt", "BackCurvature"]

        # Populate 'paramLayers' dictionary with the current info on the scene
        self.initParamLayersData()

        # Every time we create a new instance, we will automatically create our UI
        self.createUI()
        self.onReset()

        # Add ourself (QtWidgets.QWidget) to the parent's layout
        self.parent().layout().addWidget(self)

        # If docked mode is off, directly show our parent
        if not dock:
            parent.show()

    def initParamLayersData(self):
        """
        Initializes all the data structures needed for controlling animation layers and parameters.
        """

        # Get the names and weights of all the animation layers in the scene
        layersNames, layersWeights = self.library.getCurrentAnimationLayers()

        # Create ordered dictionaries to store the parameters data

        # BodyBeat
        bodyBeatDict = OrderedDict()
        bodyBeatDict[layersNames[0]] = layersWeights[0]
        bodyBeatDict[layersNames[1]] = layersWeights[1]
        bodyBeatDict[layersNames[2]] = layersWeights[2]

        # ArmsBeat
        armsBeatDict = OrderedDict()
        armsBeatDict[layersNames[3]] = layersWeights[3]
        armsBeatDict[layersNames[4]] = layersWeights[4]
        armsBeatDict[layersNames[5]] = layersWeights[5]

        # UpDown
        upDownDict = OrderedDict()
        upDownDict[layersNames[6]] = layersWeights[6]

        # BodyTilt
        bodyTiltDict = OrderedDict()
        bodyTiltDict[layersNames[7]] = layersWeights[7]

        # HeadUpDown
        headUpDownDict = OrderedDict()
        headUpDownDict[layersNames[8]] = layersWeights[8]

        # HeadPigeon
        headPigeonDict = OrderedDict()
        headPigeonDict[layersNames[9]] = layersWeights[9]

        # HeadEgoist
        headEgoist = OrderedDict()
        headEgoist[layersNames[10]] = layersWeights[10]

        # HeadNodding
        headNodding = OrderedDict()
        headNodding[layersNames[11]] = layersWeights[11]

        # HeadNodding
        headTilt = OrderedDict()
        headTilt[layersNames[12]] = layersWeights[12]

        # BackCurvature
        backCurvature = OrderedDict()
        backCurvature[layersNames[13]] = layersWeights[13]

        # Create main data list with all the layers information sorted by parameter
        self.paramLayers = {
            self.prefixes[0]: bodyBeatDict,
            self.prefixes[1]: armsBeatDict,
            self.prefixes[2]: upDownDict,
            self.prefixes[3]: bodyTiltDict,
            self.prefixes[4]: headUpDownDict,
            self.prefixes[5]: headPigeonDict,
            self.prefixes[6]: headEgoist,
            self.prefixes[7]: headNodding,
            self.prefixes[8]: headTilt,
            self.prefixes[9]: backCurvature
        }

    # UI METHODS

    # UI creation methods

    def createUI(self):
        """This method creates the UI"""

        # This is the master layout
        self.layout = QtWidgets.QVBoxLayout(self)

        # Create menu bar
        self.createMenuBar()

        # Initialize tab screen
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setUsesScrollButtons(True)
        self.layout.addWidget(self.tabs)

        # Create tabs
        self.createGeneralTab()
        self.createHeadTab()
        self.createTrunkTab()
        self.createArmsTab()
        self.createHandsTab()
        self.createLegsTab()
        self.createFeetTab()
        self.createTailTab()
        self.createSettingsTab()

        # Create bottom buttons
        self.createBottomBtns()

    def createMenuBar(self):
        """
        Creates the top menu bar.
        """

        # Creates the menu bar widges and add it to the master layout
        menubar = QtWidgets.QMenuBar()
        self.layout.addWidget(menubar)

        # Add the main menu options
        actionFile = menubar.addMenu("File")
        actionFile.addAction("New")
        actionFile.addAction("Open")
        actionFile.addAction("Save")
        actionFile.addSeparator()
        actionFile.addAction("Quit")
        menubar.addMenu("Edit")
        menubar.addMenu("View")
        menubar.addMenu("Help")

    def createGeneralTab(self):
        """
        Creates the general tab.
        """

        # Add general tab
        tabGeneral = self.addTab("General")

        # Create General tab parameters
        self.addDropDownParam(tabGeneral, "Body beat", self.frameOptions, 0, self.prefixes[0], "onDropDownBodyBeatChanged")
        self.addDropDownParam(tabGeneral, "Arms beat", self.frameOptions, 1, self.prefixes[1], "onDropDownChanged")
        self.addSliderParam(tabGeneral, "Up & Down", 2, self.prefixes[2], "onSliderChanged")
        self.addSliderParam(tabGeneral, "Body Tilt", 3, self.prefixes[3], "onSliderChanged")

    def createHeadTab(self):
        """
        Creates the head tab
        """

        # Add tab for the head
        tabHead = self.addTab("Head")

        # Create Head tab parameters
        self.addSliderParam(tabHead, "Head up-down", 0, self.prefixes[4], "onSliderChanged")
        self.addSliderParam(tabHead, "Head pigeon", 1, self.prefixes[5], "onSliderChanged")
        self.addSliderParam(tabHead, "Head egoist", 2, self.prefixes[6], "onSliderChanged")
        self.addSliderParam(tabHead, "Head nodding", 3, self.prefixes[7], "onSliderChanged")
        self.addSliderParam(tabHead, "Head tilt", 4, self.prefixes[8], "onSliderChanged", 500)

    def createTrunkTab(self):
        """
        Creates the trunk tab
        """

        # Add tab for the trunk
        tabTrunk = self.addTab("Trunk")

        # Create Head tab parameters
        self.addSliderParam(tabTrunk, "Back curvature", 0, self.prefixes[9], "onSliderChanged", 500)

    def createArmsTab(self):
        """
        Creates the arms tab
        """

        # Add tab for the arms
        tabArms = self.addTab("Arms")

        # Add placeholder text to the scroll layout
        tmpText = QtWidgets.QLabel("Work in progress.")
        self.scrollLayout.addWidget(tmpText)

    def createHandsTab(self):
        """
        Creates the hands tab
        """

        # Add tab for the hans
        tabHands = self.addTab("Hands")

        # Add placeholder text to the scroll layout
        tmpText = QtWidgets.QLabel("Work in progress.")
        self.scrollLayout.addWidget(tmpText)

    def createLegsTab(self):
        """
        Creates the legs tab
        """

        # Add tab for the legs
        tabLegs = self.addTab("Legs")

        # Add placeholder text to the scroll layout
        tmpText = QtWidgets.QLabel("Work in progress.")
        self.scrollLayout.addWidget(tmpText)

    def createFeetTab(self):
        """
        Creates the feet tab
        """

        # Add tab for the feet
        tabLegs = self.addTab("Feet")

        # Add placeholder text to the scroll layout
        tmpText = QtWidgets.QLabel("Work in progress.")
        self.scrollLayout.addWidget(tmpText)

    def createTailTab(self):
        """
        Creates the tail tab
        """

        # Add tab for the feet
        tabtail = self.addTab("Tail")

        # Add placeholder text to the scroll layout
        tmpText = QtWidgets.QLabel("Work in progress.")
        self.scrollLayout.addWidget(tmpText)

    def createSettingsTab(self):
        """
        Creates the settings tab
        """

        # Add tab for the head
        tabSettings = self.addTab("Settings")

        # Add placeholder text to the scroll layout
        tmpText = QtWidgets.QLabel("Work in progress.")
        self.scrollLayout.addWidget(tmpText)

    def createBottomBtns(self):
        """
        Creates the bottom buttons.
        """

        # This is our child widget that holds all the buttons
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        self.layout.addWidget(btnWidget)

        # Create buttons, connect them to a slot and add them to our btnLayout

        # Save button
        saveBtn = QtWidgets.QPushButton('Save preset')
        # saveBtn.clicked.connect(self.onSave)
        btnLayout.addWidget(saveBtn)

        # Read button
        importBtn = QtWidgets.QPushButton('Import preset')
        #importBtn.clicked.connect(self.onImport)
        btnLayout.addWidget(importBtn)

        # Reset
        resetBtn = QtWidgets.QPushButton('Reset')
        resetBtn.clicked.connect(self.onReset)
        btnLayout.addWidget(resetBtn)

    # UI functionality methods

    def addTab(self, tabName):
        """
        Creates a tab with the given name.
        Args:
            tabName(str): name of the tab to create.

        Returns:
            newTab(QtWidgets.QWidget): a reference to the new created tab.
        """

        # Create a new tab and add it to the QTabWidget
        newTab = QtWidgets.QWidget()
        self.tabs.addTab(newTab, tabName)

        # Set a QGridLayout for the new tab
        newTab.layout = QtWidgets.QGridLayout(newTab)
        newTab.layout.setContentsMargins(4, 4, 4, 4)
        newTab.setLayout(newTab.layout)

        # Create the scroll widget that will contain all the parameters of this new tab
        scrollWidget = QtWidgets.QWidget()
        scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)

        # Set the scroll layout
        self.scrollLayout = QtWidgets.QGridLayout(scrollWidget)

        # Create the scroll area to add the new tab
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        newTab.layout.addWidget(scrollArea, 1, 0, 5, 5)

        return newTab

    def addDropDownParam(self, tab, paramName, options, id, prefix, slotName=None):

        widget = QtWidgets.QComboBox()
        for i in range(0, len(options)):
            widget.addItem(options[i])

        widget.setCurrentIndex(1)  # TODO: not hardcode this? Maybe read from JSON default preset file

        if prefix == 'BodyBeat':
            widget.currentIndexChanged.connect(partial(getattr(self, slotName)))
        else:
            widget.currentIndexChanged.connect(partial(getattr(self, slotName), prefix))

        self.setUpParamWidget(prefix, widget, paramName, id)

    def addSliderParam(self, tab, paramName, id, prefix, slotName=None, defaultValue=200):

        widget = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        widget.setMinimum(0)
        widget.setMaximum(1000)
        widget.setValue(defaultValue)
        widget.valueChanged.connect(partial(getattr(self, slotName), prefix))

        self.setUpParamWidget(prefix, widget, paramName, id)

    def setUpParamWidget(self, prefix, widget, paramName, id):

        self.paramWidgets[prefix] = widget

        # Set parameter layout
        paramText = QtWidgets.QLabel(paramName)

        self.scrollLayout.addWidget(paramText, id, 0, 1, 3)
        paramText.setMinimumHeight(25)
        self.scrollLayout.addWidget(QtWidgets.QLabel(" "), id, 3, 1, 1)
        self.scrollLayout.addWidget(widget, id, 4, 1, 3)

    # SLOT METHODS

    def onDropDownChanged(self, prefix, index):
        """
        Takes in the new current index of the dropdown to change the layer state accordingly.

        Args:
            prefix:(string): prefix of the layer associated with this parameter.
            index (int): index of the current selected option in the dropdown
        """

        # Convert the index into a string and inside a [1-3] range to match the animation layer naming convention
        indStr = str(index + 1)

        # Change animation layers mute state according to the current index
        for key in self.paramLayers[prefix]:

            layerName = key

            if indStr in key:
                self.library.changeLayerMuteState(layerName, False)
            else:
               self.library.changeLayerMuteState(layerName, True)

        # Retrieve the current BodyBeat and ArmsBeat indices by iterating the current active layers and
        # checking for the unmuted ones
        activeLayers, weights = self.library.getActiveAnimationLayers()
        indices = []

        for i in range(0, len(activeLayers)):

            # Once we got both indices we break out of the for loop
            if len(indices) == 2:
                break

            # Split layer name into prefix and index
            splitStr = activeLayers[i].split("_")

            # If we find 'BodyBeat' or 'ArmsBeat' we store their indices
            if self.prefixes[0] in splitStr[0] or self.prefixes[1] in splitStr[0]:
                indices.append(int(splitStr[1]))

        # Calculate the playback range according to the current indices retrieved above. Body and arms beat dictate
        # the length of the whole walk cycle animation. This allows for a minimum playback time while always allowing
        # the animation to be looped properly.
        self.calculatePlaybackRange(indices)

    def onDropDownBodyBeatChanged(self, index):
        """
        Takes in the new current index of the dropdown to change the layer state accordingly. It only differs from
        the onDropDownChanged() method in the sense that this one is also in charge of moving the keyframes of the
        UpDown_1 layer in order to adapt to the BodyBeat parameter.

        Args:
            index (int): index of the current selected option in the dropdown
        """

        prefix = 'BodyBeat'

        # Convert the index into a string and inside a [1-3] range to match the animation layer naming convention
        indStr = str(index + 1)

        # Change animation layers mute state according to the current index
        for key in self.paramLayers[prefix]:

            layerName = key

            if indStr in key:
                self.library.changeLayerMuteState(layerName, False)
            else:
               self.library.changeLayerMuteState(layerName, True)

        # Retrieve the current BodyBeat and ArmsBeat indices by iterating the current active layers and
        # checking for the unmuted ones
        indices = []
        activeLayers, weights = self.library.getActiveAnimationLayers()

        for i in range(0, len(activeLayers)):

            # Once we got both indices we break out of the for loop
            if len(indices) == 2:
                break

            # Split layer name into prefix and index
            splitStr = activeLayers[i].split("_")

            # If we find 'BodyBeat' or 'ArmsBeat' we store their indices
            if self.prefixes[0] in splitStr[0] or self.prefixes[1] in splitStr[0]:
                indices.append(int(splitStr[1]))

        # Calculate the playback range according to the current indices retrieved above. Body and arms beat dictate
        # the length of the whole walk cycle animation. This allows for a minimum playback time while always allowing
        # the animation to be looped properly.
        self.calculatePlaybackRange(indices)

        # Query the current BodyBeat index
        currBodyIndex = self.paramWidgets[prefix].currentIndex() + 1

        if currBodyIndex is not None:
            # Create the ty attribute of the controller that handles the up and down body movement
            attrGeneralUpDown = 'Mr_Buttons:Mr_Buttons_COG_Ctrl.translateY'
            self.offsetKeyframes(attrGeneralUpDown, 'UpDown_1', currBodyIndex)

            attrHeadPigeon = 'Mr_Buttons:Mr_Buttons_Head_01FKCtrl.translateZ'
            self.offsetKeyframes(attrHeadPigeon, 'HeadPigeon_1', currBodyIndex)

            attrHeadUpDown = 'Mr_Buttons:Mr_Buttons_Head_01FKCtrl.translateY'
            self.offsetKeyframes(attrHeadUpDown, 'HeadUpDown_1', currBodyIndex)

            attrheadEgoist = 'Mr_Buttons:Mr_Buttons_Neck_01FKCtrl.rotateZ'
            self.offsetKeyframes(attrheadEgoist, 'HeadEgoist_1', currBodyIndex)

            attrHeadNodding = 'Mr_Buttons:Mr_Buttons_Head_01FKCtrl.rotateX'
            self.offsetKeyframes(attrHeadNodding, 'HeadNodding_1', currBodyIndex)

            attrHeadTilt = 'Mr_Buttons:Mr_Buttons_Head_01FKCtrl.rotateX'
            self.offsetKeyframes(attrHeadTilt, 'HeadTilt_1', currBodyIndex)


        # Store the previous BodyBeat index for the next calculation
        WalkLibraryUI.prevBodyIndex = self.paramWidgets[prefix].currentIndex() + 1

    def onSliderChanged(self, prefix, value):
        """
        Calculates the normalized slider value and applies it to the layer's weight
        Args:
            prefix(str): prefix of the layer associated with the slider
            value(float): current value of the slider
        """

        layerName = list(self.paramLayers[prefix].keys())[0]
        weight = value / 1000.0
        self.library.changeLayerWeight(layerName, weight)

    def onSave(self, name=None, directory=None):
        """
        Imports the given preset file into the tool.
        If not given, the default name and directory will be used.
        If just given the name the default directory will be used with the given name.
        Args:
            name(str): name of the preset file to import.
            directory(str): directory where the preset file to import is stored
        """

        if name is None and directory is None:
            self.library.savePreset()
        elif name is not None and directory is None:
            self.library.savePreset(name)
        elif name is not None and directory is not None:
            self.library.savePreset(name, directory)
        else:
            logger.debug("If a directory is given a name must be given as well.")

    def onReset(self):
        """
        Resets the tool parameters to their default state.
        """

        # Import the default preset and query the layer names and weights
        defaultLayers, defaultWeights = self.library.importPreset()

        # Set default playback options
        cmds.playbackOptions(animationEndTime=96)
        cmds.playbackOptions(minTime=1)
        cmds.playbackOptions(maxTime=24)
        cmds.playbackOptions(animationStartTime=1)

        # For each parameter apply the default layers data to the parameter
        if defaultLayers is not None and defaultWeights is not None:
            for i in range(0, len(defaultLayers)):

                # Get layer prefix
                splitStr = defaultLayers[i].split("_")
                prefix = splitStr[0]

                # Get the widget type
                widgetType = type(self.paramWidgets[prefix]).__name__

                # Set the current index or change the slider value accordingly
                if widgetType == 'QComboBox':
                    index = int(splitStr[1]) - 1
                    self.paramWidgets[prefix].setCurrentIndex(index)
                    if prefix == self.prefixes[0]:
                        self.onDropDownBodyBeatChanged(index)
                    else:
                        self.onDropDownChanged(prefix, index)
                elif widgetType == 'QSlider':
                    self.paramWidgets[prefix].setValue(defaultWeights[i]*1000.0)
                    self.onSliderChanged(prefix, defaultWeights[i]*1000.0)
        else:
            logger.debug("Query for default preset file failed.")

    def onImport(self, name=None, directory=None):
        """
        Imports the given preset file into the tool.
        If not given, the default name and directory will be used.
        If just given the name the default directory will be used with the given name.
        Args:
            name(str): name of the preset file to import.
            directory(str): directory where the preset file to import is stored
        """

        if name is None and directory is None:
            self.library.importPreset()
        elif name is not None and directory is None:
            self.library.importPreset(name)
        elif name is not None and directory is not None:
            self.library.importPreset(name, directory)
        else:
            logger.debug("If a directory is given a name must be given as well.")

    # KEYFRAMES METHODS

    def offsetKeyframes(self, attrFull, layerName, currBodyIndex):

        offset = 0

        # Calculate the offset of the keyframes that need to be moved according to the current and previous index
        # of the BodyBeat parameter
        if (self.prevBodyIndex == 1 and currBodyIndex == 2) or (self.prevBodyIndex == 2 and currBodyIndex == 3):
            offset = 1
        elif (self.prevBodyIndex == 2 and currBodyIndex == 1) or (self.prevBodyIndex == 3 and currBodyIndex == 2):
            offset = -1
        elif self.prevBodyIndex == 1 and currBodyIndex == 3:
            offset = 2
        elif self.prevBodyIndex == 3 and currBodyIndex == 1:
            offset = -2

        layerPlug = cmds.animLayer(layerName, e=True, findCurveForPlug=attrFull)
        keyframes = cmds.keyframe(layerPlug[0], q=True)

        # Select attrFull
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

        # Select the layer so its keyframes can be moved
        cmds.animLayer(layerName, edit=True, selected=False, preferred=False)

    def calculatePlaybackRange(self, indices):

        playBackEndRange = 0

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
        cmds.playbackOptions(animationEndTime=96)
        cmds.playbackOptions(minTime=1)
        cmds.playbackOptions(maxTime=playBackEndRange)
        cmds.playbackOptions(animationStartTime=1)

# MAYA WINDOWS FUNCTIONS

def getMayaMainWindow():
    """
    Get the main Maya windows (which is also built with Qt).

    Returns:
        ptr(QtWidgets.QMainWindow): The Maya MainWindow
    """

    # With OpenMayaUI API we query a reference to Maya's MainWindow
    win = omui.MQtUtil_mainWindow()

    # We cast the queried window to QMainWindow so it's manageable within our Python code
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)

    return ptr

def getWindowDock(name='WalkToolDock'):
    """
    Create dock with the given name.
    Args:
        name(str): name of the dock to create.

    Returns:
        ptr(QtWidget.QWidget): The dock's widget
    """

    # Delete older dock
    deleteWindowDock(name)

    # Create a dock and query its name
    ctrl = cmds.workspaceControl(name, tabToControl=('AttributeEditor', 2), label='Walk Tool', vis=True)

    # Query the correspondent QtWidget associated with the dock
    qtCtrl = omui.MQtUtil_findControl(name)

    # We cast the queried window to QWidget so it's manageable within our Python code
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)

    return ptr

def deleteWindowDock(name='WalkToolDock'):
    """
    Deletes the given dock if this exists.
    Args:
        name(str): name of the window to delete
    """

    if cmds.workspaceControl(name, exists=True):
        cmds.deleteUI(name)


# Call it in Maya's Script Editor
#from vmWalkingKit.vmWalkingKitFiles import libraryUI
#reload(libraryUI)

#libraryUI.WalkLibraryUI()
