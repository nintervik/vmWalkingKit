import os
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

    # Saving initial BodyBeat and ArmsBeat indices for adapting others parameters accordingly
    prevBodyIndex = 2
    prevArmsIndex = 2

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
            parent.setWindowTitle('vmWalkingKit')
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
        self.handOptions = ["Relaxed", "Fist"]
        self.faceOptions = ["Happy", "Angry", "Sad", "Cocky", "Scared"]
        self.paramWidgets = OrderedDict()

        # Prefixes
        self.prefixes = ["BodyBeat", "ArmsBeat", "UpDown", "BodyTilt", "HeadUpDown", "HeadPigeon",
                         "HeadEgoist", "HeadNodding", "HeadTilt", "FaceExpression", "BackCurvature",
                         "PelvisYRotation", "PelvisWeightShift", "ChestYRotation", "ChestUpDown",
                         "TailSwing", "TailCurl", "TailTilt", "TailWaving", "ArmsWidth", "ElbowsDrag", "HandsDrag",
                         "HandsPose", "LegsSeparation", "FeetYRotation", "StepDistance"]

        self.paramDescriptions = OrderedDict([
            (self.prefixes[0],  "Place holder description 1"),
            (self.prefixes[1],  "Place holder description 2"),
            (self.prefixes[2],  "Place holder description 3"),
            (self.prefixes[3],  "Place holder description 4"),
            (self.prefixes[4],  "Place holder description 5"),
            (self.prefixes[5],  "Place holder description 6"),
            (self.prefixes[6],  "Place holder description 7"),
            (self.prefixes[7],  "Place holder description 8"),
            (self.prefixes[8],  "Place holder description 9"),
            (self.prefixes[9],  "Place holder description 10"),
            (self.prefixes[10], "Place holder description 11"),
            (self.prefixes[11], "Place holder description 12"),
            (self.prefixes[12], "Place holder description 13"),
            (self.prefixes[13], "Place holder description 14"),
            (self.prefixes[14], "Place holder description 15"),
            (self.prefixes[15], "Place holder description 16"),
            (self.prefixes[16], "Place holder description 17"),
            (self.prefixes[17], "Place holder description 18"),
            (self.prefixes[18], "Place holder description 19"),
            ("ArmsSwing",       "Place holder description 20"),
            (self.prefixes[19], "Place holder description 21"),
            (self.prefixes[20], "Place holder description 22"),
            (self.prefixes[21], "Place holder description 23"),
            (self.prefixes[22], "Place holder description 24"),
            (self.prefixes[23], "Place holder description 25"),
            (self.prefixes[24], "Place holder description 26"),
            (self.prefixes[25], "Place holder description 27"),
        ])

        self.paramDescriptionWidgets = []

        # Populate 'paramLayers' dictionary with the current info on the scene
        self.initParamLayersData()

        # Every time we create a new instance, we will automatically create our UI
        self.createUI()
        self.onImport()

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

        # TODO: automate this below
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
        headEgoistDict = OrderedDict()
        headEgoistDict[layersNames[10]] = layersWeights[10]

        # HeadNodding
        headNoddingDict = OrderedDict()
        headNoddingDict[layersNames[11]] = layersWeights[11]

        # HeadNodding
        headTiltDict = OrderedDict()
        headTiltDict[layersNames[12]] = layersWeights[12]

        # FaceExpression
        faceExpressionDict = OrderedDict()
        faceExpressionDict[layersNames[13]] = layersWeights[13]
        faceExpressionDict[layersNames[14]] = layersWeights[14]
        faceExpressionDict[layersNames[15]] = layersWeights[15]
        faceExpressionDict[layersNames[16]] = layersWeights[16]
        faceExpressionDict[layersNames[17]] = layersWeights[17]

        # BackCurvature
        backCurvatureDict = OrderedDict()
        backCurvatureDict[layersNames[18]] = layersWeights[18]

        # PelvisYRotation
        pelvisYRotationDict = OrderedDict()
        pelvisYRotationDict[layersNames[19]] = layersWeights[19]

        # PelvisWeightShift
        pelvisWeightShiftDict = OrderedDict()
        pelvisWeightShiftDict[layersNames[20]] = layersWeights[20]

        # ChestYRotation
        chestYRotationDict = OrderedDict()
        chestYRotationDict[layersNames[21]] = layersWeights[21]

        # ChestUpDown
        chestUpDownDict = OrderedDict()
        chestUpDownDict[layersNames[22]] = layersWeights[22]

        # TailSwing
        tailSwingDict = OrderedDict()
        tailSwingDict[layersNames[23]] = layersWeights[23]

        # TailCurl
        tailCurlDict = OrderedDict()
        tailCurlDict[layersNames[24]] = layersWeights[24]

        # TailTilt
        tailTiltDict = OrderedDict()
        tailTiltDict[layersNames[25]] = layersWeights[25]

        # TailWaving
        tailWavingDict = OrderedDict()
        tailWavingDict[layersNames[26]] = layersWeights[26]

        # ArmsWidth
        armsWidthDict = OrderedDict()
        armsWidthDict[layersNames[27]] = layersWeights[27]

        # ElbowsDrag
        elbowsDragDict = OrderedDict()
        elbowsDragDict[layersNames[28]] = layersWeights[28]

        # HandsDrag
        handsDragDict = OrderedDict()
        handsDragDict[layersNames[29]] = layersWeights[29]

        # HandsPose
        handsPoseDict = OrderedDict()
        handsPoseDict[layersNames[30]] = layersWeights[30]
        handsPoseDict[layersNames[31]] = layersWeights[31]

        # LegsSeparation
        legsSeparationDict = OrderedDict()
        legsSeparationDict[layersNames[32]] = layersWeights[32]

        # FeetYRotation
        feetYRotationDict = OrderedDict()
        feetYRotationDict[layersNames[33]] = layersWeights[33]

        # StepDistance
        stepDistanceDict = OrderedDict()
        stepDistanceDict[layersNames[34]] = layersWeights[34]

        # Create main data list with all the layers information sorted by parameter

        self.paramLayers = OrderedDict([
            (self.prefixes[0],  bodyBeatDict),
            (self.prefixes[1],  armsBeatDict),
            (self.prefixes[2],  upDownDict),
            (self.prefixes[3],  bodyTiltDict),
            (self.prefixes[4],  headUpDownDict),
            (self.prefixes[5],  headPigeonDict),
            (self.prefixes[6],  headEgoistDict),
            (self.prefixes[7],  headNoddingDict),
            (self.prefixes[8],  headTiltDict),
            (self.prefixes[9],  faceExpressionDict),
            (self.prefixes[10], backCurvatureDict),
            (self.prefixes[11], pelvisYRotationDict),
            (self.prefixes[12], pelvisWeightShiftDict),
            (self.prefixes[13], chestYRotationDict),
            (self.prefixes[14], chestUpDownDict),
            (self.prefixes[15], tailSwingDict),
            (self.prefixes[16], tailCurlDict),
            (self.prefixes[17], tailTiltDict),
            (self.prefixes[18], tailWavingDict),
            (self.prefixes[19], armsWidthDict),
            (self.prefixes[20], elbowsDragDict),
            (self.prefixes[21], handsDragDict),
            (self.prefixes[22], handsPoseDict),
            (self.prefixes[23], legsSeparationDict),
            (self.prefixes[24], feetYRotationDict),
            (self.prefixes[25], stepDistanceDict)
        ])

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
        self.createTailTab()
        self.createArmsTab()
        self.createLegsTab()
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

    def createDisplaySection(self, text, id):

        # Information display area
        scrollWidgetInfo = QtWidgets.QWidget()
        scrollWidgetInfo.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)

        self.scrollLayoutInfo = QtWidgets.QGridLayout(scrollWidgetInfo)

        scrollAreaInfo = QtWidgets.QScrollArea()
        #scrollAreaInfo.setFrameShape(QtWidgets.QFrame.NoFrame)
        scrollAreaInfo.setWidgetResizable(True)
        #scrollAreaInfo.setContentsMargins(4, 4, 4, 4)
        #scrollAreaInfo.setFocusPolicy(QtCore.Qt.NoFocus)
        scrollAreaInfo.setWidget(scrollWidgetInfo)
        #scrollAreaInfo.setStyleSheet('QScrollArea {background-color: #3d3d3d; border: 1px solid grey}')
        scrollAreaInfo.setStyleSheet('QScrollArea {border: 1px solid grey}')

        textWidget = QtWidgets.QLabel(text)
        textWidget.setMinimumSize(292, 8)
        textWidget.setWordWrap(True)

        textWidget.setFont(QtGui.QFont('Arial', 9.5))
        self.paramDescriptionWidgets.append(textWidget)

        self.scrollLayoutInfo.addWidget(textWidget, 0, 0, 0, 0, QtCore.Qt.AlignTop)

        self.scrollLayout.addWidget(scrollAreaInfo, id, 0, 1, 7)

    def createTabDescription(self, text="Tab description here [WIP]."):
        # Add placeholder text to the scroll layout
        descriptionTxt = QtWidgets.QLabel(text)
        descriptionTxt.setMinimumSize(200, 8)
        descriptionTxt.setWordWrap(True)
        descriptionTxt.setFont(QtGui.QFont('Arial', 9.5))
        descriptionTxt.setStyleSheet('QLabel{color: #00ff11}')
        self.scrollLayout.addWidget(descriptionTxt)
        sepLine = QtWidgets.QFrame()
        sepLine.setFrameShape(QtWidgets.QFrame.HLine)
        sepLine.setFrameShadow(QtWidgets.QFrame.Raised)
        self.scrollLayout.addWidget(sepLine)

    def createGeneralTab(self):
        """
        Creates the general tab.
        """

        # Add general tab
        tabGeneral = self.addTab("General")

        self.createTabDescription()

        index = 0

        # Create General tab parameters
        self.addDropDownParam("Body beat", self.frameOptions, 2, self.prefixes[0], index, "onDropDownBodyBeatChanged")
        self.addDropDownParam("Arms beat", self.frameOptions, 3, self.prefixes[1], index, "onDropDownArmsBeatChanged")
        self.addSliderParam("Up & Down", 4, self.prefixes[2], index, "onSliderChanged")
        self.addSliderParam("Body Tilt", 5, self.prefixes[3], index, "onSliderChanged")

        self.createDisplaySection("Hover over a parameter to see its description.", 6)

    def createHeadTab(self):
        """
        Creates the head tab
        """

        # Add tab for the head
        tabHead = self.addTab("Head")

        self.createTabDescription()

        index = 1

        # Create Head tab parameters
        self.addSliderParam("Head up-down", 2, self.prefixes[4], index, "onSliderChanged")
        self.addSliderParam("Head pigeon", 3, self.prefixes[5], index, "onSliderChanged")
        self.addSliderParam("Head egoist", 4, self.prefixes[6], index, "onSliderChanged",)
        self.addSliderParam("Head nodding", 5, self.prefixes[7], index, "onSliderChanged")
        self.addSliderParam("Head tilt", 6, self.prefixes[8], index, "onSliderChanged", 500)
        self.addDropDownParam("Facial expression", self.faceOptions, 7, self.prefixes[9], index, "onDropDownChanged")

        self.createDisplaySection("Hover over a parameter to see its description", 8)

    def createTrunkTab(self):
        """
        Creates the trunk tab
        """

        # Add tab for the trunk
        tabTrunk = self.addTab("Trunk")

        self.createTabDescription()

        index = 2

        # TODO: do a ++i for the ui IDs

        # Create Trunk tab parameters
        self.addSliderParam("Back curvature", 2, self.prefixes[10], index, "onSliderChanged", 500)
        self.addSliderParam("Pelvis Y-rotation", 3, self.prefixes[11], index, "onSliderChanged")
        self.addSliderParam("Pelvis weight shift", 4, self.prefixes[12], index, "onSliderChanged")
        self.addSliderParam("Chest Y-rotation", 5, self.prefixes[13], index, "onSliderChanged")
        self.addSliderParam("Chest up-down", 6, self.prefixes[14], index, "onSliderChanged")

        self.createDisplaySection("Hover over a parameter to see its description", 7)

    def createTailTab(self):
        """
        Creates the tail tab
        """

        # Add tab for the trunk
        tailTrunk = self.addTab("Tail")

        self.createTabDescription()

        index = 3

        # TODO: do a ++i for the ui IDs

        # Create Trunk tab parameters
        self.addSliderParam("Tail swing", 2, self.prefixes[15], index, "onSliderChanged")
        self.addSliderParam("Tail curl", 3, self.prefixes[16], index, "onSliderChanged")
        self.addSliderParam("Tail tilt", 4, self.prefixes[17], index, "onSliderChanged")
        self.addSliderParam("Tail waving", 5, self.prefixes[18], index, "onSliderChanged")

        self.createDisplaySection("Hover over a parameter to see its description", 8)

    def createArmsTab(self):
        """
        Creates the arms tab
        """

        # Add tab for the arms
        tabArms = self.addTab("Arms")

        index = 4

        self.createTabDescription()

        # Create Arms tab parameters
        self.addSliderParam("Arms swing", 2, self.prefixes[1], index, "onSliderChanged", 500)
        self.addSliderParam("Arms separation", 3, self.prefixes[19], index, "onSliderChanged", 500)
        self.addSliderParam("Elbows drag", 4, self.prefixes[20], index, "onSliderChanged", 500)
        self.addSliderParam("Hands drag", 5, self.prefixes[21], index, "onSliderChanged", 500)
        self.addDropDownParam("Hands pose", self.handOptions, 6, self.prefixes[22], index, "onDropDownChanged")

        self.createDisplaySection("Hover over a parameter to see its description", 9)

    def createLegsTab(self):
        """
        Creates the legs tab
        """

        # Add tab for the legs
        tabLegs = self.addTab("Legs")

        index = 5

        self.addSliderParam("Legs separation", 2, self.prefixes[23], index, "onSliderChanged")
        self.addSliderParam("Feet Y-rotation", 3, self.prefixes[24], index, "onSliderChanged")
        self.addSliderParam("Step distance", 4, self.prefixes[25], index, "onSliderChanged")

        self.createTabDescription()

        self.createDisplaySection("Hover over a parameter to see its description", 10)

    def createSettingsTab(self):
        """
        Creates the settings tab
        """

        # Add tab for the head
        tabSettings = self.addTab("Settings")

        index = 5

        self.createTabDescription()

        self.createDisplaySection("Hover over a parameter to see its description", 3)

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
        saveBtn.clicked.connect(partial(self.onSave, self.library.getDirectory()))
        btnLayout.addWidget(saveBtn)

        # Read button
        importBtn = QtWidgets.QPushButton('Import preset')
        importBtn.clicked.connect(partial(self.onImport, self.library.getDirectory()))
        btnLayout.addWidget(importBtn)

        # Reset
        resetBtn = QtWidgets.QPushButton('Reset')
        resetBtn.clicked.connect(self.onImport)
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

    def addDropDownParam(self, paramName, options, id, prefix, index, slotName=None):

        widget = QtWidgets.QComboBox()
        for i in range(0, len(options)):
            widget.addItem(options[i])

        widget.setCurrentIndex(1)  # TODO: not hardcode this? Maybe read from JSON default preset file

        if prefix == 'BodyBeat' or prefix == 'ArmsBeat':
            widget.currentIndexChanged.connect(partial(getattr(self, slotName)))
        else:
            widget.currentIndexChanged.connect(partial(getattr(self, slotName), prefix))

        self.setUpParamWidget(prefix, widget, paramName, id, index)

    def addSliderParam(self, paramName, id, prefix, index, slotName=None, defaultValue=200):

        widget = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        widget.setMinimum(0)
        widget.setMaximum(1000)
        widget.setValue(defaultValue)
        widget.valueChanged.connect(partial(getattr(self, slotName), prefix))

        self.setUpParamWidget(prefix, widget, paramName, id, index)

    def setUpParamWidget(self, prefix, widget, paramName, id, index):

        if prefix == self.prefixes[1] and self.prefixes[1] not in self.paramWidgets:
            self.paramWidgets[prefix] = [widget, None]
        elif prefix == self.prefixes[1] and self.prefixes[1] in self.paramWidgets:
            self.paramWidgets[prefix][1] = widget
        else:
            self.paramWidgets[prefix] = widget

        # Set parameter layout
        paramText = ParamLabel(paramName, self, prefix, index)

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

                if self.prefixes[1] in layerName:
                    self.library.changeLayerWeight(layerName, 0.5)
                    currWeight = self.paramLayers[prefix][layerName]
                    self.paramWidgets[prefix][1].setValue(currWeight*1000.0)
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
        self.library.calculatePlaybackRange(indices)

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
        self.library.calculatePlaybackRange(indices)

        # Query the current BodyBeat index
        currBodyIndex = self.paramWidgets[prefix].currentIndex() + 1

        if currBodyIndex is not None:
            # Create the ty attribute of the controller that handles the up and down body movement
            attrGeneralUpDown = 'Mr_Buttons:Mr_Buttons_COG_Ctrl.translateY'
            self.library.offsetKeyframes(attrGeneralUpDown, 'UpDown_1', self.prevBodyIndex, currBodyIndex)

            attrPelvisYRotation = 'Mr_Buttons:Mr_Buttons_COG_Ctrl.rotateY'
            self.library.offsetKeyframes(attrPelvisYRotation, 'PelvisYRotation_1', self.prevBodyIndex, currBodyIndex)

            attrPelvisWeightShift = 'Mr_Buttons:Mr_Buttons_COG_Ctrl.translateX'
            self.library.offsetKeyframes(attrPelvisWeightShift, 'PelvisWeightShift_1', self.prevBodyIndex, currBodyIndex)

            attrHeadPigeon = 'Mr_Buttons:Mr_Buttons_Head_01FKCtrl.translateZ'
            self.library.offsetKeyframes(attrHeadPigeon, 'HeadPigeon_1', self.prevBodyIndex, currBodyIndex)

            attrHeadUpDown = 'Mr_Buttons:Mr_Buttons_Head_01FKCtrl.translateY'
            self.library.offsetKeyframes(attrHeadUpDown, 'HeadUpDown_1', self.prevBodyIndex, currBodyIndex)

            attrheadEgoist = 'Mr_Buttons:Mr_Buttons_Neck_01FKCtrl.rotateZ'
            self.library.offsetKeyframes(attrheadEgoist, 'HeadEgoist_1', self.prevBodyIndex, currBodyIndex)

            attrHeadNodding = 'Mr_Buttons:Mr_Buttons_Head_01FKCtrl.rotateX'
            self.library.offsetKeyframes(attrHeadNodding, 'HeadNodding_1', self.prevBodyIndex, currBodyIndex)

            attrHeadTilt = 'Mr_Buttons:Mr_Buttons_Head_01FKCtrl.rotateX'
            self.library.offsetKeyframes(attrHeadTilt, 'HeadTilt_1', self.prevBodyIndex, currBodyIndex)

            attrChestUpDown = 'Mr_Buttons:Mr_Buttons_Spine_03FKCtrl.translateY'
            self.library.offsetKeyframes(attrChestUpDown, 'ChestUpDown_1', self.prevBodyIndex, currBodyIndex)

            attrChestYRotation = 'Mr_Buttons:Mr_Buttons_Spine_03FKCtrl.rotateY'
            self.library.offsetKeyframes(attrChestYRotation, 'ChestYRotation_1', self.prevBodyIndex, currBodyIndex)

            attrTailSwing1 = 'Mr_Buttons:Mr_Buttons_Tail_01Ctrl.rotateY'
            self.library.offsetKeyframes(attrTailSwing1, 'TailSwing_1', self.prevBodyIndex, currBodyIndex)

            attrTailSwing2 = 'Mr_Buttons:Mr_Buttons_Tail_02Ctrl.rotateY'
            self.library.offsetKeyframes(attrTailSwing2, 'TailSwing_1', self.prevBodyIndex, currBodyIndex)

            attrTailSwing3 = 'Mr_Buttons:Mr_Buttons_Tail_03Ctrl.rotateY'
            self.library.offsetKeyframes(attrTailSwing3, 'TailSwing_1', self.prevBodyIndex, currBodyIndex)

            attrTailSwing4 = 'Mr_Buttons:Mr_Buttons_Tail_04Ctrl.rotateY'
            self.library.offsetKeyframes(attrTailSwing4, 'TailSwing_1', self.prevBodyIndex, currBodyIndex)

            attrTailSwing5 = 'Mr_Buttons:Mr_Buttons_Tail_05Ctrl.rotateY'
            self.library.offsetKeyframes(attrTailSwing5, 'TailSwing_1', self.prevBodyIndex, currBodyIndex)

            attrTailWaving = 'Mr_Buttons:Mr_Buttons_Tail_01Ctrl.rotateZ'
            self.library.offsetKeyframes(attrTailWaving, 'TailWaving_1', self.prevBodyIndex, currBodyIndex)

            attrTailWaving = 'Mr_Buttons:Mr_Buttons_Tail_02Ctrl.rotateZ'
            self.library.offsetKeyframes(attrTailWaving, 'TailWaving_1', self.prevBodyIndex, currBodyIndex)

            attrTailWaving = 'Mr_Buttons:Mr_Buttons_Tail_03Ctrl.rotateZ'
            self.library.offsetKeyframes(attrTailWaving, 'TailWaving_1', self.prevBodyIndex, currBodyIndex)

            attrTailWaving = 'Mr_Buttons:Mr_Buttons_Tail_04Ctrl.rotateZ'
            self.library.offsetKeyframes(attrTailWaving, 'TailWaving_1', self.prevBodyIndex, currBodyIndex)

            attrTailWaving = 'Mr_Buttons:Mr_Buttons_Tail_05Ctrl.rotateZ'
            self.library.offsetKeyframes(attrTailWaving, 'TailWaving_1', self.prevBodyIndex, currBodyIndex)

            attrStepDistanceRight = 'Mr_Buttons:Mr_Buttons_r_Leg_FootIKCtrl.translateZ'
            self.library.offsetKeyframes(attrStepDistanceRight, 'StepDistance_1', self.prevBodyIndex, currBodyIndex)

            attrStepDistanceLeft = 'Mr_Buttons:Mr_Buttons_l_Leg_FootIKCtrl.translateZ'
            self.library.offsetKeyframes(attrStepDistanceLeft, 'StepDistance_1', self.prevBodyIndex, currBodyIndex)

        # Store the previous BodyBeat index for the next calculation
        WalkLibraryUI.prevBodyIndex = self.paramWidgets[prefix].currentIndex() + 1

    def onDropDownArmsBeatChanged(self, index):
        """
        Takes in the new current index of the dropdown to change the layer state accordingly. It only differs from
        the onDropDownChanged() method in the sense that this one is also in charge of moving the keyframes of the
        UpDown_1 layer in order to adapt to the BodyBeat parameter.

        Args:
            index (int): index of the current selected option in the dropdown
        """

        prefix = 'ArmsBeat'

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
        self.library.calculatePlaybackRange(indices)

        # Query the current ArmsBeat index
        currArmsIndex = self.paramWidgets[prefix][0].currentIndex() + 1

        if currArmsIndex is not None:
            attrElbowsDragRight = 'Mr_Buttons:Mr_Buttons_r_Arm_ElbowFKCtrl.rotateY'
            self.library.offsetKeyframes(attrElbowsDragRight, 'ElbowsDrag_1', self.prevArmsIndex, currArmsIndex)

            attrElbowsDragLeft = 'Mr_Buttons:Mr_Buttons_l_Arm_ElbowFKCtrl.rotateY'
            self.library.offsetKeyframes(attrElbowsDragLeft, 'ElbowsDrag_1', self.prevArmsIndex, currArmsIndex)

            attrHandsDragRight = 'Mr_Buttons:Mr_Buttons_r_Arm_WristFKCtrl.rotateY'
            self.library.offsetKeyframes(attrHandsDragRight, 'HandsDrag_1', self.prevArmsIndex, currArmsIndex)

            attrHandsDragLeft = 'Mr_Buttons:Mr_Buttons_l_Arm_WristFKCtrl.rotateY'
            self.library.offsetKeyframes(attrHandsDragLeft, 'HandsDrag_1', self.prevArmsIndex, currArmsIndex)

        # Store the previous ArmsBeat index for the next calculation
        WalkLibraryUI.prevArmsIndex = self.paramWidgets[prefix][0].currentIndex() + 1

    def onSliderChanged(self, prefix, value):
        """
        Calculates the normalized slider value and applies it to the layer's weight
        Args:
            prefix(str): prefix of the layer associated with the slider
            value(float): current value of the slider
        """

        currIndex = 0

        if prefix == self.prefixes[1]:
            currIndex = self.paramWidgets[prefix][0].currentIndex()

        layerName = list(self.paramLayers[prefix].keys())[currIndex]
        weight = value / 1000.0
        self.library.changeLayerWeight(layerName, weight)

        if prefix == self.prefixes[2]:
            self.library.changeLayerWeight("CorrectiveTail_1", weight)

    def onSave(self, directory):
        """
        Imports the given preset file into the tool.
        If not given, the default name and directory will be used.
        If just given the name the default directory will be used with the given name.
        Args:
            directory(str): directory where the preset file to import is stored
        """

        directory = self.library.getDirectory()
        filePath = QtWidgets.QFileDialog.getSaveFileName(self, "Preset Browser", directory, "Text Files (*.json)")

        self.library.savePreset(filePath[0])

    def onImport(self, directory=""):
        """
        Resets the tool parameters to their default state.
        """

        if not directory:
            layers, weights = self.library.importPreset()
        else:
            browseDir = self.library.getDirectory()
            filePath = QtWidgets.QFileDialog.getOpenFileName(self, "Preset Browser", browseDir, "Text Files (*.json)")
            layers, weights = self.library.importPreset(filePath[0])

        # For each parameter apply the default layers data to the parameter
        if layers is not None and weights is not None:
            for i in range(0, len(layers)):

                # Get layer prefix
                splitStr = layers[i].split("_")
                prefix = splitStr[0]
                # Get the widget type

                if prefix == self.prefixes[1]:
                    index = int(splitStr[1]) - 1
                    self.paramWidgets[prefix][0].setCurrentIndex(index)
                    self.onDropDownChanged(prefix, index)

                    self.paramWidgets[prefix][1].setValue(weights[i]*1000.0)
                    self.onSliderChanged(prefix, weights[i]*1000.0)
                elif "Corrective" not in prefix:
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
                        self.paramWidgets[prefix].setValue(weights[i]*1000.0)
                        self.onSliderChanged(prefix, weights[i]*1000.0)
        else:
            logger.debug("Query for default preset file failed.")

    def HoverEvent(self, hovered, prefix, index):
        if hovered:
            if index == 4 and prefix == self.prefixes[1]:
                prefix = "ArmsSwing"

            self.paramDescriptionWidgets[index].setText(self.paramDescriptions[prefix])
        else:
            self.paramDescriptionWidgets[index].setText("Hover over a parameter to see its description")


class ParamLabel(QtWidgets.QLabel):
    def __init__(self, text, ref, prefix, index, parent=None):
        super(ParamLabel, self).__init__(parent)
        self.setAutoFillBackground(False)
        self.setMouseTracking(True)
        self.setText(text)
        self.hovered = False
        self.ref = ref
        self.prefix = prefix
        self.index = index

    def enterEvent(self, event):
        self.ref.HoverEvent(True, self.prefix, self.index)
        pass

    def leaveEvent(self, event):
        self.ref.HoverEvent(False, self.prefix, self.index)
        pass


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

def getWindowDock(name='WalkToolWinDock'):
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
    ctrl = cmds.workspaceControl(name, tabToControl=('AttributeEditor', 2), label='vmWalkingKit', vis=True)

    # Query the correspondent QtWidget associated with the dock
    qtCtrl = omui.MQtUtil_findControl(name)

    # We cast the queried window to QWidget so it's manageable within our Python code
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)

    return ptr

def deleteWindowDock(name='WalkToolWinDock'):
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
