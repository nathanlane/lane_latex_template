# Decision Brief — Issue #11: Evidence for the Baseline-Grid Decision

**Date:** 2026-08-11
**Author:** research worker (worktree `llt-wt-research`, branch `research/baseline-grid-decision`)
**Decision owner:** maintainer
**Options on the table:**
(a) make the documented 13.2pt baseline grid real via explicit `\fontsize{11}{13.2}\selectfont`;
(b) re-document the true measured values (10.95pt body, 16.32pt baseline) and redefine `\gridunit` as a pure spacing quantum.

---

## 0. Premise verification (done before writing this brief)

The adopter defect report's finding 1 (`notes/ADOPTER-DEFECT-REPORT-2026-08-11.md`) is correct, and it reproduces on the local toolchain.

| Claim | Verification here | Result |
|---|---|---|
| `size11.clo` sets 10.95pt on 13.6pt | `/usr/local/texlive/2022/.../size11.clo:48` = `\@setfontsize\normalsize\@xipt{13.6}` | Confirmed |
| `\linespread{1.20}` scales that to 16.32pt | minimal `article[11pt]` + `\linespread{1.20}` build: `\baselineskip` = **16.31996pt** | Confirmed |
| `\gridunit` = 13.2pt while every derived constant assumes it | `paper/modules/lltdimensions.sty:22-48` | Confirmed |
| 16.32 appears nowhere in the tree | `grep -rn "16.32"` hits only the defect report | Confirmed |
| Both styles carry the false claim | `lltpaperstyle.sty:694`, `:1087`; `lltpaperstyleminimal.sty:56` (`\linespread{1.20} % Equivalent to 13.2pt for 11pt base`) | Confirmed |
| Grid overlay steps at 13.2pt | `paper/lltgridoverlay.sty:37,72,105,110` | Confirmed |

No escalation required: the premise holds on TeX Live 2022 (local) exactly as reported for TeX Live 2026 (adopter).
The `.clo` line in question has been stable across TeX distributions for decades.

**One correction to the option-(a) phrasing that matters for implementation:** `\fontsize{11}{13.2}\selectfont` under the *current* `\linespread{1.20}` does **not** yield a 13.2pt baseline.
Verified locally: after `\fontsize{11}{13.2}\selectfont` with `\baselinestretch=1.2` in force, `\baselineskip` = **15.83995pt** (13.2 × 1.2).
Option (a) therefore requires removing `\linespread{1.20}` (or redefining `\normalsize` with `\baselinestretch` reset), which is what triggers the cascade of secondary changes costed in §3.

---

## 1. What the typographic literature recommends for ~11pt serif body text

### 1.1 The headline numbers

| Source | Recommendation for text leading | Where 13.2/11 (120%) falls | Where 16.32/10.95 (149%) falls |
|---|---|---|---|
| Butterick, *Practical Typography*, "Line spacing" | **120–145% of point size** is optimal for most text; his own worked example calls 110% "too tight", 135% "fine", 170% "too loose" | At the **floor** of the band | **Above** the band's ceiling |
| Bringhurst, *Elements of Typographic Style* v3.0, §2.2.1 (pp. 36–37) | "Settings such as 9/11, 10/12, 11/13 and 12/15 are routine" — i.e. a routine band of **~118–125%** | Inside the routine band (11/13.2 ≈ 11/13) | Outside the routine band |
| Wikipedia, "Leading" (summarizing Bringhurst pp. 36–37 and Butterick) | more leading for longer measures, darker weight, larger x-height, vertical axis, or sans serif | — | — |

Neither candidate is "the" standard practice: **13.2pt sits at the tight end of normal; 16.32pt sits just past the generous end.**
The mainstream of shipped practice (see §2) lies between them.

### 1.2 The modifiers — this is where the decision actually lives

Bringhurst's §2.2.1 immediately qualifies the routine band (v3.0, p. 37):

- "Longer measures need more lead than short ones."
- "Large-bodied faces need more lead than smaller-bodied ones." (i.e. large x-height wants more leading)
- "Extra leading is also generally welcome where the text is thickened by superscripts, subscripts, mathematical expressions, or the frequent use of full capitals."

Lane's specific design triggers **all three** modifiers, and each is locally measurable:

1. **Large x-height.** TeX Gyre Pagella's `XHeight` is 469/1000 em (`qplr.afm`), vs 450/1000 for URW Times (`utmr8a.afm`) and ≈ 431/1000 for Computer Modern.
   Pagella is the largest-x-height face of the standard LaTeX text set.
2. **Long measure.** Lane's `geometry{margin=1.25in}` gives `\textwidth` = 433.62pt; measured qpl lowercase alphabet at 10.95pt = 145.49pt ⇒ ≈ **77–78 characters per line**.
   Bringhurst's satisfactory single-column range is 45–75, ideal 66 (§2.1.2); Lane is past the top of it, which pushes leading *up*, not down.
3. **Math-heavy academic text.** The template targets empirical/quantitative papers; Bringhurst explicitly welcomes extra lead for text "thickened by… mathematical expressions".

Hochuli, *Detail in Typography* (English ed., Hyphen Press, 2008), chapter "Line spacing and the column", treats linespacing as a variable to be judged against the specific face, size and measure — not as a fixed percentage of body size — and warns against both insufficient and excessive spacing (excess breaks the even colour of the text block).
(Cited at chapter level; verbatim text was not accessible from this environment — see Sources.)
His framework supports the same conclusion as Bringhurst's modifiers: the right value for a large-x-height face on a long measure is *above* the routine band's floor.

### 1.3 Verdict of §1

- **13.2pt (120%) is defensible but tight** for an 11pt Pagella-class face on a 77-character measure with math content — every applicable modifier in the literature argues for *more* than the routine band.
- **16.32pt (149%) is defensible but generous** — it overshoots Butterick's ceiling and every shipped LaTeX default (§2), but it errs in the direction the literature's modifiers point for this face and measure.
- If the literature alone dictated the value, the answer would be **between** the two (≈ 13.6–14.5pt, 124–132%).
  It does not get a vote, because AGENTS.md rule 1 freezes the visual output (§3.3).

---

## 2. What comparable LaTeX classes actually ship for 11pt body text

All verified against the local TeX Live 2022 tree:

| Class / file | `\normalsize` at 11pt option | Ratio to nominal |
|---|---|---|
| `article` / `report` / `book` — `size11.clo:48` | 10.95pt on **13.6pt** | 124% |
| `memoir` — `mem11.clo:32` | 10.95pt on **13.6pt** | 124% |
| KOMA-Script — `scrsize11pt.clo:76` | 10.95pt on **13.6pt** | 124% |
| `amsart` — 11pt option `\@typesizes` | 10.95pt on **13pt** | 119% |
| `IEEEtran` — 11pt branch | 11bp on **13.2bp** (≈ 13.15pt) | 120% |
| **Lane, documented** | 11pt on **13.2pt** | 120% |
| **Lane, measured** | 10.95pt on **16.32pt** | **149%** |

Observations:

- The three general-purpose class families all ship 13.6pt; no mainstream class ships anything near 16.32pt.
- The one prominent shipper of 13.2-for-11pt is **IEEEtran** — a two-column, short-measure class set in Times (x-height 0.450em vs Pagella's 0.469em).
  Per §1.2's modifiers, short measure + smaller x-height is precisely the case that tolerates the tightest leading.
  Lane is the opposite case on both axes.
- Lane's documented value (13.2pt) matches IEEEtran's; Lane's measured value (16.32pt) exceeds every comparable class by ≥ 20%.

---

## 3. Practical consequences of each option

### 3.1 Option (a) — make 13.2pt real

**Mechanics.** Not a one-liner.
Because `\linespread{1.20}` multiplies whatever leading is set at font-selection time (verified: `\fontsize{11}{13.2}` under `\linespread{1.20}` ⇒ 15.84pt, not 13.2pt), option (a) requires *both* removing `\linespread{1.20}` *and* redefining `\normalsize` to 11/13.2.
That removal cascades into every context whose leading currently rides the 1.2 multiplier:

| Consequence | Current | Under (a) | Kind of change |
|---|---|---|---|
| Body baseline | 16.32pt | 13.2pt | −19% leading, every page |
| Lines per page (ratio 16.32/13.2 ≈ 1.236) | ~37–38 at 614pt textheight | ~46 | **Page count: 40pp → ≈ 32–33pp** (estimate from the ratio; floats/headings don't rescale) |
| Body font size | 10.95pt | 11.0pt | +0.5% (sub-visible but real) |
| Footnote leading (8.5/10 × 1.2) | 12.0pt | 10.0pt | tighter footnotes; re-opens defect-report finding 6's arithmetic |
| All other size leadings (footnotesize, small, headings…) | × 1.2 | × 1.0 | every context tightens |
| Table rows (`\arraystretch` 1.2 × baseline + 2.2pt) | 22.22pt | 18.04pt | visibly tighter tables |
| `\DeclareMathSizes{11}{11}{8}{6}` (dead at 10.95pt) | never fires | fires | math script sizes change (6.1pt → 6pt measured effect) |
| Grid overlay (`lltgridoverlay.sty`) | false (steps 13.2 vs real 16.32) | **truthful, unchanged** | the win |
| All `\gridunit`-derived constants (3.3/6.6/9.9/19.8/26.4/39.6) | off the real baseline | genuinely grid-aligned | zero retuning — the other win |

**Net:** the grid architecture becomes true with *no constant changes*, but at the price of changing the leading, footnote spacing, table density and page count of every document ever built with the template.

### 3.2 Option (b) — re-document the truth, redefine `\gridunit` as a spacing quantum

**Mechanics.** No code changes to document output.
The false claim must be corrected in the ~11 places the defect report enumerates: `README.md:16,374`, `INSTALL.md:304`, `API_REFERENCE.md:197`, `TROUBLESHOOTING.md:149`, `paper/README.md:119,153,350`, `docs/typography/BASELINE-GRID.md` (wholesale — the "13.2pt baseline grid" narrative becomes a "13.2pt spacing quantum" narrative), `lltpaperstyle.dtx:160`, `lltpaperstyle.sty:694,1087` (comments), `lltpaperstyleminimal.sty:56` (comment).

**What must also be decided under (b):**

- The `[grid]` debug overlay still steps at 13.2pt.
  Minimal honest repair: step the overlay at the *measured* `\baselineskip` (16.32pt) so the one diagnostic tool Lane offers stops confirming the false premise.
  This changes a development tool only, not any document's output.
- Bringhurst's grid principle (§2.2.2: intrusions should total an even multiple of the basic leading — "If the main text runs 11/13, intrusions to the text should equal some multiple of 13 points: 26, 39, 52…") remains **unmet** forever: 13.2 has no integer relationship to 16.32.
  Under (b) the "baseline grid" is conceded to be a *spacing rhythm*, not a baseline grid.
  `BASELINE-GRID.md`'s verification checklist ("body text baselines align to every grid line") must be rewritten, not just renumbered.
- Dependent factual errors in comments (`\extrarowheight` "Makes standard rows exactly 13.2pt"; `\jot` "6.6pt"; footnote "11pt/10pt leading" comments) get corrected as documentation; the values themselves stay.

### 3.3 Compatibility with AGENTS.md rule 1

AGENTS.md: "**Do not** alter margins, fonts, colours, spacing, numbering schemes, or figure placement defaults", and "Prefer the smallest possible change".

- Option (a) alters the most fundamental spacing quantity in the template (body leading −19%), the body size (10.95 → 11pt), footnote leading, and table row heights, and repaginates every adopter document by ≈ −19% (40 → ~32–33 pages for Lane's own `main.tex`).
  It is the largest visual change the template could possibly undergo; it cannot be reconciled with rule 1 without amending AGENTS.md itself.
- Option (b) changes no rendered output at all.
  It is the smallest change that makes the repo truthful.

The one interpretation under which (a) is lawful: if "visual design" in rule 1 is read as *the documented design* (13.2pt grid) rather than *the shipped design* (16.32pt).
That reading should be made explicit by the maintainer before choosing (a), because it reverses the burden of proof for every future defect in the template.

---

## 4. Impact on existing adopters

The reporting adopter (*Geopolitics and Export Miracles*) is the canonical case, and it is documented in the defect report:

- **ADR 0007** trusted Lane's documentation and shipped an explicit `11pt/13.2pt` setting.
- On measuring Lane's real output (10.95/16.32), they **superseded ADR 0007 in full (ADR 0008)** and re-implemented the port around the measured values.
- Finding 1 cost them two architecture records and one full re-implementation.

Consequences going forward:

- **Under (b):** zero further work for that adopter.
  Their ADR 0008 port matches Lane's output; the corrected documentation finally matches what they measured.
  Any adopter who pinned spacing to `\gridunit` constants is also untouched — the constants don't move.
- **Under (a):** Lane's output moves 19% in leading; the adopter's measured-reality port no longer matches Lane.
  They face a third re-implementation (or permanent divergence), and every other adopter's camera-ready documents repaginate on their next rebuild.
  For a class of user whose papers have submission page limits, an uncommanded −19% page count is a breaking change, not a fix.

Note the asymmetry: the defect in finding 1 is a **documentation defect with a diagnostic-tool defect attached**.
The rendered output was never shown to be typographically bad — §1 shows it is arguably *better* suited to Lane's face and measure than the documented value would be.

---

## 5. Recommendation

**Choose (b): re-document the true measured values (10.95pt body, 16.32pt baseline) and redefine `\gridunit` as a pure spacing quantum — with the `[grid]` overlay repaired to step at the real `\baselineskip` so the diagnostic becomes truthful.**

Reasoning, in order of weight:

1. **AGENTS.md rule 1 is non-negotiable and (a) is the maximal violation of it.**
   Option (a) changes body size, body leading, footnote leading, table density and page count (−19%) for every document and every adopter.
   A template whose entire value proposition is stability cannot repaginate its users' papers to fix what is, at root, a comment-and-docs error.
2. **The literature does not rescue (a); if anything it indicts it.**
   13.2pt on 11pt is Butterick's floor and Bringhurst's routine band for *ordinary* faces and measures; Lane's actual conditions (Pagella x-height 0.469em — largest of the standard set; ≈ 77-char measure; math-dense text) are exactly the three conditions under which Bringhurst prescribes *more* lead.
   The only major class shipping 13.2-for-11pt (IEEEtran) does so for the opposite conditions (two columns, Times).
   Making 13.2pt real would move Lane's typography *away* from what its own cited authorities recommend for its own design.
3. **Adopter cost is asymmetric.**
   (b) costs existing adopters nothing and retroactively validates the reporting adopter's ADR 0008; (a) forces a third re-port on them and breaks every other adopter's page budget.

**Strongest argument against (b), stated honestly:** the documented 13.2pt grid is a *coherent architecture* — one quantum, clean fractions, a working overlay, and Bringhurst's even-multiple discipline — while the measured reality (16.32 vs 13.2, no integer relation) is an accident that can never satisfy the grid principle.
Choosing (b) concedes that Lane's signature feature, as documented, was never real, and the template loses its most marketable claim ("every vertical measurement reinforces the reading rhythm of the baseline grid").
If the maintainer concludes the grid *is* the product, then (a) is its only honest implementation — but that requires first amending AGENTS.md rule 1 to define "visual design" as the documented design, and accepting the ≈ 20% repagination of all existing documents as a deliberate breaking release (semver-major, with a migration note).

**Explicitly out of scope but worth recording:** a third path — redesigning the quantum as a fraction of the true baseline (e.g. 16.32/5 ≈ 3.264pt, or a half-baseline 8.16pt) — would produce a real grid on the current typography.
It changes spacing constants and therefore output, so it is unavailable under rule 1 today; it is the right candidate if a grid-true major release is ever planned.

---

## Sources

**Verified primary/technical (local toolchain, TeX Live 2022):**
- `texmf-dist/tex/latex/base/size11.clo:48` — `\@setfontsize\normalsize\@xipt{13.6}`.
- `texmf-dist/tex/latex/memoir/mem11.clo:32`; `texmf-dist/tex/latex/koma-script/scrsize11pt.clo:76` — identical 13.6pt leading.
- `texmf-dist/tex/latex/amscls/amsart.cls` — 11pt option `\@typesizes`: normalsize `\@xipt` on `13`.
- `texmf-dist/tex/latex/ieeetran/IEEEtran.cls` — 11pt branch: `\@setfontsize{\normalsize}{11bp}{13.2bp}`.
- `texmf-dist/fonts/afm/public/tex-gyre/qplr.afm` — `XHeight 469`; `texmf-dist/fonts/afm/urw/times/utmr8a.afm` — `XHeight 450`.
- Local builds: `\baselineskip` = 16.31996pt under `article[11pt]` + `\linespread{1.20}`; = 15.83995pt after `\fontsize{11}{13.2}\selectfont` with `\linespread` in force; qpl alphabet width 145.49pt at 10.95pt on 433.62pt measure (⇒ ≈ 77–78 CPL).

**Typographic literature:**
- Matthew Butterick, *Practical Typography*, "Line spacing" — <https://practicaltypography.com/line-spacing.html> ("For most text, the optimal line spacing is between 120% and 145% of the point size").
- Robert Bringhurst, *The Elements of Typographic Style*, version 3.0 (Point Roberts, WA: Hartley & Marks, 2004), §2.2.1 "Choose a basic leading that suits the typeface, text and measure", pp. 36–37 (routine settings 9/11, 10/12, 11/13, 12/15; large-bodied faces and math-thickened text want more lead) and §2.2.2 "Add and delete vertical space in measured intervals", pp. 37–38 (intrusions as even multiples of the basic leading). (4th ed., 2012, renumbers these to §2.4.1–2.4.2.)
- Jost Hochuli, *Detail in Typography*, English ed. (London: Hyphen Press, 2008; orig. *Le détail en typographie*, 1987), chapter "Line spacing and the column" — cited at chapter level; verbatim text not accessible from this environment. Chapter structure confirmed via *Designer's Review of Books*, 2010-09-01: <https://www.designersreviewofbooks.com/2010/09/jost-hochuli-detail-in-typography/>.
- Wikipedia, "Leading" (accessed 2026-08-11) — <https://en.wikipedia.org/wiki/Leading> (standard summary; cites Bringhurst 2004 pp. 36–37 and Butterick).

**Repo-internal:**
- `notes/ADOPTER-DEFECT-REPORT-2026-08-11.md`, finding 1 (enumeration of all 11 doc locations carrying the 13.2pt claim; measured values; ADR 0007/0008 history).
- `paper/modules/lltdimensions.sty:20-53`; `paper/lltgridoverlay.sty:37-110`; `paper/lltpaperstyleminimal.sty:56`; `docs/typography/BASELINE-GRID.md` (passim); `README.md:16,374`.
- `AGENTS.md` — rule 1 (no changes to margins, fonts, colours, spacing) and the smallest-change rule.
