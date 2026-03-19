# CardToTrack_v9 AK

**Author:** Alexey Kuchinski

<div class="video-container" data-video-id="xjzkxVZkvXM" data-video-type="youtube" data-thumbnail="../img/video-placeholder.webp">
</div>

- Nukepedia: [https://www.nukepedia.com/tools/gizmos/3d/card-to-track/](https://www.nukepedia.com/tools/gizmos/3d/card-to-track/)
- Video: [Full tutorial](https://youtu.be/xjzkxVZkvXM)
- Video: [New features overview](https://youtu.be/sBNNLfTD0KI)
- Legacy branch in NST: [CardToTrack_v7 AK](card-to-track.md)

Finding position in 3D space based on Geometry, World position pass, Deep or manual method. Reconcile 3D position to CornerPin, Transform and Roto nodes.

### Video Tutorials

- [New Features](https://youtu.be/sBNNLfTD0KI)
- [Full Tutorial](https://youtu.be/xjzkxVZkvXM)

### Installation v9.06

add `cardtotrack` folder to your plugins directory next to your `init.py`

in your `init.py` add line

```py
nuke.pluginAddPath("./cardtotrack")
```

### v9.06

Thanks to Peter Mercell we have a fast version for Nuke 16

- Speed of generation is almost as fast as prior to Nuke 16
- Fixed glitch of Grid not being aligned to reference point sometimes
- Changed way the group is created to prevent accidental connection that broke internal connections in Group
- Fully back compatible (using good old code for Nuke 15 and lower)

### v9.05

Nuke 16 compatible version. Unfortunately had remove threading from the code as it seems like Nuke16 is more restrictive with implementation. As a result the code is way way slower than before. If someone able to improve on it - please shoot me a message.
Nuke 15 and lower - speed will remain the same.

### v9.03

Tested on Nuke15, tool will not work on Nuke16 yet, crashing on thread execution, not sure why..... will fix it eventually.

**Bugs fixed**

- Tool was not working wth Anamorphic footage corectly.
- Roto clip to format was changed to no clip

### v9.02

**Bugs fixed**

- Fixed broken calculation when label text had spaces inside
- Tproject had center point offset, now it will be correctly positioned in the center of the card
- Roto created had still format resolution set to Project fprmat and not input format
- Nuke 15.1 only it seems - stabilization in CProject became broken

### v9.01

**New features and improvements**

- Added Delete Button per Tab.
- CProject will check if another CProject is positioned upstream and adjust 'Aspect Ratio' automatically.
- Dropdown name in main dropdown changed from '3D Locator' to '3D Locator(Card or Axis)'.

**Bugs fixed**

- When stabilizing and Axis was appearing in weird places and not in the center of the card.
- In CProject When press 'Stabilize' while 'Set Input' enabled - label was not updated correctly.

**Known issues**

- Will not work correctly Under Nuke 14.0v1 due to some Nuke Bug. Fixed in Nuke 14.0v5 and higher.
- When CProject gizmo is created animation curves are not disapearing from Curve Editor, solved only when restart nuke. (Nuke bug ID 337536).

### v9.00

**New features and improvements**

- Nuke 14 tested, still fully based on Classic nodes.
- Full code refactor, various optimizations especially calculation speed improvements in long sequences.
- UI and general extraction are reworked for more fluid and user friendly workflow.
- Tabs per extraction added, extraction info now is stored within CardToTrack node itself.
- Added Stabilization option in 'Adjust TRS' area to help to get more precise card placement.
- Grid thikness and subdivision options added.
- Recalculating card by same name that already was calculated will update exsisting values in Group Tabs.
- Added option to recalculate camera for existing extracted objects.
- It is possible now after camera update to update nodes related to the CardToTrack group in nodegraph.
- Added option to generate linked TProject and CProject.
- Pixel Aspect ratio is taken from the input and not project settings.
- Option to choose between roto or rotopaint added.
- Exposed Axis in the 'Adjust TRS' area to easier card adjustment control.
- Added support to Axis connected to Camera.
- Added support to variable backplate offset in Camera.
- Added support to variable focal lenth values during a shot.
- Camera is not have to be directly connected to CardToTrack anymore.
- added input aspect option in CProject.
- added output format option in CProject.

**Known issues**

- It is impossible to create linked roto, (somehow it is not possible to link Roto's matrix knob, Nuke bug?)
- Impossible to hide CardToTrack curves (Nuke14 bug?)

### Installation v9.02 and Lower

Paste following files to your nuke plugins directory

- `card_to_track.py`
- `CardToTrack2.gizmo`
- `TProject2.gizmo`
- `CProject2.gizmo`
- `my.png`

Add those lines to your `meny.py`

```py
nodesMenu = nuke.menu('Nodes')
nodesMenu.addCommand('Transform/CardToTrack/CardToTrack', 'nuke.createNode("CardToTrack2")', icon='my.png')
nodesMenu.addCommand('Transform/CardToTrack/CProject', 'nuke.createNode("CProject2")', icon='CornerPin.png')
nodesMenu.addCommand('Transform/CardToTrack/TProject', 'nuke.createNode("TProject2")', icon='Transform.png')
```

**IMPORTANT:** Card to track must stay the group, do not convert it to the Gizmo.

**HUGE Thanks to numerous contributors and complainers that helped me to shape CardToTrack where it is now! Just to mention few:**

Eyal Shirazi, Helge Stang, Adrian Pueyo, Marco Meyer, Tony Lyons, Mark Joey Tang, Pete O'Connell, Ivan Busquets, Nikolai Wusterman, Philip Danner, Igor Majdandzic and aff course MAGNIFICENT TRIXTER FOLKS!!!!
