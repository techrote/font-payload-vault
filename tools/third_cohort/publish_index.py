"""Add cohort entries without modifying any historical font source."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HEAD='## Third Cohort / 03 — twelve new fonts'
TABLE='''## Third Cohort / 03 — twelve new fonts

![Third Cohort overview](docs/third-cohort-overview.svg)

| Practical / system | Workshop / display | Cachemonic / experimental |
|---|---|---|
| [Tracebar Mono](cmd-font-container/tracebar-mono/) | [Torque Plate](hot-font-box/torque-plate/) | [Shift Ghost](cachemonic/shift-ghost/) |
| [Bushing Sans](cmd-font-container/bushing-sans/) | [Sling Arc](hot-font-box/sling-arc/) | [Eddy Notch](cachemonic/eddy-notch/) |
| [Microslab](cmd-font-container/microslab/) | [Swarf Bridge](hot-font-box/swarf-bridge/) | [Carbon Check](cachemonic/carbon-check/) |
| [Nibble Nine](cmd-font-container/nibble-nine/) | [Raster Forge](hot-font-box/raster-forge/) | [Checksum Haze](cachemonic/checksum-haze/) |

Twelve new distinct faces across four **original alphabet lineages**, with
separate construction treatments, documented artistic goals and realistic
ergonomic limits. Each offers a TTF, WOFF2, 254 codepoints, editable sources,
complete character map, offline tester and SIL OFL 1.1. Read the
[creation and qualification workflow](docs/THIRD-COHORT-WORKFLOW.md).

'''
p=ROOT/'README.md';s=p.read_text()
if HEAD not in s:
    if not s.startswith('# Font Payload Vault\n'):raise SystemExit('Unexpected root README authority')
    s=s.replace('# Font Payload Vault\n\n','# Font Payload Vault\n\n'+TABLE,1)
    p.write_text(s)
for cat,values in {
    'cmd-font-container':('tracebar-mono','bushing-sans','microslab','nibble-nine'),
    'hot-font-box':('torque-plate','sling-arc','swarf-bridge','raster-forge'),
    'cachemonic':('shift-ghost','eddy-notch','carbon-check','checksum-haze')}.items():
    p=ROOT/cat/'README.md';s=p.read_text()
    if '## Third Cohort / 03' not in s:
        body='\n## Third Cohort / 03\n\n'+''.join(f'- [{v}]({v}/) — original source, two compiled formats, specimen, design and utility notes.\n' for v in values)
        p.write_text(s.rstrip()+'\n'+body)
print('Root/category font indexes augmented without editing older font masters.')
