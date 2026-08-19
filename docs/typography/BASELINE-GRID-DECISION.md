# Decision Record: The Baseline Grid Is a Spacing Quantum, Not a Baseline

**Date:** 2026-08-11
**Status:** Decided
**Evidence:** adopter defect report (finding 1) and decision brief (both
archived in git history under `notes/`)

## Decision

**Option (b): re-document the true measured values.** The build sets a 10.95pt
body on a 16.32pt baseline (`size11.clo` sets 10.95pt on 13.6pt;
`\linespread{1.20}` scales the class's 13.6pt baseline, not the 11pt class
option). `\gridunit` (13.2pt) is redefined in documentation as a **spacing
quantum** — the unit vertical spaces are multiples of — not the document
baseline. Option (a) (make the 13.2pt grid real) is rejected.

## Why

1. **The no-visual-change rule (AGENTS.md rule 1) is decisive.** Making 13.2pt
   real requires removing `\linespread{1.20}` (under it, even an explicit
   `\fontsize{11}{13.2}` yields 15.84pt, not 13.2pt). That tightens footnotes,
   tables, and body by ~19% — Lane's own 40-page `main.pdf` would shrink to
   ~33 pages. That is the largest visual change the template could undergo.
2. **The literature does not rescue 13.2pt.** Pagella's large x-height, a
   ~77-character measure, and math-dense text are precisely the conditions
   under which Bringhurst prescribes *more* lead; every comparable shipped
   class (article, memoir, KOMA, amsart) uses ≤13.6pt for 11pt — Lane's actual
   16.32pt exceeds them all, in the generous direction the literature favors.
3. **Adopter cost is asymmetric.** Re-documenting costs adopters nothing and
   validates the reporting adopter's ADR 0008; making the grid real forces
   re-ports.

## Consequences

- All documentation stating "13.2pt baseline" / "11pt × 1.20 = 13.2pt
  leading" must be corrected to the true values (10.95pt body, 16.32pt
  baseline) — see the dependent spacing-constants ticket.
- The `[grid]` debug overlay must step at the real `\baselineskip`, not
  `\gridunit`, or it confirms the false premise.
- `\gridunit`-derived constants remain valid as *spacing* values; constants
  that claimed to *align to the baseline* (`\footnotesep`, `\jot`,
  `\extrarowheight`, `\DeclareMathSizes`) must be recomputed or re-documented.
- If a future major release wants a true baseline grid, the brief records a
  third path (baseline-fraction quantum); it is out of scope here.
