# vmWalkingKit
 
In this README you’ll find all the steps needed in order to make the vmWalkingKit work inside Maya. The steps are the following ones: 

1. Download the latest release .zip from the release [section](https://github.com/nintervik/vmWalkingKit/releases) of the repository and unzip it anywhere on your computer.<br/>
2. Inside the *vmWalkingKit_v0.5* folder, you’ll find five things:<br/>
   a. A folder called *vmWalkingKit*.<br/>
   b. A folder called *vmWalkingKitPresets*.<br/>
   c. A script called *Qt.py*.<br/>
   d. This *README* file.<br/>
   e. A *LICENSE* file.<br/>
3. Move both the *vmWakingKit* folder and the script *Qt.py* (a. and c.) to the following directory:     
*C:\Users\UserName\Documents\maya\version\scripts*<br/>
Where:<br/>
   - *C:* is the drive where Maya is installed.
   - *UserName* is the name of your user in Windows.
   - *version* is the version number of Maya that you want to use (2017→2019)<br/>
4. And then, move the *vmWakingKitPresets* folder (b.) to the following directory:     
*C:\Users\UserName\Documents\maya*<br/>
5. Open the Maya version corresponding to where you’ve put the files.<br/>
6. Go to File→Set Project and navigate to the *vmWalkingKit* folder. Inside you’ll find another folder called *mayaProject*. Set that folder as the project.<br/> 
7. In Maya, go to File→Open Scene (Ctrl+O) and open the *characterScene_#* where *#* is the Maya version you’re using.<br/>
8. Open the Script Editor by clicking on the bottom right button with the {;} or by going to Windows→General Editors→Script Editor.<br/>
9. Click on the + icon in the tabs section to open up a new tab. Choose Python as the executer source language.<br/>
10. In this tab, paste the following code:<br/>     
```python
   from vmWalkingKit.vmWalkingKitFiles import libraryUI

   reload(libraryUI)
   libraryUI.WalkLibraryUI()
```
11. Open the Custom tab in Maya’s Shelf. If the the Shelf is not visible, go to Windows→UI Elements→Shelf.<br/>  
12. Still with the this tab opened and inside the Script Editor, go to File→Save Script To Shelf…, write a name for it (e.g. *vmWalkingKit*) and click Ok. An icon with the chosen name should have appeared in the Custom Shelf tab.<br/>
13. Now, you can click on that icon once and the tool will be opened. You can resize the window and dock it anywhere you want as any other Maya's native window. And that’s it. You can start playing around with the tool. Have fun!<br/> 
