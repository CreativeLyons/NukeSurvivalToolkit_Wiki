# CProject AK

**Author:** Alexey Kuchinski

<div class="video-container" data-video-id="N-_M2lJWpe4" data-video-type="youtube" data-thumbnail="../img/tools/transform/cproject-thumb.webp">
</div>

- [http://www.nukepedia.com/python/3d/cardtotrack](http://www.nukepedia.com/python/3d/cardtotrack)
- Video: [https://youtu.be/N-_M2lJWpe4](https://youtu.be/N-_M2lJWpe4)

CornerPin matchmove/stabilize meant to be used with CardToTrack tool.

Allows you to set frame, switch between stabilize and matchmove, add motion blur, and 3 different BBox management settings:

- **Hard Crop** - (reformat node - concatenation is preserved)
- **Adjustable crop** - breaks concatenation but allows for adjustable bbox
- **No Crop** - no crop applied at all, concatenation preserved but bbox can get quite big
**Set to input:** This will distort the image with the corner pin to fit the format, it is the same as projecting the image on a card and rendering in UV space.

![shared-transform-2.webp](../img/tools/transform/shared-transform-2.webp)

![shared-transform-3.webp](../img/tools/transform/shared-transform-3.webp)
