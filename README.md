# vmWalkingKit
 
In this README you’ll find all the steps needed in order to make the vmWalkingKit work inside Maya. The steps are the following ones: 

**1.** Download the latest release .zip from the release [section](https://github.com/nintervik/vmWalkingKit/releases) of the repository and unzip it anywhere on your computer.
**2.** Inside the *vmWalkingKit_v0.5* folder, you’ll find two things:<br/>
   a. A folder called *vmWalkingKit*.<br/> 
   b. A script called *Qt.py*.<br/>
   c. This *README* file.<br/>
   d. A *LICENSE* file.<br/>
Move both the folder and the script (a. and b.) to the following directory:     
*C:\Users\UserName\Documents\maya\version\scripts<br/>*
Where:
   - *C:* is the drive where Maya is installed.
   - *UserName* is the name of your user in Windows.
   - *version* is the version number of Maya that you want to use (2017→2019)
**3.** Open the Maya version corresponding to where you’ve put the files.
**4.** Go to File→Set Project and navigate to the *vmWalkingKit* folder. Inside you’ll find another folder called *mayaProject*. Set that folder as the project. 
**5.** In Maya, go to File→Open Scene (Ctrl+O) and open the *characterScene_#* where *#* is the Maya version you’re using.
**6.** Open the Script Editor by clicking on the bottom right button with the {;} or by going to Windows→General Editors→Script Editor.
**7.** Click on the + icon in the tabs section to open up a new tab. Choose Python as the executer source language.
**8.** In this tab, paste the following code:     
```python
   from vmWalkingKit.vmWalkingKitFiles import libraryUI

   reload(libraryUI)
   libraryUI.WalkLibraryUI()
```
**9.** Open the Custom tab in Maya’s Shelf. If the the Shelf is not visible, go to Windows→UI Elements→Shelf.  
**10.** Still with the this tab opened and inside the Script Editor, go to File→Save Script To Shelf…, write a name for it (e.g. *vmWalkingKit*) and click Ok. An icon with the chosen name should have appeared in the Custom Shelf tab.
**11.** Now, you can click on that icon once and the tool will be opened. You can resize the window and dock it anywhere you want as any other Maya's native window. And that’s it. You can start playing around with the tool. Have fun! 
