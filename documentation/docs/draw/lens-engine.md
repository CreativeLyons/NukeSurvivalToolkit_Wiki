# LensEngine KB

**Author:** Kyran Bishop - [https://www.kyranbishop3d.com](https://www.kyranbishop3d.com)

![lens-engine-2.webp](../img/tools/draw/lens-engine-2.webp)

- [https://www.nukepedia.com/tools/gizmos/draw/lens-engine/](https://www.nukepedia.com/tools/gizmos/draw/lens-engine/)

A comprehensive lens flare, lens FX, and glass reflection simulator built as a single self-contained gizmo. Position the flare source with a 2D point control, then independently enable and adjust each optical element through a tabbed UI.

Built as part of a research project into lens optics, drawing design inspiration from Doug Hogan's Flare Factory and Vincent Wauters' AutoFlare, with improved concatenation and additional FX layers.

### Core elements (Cores tab)

- **Core** — central bright spot with type picker: white orb, anamorphic, hot orb, prism
- **Core rays** — star burst rays with thickness, rotation, and seed controls
- **Core corona** — inner corona ring with noise and tint
- **Extra corona** — secondary outer corona ring

### Anomalies tab

- **Lens anomaly** — secondary orb-style artifact that tracks along the flare axis
- **Dog schidt** — elongated streak artifact with thickness, falloff, and anamorph controls
- **Frame ghosting** — up to four independent ghost reflections with shape, diaphragm, and noise controls

### Lens pieces tab

- **Main pieces** — small randomised bokeh-shaped elements scattered along the axis
- **Big pieces** — larger individual lens flare elements
- **Rings** — circular ring artifacts
- **Lines** — linear streak elements

### Screen FX tab

- **Bloom** — threshold-based bloom with center, edge, and photographically-based modes
- **Edge shimmer** — shimmer glow along the frame edge
- **Vignetting** — adjustable vignette with region controls
- **Edge blur** — softens the frame edges
- **Chroma shift** — chromatic aberration with red/green/blue axis controls
- **Lens distortion** — barrel/pincushion distortion with two coefficients

### Lens dirt tab

- **Lens dirt** — choose from built-in patterns (water, scratches, streaks) or a custom input; supports simple and normals-based calculation modes with bokeh blur option

![lens-engine-1.webp](../img/tools/draw/lens-engine-1.webp)
