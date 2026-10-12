# Naming guide: textural and onomatopoeic names

The house style for every font, folder and variant in this repo.
Pair it with [rating-system.md](rating-system.md) to score candidates.

## The rules

1. **Name what you'd feel or hear, never what you'd see.** Textures, surface finishes, workshop processes and sounds.
   No colour words, including disguised ones (see the banned list).
2. **Workshop over sci-fi.** Machining, metalwork, casting, woodwork, composites, sewing and garage noise outrank neon-and-chrome
   cyberpunk clichés. The aesthetic is industrial, down-to-earth, ratrod: something that still works after being dropped
   down the stairs and dragged through gravel.
3. **Obscure is fine.** If it's a real shop word (knurled, galled, cold-shut), use it. The README can explain it in one line.
4. **Two words, max.** `[Adjective] [Noun]` is the default. One word works when it's strong enough on its own.
5. **Read it aloud.** If it trips the tongue, or sounds like a medicine, a supplement or a sports drink, drop it.
6. **Check for collisions.** Web-search `"<name> font"` before committing. Existing families are a hard no.

### Banned: colour names

`red, blue, green, black, white, grey/gray, gold, silver, bronze, copper` (as colours), `amber, neon, chrome` (as an adjective),
`blued, straw, rainbow, oxide-red, rusty-orange, glowing, golden, ivory, jet, ebony, crimson, cobalt, cyan, magenta, ultraviolet, infrared`,
and temper/heat colours (`blued, straw, purple-heat, cherry-red`).

Allowed edge cases: a **material** as a noun is fine when it's the thing rather than its colour (`Brass Shim`, `Copper Slug`
only if the font really is "about" that material). `Rusted`/`Pitted` are fine: they describe a surface you can feel.
When unsure, swap to a texture word.

---

## Patterns

| pattern | shape | examples |
|---|---|---|
| **Texture + Leftover** *(house default)* | adjective for the surface + noun for a workshop by-product | Knurled Swarf, Galled Slug, Pitted Dross, Burred Chad |
| **Sound + Part** | onomatopoeia + small hardware noun | Clatter Rivet, Tink Washer, Thunk Shim, Brap Ferrule |
| **Process + Tool** | what was done + what did it | Peened Anvil, Nibbled Punch, Swaged Die |
| **Single strong word** | one shop or sound word | Kerf, Dross, Judder, Clank |
| **Doubled sound** | reduplicated onomatopoeia, for loud or silly faces | Clank-Clank, Tik-Tak, Brap-Brap |
| **Defect name** | a manufacturing fault as a badge of honour (great for `cachemonic/`) | Cold Shut, Chatter Mark, Porosity, Galling |

### Derived names (inside a family)

| thing | rule | Knurled Swarf example |
|---|---|---|
| Family name (installed) | `Adjective Noun`, Title Case, spaces | `Knurled Swarf` |
| Per-size families | family + ` {N}px` | `Knurled Swarf 11px` |
| Raster `.fon` face | family + ` Sys` (keeps it distinct from the TrueType family) | `Knurled Swarf Sys` |
| File stem | CamelCase, no spaces | `KnurledSwarf-Bold.ttf`, `KnurledSwarf11px-Regular.ttf` |
| Repo folder | lowercase-hyphen | `cmd-font-container/knurled-swarf/` |
| Variants / sister fonts | keep the noun, change the texture | `Peened Swarf` (heavier), `Lapped Swarf` (smoother) |
| Weights beyond Regular/Bold | named weights stay standard (`Light`, `Bold`, `Black`); texture lives in the family, not the weight | `Knurled Swarf Black` |

---

## Word banks

Grouped by feel, so you can match a word to what the font actually does.
**(o)** = onomatopoeic. The "feel" column is the font quality the word suits.

### Machining and metalwork: textures

| word | what it is | feel |
|---|---|---|
| knurled | diamond/straight grip pattern rolled into metal | gridded, crisp, pixel-perfect, grippy |
| burred | rough raised edge left by a cut | jagged edges, unpolished pixels |
| chattered (o) | ripple marks from a vibrating tool | wavy, rhythmic, glitchy |
| galled | surfaces torn by friction welding | torn, scuffed, distressed |
| scored | scratched grooves | linear, hairline, engraved |
| peened | dimpled by hammer strikes | heavy, rounded, punchy |
| planished | hammered smooth with small blows | refined but hand-made |
| swaged | squeezed into shape through a die | condensed, drawn-out, narrow |
| upset | shortened and thickened by forging | squat, extended, heavy |
| stippled | covered in dots | dotted, dither, halftone, dot-matrix |
| serrated | saw-toothed | spiky, aggressive |
| fluted / ribbed | parallel grooves | inline, multi-line strokes |
| splined / keyed | interlocking teeth / slot | modular, interlocking |
| threaded | helical groove | rhythmic, repeating |
| pitted | small corrosion holes | worn, eroded, speckled |
| scaled | mill-scale flaking | patchy, flaky |
| sandblasted / bead-blasted | uniform matte | even texture, soft-edged |
| linished / ground | belt-ground satin | clean, directional, mechanical |
| lapped / honed | very fine smooth finish | ultra-clean, precise |
| nibbled | cut by a nibbler, scalloped edge | stepped, chunky curves |
| sheared | guillotined straight | blunt cuts, stencil |
| punched / stamped | press-formed | stencil, bold, industrial labels |
| embossed / debossed | raised / sunk lettering | dimensional, inline/outline |
| perforated / expanded | holes / stretched mesh | dot, grid, see-through |
| corrugated | wavy sheet | rippled, rhythmic |
| riveted / welded | joined | modular, constructed |
| work-hardened | brittle from repeated working | tense, angular |
| deburred | edges cleaned up | tidied, polished version of a font |

### Casting, composites, wood, sewing: textures

| word | what it is | feel |
|---|---|---|
| flashed | thin fins where mould halves meet | messy edges, overflow |
| sprued | still attached to the casting channel | unfinished, kit-of-parts (very ratrod) |
| cold-shut | casting defect where two flows don't fuse | broken strokes, glitch, cachemonic |
| porous / pinholed | gas bubbles | speckled, eroded |
| shrunk | contracted while cooling | tight, condensed |
| laid-up / laminated | layered composite | layered, multi-pass strokes |
| voided | air pocket in a layup | hollow, outline |
| frayed | loose fibre ends | rough, hairy edges |
| kerfed | saw-cut slots | stencil, slotted |
| rived / split | split along the grain | rough, directional |
| splintered | broken into shards | sharp, shattered |
| checked | cracks from drying wood | cracked, distressed |
| spalted | fungal line patterns in wood | organic lines (patterned, no colour) |
| adzed | hand-hewn surface | hand-made, irregular |
| quilted | stitched padded grid | soft grid, rounded pixels |
| overlocked / serged | edge-stitched | outlined, bordered |
| ruched / puckered | gathered fabric | wavy, compressed |
| felted | matted fibres | soft, fuzzy, blurred-on-purpose |
| darned | patched with woven thread | repaired, patchwork |

### Onomatopoeia

| word | sound | feel |
|---|---|---|
| clank, klonk, clunk, thunk | heavy metal on metal | heavy, slab, bold |
| clack, clatter, rattle | many small hard hits | busy, typewriter, monospace |
| chatter, judder | vibration | wavy, glitch |
| tink, tik, ping, plink, ting | small light hits | tiny sizes, light weights |
| chunk, ka-chunk | a press or a latch | stamped, modular, bold |
| crunch, grind, rasp, scrape, skritch | abrasion | rough, distressed |
| hiss, fizz, sizzle, spit, zzt, bzzt | welding arc, sparks | electric, cyber, glitch |
| whirr, whine, thrum, hum | motors, spindles | smooth, mechanical, continuous |
| chug, putter, brap, blat, burble | engines and exhausts | ratrod, loud display |
| snap, crack, pop | breaking | sharp, brittle, angular |
| wheeze, sputter, glug | tired machines | worn, eroded, abandonware |

### Nouns: the leftover, the part, the tool

| group | words |
|---|---|
| workshop leftovers | swarf, turnings, filings, shavings, slag, dross, spatter, scale, burr, flash, sprue, offcut, slug (punched-out disc), chad, kerf |
| small hardware | rivet, washer, shim, grommet, ferrule, cotter, circlip, grub (screw), nib, tang, shank, gib, collet |
| tools and fixtures | anvil, die, punch, jig, platen, mandrel, swage, peen, scriber, burin, nibbler |
| garage and ratrod | gasket, manifold, header, choke, tappet, sump, stud, lug |

Avoid nouns that already mean something in computing and would confuse folder names or code: `shell, module, core, kernel, cache, build, bin`.
*(Cachemonic is an exception: it was picked on purpose as a folder.)*

---

## Matching names to fonts

| if the font is… | reach for… | examples |
|---|---|---|
| crisp pixel / system UI | knurled, stamped, punched, nibbled, tink, clack | Knurled Swarf, Stamped Chad, Clack Shim |
| monospace terminal | clatter, threaded, splined, ratchet sounds | Clatter Gib, Splined Kerf |
| tiny (≤ 8px) | chad, slug, nib, tink, ping | Tink Chad, Punched Nib |
| heavy / bold display | upset, peened, thunk, clank, brap | Peened Anvil, Brap Gasket |
| condensed | swaged, drawn, shrunk, sheared | Swaged Shim |
| rounded / soft | planished, quilted, lapped, whirr | Quilted Rivet, Whirr Collet |
| distressed / worn | pitted, galled, scaled, porous, wheeze | Pitted Dross, Galled Ferrule |
| glitch / broken (cachemonic) | cold-shut, chattered, zzt, crazed, flashed | Cold Shut, Zzt Spatter, Chattered Slag |
| stencil / modular | kerfed, sheared, riveted, sprued | Kerfed Sprue, Riveted Gib |
| dot-matrix / LED / halftone | stippled, perforated, pinholed | Stippled Platen, Perforated Shim |

## Quick checklist

- [ ] texture or sound, no colour
- [ ] read aloud: no medicine/snack/sports-drink energy
- [ ] ≤ 2 words; `"<Family> 16px Bold"` ≤ 31 chars
- [ ] no existing font with that name
- [ ] scored with [rating-system.md](rating-system.md); runner-ups recorded
