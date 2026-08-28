---
status: accepted
date: 2026-08-25
---

# What the spacing quantum is, and what it is not

[ADR-0004](0004-baseline-grid-is-a-spacing-quantum.md) established that the
document baseline measures 16.32pt, not 13.2pt, and that `\gridunit` is a
spacing quantum rather than a baseline. It settled what 13.2pt **is not**. It
did not settle what it **is**, and it left three questions open that the
package answers by accident today.

This ADR exists to make the decision explicit rather than inherit it.

> **v3 revision (2026-08-28).** The numerical decision remains accepted, but
> ADR-0006 makes the quantum private. V3 removes `\gridunit`, its derived public
> helpers, and the grid overlay instead of carrying misleading grid vocabulary
> into the public API. The retained 13.2pt value and rendering are unchanged.

## The problem ADR-0004 left behind

**13.2pt has no derivation.** It was produced by `11 × 1.20`. Both inputs are
wrong: the `11pt` class option sets 10.95pt, and `\linespread{1.20}` scales the
class's 13.6pt baseline rather than the nominal size. ADR-0004 kept the number
because changing it changes rendering, but never re-justified it. It is a
residue of arithmetic known to be false.

**The quantum and the baseline are incommensurable.**

```
13.2 ÷ 16.32 = 0.80882…      16.32 ÷ 13.2 = 1.23636…
```

Neither is a rational multiple of the other. Two systems that do not divide
into each other cannot both be honoured: adding one quantum of vertical space
never returns the text to the line grid. So "all vertical spacing is a multiple
of the quantum" is true, and "vertical rhythm" is not, and the package asserts
both.

**Measured on page 12 of the shipped demo**, line-to-line gaps in the rendered
PDF:

| Gap | In baselines | In quanta |
|---|---|---|
| 16.26pt (×10, dominant) | 0.996 | **1.232** |
| 24.31pt | 1.490 | **1.842** |
| 19.46pt | 1.192 | **1.474** |
| 61.46pt | 3.766 | **4.656** |

Nothing lands on a quantum multiple. The quantum is an input to spacing
calculations; the grid the output actually sits on is 16.32pt.

**One document runs three vertical pitches**, none a whole quantum:

| Context | Pitch | In quanta | Set where |
|---|---|---|---|
| body | 16.32pt | 1.236 | `\linespread{1.20}` on the class baseline |
| quote | 15.84pt | 1.200 | `\fontsize{10.5}{13.2}` × `\linespread` |
| footnote | 12.00pt | 0.909 | class default |

An earlier draft of this ADR listed a fourth pitch, display maths at 13.2pt
from `lnpmathgridlocked.sty:130` — that attribution was wrong; see issue 1.

## Decision

**Option A, with one addition: the gridlocked modules are deleted.**

`\gridunit` is a **spacing quantum** — the unit vertical space values are
drawn from — and nothing more. It has no relationship to where text lands.
Every claim of rhythm, alignment, or grid-locking comes out of documentation,
comments, and the demo. "Spacing quantum" (ADR-0004) remains the canonical
term.

Two observations are recorded without weight being put on them. The quantum
is ≈1.2 nominal ems (1.2 × 11pt; 1.205 × the true 10.95pt em) — a
size-relative modulus is a legitimate tradition, but this rationale is
retrofitted, so it is noted, not relied on. And ADR-0004's third path (a
baseline-fraction quantum — Option B below) stays open to a future major
release; deciding A now forecloses nothing.

**The deletion.** `lnpheadingsgridlocked.sty` and `lnpmathgridlocked.sty` are
removed rather than renamed. Nothing loads them — not `lanepaper.sty`, not the
demo (verified under issue 1) — and their mechanisms cannot do what their
names promise: the "grid recovery" commands are `\vspace{0pt plus X minus X}`,
glue centred on zero, which snaps to nothing. Pre-CTAN is the cheapest moment
the names will ever be free. No stubs ship.

Sub-decisions, so none is inherited silently:

- **The 13.2pt quantum stays, but its public names do not.** V3 absorbs it into
  a private package owner and removes `\gridunit` plus the five derived public
  helpers. No compatibility aliases ship.
- **The `[grid]` option and overlay are removed.** A spacing scale is not a set
  of positions, and a diagnostic overlay does not justify a public subsystem.
- **Executable spacing values use the private quantum owner** rather than
  scattered literals, where that relationship is real.
- **`\parindent` is set to an explicit `13.2pt`**, deliberately not
  `\gridunit`: a horizontal indent must not follow a vertical unit (issue 6).
  `1.2em` would be 13.14pt — a rendering change — so the literal is the
  rule-compliant form. This is the one deliberate `13.2pt` literal.
- **Display spacing in `lanepaper.sty` keeps its values, with the rationale
  written down**: a multi-line display is read as one object, so compact
  internal leading binds its rows while `\abovedisplayskip` separates the
  block from prose; maths rows carry their own vertical bulk and `\lineskip`
  guards collisions.

The options considered:

### Option A — accept the quantum as a plain spacing unit (chosen)

Keep 13.2pt. Delete every claim of rhythm, alignment, or grid-locking from
documentation, comments, module names, and the demo. In v3 the quantum is a
private implementation value with no relationship to where text lands.

This changes no rendering and is honest. Its cost is that the package keeps a
number nobody can justify; keeping it private avoids turning that residue into
an adopter-facing abstraction.

### Option B — re-derive the quantum from the baseline (rejected; stays the future-major path)

Choose a quantum that divides the baseline: 16.32 / 2 = 8.16pt, or / 4 =
4.08pt. Spacing in whole quanta then preserves the line grid, and the rhythm
claim becomes true rather than aspirational.

This changes rendering wherever a spacing value is not already a multiple of
the new quantum, so it needs the same per-page raster proof any typographic
change needs. ADR-0004 records this as the "third path" and put it out of
scope; it is the only option that makes the existing vocabulary correct.

Rejected for a further reason: re-deriving the number does not deliver the
discipline. The package spaces with stretchable glue, and TeX stretches it
whenever a page needs flushing — text drifts off *any* grid on any page with
flexible material (the dominant 16.26pt gap above is that stretch showing).
A true grid needs rigid skips plus snap-back machinery, which is the
future-major project, not a constant change.

### Option C — keep 13.2pt and justify it independently (collapsed into A)

If 13.2pt is defensible on its own typographic merits — as a spacing interval
unrelated to leading — say so with a reason, and keep the vocabulary honest the
same way Option A does. This differs from A only in whether the number gets a
rationale or is simply grandfathered.

Making the 13.2pt grid *real* is **not** an option here. ADR-0004 rejected it
on three grounds that still hold: it requires removing `\linespread{1.20}`,
which tightens the whole document by ~19%; the literature favours the generous
lead for Pagella at this measure; and it forces every fork to re-port.

## Issues this decision has to resolve

These exist today regardless of which option wins. Each is a defect or a
question the current code answers silently.

1. **`lnpmathgridlocked.sty:130` sets display maths to the discredited number
   — in a module nothing loads.** `\everydisplay{\baselineskip=13.2pt}` is a
   bare literal, its comment reads "Ensure inline math doesn't disrupt line
   spacing" when `\everydisplay` fires on *display* maths, and no test pins
   it. But neither `lanepaper.sty` nor the demo loads either gridlocked
   module; the line's only executions were the standalone compile probe in
   `tests/run-tests.sh`. Measured in the shipped demo (2026-08-25, page 38,
   same-glyph pairs across the two `align` rows: ε↔ε 26.12pt, tags (2)↔(3)
   26.13pt): the row pitch is 26.1pt — the real 16.32pt baseline + 9.9pt
   `\jot` — not the 23.1pt an earlier draft of this ADR reported. That figure
   reproduces only when the module is loaded directly. **Resolved by the
   deletion**; the shipped display leading was body-derived all along.

2. **"Grid-locked" is wrong twice.** `CONTEXT.md` defines it as forcing output
   onto "the baseline grid"; the modules lock to the quantum, not the baseline.
   And they cannot lock to anything: `lnpheadingsgridlocked.sty:86` uses
   `{19.8pt plus 1.65pt minus 0.825pt}` — stretchable glue. A name promising
   rigidity over glue that stretches is a claim the code cannot keep.

3. **The demo prints the false claim.** `demo/main.tex:154` states that all
   vertical spacing derives from the quantum "giving professional vertical
   rhythm throughout the document". The measurement above contradicts it, and
   it ships in the published PDF.

4. **45 hardcoded `13.2pt` literals in executable positions**, across 9 files,
   against 162 uses of `\gridunit` and 44 derived lengths. Under Option B a
   third of the call sites would not follow the change. This is the reason the
   decision cannot be deferred indefinitely: the longer it waits, the more
   expensive B becomes.

5. **`\lnp@listbaselineskip` is not a baselineskip.** It is used as `topsep`
   (`lnplists.sty:262`, `:378`). The name asserts the same confusion this ADR
   exists to end.

6. **`\parindent` is set to `\gridunit`.** A vertical spacing quantum used as a
   horizontal indent. It happens to be a reasonable 13.2pt (~1.2em at this
   size), but the coupling is accidental and would follow any change to the
   quantum into a place it has no business being.

7. **The grid overlay draws both grids.** `lnpgridoverlay.sty` steps base lines
   at the real `\baselineskip` and quantum lines at 13.2pt, labelling both.
   That is honest and was the right fix in ADR-0004 — and it is also a visual
   admission that the package maintains two incompatible grids at once.

8. **Dead fallbacks.** `lnpminimal.sty:176–178` `\providecommand{\gridunit}`
   and friends, under a "FALLBACK DEFINITIONS" heading, can never fire —
   `\newlength{\gridunit}` at line 105 already defined it in the same file.

## Consequences

- The v3 public-surface contraction removes the remaining grid helpers and
  overlay under issue #85; rendering changes are not implied by this decision.
- `lnpheadingsgridlocked.sty` and `lnpmathgridlocked.sty` are deleted along
  with their references (README, the generated `CONVENTIONS.md` module table,
  `API_REFERENCE.md`'s tree, the `run-tests.sh` probe). No stubs: nothing
  shipped loads them, and CTAN has not yet frozen the names.
- Item 1 is resolved by the deletion. Items 4, 6 and 7 are resolved as
  decided above. Items 2, 3, 5 and 8 proceed under #73; the modules' half of
  item 2 dies with the files, leaving the `CONTEXT.md` glossary entry.
- `CONTEXT.md`'s glossary and the demo's rhythm claim are part of the
  deliverable. A decision that leaves the vocabulary asserting the old model
  has not been implemented.
- CTAN remains separate and on hold. The GitHub v3 release follows the manual,
  exact-green-SHA decision in ADR-0006 and issue #82.
