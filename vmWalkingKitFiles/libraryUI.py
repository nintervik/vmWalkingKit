from maya import cmds

# This is not done like this when shipping the tool.
# See first 10 minutes of video 57
import walkLibrary
reload(walkLibrary)
# Substitute PySide2 with Qt when shipping the tool.
# This is only for develop purposes
from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial

class WalkLibraryUI(QtWidgets.QDialog):
    """
    The WalkLibraryUI is a dialog that lets us control all the walkTool parameters.
    """
    windowName = "WalkLibrary"

    def __init__(self):
        super(WalkLibraryUI, self).__init__()

        self.setWindowTitle(self.windowName)
        self.resize(400, 350)

        # The Library variable points to an instance of our controller library
        self.library = walkLibrary.WalkLibrary()

        # Dropdown options list
        self.frameOptions = ["8f", "12f", "16f"]
        self.rangeOptions = ["Low", "Mid", "High"]
        self.paramDropDowns = {}

        # Prefixes
        self.prefixes = ["BodyBeat", "ArmsBeat", "UpDown", "BodyTilt"]

        # Populate 'paramLayers' dictionary with the current info on the scene
        self.initParamLayersData()

        # Every time we create a new instance, we will automatically create our UI
        self.createUI()

    def initParamLayersData(self):

        childLayers = self.library.getCurrentAnimationLayers()

        # General tab
        bodyBeatList = [childLayers[0],  childLayers[1],  childLayers[2]]
        armsBeatList = [childLayers[3],  childLayers[4],  childLayers[5]]
        upDownList =   [childLayers[6],  childLayers[7],  childLayers[8]]
        bodyTiltList = [childLayers[9],  childLayers[10], childLayers[11]]

        self.paramLayers = {
            self.prefixes[0]: bodyBeatList,
            self.prefixes[1]: armsBeatList,
            self.prefixes[2]: upDownList,
            self.prefixes[3]: bodyTiltList
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
        self.addParam(tabGeneral, "Body beat", self.frameOptions, 0, self.prefixes[0], "onParamChanged")
        self.addParam(tabGeneral, "Arms beat", self.frameOptions, 1, self.prefixes[1], "onParamChanged")
        self.addParam(tabGeneral, "Up & Down", self.rangeOptions, 2, self.prefixes[2], "onParamChanged")
        self.addParam(tabGeneral, "Body Tilt", self.rangeOptions, 3, self.prefixes[3], "onParamChanged")

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

        self.paramDropDowns[prefix] = dropDown

        # Set parameter layout
        self.scrollLayout.addWidget(paramText, id, 0, 1, 1)
        self.scrollLayout.addWidget(dropDown, id, 1, 1, 1)

        return dropDown


    # SLOT METHODS

    def onParamChanged(self, prefix, index):

        prefixLayers = []

        for i in range(0, len(self.paramLayers[prefix])):
            prefixLayers.append(self.paramLayers[prefix][i])

        self.library.setActiveLayer(prefixLayers, index)

    def onSave(self):
        self.library.savePreset()

    def onReset(self):

        activeLayers = self.library.resetPreset()

        if activeLayers is not None:
            for i in range(0, len(activeLayers)):
                splitStr = activeLayers[i].split("_")
                prefix = splitStr[0]
                index = int(splitStr[1]) - 1
                self.paramDropDowns[prefix].setCurrentIndex(index)
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

#ui = libraryUI.showUI()
