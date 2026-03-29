# TProject AK

**Author:** Alexey Kuchinski

<div class="video-container" data-video-id="xjzkxVZkvXM" data-video-type="youtube" data-thumbnail="../img/video-placeholder.webp">
</div>

- **Video Tutorial v9.0:** [https://youtu.be/xjzkxVZkvXM](https://youtu.be/xjzkxVZkvXM)

<div class="video-container" data-video-id="N-_M2lJWpe4" data-video-type="youtube" data-thumbnail="../img/tools/transform/tproject-thumb.webp">
</div>

- **Video Tutorial v7.0:** [https://youtu.be/N-_M2lJWpe4](https://youtu.be/N-_M2lJWpe4)

- [http://www.nukepedia.com/python/3d/cardtotrack](http://www.nukepedia.com/python/3d/cardtotrack)

TProject is similar to CProject but uses a Transform instead of a CornerPin to do a basic single point track.

Allows you to set frame, switch between stabilize and matchmove, add motion blur, and 3 different BBox management settings:

- **Hard Crop** - (reformat node - concatenation is preserved)
- **Adjustable crop** - breaks concatenation but allows for adjustable bbox
- **No Crop** - no crop applied at all, concatenation preserved but bbox can get quite big
**Set to input:** This will distort the image with the corner pin to fit the format, it is the same as projecting the image on a card and rendering in UV space.

### Screenshots

**TProject v9.0** - new UI

![TProject v9.0 — new UI](../img/tools/transform/tproject-v9-1.webp)

**TProject v7.0** - old UI

![tproject-1.webp](../img/tools/transform/tproject-1.webp)
