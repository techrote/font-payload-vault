# Rating system: requesting fonts and naming them

One scale, used twice:

1. **Request:** before a font is built, the request sets a *target* for each dial. This is what the agent designs towards.
2. **Delivery:** when the font is finished, the agent scores what it *actually* built on the same dials, and scores the proposed name.
   Target vs achieved sits side by side in the font's README, so drift is visible at a glance.

Scores run **0–10**, with **11** reserved for something that nails a dial completely. A number says *how strongly it matches*
the dial, never "how good". A cringe 11 can be exactly what was ordered.

This system grew out of [`subfolder-name-ideadump-refonly.md`](subfolder-name-ideadump-refonly.md), which is the historical first use.

---

## The dials

| dial | tag | high number means… | as a **request** target | as a **name** score |
|---|---|---|---|---|
| Cool | `cool` | you'd show it off without wincing | how impressive it should look | say it out loud: no wince |
| Cringe | `cringe` | you'd show it off, then wince | how much so-bad-it's-good is wanted (0 = none tolerated) | say it out loud: wince |
| Uninspired → **Workhorse** | `work` | plain, conventional, does the job | how invisible/standard it must be (11 = a system UI font nobody notices) | stock-photo-caption energy |
| Cybernetic | `cyber` | terminals, wetware, machine control | how much machine/terminal DNA | same |
| Chuck-wrap | `wrap` | grabs hold and won't let go, like a 3 m chip round the chuck | how distinctive/memorable it should be at a glance | how sticky the name is |
| Watchlist | `watch` | so deranged daily use should put you on an FBI watchlist | how unhinged it's allowed to get | how unhinged the name is |

For **requests**, "Uninspired" is renamed **Workhorse**, because sometimes plain is the brief (a terminal font *should* score high).
For **names**, it keeps its original meaning: a high score is a warning.

### Filters (pass/fail, never added to totals)

| filter | applies to | passes when |
|---|---|---|
| **Folderability** | names | lowercase-hyphen slug works as a folder: ASCII only, ≤ 32 chars, no ambiguity with tooling words (`shell`, `module`, `build`, `test`, `src`) |
| **Texture rule** | names | the adjective is textural or onomatopoeic, **not a colour** (see [naming-guide.md](naming-guide.md)) |
| **Collision** | names | a web search finds no existing font family with the same name |
| **Family-name length** | names | `"<Family> 16px Bold"` fits in 31 characters (Windows' limit) |

A name that fails a filter can still *inspire* a name. It can't ship as-is.

### Totals

Total = sum of the six dials. High totals mean "commits hardest to *something*", not "best". Use totals only to rank
candidate *names*. Requests don't have a total: the dials are a target profile.

---

## Request sheet

Copy this into an issue, a chat message or `REQUEST.md` in the new font's folder. Anything left blank → the agent picks and says what it picked.

```md
## Font request
- Working title (optional, can be ugly):
- Job: (where it will be used: taskbar, terminal, poster, HUD, labels on 3D prints, ...)
- Sizes / scale: (pixel sizes, or "display, 48px+", or "print at 10 mm cap height")
- Must-have characters: (default: ASCII + Latin-1 + cp1252 punctuation; add box drawing / arrows / symbols if needed)
- Weights / styles: (default: Regular + Bold)
- Spacing: proportional | monospace
- References / vibe words: (machines, objects, sounds; see naming-guide.md word banks)
- Hard no's:

| dial   | target 0-11 | notes |
|--------|-------------|-------|
| cool   |             |       |
| cringe |             |       |
| work   |             |       |
| cyber  |             |       |
| wrap   |             |       |
| watch  |             |       |

- Destination folder: (auto from routing table if blank)
```

### Routing: which folder a font lands in

| condition (checked top to bottom) | folder |
|---|---|
| user has soured on it after use | `abandonware/` |
| request `watch` ≥ 8, or it's a deliberately broken/glitched/generative experiment | `cachemonic/` |
| job is terminals, consoles, system UI, taskbars, menus; or `cyber` ≥ 7 with `work` ≥ 7 | `cmd-font-container/` |
| job is titles, logos, posters, splash screens; display sizes | `hot-font-box/` |
| none of the above | propose a new folder (name it with this system) and ask |

---

## Delivery sheet

Every finished font's README ends with this block, filled in honestly:

```md
## Ratings

| dial   | requested | achieved | note |
|--------|-----------|----------|------|
| cool   | 7 | 8 | ... |
| cringe | 0 | 1 | ... |
| work   | 9 | 9 | ... |
| cyber  | 8 | 7 | ... |
| wrap   | 5 | 6 | ... |
| watch  | 1 | 0 | ... |

**Name:** Knurled Swarf: `cool 8 · cringe 1 · uninsp 2 · cyber 4 · wrap 8 · watch 2` (total 25)
Filters: folder ✓ · texture ✓ · collision ✓ · length ✓ ("Knurled Swarf 16px Bold" = 23 chars)
Runner-up names: ...
```

Any dial more than 3 points off its target needs a one-line reason in the note column.

---

## Naming procedure (finished fonts)

1. Describe what the finished font *feels and sounds* like in 3–5 words (not what it looks like). Example: "crisp, gridded, gripping, clicky".
2. Pull 8–12 candidates from [naming-guide.md](naming-guide.md) using its patterns.
3. Score each candidate on the six dials and run the four filters.
4. Shortlist the top 3–5 by total *and* closeness to the font's own achieved dial profile.
   A loud display font wants a loud name; a workhorse UI font wants a sturdy one.
5. Pick one, and record the runner-ups in the README so the user can swap with a single rename.

## Worked example: Knurled Swarf

The font: hand-tuned DOS/Win3.x system pixel font, 6–16px. Requested (inferred from the original brief): cool 7, cringe 0, work 9, cyber 8, wrap 5, watch 0.

| candidate | cool | cringe | uninsp | cyber | wrap | watch | total | filters | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Swarf (bare) | 6 | 1 | 4 | 3 | 6 | 1 | 21 | ✓ | the root word: good, but one word is thin for a family |
| Blued Swarf | 8 | 1 | 2 | 4 | 7 | 2 | 24 | **texture ✗** (colour) | rejected: colour name |
| **Knurled Swarf** | 8 | 1 | 2 | 4 | 8 | 2 | 25 | ✓ ✓ ✓ ✓ | **picked**: the texture *is* the idea (a pixel grid in steel) |
| Chattered Swarf | 7 | 3 | 2 | 5 | 6 | 3 | 26 | ✓ | runner-up: onomatopoeic, reads slightly "talkative" |
| Snarled Swarf | 7 | 3 | 3 | 2 | 7 | 5 | 27 | ✓ | runner-up: too aggressive for a workhorse UI font |
| Stringy Swarf | 4 | 5 | 4 | 1 | 5 | 2 | 21 | ✓ | limp |

Snarled has the highest total but the worst fit to a calm UI font: an example of step 4 overruling the raw total.
