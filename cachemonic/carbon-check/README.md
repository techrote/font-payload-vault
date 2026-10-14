# Carbon Check

Massive angled serif material cut by three controlled chatter marks.

**Category:** `cachemonic` · **Regular** · **proportional** · trial **44–120 px** · **SIL OFL 1.1**.

- Install `fonts/CarbonCheck-Regular.ttf`; for web use the adjacent `.woff2`.
- `source/design.py`: this face's settings and glyph-level design changes.
- [`DESIGN.md`](DESIGN.md): construction, artistic goals, utility and exclusions.
- [`specimen/specimen.svg`](specimen/specimen.svg): entire alphabet and useful mixed text.
- [`specimen/character-map.svg`](specimen/character-map.svg): all 254 encoded characters.
- [`specimen/index.html`](specimen/index.html): offline type tester (open from a local clone/download).
- [`OFL.txt`](OFL.txt): licensing for this newly created font software.

The full handwritten micro master is held in [`tools/third_cohort/masters.py`](../../tools/third_cohort/masters.py). These twelve designs share four **original** drawn alphabet lineages; each face applies its documented separate outline grammar. See the [shared build and verification workflow](../../docs/THIRD-COHORT-WORKFLOW.md). No copied commercial font outlines or existing vault master files are used.

Rebuild from the repository root:

```sh
python -m pip install -r requirements-third-cohort.txt
python tools/third_cohort/build.py
python tools/third_cohort/verify.py
python tools/third_cohort/specimen.py
```

The font is a first-edition, unhinted outline, not a verified Windows bitmap font. Suggested sizes are trial targets rather than tested human-factors performance.
