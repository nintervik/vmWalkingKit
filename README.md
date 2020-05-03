# vmWalkingKit

*vmWalkingKit* is an animation tool for Maya developed with Python for my Bachelor's Thesis. The tool's goal is to teach the theory behind walking animations while giving the user an interactive playground to experiment while learning. This will be achieved by providing an easy-to-use UI that will allow the animator to tweak parameters in order to modify the end result of a character walking animation. The parameters will be divided into sections representing the main parts of the body.

The program will also come with a set of tool tips and useful information regarding walking animations and the available parameters. This tool is heavily based on the theory of *The Animator's Survival Kit* by Richard Williams; as it contains one of the best studies on the subject of walking.

# Changelog

Down below you'll find the changelog for each version of tool along with the
correspondent showcase video illustrating the new features.

v0.1 ([video](https://vimeo.com/402131641)):
* Code structure is done.
* The tool can be reset to its default values by reading from a JSON file.
* General tab works and the respective animations are done.
* Animations always loop correctly.
* Animations adapt to the beat.
* UI is native and usable (resizable, with scrollbar, can be docked,
etc)
* Performance issues are fixed.

v0.5 ([video](https://vimeo.com/413653094)):
* Head, trunk, arms tabs and animations are done.
* Section for the information display works (with placeholder text).
* Presets can be saved and imported into the tool.

v0.9 (*in progress*):
* Hands poses, legs and tail parameters work and are animated.
* All the theory and information is written and displayed where
needed.
* Performance settings tab is implemented.
 
# Installation instructions

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

**Side note:** if you click on the shelf icon and you cannot see the tool window check the following cases in order:
* The tool is probably minimized as a tab on the right side of the screen (usually next to the Attribute Editor or the Channel Box tab). * If you still cannot see it try opening a tab that is docked the right side of the screen (e.g the Attribute Editor); then, the tool tab will probably pop up. 
* Also check the tool window is not minimized on the left bottom of Maya.

# Attributions

[Mr. Buttons](bloomsbury.com/cw/cartoon-character-animation-with-maya/student-resources/mr-buttons/) rig by [Keith Osborn](http://www.keithosborn.com/).
