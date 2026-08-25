---
status: proposed
date: 2026-08-25
---

# What the spacing quantum is, and what it is not

[ADR-0004](0004-baseline-grid-is-a-spacing-quantum.md) established that the
document baseline measures 16.32pt, not 13.2pt, and that `\gridunit` is a
spacing quantum rather than a baseline. It settled what 13.2pt **is not**. It
did not settle what it **is**, and it left three questions open that the
package answers by accident today.

This ADR is `proposed`, not accepted. It exists to make the decision explicit
rather than inherit it.

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

**One document runs four vertical pitches**, only one of which is a whole
quantum, and that one by accident:

| Context | Pitch | In quanta | Set where |
|---|---|---|---|
| body | 16.32pt | 1.236 | `\linespread{1.20}` on the class baseline |
| quote | 15.84pt | 1.200 | `\fontsize{10.5}{13.2}` × `\linespread` |
| display maths | 13.20pt | 1.000 | `lnpmathgridlocked.sty:130` |
| footnote | 12.00pt | 0.909 | class default |

## Decision

**Not yet made.** The options are below.

### Option A — accept the quantum as a plain spacing unit

Keep 13.2pt. Delete every claim of rhythm, alignment, or grid-locking from
documentation, comments, module names, and the demo. `\gridunit` becomes what
it demonstrably is: a convenient unit that spacing values are quoted in, with
no relationship to where text lands.

Cheapest, changes no rendering, and is honest. Its cost is that the package
keeps a number nobody can justify, and the name `\gridunit` keeps implying a
grid that does not exist.

### Option B — re-derive the quantum from the baseline

Choose a quantum that divides the baseline: 16.32 / 2 = 8.16pt, or / 4 =
4.08pt. Spacing in whole quanta then preserves the line grid, and the rhythm
claim becomes true rather than aspirational.

This changes rendering wherever a spacing value is not already a multiple of
the new quantum, so it needs the same per-page raster proof any typographic
change needs. ADR-0004 records this as the "third path" and put it out of
scope; it is the only option that makes the existing vocabulary correct.

### Option C — keep 13.2pt and justify it independently

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

1. **`lnpmathgridlocked.sty:130` sets display maths to the discredited number.**
   `\everydisplay{\baselineskip=13.2pt}` — measured live and unscaled. It is a
   bare literal rather than `\gridunit`, the comment above it reads "Ensure
   inline math doesn't disrupt line spacing" when `\everydisplay` fires on
   *display* maths, and no test covers it. It materially sets multi-line
   display spacing: `align` rows measure 23.1pt (13.2 + `\jot` 9.9) where the
   real baseline would give 26.2pt. **Tighter display leading may well be
   right — but it has never been decided, only inherited.**

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

- Options A and C are documentation-and-naming work: no rendering changes, so
  no raster proof needed beyond a confirmation that nothing moved.
- Option B is a typographic change and needs per-page raster proof at 150dpi,
  read page by page rather than tallied.
- Items 1–3, 5 and 8 above are fixable under any option and should not wait for
  this decision. Item 4 is blocked by it. Items 6 and 7 are for the decision
  itself to answer.
- Whichever option wins, `CONTEXT.md`'s glossary and the `*gridlocked* module
  names are part of the deliverable. A decision that leaves the vocabulary
  asserting the old model has not been implemented.
