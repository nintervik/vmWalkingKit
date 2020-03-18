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
        self.resize(200, 200)

        # The Library variable points to an instance of our controller library
        self.library = walkLibrary.WalkLibrary()

        # Dropdown options list
        self.frameOptions = ["8f", "12f", "16f"]
        self.rangeOptions = ["Low", "Mid", "High"]

        # Every time we create a new instance, we will automatically create our UI
        self.createUI()

    def deleteInstance(self):
        if self.__class__.instance is not None:
            try:
                self.__class__.instance.deleteLater()
            except Exception as e:
                pass

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
        self.layout.addWidget(self.tabs)

        # Create tabs
        self.createGeneralTab()
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
        self.addParam(tabGeneral, "Body beat", self.frameOptions, 0, "onBeatChange")
        self.addParam(tabGeneral, "Arms beat", self.frameOptions, 1)
        self.addParam(tabGeneral, "Up & Down", self.rangeOptions, 2)
        self.addParam(tabGeneral, "Body Tilt", self.rangeOptions, 3)

    def createHeadTab(self):
        tabHead = self.addTab("Head")

    def createBottomBtns(self):

        # This is our child widget that holds all the buttons
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        self.layout.addWidget(btnWidget)

        # Create 'save' button
        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.onSave)
        btnLayout.addWidget(saveBtn)

        # Create 'read' button
        importBtn = QtWidgets.QPushButton('Read')
        importBtn.clicked.connect(self.onImport)
        btnLayout.addWidget(importBtn)

    # UI functionality methods

    def addTab(self, tabName):

        newTab = QtWidgets.QWidget()
        self.tabs.addTab(newTab, tabName)
        newTab.layout = QtWidgets.QGridLayout(self)
        newTab.layout.setContentsMargins(15, 15, 250, 10)
        newTab.setLayout(newTab.layout)

        return newTab

    def addParam(self, tab, paramName, options, id, slotName=None):

        # Create parameter
        paramText = QtWidgets.QLabel(paramName)
        dropDown = QtWidgets.QComboBox()
        dropDown.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)

        for i in range(0, len(options)):
            dropDown.addItem(options[i])

        if slotName is not None:
            dropDown.currentIndexChanged.connect(partial(getattr(self, slotName)))

        # Set parameter layout
        tab.layout.addWidget(paramText, id, 0, QtCore.Qt.AlignTop)
        tab.layout.addWidget(dropDown, id, 1, 15, 20, QtCore.Qt.AlignTop)
        paramText.setMinimumHeight(20)

    # SLOT METHODS

    def onBeatChange(self, index):
        self.library.setBeat(index)

    def onSave(self):
        self.library.savePreset()

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
