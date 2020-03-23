from maya import cmds
from collections import OrderedDict

# This is not done like this when shipping the tool.
# Watch from 5:30 of video 57
import walkLibrary
reload(walkLibrary)  # <- delete this

# Substitute 'PySide2' with 'Qt' when shipping the tool.
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
else: # For PySide2 (Maya 2017 and above)
    logger.debug('Using PySide2 with shiboken2')
    from shiboken2 import wrapInstance

def getMayaMainWindow():
    win = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)

    return ptr

def getWindowDock(name='WalkToolDock'):
    deleteWindowDock(name)
    ctrl = cmds.workspaceControl(name, tabToControl=('AttributeEditor', 2), label='Walk Tool', vis=True)
    qtCtrl = omui.MQtUtil_findControl(name)
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)

    return ptr

def deleteWindowDock(name='WalkToolDock'):
    if cmds.workspaceControl(name, exists=True):
        cmds.deleteUI(name)

class WalkLibraryUI(QtWidgets.QWidget):
    """
    The WalkLibraryUI is a dialog that lets us control all the walkTool parameters.
    """

    def __init__(self, dock=True):

        try:
            cmds.deleteUI('walktool')
        except:
            logger.debug('No previous UI exists.')

        if dock:
            parent = getWindowDock()
        else:
            deleteWindowDock()

            parent = QtWidgets.QDialog(parent=getMayaMainWindow())
            parent.setObjectName('walktool')
            parent.setWindowTitle('Walk Tool')
            layout = QtWidgets.QVBoxLayout(parent)

        super(WalkLibraryUI, self).__init__(parent=parent)
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

        self.parent().layout().addWidget(self)
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
        self.layout.addWidget(menubar, 0, 0)
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
        self.addParam(tabGeneral, "Body beat", self.frameOptions, 0, self.prefixes[0], "onDropDownChanged")
        self.addParam(tabGeneral, "Arms beat", self.frameOptions, 1, self.prefixes[1], "onDropDownChanged")
        self.addParam(tabGeneral, "Up & Down", self.rangeOptions, 2, self.prefixes[2], "onSliderChanged")
        self.addParam(tabGeneral, "Body Tilt", self.rangeOptions, 3, self.prefixes[3], "onSliderChanged")

    def createHeadTab(self):
        tabHead = self.addTab("Head")

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

        # Create parameter
        paramText = QtWidgets.QLabel(paramName)
        dropDown = QtWidgets.QComboBox()
        dropDown.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)

        for i in range(0, len(options)):
            dropDown.addItem(options[i])

        if slotName is not None:
            dropDown.currentIndexChanged.connect(partial(getattr(self, slotName), prefix))

        self.paramWidgets[prefix] = dropDown

        # Set parameter layout
        self.scrollLayout.addWidget(paramText, id, 0, 1, 1)
        self.scrollLayout.addWidget(dropDown, id, 1, 1, 1)

        return dropDown


    # SLOT METHODS

    def onDropDownChanged(self, prefix, index):

        indStr = str(index + 1)

        for key in self.paramLayers[prefix]:

            layerName = key

            if indStr in key:
                self.library.changeLayerStateDropDown(layerName, False)
            else:
               self.library.changeLayerStateDropDown(layerName, True)

    def onSliderChanged(self, prefix, index):

        indStr = str(index + 1)

        for key in self.paramLayers[prefix]:

            layerName = key
            weight = self.paramLayers[prefix][layerName]

            if indStr in key:
                self.library.changeLayerStateSlider(layerName, weight)
            else:
               self.library.changeLayerStateSlider(layerName, weight)

    def onSave(self):
        self.library.savePreset()

    def onReset(self):

        activeLayers = self.library.resetPreset()

        if activeLayers is not None:
            for i in range(0, len(activeLayers)):
                splitStr = activeLayers[i].split("_")
                prefix = splitStr[0]
                index = int(splitStr[1]) - 1
                self.paramWidgets[prefix].setCurrentIndex(index)
        else:
            print "Query for default preset file failed."

    def onImport(self):
        self.library.importPreset()

def showUI():
    """
    This shows and returns a handle to the ui
    Returns:
        QDialog
    """
    ui = WalkLibraryUI()

    ui.show()
    return ui

# Call it in Maya's Script Editor
#from vmWalkingKit.vmWalkingKitFiles import libraryUI
#reload(libraryUI)

#libraryUI.WalkLibraryUI()
