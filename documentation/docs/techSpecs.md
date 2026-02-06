# Technical Details

There are a few things about this menu that try and make it both easy and safe to use.

1. In the main folder there is a menu.py file that is used to add 5 relative plugin paths.  These are the following folders:
    1. `./gizmos` - for all NST gizmo files
    2. `./nk_files` - for all NST .nk scripts
    3. `./python`  - 1 helper file, and a handful of tool-specific python files
    4. `./icons`    - for all tool icons
    5. `./images` - for all image files required for some tools/examples

    **IMPORTANT:** This has changed from the v1.1.1 version of the NST to be relative paths. There were some network startup slowdowns happening from nuke recursively adding many pluginPaths in the previous init.py. Removing all the folders and narrowing it down to just 5 seemed to speed up start up time while keeping the menu looking the same. Also adding the plugin paths in the menu instead of the init made sure that there was not unnecessary load time happening for renderfarms or command-line nuke sessions where the GUI and menu is not needed.



2. The `menu.py` in the main folder is primarily building almost the entire toolkit menu.  You will find it organized into sections: `Draw, Time, Color, Filter`, etc.  The tools will show up in the order that you designate them in this menu.  

3. Nuke does not like to load multiple gizmo files with the same name.  Because the Nuke Survival Toolkit may be added into company pipelines that already have many gizmo’s being loaded in, I have given all .gizmo files their own prefix `“NST_”`.  This means all files should have a unique name to any file that would be already installed.  For example, if there was an `iBlur.gizmo` installed, the one in Nuke Survival Toolkit is named `NST_iBlur.gizmo`, so there should be no conflicts.  In the main menu.py at the top, there is a variable that you can replace if you choose to find/replace the `"NST_"` prefix to a custom one for all the gizmos.  You could do this with a renaming software or via the terminal for all gizmos with the `"NST_"` prefix.  If you change `"NST_"` to `"WOW_"` for example, just enter `"WOW_"` in this variable.  This might help if two different Nuke Survival Toolkits are being loaded at once, to keep them unique.

4. All gizmo’s are stored as `.gizmo` files on the folder system, but are all actually loaded into nuke as Groups, with no link back to the gizmo filepath.   This is a strange bug / feature / work around that sort of tricks nuke into thinking you have loaded a gizmo, but actually have loaded a group.  There are a few advantages to this method:

    1. Nuke will automatically open the properties panel of the tool, unlike if you nuke.nodePaste() a .nk file
    2. Nuke actually stores the defaults of the gizmo in memory, during that specific nuke session.  This means you will be able to `ctrl + right click` on knobs and reset them to their intended default settings.  This unfortunately goes away once you close and re-open the script, as nuke will just consider the nodes a normal group and will not know what the defaults are.
    3. Groups are generally easier to debug and enter inside to see what is going on.
    4. This will help with render farms or other users opening scripts that would normally be sourcing the gizmos from wherever you have placed the Nuke Survival Toolkit.  Sometimes render farms or other users cannot access your local directories, which might cause errors when other artists or render farms are trying to open the script, since they may not be loading the NukeSurvivalToolkit.  Making sure the tools are Groups will mean the tools exist in your nuke script and will never be unlinked/unsourced when someone else is opening the nuke script.

        If you prefer to use gizmos instead of groups, you simply have to open the gizmo in a text editor and change where it says `"Group"` at the top of each .gizmo file, and replace it with `"Gizmo"`.  It is case sensitive, so make sure you capitalize `Gizmo `or` Group.`

5. Removed all x and y node graph positions from the gizmos, (xpos and ypos).  If you leave these in; when you have a node selected and create a gizmo, instead of spawning under the node, it can fly to the part of the node graph where the x and y positions were stored at.

6. Removed all Nuke Version lines from the gizmos to avoid annoying errors about different versions.  Most of these tools were tested using Nuke 11.3v4,  but that does not mean they require that version. Some gizmos were created for different versions, so please use the links provided to see what versions the tools are compatible with if something is not working.

7. Tried consolidating the types of channels the gizmos might be bringing into your scripts by making sure they are using the same types of channel names.  For example, all Position World pass channels will come in as `P.red, P.green, P.blue, P.alpha`, and all Normals World pass channels will come in as `N.red, N.green, N.blue, N.alpha`.  There are a few exceptions where some tools are using unique channel names, but for the most part they are always using `.red, .green, .blue, .alpha, .u, or .v` at the end of the channels.  Most channel/layer names are kept as the original tool had them.  For example apChroma, hag_pos, despill, etc.

8. Added an Author Tag to the end of all Gizmos in the menu.  NKPD just stands for Nukepedia, where I did not make a custom tag if there weren't many tools from this author.  These might help in 2 ways: 

    1. To filter for certain tools if you want to search by all of Adrian Pueyo’s AP tools or Mark Joey Tang’s MJT tools using nuke’s tab search.  Will also help you identify who made what, and make it easier to find in the Tool Documentation


    2. To help identify that this gizmo is from the Nuke Survival Toolkit, in case there are  duplicate tools in the pipeline loaded with the same name.

9. Dealing with Hard Coded filepaths on Gizmo Creation

    1. There is a function, `filepathCreateNode()`, stored in the `NST_helper.py` file, that first detects if the Group/Gizmo being created has a `Read, DeepRead, ReadGeo, Camera, Axis`. Then, if the file knob in the node contains the string `<<<replace>>>` in the filepath, this will be replaced by the location where the NukeSurvivalToolkit is stored.
    2. This means for templates, example scripts, and occasional gizmos that require image files, They will be created with hardcoded links pointing to images in the Nuke Survival Toolkit.
    3. This was necessary because if I manually hardcoded the filepath, it will error because it does not know where your NST image is.  If you use a live variable, similar to [root.name] to try and point to the NST, it will work for you and anyone with the same NST installed, but not if you try and render on a renderfarm without the NST installed or pass the script to the artist without the NST installed, as nuke won’t find the variable and won’t know where to point to. Replacing the variable and hard coding the filepath on creation is the best way to make sure the tool to work with anyone opening the script, as long as the Nuke Survival Toolkit does not move locations, or the image file is not moved, deleted, renamed, etc