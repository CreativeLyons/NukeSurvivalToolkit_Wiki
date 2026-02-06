# Looper NKPD

**Author:** Damian Binder

![looper-2.webp](../img/tools/time/looper-2.webp)

- [http://www.nukepedia.com/gizmos/time/looper](http://www.nukepedia.com/gizmos/time/looper)

Looper is a tool that allows you to create seamless loops of playing clips.

Looping is not only a useful way to lengthen clips that are too short to be used in a comp but it is also a great way to save rendering times since only a specific frame range needs to be rendered.

Looper has two looping methods: Dissolve and Morph
**Dissolve:** Uses a simple Dissolve node to dissolve the input clip between an offset version of the same clip. The offset amount is determined by the number of frames looped. Works great when looping clips with constant/similar movement like rain or snow stock footage.

**Morph:** Similar to the Dissolve method but instead uses a Kronos node to calculate motion vectors to then generate a morphed loop. Best used with clips containing complex but well defined movement.
### Other Features:

- **FgMatte input:** An optional matte of the foreground can be used which may improve Kronos's motion estimation. (Highly recommended)
- Vector generator settings like Vector Detail and Strength are accessible.
- **Avoid Clip End knob:** Negatively offsets the input clip to avoid looping unexisting frames before first frame.
- A dynamic text visually indicates the total number of frames being looped.
