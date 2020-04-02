from maya import cmds
from collections import OrderedDict

# This is not done like this when shipping the tool.
# Watch from 5:30 of video 57
import walkLibrary
reload(walkLibrary)  # TODO: delete this when shipping.

# TODO: Substitute 'PySide2' with 'Qt' when shipping the tool.
# This is only for develop purposes
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
        self.prefixes = ["BodyBeat", "ArmsBeat", "UpDown", "BodyTilt"]

        # Populate 'paramLayers' dictionary with the current info on the scene
        self.initParamLayersData()

        # Every time we create a new instance, we will automatically create our UI
        self.createUI()
        self.onReset()

        # Saving initial BodyBeat index for adapting UpDown paramater accordingly
        self.prevBodyIndex = 2

        # Add ourself (QtWidgets.QWidget) to the parent's layout
        self.parent().layout().addWidget(self)

        # If docked mode is off, directly show our parent
        if not dock:
            parent.show()

    def initParamLayersData(self):

        layersNames, layersWeights = self.library.getCurrentAnimationLayers()

        # General tab
        bodyBeatDict = OrderedDict()
        bodyBeatDict[layersNames[0]] = layersWeights[0]
        bodyBeatDict[layersNames[1]] = layersWeights[1]
        bodyBeatDict[layersNames[2]] = layersWeights[2]

        armsBeatDict = OrderedDict()
        armsBeatDict[layersNames[3]] = layersWeights[3]
        armsBeatDict[layersNames[4]] = layersWeights[4]
        armsBeatDict[layersNames[5]] = layersWeights[5]

        upDownDict = OrderedDict()
        upDownDict[layersNames[6]] = layersWeights[6]

        bodyTiltDict = OrderedDict()
        bodyTiltDict[layersNames[7]] = layersWeights[7]

        self.paramLayers = {
            self.prefixes[0]: bodyBeatDict,
            self.prefixes[1]: armsBeatDict,
            self.prefixes[2]: upDownDict,
            self.prefixes[3]: bodyTiltDict
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
        #self.tabs.setDocumentMode(True)
        self.tabs.setUsesScrollButtons(True)
        self.layout.addWidget(self.tabs)

        # Create tabs
        self.createGeneralTab()
        self.createHeadTab()
        self.createHeadTab()
        self.createHeadTab()
        self.createHeadTab()
        self.createHeadTab()
        self.createHeadTab()
        self.createHeadTab()
        self.createHeadTab()

        # Create bottom buttons
        self.createBottomBtns()

    def createMenuBar(self):
        menubar = QtWidgets.QMenuBar()
        self.layout.addWidget(menubar)
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

        # Add tab
        tabGeneral = self.addTab("General")

        # Create General tab parameters
        self.addParam(tabGeneral, "Body beat", self.frameOptions, 0, self.prefixes[0], "onDropDownBodyBeatChanged")
        self.addParam(tabGeneral, "Arms beat", self.frameOptions, 1, self.prefixes[1], "onDropDownChanged")
        self.addParam(tabGeneral, "Up & Down", self.rangeOptions, 2, self.prefixes[2], "onSliderChanged")
        self.addParam(tabGeneral, "Body Tilt", self.rangeOptions, 3, self.prefixes[3], "onSliderChanged")

    def createHeadTab(self):
        tabHead = self.addTab("Head")
        tmpText = QtWidgets.QLabel("Work in progress.")
        self.scrollLayout.addWidget(tmpText)

    def createBottomBtns(self):

        # This is our child widget that holds all the buttons
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        self.layout.addWidget(btnWidget)

        # Create 'save' button
        saveBtn = QtWidgets.QPushButton('Save preset')
        # saveBtn.clicked.connect(self.onSave)
        btnLayout.addWidget(saveBtn)

        # Create 'read' button
        importBtn = QtWidgets.QPushButton('Import preset')
        #importBtn.clicked.connect(self.onImport)
        btnLayout.addWidget(importBtn)

        # Create 'read' button
        resetBtn = QtWidgets.QPushButton('Reset')
        resetBtn.clicked.connect(self.onReset)
        btnLayout.addWidget(resetBtn)

    # UI functionality methods

    def addTab(self, tabName):

        newTab = QtWidgets.QWidget()
        self.tabs.addTab(newTab, tabName)

        newTab.layout = QtWidgets.QGridLayout(newTab)
        newTab.layout.setContentsMargins(4, 4, 4, 4)
        newTab.setLayout(newTab.layout)

        scrollWidget = QtWidgets.QWidget()
        scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)

        self.scrollLayout = QtWidgets.QGridLayout(scrollWidget)
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        newTab.layout.addWidget(scrollArea, 1, 0, 5, 5)

        return newTab

    def addParam(self, tab, paramName, options, id, prefix, slotName=None):

        widget = None

        if slotName == "onDropDownChanged" or slotName == "onDropDownBodyBeatChanged":
            widget = QtWidgets.QComboBox()

            for i in range(0, len(options)):
                widget.addItem(options[i])

            widget.setCurrentIndex(1)
            widget.currentIndexChanged.connect(partial(getattr(self, slotName), prefix))

        elif slotName == "onSliderChanged":
            widget = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            widget.setMinimum(0)
            widget.setMaximum(1000)
            widget.setValue(200)
            widget.valueChanged.connect(partial(getattr(self, slotName), prefix))

        self.paramWidgets[prefix] = widget

        # Set parameter layout
        paramText = QtWidgets.QLabel(paramName)

        self.scrollLayout.addWidget(paramText, id, 0, 1, 3)
        paramText.setMinimumHeight(25)
        self.scrollLayout.addWidget(QtWidgets.QLabel(" "), id, 3, 1, 1)
        self.scrollLayout.addWidget(widget, id, 4, 1, 3)

        return widget

    # SLOT METHODS

    def onDropDownChanged(self, prefix, index):

        indStr = str(index + 1)

        for key in self.paramLayers[prefix]:

            layerName = key

            if indStr in key:
                self.library.changeLayerMuteState(layerName, False)
            else:
               self.library.changeLayerMuteState(layerName, True)

        activeLayers, weights = self.library.getActiveAnimationLayers()
        indices = []

        for i in range(0, len(activeLayers)):

            if len(indices) == 2:
                break

            splitStr = activeLayers[i].split("_")

            if self.prefixes[0] in splitStr[0] or self.prefixes[1] in splitStr[0]:
                indices.append(int(splitStr[1]))

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

        cmds.playbackOptions(animationEndTime=96)
        cmds.playbackOptions(minTime=1)
        cmds.playbackOptions(maxTime=playBackEndRange)
        cmds.playbackOptions(animationStartTime=1)

    def onDropDownBodyBeatChanged(self, prefix, index):

        indStr = str(index + 1)

        for key in self.paramLayers[prefix]:

            layerName = key

            if indStr in key:
                self.library.changeLayerMuteState(layerName, False)
            else:
               self.library.changeLayerMuteState(layerName, True)

        indices = []
        activeLayers, weights = self.library.getActiveAnimationLayers()

        for i in range(0, len(activeLayers)):

            if len(indices) == 2:
                break

            splitStr = activeLayers[i].split("_")

            if self.prefixes[0] in splitStr[0] or self.prefixes[1] in splitStr[0]:
                indices.append(int(splitStr[1]))

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

        currBodyIndex = self.paramWidgets[prefix].currentIndex() + 1

        if currBodyIndex is not None:

            cntrlName = 'Mr_Buttons:Mr_Buttons_COG_Ctrl'
            attrFull = '%s.%s' % (cntrlName, 'translateY')
            newKeys = []
            offset = 0

            if (self.prevBodyIndex == 1 and currBodyIndex == 2) or (self.prevBodyIndex == 2 and currBodyIndex == 3):
                offset = 1
            elif (self.prevBodyIndex == 2 and currBodyIndex == 1) or (self.prevBodyIndex == 3 and currBodyIndex == 2):
                offset = -1
            elif self.prevBodyIndex == 1 and currBodyIndex == 3:
                offset = 2
            elif self.prevBodyIndex == 3 and currBodyIndex == 1:
                offset = -2

            cmds.animLayer('UpDown_1', edit=True, selected=True)
            cmds.animLayer('UpDown_1', edit=True, lock=False)
            keyframes = cmds.keyframe(attrFull, query=True)

            for i in range(0, len(keyframes)):
                if i != 0:
                    keyframes = cmds.keyframe(attrFull, query=True)
                    cmds.keyframe(attrFull, edit=True, relative=True, timeChange=offset, time=(keyframes[i], keyframes[len(keyframes)-1]))                #increment += offset

            #for i in range(0, len(newKeys)):
            #   cmds.keyframe(cntrlName, edit=True, time=(keyframes[i], keyframes[i]), timeChange=newKeys[i])

            cmds.animLayer('UpDown_1', edit=True, lock=True)
            cmds.animLayer('UpDown_1', edit=True, selected=False)

        cmds.playbackOptions(animationEndTime=96)
        cmds.playbackOptions(minTime=1)
        cmds.playbackOptions(maxTime=playBackEndRange)
        cmds.playbackOptions(animationStartTime=1)

        self.prevBodyIndex = self.paramWidgets[prefix].currentIndex() + 1

    def onSliderChanged(self, prefix, value):

        layerName = list(self.paramLayers[prefix].keys())[0]
        weight = value / 1000.0
        self.library.changeLayerWeight(layerName, weight)

    def onSave(self):
        self.library.savePreset()

    def onReset(self):

        defaultLayers, defaultWeights = self.library.importPreset()

        # Setting default playback options
        cmds.playbackOptions(animationEndTime=96)
        cmds.playbackOptions(minTime=1)
        cmds.playbackOptions(maxTime=24)
        cmds.playbackOptions(animationStartTime=1)

        if defaultLayers is not None and defaultWeights is not None:
            for i in range(0, len(defaultLayers)):

                splitStr = defaultLayers[i].split("_")
                prefix = splitStr[0]
                widgetType = type(self.paramWidgets[prefix]).__name__

                if widgetType == 'QComboBox':
                    index = int(splitStr[1]) - 1
                    self.paramWidgets[prefix].setCurrentIndex(index)
                elif widgetType == 'QSlider':
                    self.paramWidgets[prefix].setValue(defaultWeights[i]*1000.0)
        else:
            print "Query for default preset file failed."

    def onImport(self):
        self.library.importPreset()

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
