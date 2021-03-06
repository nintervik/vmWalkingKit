from maya import cmds
import maya.mel as mel
from collections import OrderedDict
import time
import webbrowser

# Reload walkLibrary each time we execute this script to keep the package updated
import walkLibrary
reload(walkLibrary)

# This is only for developing purposes
from Qt import QtWidgets, QtCore, QtGui
from functools import partial
import Qt
import logging
from maya import OpenMayaUI as omui


# Setting up logger
logger = logging.getLogger('WalkLibraryUI')
logger.setLevel(logging.INFO)
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


class ToolStartupWindow(QtWidgets.QWidget):
    """The ToolStartupWindow is a startup dialog that is only used to show the startup window."""

    def __init__(self, library=None):
        """Init method to initialize the dialog.

        Args:
            library(walkLibrary): reference to the walkLibrary instance.
        """
        # Store the instance of walkLibrary in a local variable
        self.library = library

        # Delete UI if it already exists
        self.deleteUI()

        # Set the parent and layout
        self.parent = QtWidgets.QDialog(parent=getMayaMainWindow())
        self.parent.setObjectName('startup')
        self.parent.setWindowTitle('Startup Window')
        self.layout = QtWidgets.QGridLayout(self.parent)

        # Now that our parent is set we can initialize it
        super(ToolStartupWindow, self).__init__(parent=self.parent)

        # Customize window properties
        self.parent.setFixedSize(400, 350)
        self.parent.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint
                                   | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)

        # Create the UI
        self.createUI()

    def createUI(self):
        """Creates the UI for the startup window."""

        # Title
        welcomeLabel = QtWidgets.QLabel("            Welcome to vmWalkingKit!   ")
        welcomeLabel.setFont(QtGui.QFont('Arial', 15))
        self.layout.addWidget(welcomeLabel, 0, 0, QtCore.Qt.AlignTop)

        # Image
        label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap(walkLibrary.IMG_DIR)
        label.setPixmap(pixmap)
        self.layout.addWidget(label, 0, 0, 1, 2, QtCore.Qt.AlignCenter)

        # Checkbox to enable or disable the window creation at startup
        cb = QtWidgets.QCheckBox("Show this at startup")
        cb.setChecked(self.library.getStartupWinPref())
        cb.stateChanged.connect(self.onStartupChanged)
        self.layout.addWidget(cb, 0, 0, QtCore.Qt.AlignBottom)

        # OK button
        okBtn = QtWidgets.QPushButton('OK')
        okBtn.clicked.connect(self.deleteUI)
        okBtn.setMaximumWidth(60)
        self.layout.addWidget(okBtn, 0, 1, QtCore.Qt.AlignBottom)

    def onStartupChanged(self, state):
        """Sets the startup window user preferences based on the checkbox state.

        Args:
            state(int): indicates whether or not the user wants the startup window at startup.
        """

        self.library.setStartupWinPref(state)

    def showUI(self):
        """Displays the UI on screen."""

        self.parent.show()

    def deleteUI(self):
        """If the window already exists it will be deleted."""

        try:
            cmds.deleteUI('startup')
        except:
            logger.debug('No previous UI exists.')

class AboutWindow(QtWidgets.QWidget):
    """The AboutWindow is a dialog that is only used to show the about window."""

    def __init__(self):
        """Init method to initialize the dialog."""

        # Delete UI if it already exists
        self.deleteUI()

        # Set the parent and the UI
        self.parent = QtWidgets.QDialog(parent=getMayaMainWindow())
        self.parent.setObjectName('about')
        self.parent.setWindowTitle('About')
        self.layout = QtWidgets.QVBoxLayout(self.parent)

        # Now that our parent is set we can initialize it
        super(AboutWindow, self).__init__(parent=self.parent)

        # Set some window properties
        self.parent.setFixedSize(400, 565)
        self.parent.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint
                                   | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        # Create the UI
        self.createUI()

    def createUI(self):
        """Creates the UI for the startup window."""

        # Title
        titleLabel = QtWidgets.QLabel("vmWalkingKit v1.0")
        titleLabel.setFont(QtGui.QFont('Arial', 12, weight=QtGui.QFont.Bold))
        titleLabel.setStyleSheet('QLabel{color: #b0f5b0, font-weight: bold}')
        self.layout.addWidget(titleLabel, 0, QtCore.Qt.AlignTop)

        # Tool's description
        welcomeLabel = QtWidgets.QLabel()
        welcomeLabel.setText('<a href="https://nintervik.github.io/vmWalkingKit/"><span style="color:#7be36f;">vmWalkingKit</span></a>' +
                             " is an animation tool for Maya developed with " +
                             "Python for my Bachelor's Thesis. The tool's goal is to teach " +
                             "the theory behind walking animations while giving the user an " +
                             "interactive playground to experiment while learning.")
        welcomeLabel.setFont(QtGui.QFont('Arial', 9.5))
        welcomeLabel.setWordWrap(True)
        welcomeLabel.setOpenExternalLinks(True)
        self.layout.addWidget(welcomeLabel, 1, QtCore.Qt.AlignTop)

        # Author
        devLabel = QtWidgets.QLabel()
        devLabel.setText('<br>Developed & animated by ' + '<a href="https://nintervik.github.io/"><span style="color:#7be36f;">Victor Maso Garcia</span></a>')
        devLabel.setOpenExternalLinks(True)
        devLabel.setFont(QtGui.QFont('Arial', 9.5))
        self.layout.addWidget(devLabel, 1)

        # Rig credits
        websiteLabel = QtWidgets.QLabel()
        websiteLabel.setText('<br>' + '- ' + '<a href="https://www.bloomsbury.com/cw/cartoon-character-animation-with-maya/student-resources/mr-buttons/"><span style="color:#7be36f;">Mr. Buttons</span></a>'
                             + ' rig by ' + '<a href="http://www.keithosborn.com/"><span style="color:#7be36f;">Keith Osborn</span></a>')
        websiteLabel.setFont(QtGui.QFont('Arial', 9.5))
        websiteLabel.setOpenExternalLinks(True)
        self.layout.addWidget(websiteLabel, 1)

        # Libraries credits
        qtLabel = QtWidgets.QLabel()
        qtLabel.setText('- ' + 'UI programmed with ' + '<a href="https://github.com/mottosso/Qt.py"><span style="color:#7be36f;">Qt.py</span></a>'
                        + ' by ' + '<a href="https://mottosso.com/"><span style="color:#7be36f;">Marcus Ottosson</span></a>')
        qtLabel.setFont(QtGui.QFont('Arial', 9.5))
        qtLabel.setOpenExternalLinks(True)
        self.layout.addWidget(qtLabel, 1)

        # License
        licenseLabel = QtWidgets.QLabel()
        licenseLabel.setText("\n\nMIT License Copyright (c) 2020 nintervik" +
                             "\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated" +
                             ' documentation files (the "Software"), to deal in the Software without restriction, including without limitation the' +
                                                                 " rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell " +
                                                                 " copies of the Software, and to permit persons to whom the Software is furnished to do " +
                                                                 " so, subject to the following conditions:\n\n" +
                                                                 "The above copyright notice and this permission notice shall be included in all copies or "
                                                                 " substantial portions of the Software.\n\n" +
                                                                 'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING ' \
                                                                 "BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. " \
                                                                 "IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, " \
                                                                 "WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE " \
                                                                  "OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.")
        licenseLabel.setFont(QtGui.QFont('Arial', 9.5))
        licenseLabel.setWordWrap(True)
        self.layout.addWidget(licenseLabel, 1, QtCore.Qt.AlignTop)

    def showUI(self):
        """Displays the UI on screen."""

        self.parent.show()

    def deleteUI(self):
        """If the window already exists it will be deleted."""

        try:
            cmds.deleteUI('about')
        except:
            logger.debug('No previous UI exists.')

class WalkLibraryUI(QtWidgets.QWidget):
    """The WalkLibraryUI is a dialog that lets us control all the walkTool parameters."""

    # Saving initial BodyBeat and ArmsBeat indices for adapting others parameters accordingly
    prevBodyIndex = 2
    prevArmsIndex = 2

    # Settings variables to default values
    currLightingSetting = "default"
    startupWin = None
    aboutWin = None

    def __init__(self, dock=True):
        """Method to initialize the class.

        Args:
            dock(bool): wether or not to make to tool window dockable.
        """

        # Delete UI if it already exists
        try:
            cmds.deleteUI('walktool')
        except:
            logger.debug('No previous UI exists.')

        # If dock mode is queried the parent will be the docked window
        # If not, the parent will be the main Maya window
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

        # The Library variable points to an instance of our walkLibrary library
        self.library = walkLibrary.WalkLibrary()

        # Drop-down options list
        self.frameOptions = ["8f", "12f", "16f"]
        self.rangeOptions = ["Low", "Mid", "High"]
        self.handOptions = ["Relaxed", "Fist"]
        self.faceOptions = ["Happy", "Angry", "Sad", "Cocky", "Scared"]
        self.qualityOptions = ["Low", "Medium", "High"]

        # Parameters + Widgets relationship
        self.paramWidgets = OrderedDict()

        # Prefixes
        self.prefixes = ["BodyBeat", "ArmsBeat", "UpDown", "BodyTilt", "HeadUpDown", "HeadPigeon",
                         "HeadEgoist", "HeadNodding", "HeadTilt", "FaceExpression", "BackCurvature",
                         "PelvisYRotation", "PelvisWeightShift", "ChestYRotation", "ChestUpDown",
                         "TailSwing", "TailCurl", "TailTilt", "TailWaving", "ArmsWidth", "ElbowsDrag", "HandsDrag",
                         "HandsPose", "LegsSeparation", "FeetYRotation", "StepDistance"]

        # Layers + Attributes that need offset
        self.offsetBodyAttrDict = [
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_COG_Ctrl.translateY'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_r_Bowtie_01Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_r_Bowtie_02Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_l_Bowtie_01Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_l_Bowtie_02Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_r_Ear_01Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_r_Ear_02Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_l_Ear_01Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_l_Ear_02Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_Nose_01Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_Nose_02Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_r_Cheek_01Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_r_Cheek_02Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_l_Cheek_01Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_l_Cheek_02Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_Hair_01_01Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_Hair_01_02Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_Hair_02_01Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_Hair_02_02Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_Hair_03_01Ctrl.rotateZ'),
            ('UpDown_1',            'Mr_Buttons:Mr_Buttons_Hair_03_02Ctrl.rotateZ'),
            ('PelvisYRotation_1',   'Mr_Buttons:Mr_Buttons_COG_Ctrl.rotateY'),
            ('PelvisWeightShift_1', 'Mr_Buttons:Mr_Buttons_COG_Ctrl.translateX'),
            ('HeadPigeon_1',        'Mr_Buttons:Mr_Buttons_Head_01FKCtrl.translateZ'),
            ('HeadUpDown_1',        'Mr_Buttons:Mr_Buttons_Head_01FKCtrl.translateY'),
            ('HeadUpDown_1',        'Mr_Buttons:Mr_Buttons_r_Ear_01Ctrl.rotateZ'),
            ('HeadUpDown_1',        'Mr_Buttons:Mr_Buttons_r_Ear_02Ctrl.rotateZ'),
            ('HeadUpDown_1',        'Mr_Buttons:Mr_Buttons_l_Ear_01Ctrl.rotateZ'),
            ('HeadUpDown_1',        'Mr_Buttons:Mr_Buttons_l_Ear_02Ctrl.rotateZ'),
            ('HeadUpDown_1',        'Mr_Buttons:Mr_Buttons_Nose_01Ctrl.rotateZ'),
            ('HeadUpDown_1',        'Mr_Buttons:Mr_Buttons_Nose_02Ctrl.rotateZ'),
            ('HeadUpDown_1',        'Mr_Buttons:Mr_Buttons_r_Cheek_01Ctrl.rotateZ'),
            ('HeadUpDown_1',        'Mr_Buttons:Mr_Buttons_r_Cheek_02Ctrl.rotateZ'),
            ('HeadUpDown_1',        'Mr_Buttons:Mr_Buttons_l_Cheek_01Ctrl.rotateZ'),
            ('HeadUpDown_1',        'Mr_Buttons:Mr_Buttons_l_Cheek_02Ctrl.rotateZ'),
            ('HeadUpDown_1',        'Mr_Buttons:Mr_Buttons_Hair_01_01Ctrl.rotateZ'),
            ('HeadUpDown_1',        'Mr_Buttons:Mr_Buttons_Hair_01_02Ctrl.rotateZ'),
            ('HeadUpDown_1',        'Mr_Buttons:Mr_Buttons_Hair_02_01Ctrl.rotateZ'),
            ('HeadUpDown_1',        'Mr_Buttons:Mr_Buttons_Hair_02_02Ctrl.rotateZ'),
            ('HeadUpDown_1',        'Mr_Buttons:Mr_Buttons_Hair_03_01Ctrl.rotateZ'),
            ('HeadUpDown_1',        'Mr_Buttons:Mr_Buttons_Hair_03_02Ctrl.rotateZ'),
            ('HeadEgoist_1',        'Mr_Buttons:Mr_Buttons_Neck_01FKCtrl.rotateZ'),
            ('HeadEgoist_1',        'Mr_Buttons:Mr_Buttons_r_Ear_01Ctrl.rotateZ'),
            ('HeadEgoist_1',        'Mr_Buttons:Mr_Buttons_r_Ear_02Ctrl.rotateZ'),
            ('HeadEgoist_1',        'Mr_Buttons:Mr_Buttons_l_Ear_01Ctrl.rotateZ'),
            ('HeadEgoist_1',        'Mr_Buttons:Mr_Buttons_l_Ear_02Ctrl.rotateZ'),
            ('HeadEgoist_1',        'Mr_Buttons:Mr_Buttons_r_Cheek_01Ctrl.rotateZ'),
            ('HeadEgoist_1',        'Mr_Buttons:Mr_Buttons_r_Cheek_02Ctrl.rotateZ'),
            ('HeadEgoist_1',        'Mr_Buttons:Mr_Buttons_l_Cheek_01Ctrl.rotateZ'),
            ('HeadEgoist_1',        'Mr_Buttons:Mr_Buttons_l_Cheek_02Ctrl.rotateZ'),
            ('HeadEgoist_1',        'Mr_Buttons:Mr_Buttons_Hair_01_01Ctrl.rotateY'),
            ('HeadEgoist_1',        'Mr_Buttons:Mr_Buttons_Hair_01_02Ctrl.rotateY'),
            ('HeadEgoist_1',        'Mr_Buttons:Mr_Buttons_Hair_02_01Ctrl.rotateY'),
            ('HeadEgoist_1',        'Mr_Buttons:Mr_Buttons_Hair_02_02Ctrl.rotateY'),
            ('HeadEgoist_1',        'Mr_Buttons:Mr_Buttons_Hair_03_01Ctrl.rotateY'),
            ('HeadEgoist_1',        'Mr_Buttons:Mr_Buttons_Hair_03_02Ctrl.rotateY'),
            ('HeadNodding_1',       'Mr_Buttons:Mr_Buttons_Head_01FKCtrl.rotateX'),
            ('HeadNodding_1',       'Mr_Buttons:Mr_Buttons_Nose_01Ctrl.rotateZ'),
            ('HeadNodding_1',       'Mr_Buttons:Mr_Buttons_Nose_02Ctrl.rotateZ'),
            ('HeadNodding_1',       'Mr_Buttons:Mr_Buttons_r_Ear_01Ctrl.rotateY'),
            ('HeadNodding_1',       'Mr_Buttons:Mr_Buttons_r_Ear_02Ctrl.rotateY'),
            ('HeadNodding_1',       'Mr_Buttons:Mr_Buttons_l_Ear_01Ctrl.rotateY'),
            ('HeadNodding_1',       'Mr_Buttons:Mr_Buttons_l_Ear_02Ctrl.rotateY'),
            ('HeadNodding_1',       'Mr_Buttons:Mr_Buttons_r_Cheek_01Ctrl.rotateX'),
            ('HeadNodding_1',       'Mr_Buttons:Mr_Buttons_r_Cheek_02Ctrl.rotateX'),
            ('HeadNodding_1',       'Mr_Buttons:Mr_Buttons_l_Cheek_01Ctrl.rotateX'),
            ('HeadNodding_1',       'Mr_Buttons:Mr_Buttons_l_Cheek_02Ctrl.rotateX'),
            ('HeadNodding_1',       'Mr_Buttons:Mr_Buttons_Hair_01_01Ctrl.rotateZ'),
            ('HeadNodding_1',       'Mr_Buttons:Mr_Buttons_Hair_01_02Ctrl.rotateZ'),
            ('HeadNodding_1',       'Mr_Buttons:Mr_Buttons_Hair_02_01Ctrl.rotateZ'),
            ('HeadNodding_1',       'Mr_Buttons:Mr_Buttons_Hair_02_02Ctrl.rotateZ'),
            ('HeadNodding_1',       'Mr_Buttons:Mr_Buttons_Hair_03_01Ctrl.rotateZ'),
            ('HeadNodding_1',       'Mr_Buttons:Mr_Buttons_Hair_03_02Ctrl.rotateZ'),
            ('HeadTilt_1',          'Mr_Buttons:Mr_Buttons_Head_01FKCtrl.rotateX'),
            ('HeadPigeon_1',        'Mr_Buttons:Mr_Buttons_r_Ear_01Ctrl.rotateY'),
            ('HeadPigeon_1',        'Mr_Buttons:Mr_Buttons_r_Ear_02Ctrl.rotateY'),
            ('HeadPigeon_1',        'Mr_Buttons:Mr_Buttons_l_Ear_01Ctrl.rotateY'),
            ('HeadPigeon_1',        'Mr_Buttons:Mr_Buttons_l_Ear_02Ctrl.rotateY'),
            ('HeadPigeon_1',        'Mr_Buttons:Mr_Buttons_r_Cheek_01Ctrl.rotateY'),
            ('HeadPigeon_1',        'Mr_Buttons:Mr_Buttons_r_Cheek_02Ctrl.rotateY'),
            ('HeadPigeon_1',        'Mr_Buttons:Mr_Buttons_l_Cheek_01Ctrl.rotateY'),
            ('HeadPigeon_1',        'Mr_Buttons:Mr_Buttons_l_Cheek_02Ctrl.rotateY'),
            ('HeadPigeon_1',        'Mr_Buttons:Mr_Buttons_Hair_01_01Ctrl.rotateZ'),
            ('HeadPigeon_1',        'Mr_Buttons:Mr_Buttons_Hair_01_02Ctrl.rotateZ'),
            ('HeadPigeon_1',        'Mr_Buttons:Mr_Buttons_Hair_02_01Ctrl.rotateZ'),
            ('HeadPigeon_1',        'Mr_Buttons:Mr_Buttons_Hair_02_02Ctrl.rotateZ'),
            ('HeadPigeon_1',        'Mr_Buttons:Mr_Buttons_Hair_03_01Ctrl.rotateZ'),
            ('HeadPigeon_1',        'Mr_Buttons:Mr_Buttons_Hair_03_02Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_Spine_03FKCtrl.translateY'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_r_Bowtie_01Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_r_Bowtie_02Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_l_Bowtie_01Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_l_Bowtie_02Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_Nose_01Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_Nose_02Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_r_Ear_01Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_r_Ear_02Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_l_Ear_01Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_l_Ear_02Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_r_Cheek_01Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_r_Cheek_02Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_l_Cheek_01Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_l_Cheek_02Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_Hair_01_01Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_Hair_01_02Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_Hair_02_01Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_Hair_02_02Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_Hair_03_01Ctrl.rotateZ'),
            ('ChestUpDown_1',       'Mr_Buttons:Mr_Buttons_Hair_03_02Ctrl.rotateZ'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_Spine_03FKCtrl.rotateY'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_r_Bowtie_01Ctrl.rotateY'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_r_Bowtie_02Ctrl.rotateY'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_l_Bowtie_01Ctrl.rotateY'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_l_Bowtie_02Ctrl.rotateY'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_Nose_01Ctrl.rotateY'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_Nose_02Ctrl.rotateY'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_r_Ear_01Ctrl.rotateX'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_r_Ear_02Ctrl.rotateX'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_l_Ear_01Ctrl.rotateX'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_l_Ear_02Ctrl.rotateX'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_r_Cheek_01Ctrl.rotateY'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_r_Cheek_02Ctrl.rotateY'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_l_Cheek_01Ctrl.rotateY'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_l_Cheek_02Ctrl.rotateY'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_Hair_01_01Ctrl.rotateY'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_Hair_01_02Ctrl.rotateY'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_Hair_02_01Ctrl.rotateY'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_Hair_02_02Ctrl.rotateY'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_Hair_03_01Ctrl.rotateY'),
            ('ChestYRotation_1',    'Mr_Buttons:Mr_Buttons_Hair_03_02Ctrl.rotateY'),
            ('TailSwing_1',         'Mr_Buttons:Mr_Buttons_Tail_01Ctrl.rotateY'),
            ('TailSwing_1',         'Mr_Buttons:Mr_Buttons_Tail_02Ctrl.rotateY'),
            ('TailSwing_1',         'Mr_Buttons:Mr_Buttons_Tail_03Ctrl.rotateY'),
            ('TailSwing_1',         'Mr_Buttons:Mr_Buttons_Tail_04Ctrl.rotateY'),
            ('TailSwing_1',         'Mr_Buttons:Mr_Buttons_Tail_05Ctrl.rotateY'),
            ('TailWaving_1',        'Mr_Buttons:Mr_Buttons_Tail_01Ctrl.rotateZ'),
            ('TailWaving_1',        'Mr_Buttons:Mr_Buttons_Tail_02Ctrl.rotateZ'),
            ('TailWaving_1',        'Mr_Buttons:Mr_Buttons_Tail_03Ctrl.rotateZ'),
            ('TailWaving_1',        'Mr_Buttons:Mr_Buttons_Tail_04Ctrl.rotateZ'),
            ('TailWaving_1',        'Mr_Buttons:Mr_Buttons_Tail_05Ctrl.rotateZ'),
            ('StepDistance_1',      'Mr_Buttons:Mr_Buttons_r_Leg_FootIKCtrl.translateZ'),
            ('StepDistance_1',      'Mr_Buttons:Mr_Buttons_l_Leg_FootIKCtrl.translateZ')
        ]
        self.offsetArmsAttrDict = [
            ('ElbowsDrag_1', 'Mr_Buttons:Mr_Buttons_r_Arm_ElbowFKCtrl.rotateY'),
            ('ElbowsDrag_1', 'Mr_Buttons:Mr_Buttons_l_Arm_ElbowFKCtrl.rotateY'),
            ('HandsDrag_1',  'Mr_Buttons:Mr_Buttons_r_Arm_WristFKCtrl.rotateY'),
            ('HandsDrag_1',  'Mr_Buttons:Mr_Buttons_l_Arm_WristFKCtrl.rotateY')
        ]

        # UI text data
        self.paramDescriptions = self.library.getUIText("param")
        self.tabDescriptions = self.library.getUIText("tab")
        self.paramDescriptionWidgets = []

        # Populate 'paramLayers' dictionary with the current info on the scene
        self.initParamLayersData()

        # Every time we create a new instance, we will automatically create our UI
        self.createUI()
        self.onImport()

        # Add ourselves (QtWidgets.QWidget) to the parent's layout
        self.parent().layout().addWidget(self)

        # If docked mode is off, directly show our parent
        if not dock:
            parent.show()

        # Activate the Framerate visibility for Maya's heads up display
        mel.eval('setFrameRateVisibility(1);')

        # Create the instances for the startup and about window
        WalkLibraryUI.startupWin = ToolStartupWindow(self.library)
        WalkLibraryUI.aboutWin = AboutWindow()

        # Show the startup window if the user preferences indicate so
        if self.library.getStartupWinPref():
            WalkLibraryUI.startupWin.showUI()

    def initParamLayersData(self):
        """Initializes all the data structures needed for controlling animation layers and parameters."""

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

        # Create main data dictionary with all the layers information sorted by parameter
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

    # UI CREATION METHODS

    def createUI(self):
        """This method creates the UI."""

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
        """Creates the top menu bar."""

        # Creates the menu bar widges and add it to the master layout
        menubar = QtWidgets.QMenuBar()
        self.layout.addWidget(menubar)

        # Add the two top menu bar options
        actionFile = menubar.addMenu("File")
        actionHelp = menubar.addMenu("Help")

        # Add the options for File
        importOpt = actionFile.addAction('Import preset', partial(self.onImport, self.library.createDirectory()))
        importOpt.setStatusTip('Import a saved preset into the tool.')
        saveOpt = actionFile.addAction('Save preset', partial(self.onSave, self.library.createDirectory()))
        saveOpt.setStatusTip('Save a preset in your computer.')
        resetOpt = actionFile.addAction("Reset", self.onImport)
        resetOpt.setStatusTip('Reset the tool parameters to their default state.')
        actionFile.addSeparator()
        quitOpt = actionFile.addAction("Quit", self.onQuitTool)
        quitOpt.setStatusTip('Quit vmWalkingKit.')

        # Add the options for Help
        docOpt = actionHelp.addAction("Documentation", self.onDocClicked)
        docOpt.setStatusTip('Go to the documentation website.')
        startupOpt = actionHelp.addAction('Startup window', self.onWinStartup)
        startupOpt.setStatusTip('Open the startup window.')
        actionHelp.addSeparator()
        aboutOpt = actionHelp.addAction('About', self.onAboutClicked)
        aboutOpt.setStatusTip('Show information about vmWalkingKit.')

    def createDisplaySection(self, text, id):
        """Creates the display section for the animation theory of a tab.

        Args:
            text(str): text to be displayed.
            id(int): id of the widget within the tab.
        """

        # Information display area
        scrollWidgetInfo = QtWidgets.QWidget()
        scrollWidgetInfo.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)

        # Scroll layout
        self.scrollLayoutInfo = QtWidgets.QGridLayout(scrollWidgetInfo)

        # Scroll area widget creation
        scrollAreaInfo = QtWidgets.QScrollArea()
        scrollAreaInfo.setWidgetResizable(True)
        scrollAreaInfo.setWidget(scrollWidgetInfo)
        scrollAreaInfo.setStyleSheet('QScrollArea {border: 1px solid grey}')
        scrollAreaInfo.setMinimumSize(292, 260)

        # Parameter description setup
        textWidget = QtWidgets.QLabel(text)
        textWidget.setMinimumSize(292, 8)
        textWidget.setWordWrap(True)
        textWidget.setFont(QtGui.QFont('Arial', 9.5))

        # Add description to the list of paramDescriptionWidgets
        self.paramDescriptionWidgets.append(textWidget)

        # Add widgets to he layouts
        self.scrollLayoutInfo.addWidget(textWidget, 0, 0, 0, 0, QtCore.Qt.AlignTop)
        self.scrollLayout.addWidget(scrollAreaInfo, id, 0, 1, 7)

    def createTabDescription(self, tabName):
        """Creates tab description before the parameters.

        Args:
            tabName(str): name of the tab.
        """

        # Add the description text to the layout
        descriptionTxt = QtWidgets.QLabel(self.tabDescriptions[tabName])
        descriptionTxt.setMinimumSize(200, 8)
        descriptionTxt.setWordWrap(True)
        descriptionTxt.setFont(QtGui.QFont('Arial', 9.5))
        self.scrollLayout.addWidget(descriptionTxt, 0, 0, 1, 7)

        # Add separation line below the tab description
        sepLine = QtWidgets.QFrame()
        sepLine.setFrameShape(QtWidgets.QFrame.HLine)
        sepLine.setFrameShadow(QtWidgets.QFrame.Raised)

        # Add the widget to the main scroll layout
        self.scrollLayout.addWidget(sepLine, 1, 0, 1, 7)

    def createGeneralTab(self):
        """Creates the general tab."""

        # Add the new tab
        tabName = "General"
        self.addTab(tabName)

        # Create the tab description
        self.createTabDescription(tabName)

        index = 0

        # Create General tab parameters
        self.addDropDownParam("Body beat", self.frameOptions, 2, self.prefixes[0], index, "onDropDownBodyBeatChanged")
        self.addDropDownParam("Arms beat", self.frameOptions, 3, self.prefixes[1], index, "onDropDownArmsBeatChanged")
        self.addSliderParam("Up & Down", 4, self.prefixes[2], index, "onSliderChanged")
        self.addSliderParam("Body Tilt", 5, self.prefixes[3], index, "onSliderChanged")

        # Create the display section for the parameters descriptions
        self.createDisplaySection("Hover over a parameter to see its description.", 6)

    def createHeadTab(self):
        """Creates the head tab."""

        # Add the new tab
        tabName = "Head"
        self.addTab(tabName)

        # Create the tab description
        self.createTabDescription(tabName)

        index = 1

        # Create Head tab parameters
        self.addSliderParam("Head up-down", 2, self.prefixes[4], index, "onSliderChanged")
        self.addSliderParam("Head pigeon", 3, self.prefixes[5], index, "onSliderChanged")
        self.addSliderParam("Head egoist", 4, self.prefixes[6], index, "onSliderChanged",)
        self.addSliderParam("Head nodding", 5, self.prefixes[7], index, "onSliderChanged")
        self.addSliderParam("Head tilt", 6, self.prefixes[8], index, "onSliderChanged", 500)
        self.addDropDownParam("Facial expression", self.faceOptions, 7, self.prefixes[9], index, "onDropDownChanged")

        # Create the display section for the parameters descriptions
        self.createDisplaySection("Hover over a parameter to see its description", 8)

    def createTrunkTab(self):
        """Creates the trunk tab."""

        # Add the new tab
        tabName = "Trunk"
        self.addTab(tabName)

        # Create the tab description
        self.createTabDescription(tabName)

        index = 2

        # Create Trunk tab parameters
        self.addSliderParam("Back curvature", 2, self.prefixes[10], index, "onSliderChanged", 500)
        self.addSliderParam("Pelvis Y-rotation", 3, self.prefixes[11], index, "onSliderChanged")
        self.addSliderParam("Pelvis weight shift", 4, self.prefixes[12], index, "onSliderChanged")
        self.addSliderParam("Chest Y-rotation", 5, self.prefixes[13], index, "onSliderChanged")
        self.addSliderParam("Chest up-down", 6, self.prefixes[14], index, "onSliderChanged")

        # Create the display section for the parameters descriptions
        self.createDisplaySection("Hover over a parameter to see its description", 7)

    def createTailTab(self):
        """Creates the tail tab."""

        # Add the new tab
        tabName = "Tail"
        self.addTab(tabName)

        # Create the tab description
        self.createTabDescription(tabName)

        index = 3

        # Create Trunk tab parameters
        self.addSliderParam("Tail swinging", 2, self.prefixes[15], index, "onSliderChanged")
        self.addSliderParam("Tail curl", 3, self.prefixes[16], index, "onSliderChanged")
        self.addSliderParam("Tail tilt", 4, self.prefixes[17], index, "onSliderChanged")
        self.addSliderParam("Tail waving", 5, self.prefixes[18], index, "onSliderChanged")

        # Create the display section for the parameters descriptions
        self.createDisplaySection("Hover over a parameter to see its description", 8)

    def createArmsTab(self):
        """Creates the arms tab."""

        # Add the new tab
        tabName = "Arms"
        self.addTab(tabName)

        index = 4

        # Create the tab description
        self.createTabDescription(tabName)

        # Create Arms tab parameters
        self.addSliderParam("Arms swinging", 2, self.prefixes[1], index, "onSliderChanged", 500)
        self.addSliderParam("Arms separation", 3, self.prefixes[19], index, "onSliderChanged", 500)
        self.addSliderParam("Elbows drag", 4, self.prefixes[20], index, "onSliderChanged", 500)
        self.addSliderParam("Hands drag", 5, self.prefixes[21], index, "onSliderChanged", 500)
        self.addDropDownParam("Hands pose", self.handOptions, 6, self.prefixes[22], index, "onDropDownChanged")

        # Create the display section for the parameters descriptions
        self.createDisplaySection("Hover over a parameter to see its description", 9)

    def createLegsTab(self):
        """Creates the legs tab."""

        # Add the new tab
        tabName = "Legs"
        self.addTab(tabName)

        index = 5

        # Create the tab description
        self.createTabDescription(tabName)

        # Create General tab parameters
        self.addSliderParam("Legs separation", 2, self.prefixes[23], index, "onSliderChanged")
        self.addSliderParam("Feet Y-rotation", 3, self.prefixes[24], index, "onSliderChanged")
        self.addSliderParam("Step distance", 4, self.prefixes[25], index, "onSliderChanged")

        # Create the display section for the parameters descriptions
        self.createDisplaySection("Hover over a parameter to see its description", 10)

    def createSettingsTab(self):
        """Creates the settings tab."""

        # Add the new tab
        tabName = "Settings"
        self.addTab(tabName)

        index = 6

        # Create the tab description
        self.createTabDescription(tabName)

        # Create General tab parameters
        self.addDropDownSetting("Quality", self.qualityOptions, 2, "SettingsQuality", index, "onDropDownQualityChanged")
        self.addCheckboxSetting("Silhouette", 3, "SettingsSilhouette", index, "onCheckBoxSilhouetteChanged")
        self.addButtonPlayback("Playblast", 4, "SettingsPlayblast", index, "onPlayblastButtonPressed")

        # Create the display section for the parameters descriptions
        self.createDisplaySection("Hover over a parameter to see its description.", 11)

    def createBottomBtns(self):
        """Creates the bottom buttons."""

        # This is our child widget that holds all the buttons
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        self.layout.addWidget(btnWidget)

        # Create buttons, connect them to a slot and add them to our btnLayout

        # Save button
        saveBtn = QtWidgets.QPushButton('Save preset')
        saveBtn.clicked.connect(partial(self.onSave, self.library.createDirectory()))
        btnLayout.addWidget(saveBtn)

        # Read button
        importBtn = QtWidgets.QPushButton('Import preset')
        importBtn.clicked.connect(partial(self.onImport, self.library.createDirectory()))
        btnLayout.addWidget(importBtn)

        # Reset
        resetBtn = QtWidgets.QPushButton('Reset')
        resetBtn.clicked.connect(self.onImport)
        btnLayout.addWidget(resetBtn)

    # UI FUNCTIONALITY METHODS

    def addTab(self, tabName):
        """Creates a tab with the given name.

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
        """Adds a parameter of type drop-down.

        Args:
            paramName(str): the name of the parameter.
            options(list str): the list of options of the drop-down.
            id(int): the widget id.
            prefix(str): the prefix associated with the parameter.
            index(int): the tab index.
            slotName(str): the name of the slot method.
        """

        # Create drop-down and fill it with the options
        widget = QtWidgets.QComboBox()
        for i in range(0, len(options)):
            widget.addItem(options[i])

        # Set the drop-down default option
        widget.setCurrentIndex(1)

        # Connect the drop-down widget with the given slot (beats have a different slot than the rest
        # because they need to offset all the keyframes when changed).
        if prefix == 'BodyBeat' or prefix == 'ArmsBeat':
            widget.currentIndexChanged.connect(partial(getattr(self, slotName)))
        else:
            widget.currentIndexChanged.connect(partial(getattr(self, slotName), prefix))

        # Set up the widget to be displayed
        self.setUpParamWidget(prefix, widget, paramName, id, index)

    def addDropDownSetting(self, paramName, options, id, prefix, index, slotName=None):
        """Adds a parameter of type drop-down for the settings tab.

        Args:
            paramName(str): the name of the parameter.
            options(list str): the list of options of the drop-down.
            id(int): the widget id.
            prefix(str): the prefix associated with the parameter.
            index(int): the tab index.
            slotName(str): the name of the slot method.
        """

        # Create drop-down and fill it with the options
        widget = QtWidgets.QComboBox()
        for i in range(0, len(options)):
            widget.addItem(options[i])

        # Connect the drop-down widget with the given slot
        widget.currentIndexChanged.connect(getattr(self, slotName))

        # Set the drop-down default option
        widget.setCurrentIndex(1)

        # Set up the widget to be displayed
        self.setUpSettingWidget(prefix, widget, paramName, id, index)

    def addCheckboxSetting(self, paramName, id, prefix, index, slotName=None):
        """Adds a checkbox widget.

        Args:
            paramName(str): the name of the parameter.
            id(int): the widget id.
            prefix(str): the prefix associated with the parameter.
            index(int): the tab index.
            slotName(str): the name of the slot method.
        """

        # Create the checkbox widget and connect it to the slot
        widget = QtWidgets.QCheckBox("")
        widget.stateChanged.connect(getattr(self, slotName))

        # Set up the widget to be displayed
        self.setUpSettingWidget(prefix, widget, paramName, id, index)

    def addButtonPlayback(self, paramName, id, prefix, index, slotName=None):
        """Adds the playback button for the settings tab.

        Args:
            paramName(str): the name of the parameter.
            id(int): the widget id.
            prefix(str): the prefix associated with the parameter.
            index(int): the tab index.
            slotName(str): the name of the slot method.
        """

        # Create the button widget and connect it to the slot
        widget = QtWidgets.QPushButton('Apply')
        widget.clicked.connect(getattr(self, slotName))

        # Set up the widget to be displayed
        self.setUpSettingWidget(prefix, widget, paramName, id, index)

    def addSliderParam(self, paramName, id, prefix, index, slotName=None, defaultValue=200):
        """Adds ans slider widget.

        Args:
            paramName(str): the name of the parameter.
            id(int): the widget id.
            prefix(str): the prefix associated with the parameter.
            index(int): the tab index.
            slotName(str): the name of the slot method.
            defaultValue(float): default value for the slider.
        """

        # Create the slider widget and set the default value
        widget = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        widget.setMinimum(0)
        widget.setMaximum(1000)
        widget.setValue(defaultValue)

        # Connect the slider to the slot
        widget.valueChanged.connect(partial(getattr(self, slotName), prefix))

        # Set up the widget to be displayed
        self.setUpParamWidget(prefix, widget, paramName, id, index)

    def setUpParamWidget(self, prefix, widget, paramName, id, index):
        """Sets up the given widget to be displayed.

        Args:
            prefix(str): prefix associated with that widget.
            widget(QWidget): widget to be displayed
            paramName(str): name of the parameter associated with the widget.
            id(int): the widget id.
            index(int): the tab index.
        """

        # Add the prefix and widgets to paramWidgets to keep track of them
        if prefix == self.prefixes[1] and self.prefixes[1] not in self.paramWidgets:
            self.paramWidgets[prefix] = [widget, None]
        elif prefix == self.prefixes[1] and self.prefixes[1] in self.paramWidgets:
            self.paramWidgets[prefix][1] = widget
        else:
            self.paramWidgets[prefix] = widget

        # Set the text for the parameter
        paramText = ParamLabel(paramName, self, prefix, index)
        self.scrollLayout.addWidget(paramText, id, 0, 1, 3)
        paramText.setMinimumHeight(25)

        # Add the parameter text and the widget to the layout
        self.scrollLayout.addWidget(QtWidgets.QLabel(" "), id, 3, 1, 1)
        self.scrollLayout.addWidget(widget, id, 4, 1, 3)

    def setUpSettingWidget(self, prefix, widget, paramName, id, index):
        """Sets up the given settings widget to be displayed.

        Args:
            prefix(str): prefix associated with that widget.
            widget(QWidget): widget to be displayed
            paramName(str): name of the parameter associated with the widget.
            id(int): the widget id.
            index(int): the tab index.
        """

        # Set the text for the parameter
        settingText = ParamLabel(paramName, self, prefix, index)

        # Add the parameter text and the widget to the layout
        self.scrollLayout.addWidget(settingText, id, 0, 1, 3)
        settingText.setMinimumHeight(25)
        self.scrollLayout.addWidget(QtWidgets.QLabel(" "), id, 3, 1, 1)
        self.scrollLayout.addWidget(widget, id, 4, 1, 3)

    # SLOT METHODS

    def onDropDownChanged(self, prefix, index):
        """Takes in the new current index of the drop-down to change the layer state accordingly.

        Args:
            prefix:(string): prefix of the layer associated with this parameter.
            index (int): index of the current selected option in the drop-down.
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
        """Takes in the new current index of the drop-down to change the layer state accordingly. It only differs from
        the onDropDownChanged() method in the sense that this one is also in charge of moving the keyframes of other
        layers in order to adapt to the BodyBeat parameter.

        Args:
            index (int): index of the current selected option in the drop-down
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
            for attrInfo in self.offsetBodyAttrDict:
                layer, attr = attrInfo
                self.library.offsetKeyframes(attr, layer,
                                             self.prevBodyIndex,
                                             currBodyIndex)

        # Store the previous BodyBeat index for the next calculation
        WalkLibraryUI.prevBodyIndex = self.paramWidgets[prefix].currentIndex() + 1

    def onDropDownArmsBeatChanged(self, index):
        """Takes in the new current index of the drop-down to change the layer state accordingly. It only differs from
        the onDropDownChanged() method in the sense that this one is also in charge of moving the keyframes of other layers
        in order to adapt to the BodyBeat parameter.

        Args:
            index (int): index of the current selected option in the drop-down.
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
            for attrInfo in self.offsetArmsAttrDict:
                layer, attr = attrInfo
                self.library.offsetKeyframes(attr, layer,
                                             self.prevArmsIndex,
                                             currArmsIndex)

        # Store the previous ArmsBeat index for the next calculation
        WalkLibraryUI.prevArmsIndex = self.paramWidgets[prefix][0].currentIndex() + 1

    def onDropDownQualityChanged(self, index):
        """Changes the viewport configuration when the quality settings of the tool are changed.

        Args:
            index(int): current quality settings option.
        """

        # Low quality
        if index == 0:
            cmds.modelEditor('modelPanel4', e=True, displayTextures=False)
            cmds.modelEditor('modelPanel4', e=True, displayLights="default")
            cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", 0)
        # Medium quality
        elif index == 1:
            cmds.modelEditor('modelPanel4', e=True, displayTextures=True)
            cmds.modelEditor('modelPanel4', e=True, displayLights="default")
            cmds.modelEditor('modelPanel4', e=True, shadows=False)
            cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", 1)
        # High quality
        else:
            cmds.modelEditor('modelPanel4', e=True, displayTextures=True)
            cmds.modelEditor('modelPanel4', e=True, displayLights="all")
            cmds.modelEditor('modelPanel4', e=True, shadows=True)
            cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", 1)

        # Store the current lighting settings for future use
        WalkLibraryUI.currLightingSetting = cmds.modelEditor('modelPanel4', q=True, displayLights=True)

    def onSliderChanged(self, prefix, value):
        """Calculates the normalized slider value and applies it to the layer's weight.
        Args:
            prefix(str): prefix of the layer associated with the slider.
            value(float): current value of the slider.
        """

        currIndex = 0

        # Workaround to get the current index for the arms parameters
        if prefix == self.prefixes[1]:
            currIndex = self.paramWidgets[prefix][0].currentIndex()

        # Get the layer name
        layerName = list(self.paramLayers[prefix].keys())[currIndex]

        # Set up the normalized value and change the layer's weight accordingly
        weight = value / 1000.0
        self.library.changeLayerWeight(layerName, weight)

    def onCheckBoxSilhouetteChanged(self, state):
        """Change the scene lighting according to the silhouette checkbox.

        Args:
            state(bool): whether or not the silhouette checkbox is checked or not.
        """

        # If checked, turn the lights off
        if state:
            cmds.modelEditor('modelPanel4', e=True, displayLights="none")

        # If not checked, set the corresponding lighting that was previously set
        else:
            if WalkLibraryUI.currLightingSetting == "all":
                cmds.modelEditor('modelPanel4', e=True, displayLights="all")
            else:
                cmds.modelEditor('modelPanel4', e=True, displayLights="default")

    def onPlayblastButtonPressed(self):
        """Playblast the scene and stores the file with a unique name."""

        # Store the start and end times according to the timeline
        pStart = cmds.playbackOptions(q=True, animationStartTime=True)
        pEnd = cmds.playbackOptions(q=True, animationEndTime=True)

        # Generate a unique name based on the current date and time
        name = 'movies/vmwPlayblast_%s_%s' % (time.strftime('%d%m%Y'), time.strftime('%H%M%S'))

        # Save the playblast at maximum quality with the generated name
        cmds.playblast(st=pStart, et=pEnd, filename=name, format='avi', quality=100, p=100)

    def onSave(self, directory):
        """Imports the given preset file into the tool.
        If not given, the default name and directory will be used.
        If just given the name the default directory will be used with the given name.

        Args:
            directory(str): directory where the preset file to import is stored
        """

        # Open the browser window and save the preset with the user input name
        filePath = QtWidgets.QFileDialog.getSaveFileName(self, "Preset Browser", directory, "Text Files (*.json)")
        self.library.savePreset(filePath[0])

    def onImport(self, directory=""):
        """Imports the given directory.

        Args:
            directory(str): directory where the preset to be imported is located. If none, it will import the default
            preset. Hence, the tool will be reset.
        """

        # Open the browser to select the desired preset to import or import default one directly if none is given
        if not directory:
            layers, weights = self.library.importPreset()
        else:
            browseDir = self.library.createDirectory()
            filePath = QtWidgets.QFileDialog.getOpenFileName(self, "Preset Browser", browseDir, "Text Files (*.json)")
            layers, weights = self.library.importPreset(filePath[0])

        # For each parameter apply the default layers data to the parameter
        if layers is not None and weights is not None:
            for i in range(0, len(layers)):

                # Get layer prefix
                splitStr = layers[i].split("_")
                prefix = splitStr[0]

                # Workaround for a special case regarding the arms beat (as they have different data structure)
                if prefix == self.prefixes[1]:
                    # Get the index from the imported preset, set it on the drop-down and notify it has changed
                    # so keyframes from arms parameters can be offset properly
                    index = int(splitStr[1]) - 1
                    self.paramWidgets[prefix][0].setCurrentIndex(index)
                    self.onDropDownChanged(prefix, index)

                    # Set the value to the sliders according to the preset weights and notify it has changed
                    self.paramWidgets[prefix][1].setValue(weights[i]*1000.0)
                    self.onSliderChanged(prefix, weights[i]*1000.0)
                # Check first the animation layer is not corrective (they are just there to correct and are not
                # associated with
                elif "Corrective" not in prefix:
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
                        self.paramWidgets[prefix].setValue(weights[i]*1000.0)
                        self.onSliderChanged(prefix, weights[i]*1000.0)
        else:
            logger.debug("Query for default preset file failed.")

    def onQuitTool(self):

        if WalkLibraryUI.startupWin is not None:
            WalkLibraryUI.startupWin.deleteUI()

        if WalkLibraryUI.aboutWin is not None:
            WalkLibraryUI.aboutWin.deleteUI()

        deleteWindowDock()

    def onWinStartup(self):
        """Instantiates and shows the UI for the start up window."""

        WalkLibraryUI.startupWin = ToolStartupWindow(self.library)
        WalkLibraryUI.startupWin.showUI()

    def onDocClicked(self):
        """Open tool's website."""
        webbrowser.open('https://nintervik.github.io/vmWalkingKit/')

    def onAboutClicked(self):
        """Instantiates and shows the UI for the about window."""
        WalkLibraryUI.aboutWin = AboutWindow()
        WalkLibraryUI.aboutWin.showUI()

    # EVENT METHODS

    def HoverEvent(self, hovered, prefix, index):
        """Method that is called when a hover event occurs over a parameter label.

        Args:
            hovered(bool): indicates if the mouse pointer has entered or exit the label.
            prefix(str): the prefix associated with the parameter that has triggered the event.
            index(int): index associated with the parameter.
        """

        # If hovered, display the correspondent animation theory text
        if hovered:
            if index == 4 and prefix == self.prefixes[1]:
                prefix = "ArmsSwing"

            self.paramDescriptionWidgets[index].setText(self.paramDescriptions[prefix])
        else:
            self.paramDescriptionWidgets[index].setText("Hover over a parameter to see its description.")

class ParamLabel(QtWidgets.QLabel):
    """This class overwrites the QLabel in order to add the events for hovering over a label
    that will be used for displaying the animation theory of each parameter."""

    def __init__(self, text, ref, prefix, index, parent=None):
        """Initialize the ParamLabel class.

        Args:
            text(str): the text of the label to be displayed.
            ref(WalkLibraryUI): reference to the WalkLibraryUI instance.
            prefix(str): prefix associated with the parameter.
            index(int): index associated with the parameter.
            parent(obj): parent of the label (optional).
        """

        # Initialize the class variables with the given parameters
        super(ParamLabel, self).__init__(parent)
        self.setAutoFillBackground(False)
        self.setMouseTracking(True)
        self.setText(text)
        self.hovered = False
        self.ref = ref
        self.prefix = prefix
        self.index = index

    def enterEvent(self, event):
        """Event triggered when the mouse pointer hovers over the label.

        Args:
            event(obj): event object.
        """

        # Call a method in WalkLibraryUI to notify of the event
        self.ref.HoverEvent(True, self.prefix, self.index)

    def leaveEvent(self, event):
        """Event triggered when the mouse pointer stops hovering over the label.

        Args:
            event(obj): event object.
        """

        # Call a method in WalkLibraryUI to notify of the event
        self.ref.HoverEvent(False, self.prefix, self.index)

# MAYA WINDOWS FUNCTIONS

def getMayaMainWindow():
    """Get the main Maya window (which is also built with Qt).

    Returns:
        ptr(QtWidgets.QMainWindow): The Maya MainWindow.
    """

    # With OpenMayaUI API we query a reference to Maya's MainWindow
    win = omui.MQtUtil_mainWindow()

    # We cast the queried window to QMainWindow so it's manageable within our Python code
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)

    return ptr

def getWindowDock(name='WalkToolWinDock'):
    """Create dock with the given name.

    Args:
        name(str): name of the dock to create.

    Returns:
        ptr(QtWidget.QWidget): The dock's widget.
    """

    # Delete older dock
    deleteWindowDock(name)

    # Create a dock next to the Attribute Editor and query its name
    ctrl = cmds.workspaceControl(name, tabToControl=('AttributeEditor', 2), label='vmWalkingKit', vis=True)

    # Query the correspondent QtWidget associated with the dock
    qtCtrl = omui.MQtUtil_findControl(name)

    # We cast the queried window to QWidget so it's manageable within our Python code
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)

    return ptr

def deleteWindowDock(name='WalkToolWinDock'):
    """Deletes the given dock if this exists.

    Args:
        name(str): name of the window to delete.
    """

    if cmds.workspaceControl(name, exists=True):
        cmds.deleteUI(name)


# Call it in Maya's Script Editor
#from vmWalkingKit.vmWalkingKitFiles import libraryUI
#reload(libraryUI)

#libraryUI.WalkLibraryUI()
