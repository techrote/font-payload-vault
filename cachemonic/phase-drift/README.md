# Phase Drift

Dot-matrix experiment: each glyph is a 5×7 raster of round dots, and every row is
displaced sideways by a fixed phase, so the lines look slightly out of register.

- Style: Regular, 1000 units/em, 254 encoded characters, fixed-pitch 600-unit cell
- Lowercase input is set as the capital raster (no text lowercase)
- Files: `fonts/PhaseDrift-Regular.ttf`, `fonts/PhaseDrift-Regular.woff2`
- Source: `source/design.py` (5×7 raster tables, row drift table `DRIFT`)
- Proofs: `specimen/specimen.svg`, `specimen/character-map.svg`, `specimen/index.html`
- Licence: SIL Open Font License 1.1, see `OFL.txt`

See [DESIGN.md](DESIGN.md) for intent, construction and limits.
