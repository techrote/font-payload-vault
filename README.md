# Font Payload Vault

Original type experiments with their complete design sources, rebuild tooling,
specimens and notes about what they are actually good for.

## Original Trio / 01

![Three new original faces](docs/original-trio-overview.svg)

| Family | Intended use | Character |
|---|---|---|
| [Latchline Mono](cmd-font-container/latchline-mono/) | Terminals, diagnostic panes, source listings | Monoline precision; genuine lowercase; fixed 640-unit cells |
| [Diecast Relay](hot-font-box/diecast-relay/) | Short titles and workshop-themed labels | Heavy chamfered solids; relief slots; proportional caps and small capitals |
| [Cache Rattle](cachemonic/cache-rattle/) | Short glitch titles and fictional diagnostics | Original pixel master; deterministic scanline tearing; fixed 660-unit cells |

Each is a new independent design with one Regular style, TTF + WOFF2, 254 encoded
characters, a full character map and an offline browser tester. They do not reuse
an existing font's outlines. The fonts, sources and accompanying design documents
are included in their respective folders under SIL OFL 1.1, with no Reserved
Font Names. This does not change the licensing status of older repository work.

Read the [production and verification workflow](docs/ORIGINAL-TRIO-WORKFLOW.md)
for provenance, build commands, checks and limits. Practical benefits and size
ranges are design intentions, not measured accessibility or reading-performance
claims. Download/clone the repository before opening an interactive specimen;
GitHub's source viewer does not execute the tester.

## Vault compartments

| Folder | Contents |
|---|---|
| [cmd-font-container](cmd-font-container/) | Terminal, command-line and system-UI faces, including the existing [Knurled Swarf](cmd-font-container/knurled-swarf/) multi-size pixel family |
| [hot-font-box](hot-font-box/) | Loud display, headline and poster work |
| [cachemonic](cachemonic/) | Deliberately broken grids and visual experiments |
| [abandonware](abandonware/) | Retired experiments, preserved with reasons for retirement |

The [name-idea archive](docs/subfolder-name-ideadump-refonly.md) is reference
material, not a specification or source of glyph outlines.
