# JarvisMobil Custom Wraps

Target: Tesla Model Y Premium (2025+) / Juniper.

## Ready for vehicle test

### 1. JarvisMobil_Mark85_v1.png
Armor-inspired palette: deep metallic red, muted gold, carbon-black and arc-reactor cyan.

### 2. JarvisMobil_ArcBlue_v1.png
JARVIS / arc-reactor palette: deep metallic blue, silver, carbon-black and luminous cyan.

Both files are generated directly against Tesla's authoritative `modely-2025-premium/template.png`.

## Validation
- PNG
- 1024 × 1024
- Under Tesla's 1 MB limit
- Original Tesla template remains unchanged
- Generated deterministically by `generate_wraps.py`

## Vehicle test
Upload through Tesla app v4.59+:
`Creations → Wrap → Upload`

The first in-car render is the UV-fit validation pass. Any seam/alignment correction should be made from screenshots of the rendered 3D vehicle.
