# About

<img src="webImgs/startup.png" width="400">

*vmWalkingKit* is an animation tool for Maya developed with Python for my Bachelor's Thesis. The tool's goal is to offer an interactive study about the theory behind walk cycles by providing the user with a playground to experiment with. This will be achieved through an easy-to-use UI that will allow the animator to tweak parameters in order to modify the end result of a character walking animation. The parameters will be divided into sections representing the main parts of the body.

The program will also come with a set of tool tips and useful information regarding walking animations and the available parameters. This tool is heavily based on the theory of *The Animator's Survival Kit* by Richard Williams; as it contains one of the best studies on the subject of walking.

Development and animation by [Víctor Masó Garcia](https://www.linkedin.com/in/vmasogarcia/).

You can check my other work in my [website](https://nintervik.github.io).

> Download the latest release [here](https://github.com/nintervik/vmWalkingKit/releases/tag/v0.95)

***

# Showcase video

<iframe src="https://player.vimeo.com/video/417271920" width="640" height="360" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>

# Attributions

[Mr. Buttons](bloomsbury.com/cw/cartoon-character-animation-with-maya/student-resources/mr-buttons/) rig by [Keith Osborn](http://www.keithosborn.com/).

<img src="webImgs/mrbuttons_rig.jpg" width="500">


# Installation instructions

**DISCLAIMERS:** 
* The tool should work with Maya 2017-2020 but it will perform best with later versions of Maya, especially with Maya 2019 and 2020. 
* When closing the tool, **always use the File->Quit option**. Do this operation before closing Maya or opening a new scene. 

You can watch this video down below or follow the written steps.

<iframe src="https://player.vimeo.com/video/430754588" width="640" height="360" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>

1. Download the latest release .zip from the release [section](https://github.com/nintervik/vmWalkingKit/releases) of the repository and unzip it anywhere on your computer.<br/>
2. Inside the *vmWalkingKit_v091* folder, you’ll find six items:<br/>
  
   <img src="webImgs/release_contents.png" width="200">
   
3. Move both the *vmWakingKit* folder and the script *Qt.py* (a. and f.) to the following directory: *C:\Users\UserName\Documents\maya\version\scripts* Where:
   - *C:* is the drive where Maya is installed.
   - *UserName* is the name of your user in Windows.
   - *version* is the version number of Maya that you want to use (2017-2019)<br/>
4. And then, move the *vmWalkingKitData* folder (b.) to the following directory:     
*C:\Users\UserName\Documents\maya*<br/>
5. Open the Maya version corresponding to where you’ve put the files.<br/>
6. Go to File→Set Project and navigate to the *vmWalkingKit* folder. Inside you’ll find another folder called *mayaProject*. Set that folder as the project.<br/> 
7. In Maya, go to File→Open Scene (Ctrl+O) and open the *characterScene*. You'll find the scene file in *mayaProject/scenes*.<br/>
8. Open the Script Editor by clicking on the bottom right button with the {;} or by going to Windows→General Editors→Script Editor.<br/>
9. Click on the + icon in the tabs section to open up a new tab. Choose Python as the executer source language.<br/>
10. In this tab, paste the following code:<br/>    

<!-- HTML generated using hilite.me --><div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%"><span style="color: #008800; font-weight: bold">from</span> <span style="color: #0e84b5; font-weight: bold">vmWalkingKit.vmWalkingKitFiles</span> <span style="color: #008800; font-weight: bold">import</span> libraryUI

<span style="color: #007020">reload</span>(libraryUI)
libraryUI<span style="color: #333333">.</span>WalkLibraryUI()
</pre></div>

**Important:** it is possible that when you paste the code above into the Script Editor the lines are indented (they contain spaces before them). Just make sure to delete any spaces before the lines; if the lines are indented the code won't compile at all.

11. Open the Custom tab in Maya’s Shelf. If the the Shelf is not visible, go to Windows→UI Elements→Shelf.<br/>  
12. Still with the this tab opened and inside the Script Editor, go to File→Save Script To Shelf…, write a name for it (e.g. *vmWK*) and click Ok. An icon with the chosen name should have appeared in the Custom Shelf tab.<br/>

<img src="webImgs/shelf_custom_script.png" width="900">

**Optional:** In case, you want the tool icon to show up instead of the Maya's Pyhton default one this can be done quickly. Right click on the new created shelf icon and go to Edit. Go the the Shelves tab and in the Icon Name field you will see a browse icon folder. The default path usually is *C:/Users/UserName/Documents/maya/mayaVersion/prefs/icons/*. You can move the icon image (*vmWK_icon.png*) from step 1 into that folder or any other that you like. Then, just navigate to the folder where you moved the icon image and select it. Leave the Icon Width field to automatic. And press the Save All Shelves button at the bottom left of the window. The icon should be changed for the tool one as in the below image.

<img src="webImgs/icon_shelf_window.PNG" width="650">

13. Now, you can click on that icon once and the tool will be opened. You can resize the window and dock it anywhere you want as any other Maya's native window.<br/>

14. Make sure to set the playback speed to *24 fps x 1* before starting to use the tool.<br/>

<img src="webImgs/fps_settings.png" width="900">

**Side note 1:** if you click on the shelf icon and you cannot see the tool window check the following cases in order:
* The tool is probably minimized as a tab on the right side of the screen (usually next to the Attribute Editor or the Channel Box tab).
* If you still cannot see it try opening a tab that is docked the right side of the screen (e.g the Attribute Editor); then, the tool tab will probably pop up. 
* The tool window may as well be minimized on the bottom left of Maya.

**Side note 2:** please do not delete any of the files that come with the release as they might be crucial in order to run the tool.

**Side note 3:** for a cleaner view, you can hide the grid by going to *Show->Grid* or by clicking on the grid icon. 

<img src="webImgs/grid_show.png" width="500">

The background color can also be changed: press ALT+B to cycle through the different default colors. You can also go to *Windows->Settings/Preferences->Color Settings->General->3D Views* to tweak the background colors to your taste.  

# How to use the tool

The tool is divided into three parts:

1. **The animation tabs:** each tab represents a body part of the character. Navigate through them to see all the possible options (the last one is related to the settings of the tool).
2. **The tabs content:** in each tab you'll find different parameters, hover over them to see their descriptions and tips about how to use them.
3. **Bottom buttons:** you'll find three buttons at the bottom of the tool to reset the parameters, import or save a preset. If you like a combination you can save the preset anywhere on your computer and import it later. There's already a couple of presets if you want to load them up into the tool.

<img src="webImgs/tool_window.png" width="500">

# About performance

The tool uses a lot of animation layers in order to create all the combinations. That has a considerable hit on performance that may affect your overall experience with the tool. In order to smooth out the potential performance issues it's recommended to follow these tips (in case of bad performance):

1. If you are using Maya 2019 or 2020 activate the Cached Playback option (*Playback → Cached Playback → Cached Playback*). If you can see the playback menu, check that you have the Animation menu set selected. You can find a drop-down menu to change this in the top left corner.

<img src="webImgs/cached_playback.png" width="900">

2. In the settings tab of the tool (the last one) you'll find information about how to minimize perfomance issues. Make sure to check that section if you run into performance problems.

<img src="webImgs/settings_tab.PNG" width="350">

3. Before changing any parameter or importing/saving a preset pause the animation and play it back once the changes are done.
3. Close any other programs that you don't need while using the tool. 

You can visualize the framerate of the scene by looking at the number displayed on the right bottom corner of the viewport. Anything below 20 fps is an indication of bad performance.

<img src="webImgs/framerate_display.png" width="500">


# License

~~~~~~~~~~~~~~~

MIT License

Copyright (c) 2020 nintervik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

~~~~~~~~~~~~~~~
