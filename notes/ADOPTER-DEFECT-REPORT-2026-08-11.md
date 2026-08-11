# Lane LaTeX Template — defect report from an adopting project

**Reported:** 2026-08-11
**Lane version examined:** `92b8fbc` (current `main`), `lltpaperstyle.sty` v1.7 (2026/05/28)
**Toolchain:** TeX Live 2026, pdfTeX 1.40.29
**Adopter:** *Geopolitics and Export Miracles* (`korea_war_procurement`), which ported Lane's
typography into a standalone `preamble.tex` over 2026-08-02 → 2026-08-11.

Everything below is attributable to Lane itself: code that misbehaves, comments that state
values the build does not produce, rules that silently cancel each other, or designs that
predictably mislead an adopter. Mistakes that were purely the adopter's own are listed at the
end under *Excluded*, for completeness only.

Findings were verified by compiling fixtures that `\usepackage{lltpaperstyle}` directly with
`TEXINPUTS` pointed at `paper/`, and by compiling Lane's own `main.tex` (exit 0, 40 pages).
Measurements are from those builds, not from reading source. Source line numbers were
re-checked against `92b8fbc` by hand.

---

## Summary

| # | Finding | Severity | Fix size |
|---|---|---|---|
| 1 | The 13.2pt baseline grid does not exist; the build sets 16.32pt | **Critical** | Design decision |
| 2 | Heading tracking `+80/+60` is annulled by Lane's own `series=b` rule | **High** | 2 lines |
| 3 | Run-in `\paragraph` emits zero space before the following text | **High** | 1 line |
| 4 | Math notation is silently redefined (`\epsilon`, `\phi`, `\vec`, `\le`, `\ge`) | **High** | Guard with an option |
| 5 | Footnote marker box is fixed at 7pt; overflows from footnote 100 | **High** | 1 line |
| 6 | `\footnotesep` is set below its own floor and does nothing | Medium | 1 line |
| 7 | `footmisc`'s `hang,flushmargin` are dead, and cannot be overridden | Medium | Option pass-through |
| 8 | Four parameters are silently reassigned later in the same file | Medium | Delete duplicates |
| 9 | `\spaceskip` freezes word spacing at body size document-wide | Medium | Scope it |
| 10 | Widow/orphan penalties take four different values across four modules | Medium | Consolidate |
| 11 | `\jot` is documented as 6.6pt and ships as 9.9pt | Medium | 1 line |
| 12 | `\SetTracking` leaks its numeric argument into PDF bookmarks | Medium | 1 character |
| 13 | Protrusion list declares TS1-only characters in T1/OT1 | Low | Move to TS1 list |
| 14 | `\hfuzz=0.2pt` is commented "tighter" but is looser than default | Low | 1 line |
| 15 | Harness targets and docs point at files that do not exist | Low | 4 spots |

Two cross-cutting causes account for most of the list: **`\linespread` was assumed to scale the
class option** (finding 1, which propagates into 6, 9, 11 and the table metrics), and
**`verbose=silent`** suppresses precisely the diagnostics that would have surfaced findings 2
and 13.

---

## 1. The "13.2pt baseline grid" does not exist; the build sets 16.32pt

**Critical.** This is the load-bearing claim of the whole spacing system.

`paper/modules/lltdimensions.sty:22-26`:

```tex
\newlength{\gridunit}
\setlength{\gridunit}{13.2pt}  % 11pt × 1.20 leading
% CORE SPACING VALUES
\linespread{1.20}              % 11pt × 1.20 = 13.2pt baseline grid increment
```

`\linespread` scales the *class's* `\baselineskip`, not the class option. `size11.clo:48` is
`\@setfontsize\normalsize\@xipt{13.6}` — that is 10.95pt on 13.6pt, so `\linespread{1.20}`
produces 13.6 × 1.2 = **16.32pt**, and the nominal "11pt" body is really 10.95pt.

Measured with the real package:

| Quantity | Lane's comment | Lane's build |
|---|---:|---:|
| normal font size | 11pt | **10.95pt** |
| `\baselineskip` | 13.2pt | **16.31996pt** |
| `\gridunit` | 13.2pt | 13.2pt |

The body sits 3.12pt per line — 23.6% — off the unit that every other constant derives from
(`\quartergridunit` 3.3, `\halfgridunit` 6.6, 9.9, 19.8, 26.4, 39.6). Nothing in the document
lands on the declared grid, and the two values never re-converge. `grep -rl 16.32` over the
whole tree returns nothing.

The claim is repeated in every place an adopter would check, so it cannot be caught by reading:
`lltpaperstyle.dtx:160`, `README.md:374`, `INSTALL.md:304`, `API_REFERENCE.md:197`,
`TROUBLESHOOTING.md:149`, `paper/README.md:119`, `docs/typography/BASELINE-GRID.md:5`,
`lltpaperstyle.sty:694`, `:1087`, and `lltpaperstyleminimal.sty:56`
(`\linespread{1.20}  % Equivalent to 13.2pt for 11pt base`).

**Three dependent failures follow from it:**

- `lltgridoverlay.sty:37,72` — the `[grid]` debug overlay steps at 13.2pt, so the one tool
  offered for diagnosing misalignment confirms the false premise.
- `lltpaperstyle.sty:2606` — `\DeclareMathSizes{11}{11}{8}{6}` keys on 11pt, but the document
  runs at 10.95pt, so it never fires. Measured `\scriptscriptfont0` = `rm-qplr at 6.1pt`, not
  the declared 6pt.
- `lltpaperstyle.sty:2213` — `\setlength{\extrarowheight}{2.2pt}  % Makes standard rows exactly
  13.2pt with 11pt text`, and `:2223` `% Exactly 13.2pt rows`. Measured on a three-row
  `tabular` under the loaded package: **22.22pt per row** (`\arraystretch` 1.2 × 16.32 + 2.2).

**Impact on the adopter.** An entire architecture decision (ADR 0007) was written around the
documented 13.2pt body leading and shipped as an explicit `11pt/13.2pt` setting. It was
superseded in full (ADR 0008) once Lane's real output was measured, forcing a second
re-implementation of the port.

**Suggested fix.** Either state the true figures (10.95pt/16.32pt) and rename `\gridunit` to
what it actually is — a spacing quantum, not a baseline — or make the grid real with an
explicit `\fontsize{11}{13.2}\selectfont` / `\setlength{\baselineskip}{\gridunit}`. The second
is the larger change but is what the documentation currently promises.

---

## 2. Heading tracking `+80/+60` is annulled by Lane's own bold rule

**High.**

`paper/modules/lltheadings.sty:91-93` (and `:104-106` for `\subsection`):

```tex
\titleformat{\section}
  {\normalfont\fontsize{18}{26.4}\selectfont\bfseries\color{sectioncolor}%
   \SetTracking{encoding=*}{80}\lsstyle}  % 18pt bold, softened navy, +8% tracking
```

`paper/modules/lltmicrotype.sty:139-143`:

```tex
% Standard bold text tracking (body text sizes)
\SetTracking{
  encoding = {T1},
  series = b
}{-10}
```

Microtype resolves `\SetTracking` by font-axis specificity, not declaration order. `{T1},
series=b` is more specific than `encoding=*`, so it wins on every bold heading — even though
the broad rule is re-executed each time a heading is typeset.

Measured, 18pt bold Pagella, string `Sample Heading Width Test`:

| Configuration | Width | vs untracked |
|---|---:|---:|
| bold, no tracking rules | 231.75pt | — |
| bold, broad `encoding=*` +80 only — *what `lltheadings` promises* | 264.51pt | +14.1% |
| **bold, +80 with `series=b` −10 present — *what Lane actually loads*** | **227.66pt** | **−1.8%** |
| regular weight + broad +80 (specific rule cannot match) | 255.67pt | +14.7% |

Confirmed through the full package: a plain 18pt bold heading measures 229.75pt, and after
`\SetTracking{encoding=*}{80}\lsstyle` it measures **225.79pt**. It gets *narrower*. Headings
render ~2% tighter than untracked — the opposite sign from the "+8% tracking" the comment
promises, and about 16% away from the declared value. The `+80/+60` lines are dead code
carrying comments that assert an effect that never occurs at any heading level.

Note that `lltmicrotype.sty:90-94` already reserves +80 for *display small caps*, which is the
conventionally correct home for a value that large.

**Two aggravating factors.**

`\SetTracking` is global. Microtype records tracking lists with global definitions, so placing
it inside a `\titleformat` font argument does not scope it — each heading *execution* replaces
the broad list document-wide:

| State | Test width |
|---|---:|
| after grouped +80 declaration | 138.45601pt |
| after grouped +60 declaration | 134.76600pt |
| after a `\section` executes | 138.45601pt |
| after a `\subsection` executes | 134.76600pt |

Compiling Lane's own `main.tex` yields **122** `tracking amount list ... will override`
messages. They surface as `Package microtype Info` rather than Warning because
`lltmicrotype.sty:28,42` load microtype with `verbose=silent` — the same module that creates
the conflict also silences the diagnostic that would reveal it.

**Why this is a footgun, not just dead code.** The broad rule and its suppressor live in
different files, ~400 lines apart, with the warning turned off. An adopter taking the heading
module without the microtype module — a reasonable split, and exactly what the adopter's ADR
0008 chose when it excluded Lane's "detailed custom microtype tables" — removes the suppressor
and gets the live +80. That produced a 9.97pt overfull `\subsection`, 68 tracking-list
overrides, and headings compressed to near pdfTeX's 2% maximum font-expansion shrink;
disabling expansion moved the same heading to 18.15pt overfull and total overfull hboxes from
4 to 15.

**Adopter's fix**, `a6610b5`: removed `\SetTracking`/`\lsstyle` from both `\titleformat` blocks
rather than retuning to −10, precisely because `\SetTracking` is global. Overfull hboxes 4 → 3,
tracking-list overrides 68 → 52, pagination and cross-references unchanged.

---

## 3. Run-in `\paragraph` emits zero space before the following text

**High.**

`paper/modules/lltheadings.sty:130-139`:

```tex
\titleformat{\paragraph}[runin]
  {\normalfont\fontsize{11}{13.2}\selectfont\bfseries\itshape\color{paragraphcolor}}
  {}
  {0em}
  {}
  [~]  % Add space after heading
\titlespacing*{\paragraph}
  {0pt}
  {13.2pt plus 3.3pt minus 1.65pt}
  {0pt}  % No space after for runin format
```

The `[~]` after-code and `\titlespacing`'s `{0pt}` after-value each justify the other in their
comments, and the combination yields nothing. titlesec drives run-in separation from
`\titlespacing`'s after-value, so the tie's space is set to 0pt. `\showbox` of
`\paragraph{Robustness}Estimates remain stable.` in Lane's own build:

```
..\T1/qpl/b/it/11 s          <- last letter of "Robustness"
..\penalty 10000
..\glue 0.0                  <- the [~] after-code, zero width
..\T1/qpl/m/n/10.95 E        <- first letter of "Estimates"
```

It renders as `RobustnessEstimates`, and the `\penalty 10000` means the line cannot even break
there.

**Adopter's fix**, `6bbe340`: drop the `[~]`, set the after-value to `0.75em`.

---

## 4. A typography package silently redefines mathematical notation

**High.**

`paper/lltpaperstyle.sty:2683-2689`, unconditional, with no option to disable:

```tex
\renewcommand{\le}{\leqslant}        % Slanted inequality (more elegant)
\renewcommand{\ge}{\geqslant}        % Slanted inequality
\renewcommand{\epsilon}{\varepsilon} % Lunate epsilon (preferred)
\renewcommand{\phi}{\varphi}         % Curly phi (more readable)
\renewcommand{\vec}[1]{\mathbf{#1}}  % Bold vectors (modern style)
```

These change meaning, not appearance. A paper that distinguishes `\epsilon` from
`\varepsilon` (residual vs. small quantity) or `\phi` from `\varphi` loses the distinction on
adoption, with no error and no warning. `\vec{x}` silently loses its arrow and becomes
indistinguishable from `\mathbf{x}`. A style package should not be able to change what a
manuscript's mathematics says.

This was the single largest reason the adopter ported source rather than loading the package,
and it is written into their ADR 0007 as an explicit prohibition.

**Suggested fix.** Move the block behind a package option, default off.

---

## 5. The footnote marker box is fixed at 7pt and overflows at three digits

**High.**

`paper/lltpaperstyle.sty:1762-1770`, with `:1799`
`\renewcommand{\thefootnote}{\oldstylenums{\arabic{footnote}}}`:

```tex
\renewcommand\@makefntext[1]{%
  % Professional hanging indent: 7pt (0.53 grid units)
  \setlength{\parindent}{7pt}%
  \noindent
  \makebox[7pt][l]{%
    \fontsize{6}{7}\selectfont
    \SetTracking{encoding={T1,OT1}}{50}\lsstyle
    \@thefnmark
```

Marker widths measured inside Lane's own loaded package, at that size and tracking:

| Marker | Width | Room left in the 7pt box |
|---|---:|---:|
| `\oldstylenums{9}` | 3.3pt | 3.7pt |
| `\oldstylenums{99}` | 6.6pt | **0.4pt** |
| `\oldstylenums{999}` | 9.9pt | **−2.9pt — overflows** |

A `\makebox` with an explicit width does not grow, so from footnote 100 the marker overprints
the note text. From footnote 10 the 0.4pt gap is not a box collision in TeX geometry, but at
8.5pt text it is visually jammed and makes PDF text extraction concatenate the marker with the
following word. The adopter's paper rendered `16Our`, `11Based`, `12This` — 13 of 22 numbered
body footnotes were two-digit. Most papers pass footnote 9.

**Adopter's fix**, `1b2d740`: `\makebox[10.3pt][l]`, giving every marker up to 99 the same
3.7pt gap single digits already had. A `\settowidth` from `\oldstylenums{99}` plus a minimum
gap would be the self-correcting version.

---

## 6. `\footnotesep` is set below its own floor and does nothing

**Medium.**

`paper/lltpaperstyle.sty:1784`:

```tex
\setlength{\footnotesep}{0.25\gridunit}   % 0.25 grid units between footnotes
```

Two errors in one line. `\footnotesep` is not the space between footnotes — LaTeX inserts
`\rule\z@\footnotesep` at the head of each note, so it is a *floor* on the first line's height.
At 0.25 × 13.2 = 3.3pt it sits below the natural strut and contributes nothing. Measured in
footnote context inside Lane's own package:

```
footnote \baselineskip  = 11.99997pt
footnote \strut height  =  8.39993pt   depth = 3.60002pt
\footnotesep            =  3.29999pt
```

Any value from 0 to ~8.4pt renders identically. Consecutive notes end up *closer together* than
lines within a single note. Measured sweep in the adopter's paper at identical settings:

| `\footnotesep` | between notes | within a note |
|---:|---:|---:|
| 3.3 (Lane) | 9.72pt | 12.00pt |
| 7.7 | 11.28pt | 12.00pt |
| 8.4 | 12.12pt | 12.00pt |
| 12.0 | 15.72pt | 11.88pt |

Lane disagrees with itself here: `lltpaperstyle.sty:1670` sets `0.75\gridunit` = 9.9pt for the
title-page footnote block, which *does* bind. Title notes and body notes therefore separate
differently, by accident, while both comments describe their value as intentional.

The surrounding leading comments are also wrong in three directions: `:1758` says 11pt leading,
`:1772` says 10pt (`\fontsize{8.5}{10}`), and the build produces **12pt**, because
`\linespread{1.20}` scales the leading but not the absolute 3.3pt constant paired with it.
This is finding 1 resurfacing.

**Adopter's fix**, `907035b`: 8.4pt (0.7 × the 12pt footnote baseline, LaTeX's strut
proportion), giving exactly 12pt separation once the previous note's 3.6pt strut depth is
added, with no repagination across 52 pages. Still a hand-computed literal coupled to
`\linespread` by hand — deriving it from the leading measured *inside* footnote context is the
durable version.

---

## 7. `footmisc`'s options are dead, and adopters cannot override them

**Medium.**

`paper/lltpaperstyle.sty:1752`, ten lines before the `\@makefntext` above:

```tex
\RequirePackage[hang,flushmargin]{footmisc} % Hanging indent, flush left
```

footmisc implements both options *by* defining `\@makefntext`, which `:1762` then replaces
wholesale. Dumping the final meaning under the loaded package gives Lane's own body verbatim,
with no footmisc content — so the comment names two behaviours the package cancels, and Lane's
replacement produces flush-left wrapped lines rather than a hanging indent. Compounding it,
`:1815` does `\AtBeginDocument{\setlength{\footnotemargin}{7pt}}`, contradicting `flushmargin`,
whose entire job is `\footnotemargin=0pt`. Measured final value: `\footnotemargin = 7.0pt`.

Separately, the options are hard-coded with no pass-through, so an adopter needing `bottom`
(footnotes pinned below floats — common in empirical papers) cannot have it:

```
! LaTeX Error: Option clash for package footmisc.
```

The two combine into a trap: the options you cannot override are inert, and the one you must
drop to adopt Lane was load-bearing. The adopter's paper copied Lane's option list wholesale
and lost `bottom` in a 21-float document; restored in `1b2d740`.

**Suggested fix.** Drop the inert options, and expose a package option or hook for footmisc
options an adopter needs.

---

## 8. Four parameters are silently reassigned ~2000 lines later in the same file

**Medium.**

| Parameter | Declared | Overridden | In force |
|---|---|---|---:|
| `\spaceskip` | `:658` `0.35em plus 0.25em minus 0.15em` | `:2774` `0.33em…` | 0.33em |
| `\xspaceskip` | `:659` `0.5em plus 0.3em minus 0.2em` | `:2775` `0.48em…` | 0.48em |
| `\brokenpenalty` | `:715` `5000` | `:2748` `2000` | **2000** |
| `\postdisplaypenalty` | `:717` `10000` | `:2757` `2000` | **2000** |

Both members of each pair carry a confident explanatory comment — `:717` says "Keep at least 2
lines after display math", `:2757` says "Some flexibility after math". An adopter reading
section V, *Baseline Grid and Spacing System*, gets values the build never produces. Measured
in force: `\brokenpenalty=2000`, `\postdisplaypenalty=2000`, `\interlinepenalty=2500`.

Worth noting the declared values may be the better ones: in the adopter's 52-page paper,
`\brokenpenalty=5000` (the `:715` value) took overfull vboxes 8 → 6 and cleared 3 hyphenation
warnings relative to the 2000 that actually ships.

`\raggedbottom` (`:2421`, `:2912`), `\parindent` (`lltdimensions.sty:28` vs `:2770`) and
`\arraystretch` (`:1377`, `:2294`) are also set twice, though to consistent values.

---

## 9. `\spaceskip` freezes word spacing at body size for the whole document

**Medium.**

`paper/lltpaperstyle.sty:657-659`, re-set at `:2774-2775`:

```tex
% Hochuli: Optimize word spacing for Pagella's wider characters
\spaceskip=0.35em plus 0.25em minus 0.15em
```

`\spaceskip` is a glue register: `em` resolves at assignment time, in the preamble, at the body
font. The result is one absolute word space used at every size in the document.

| Context | Pagella natural space (`\fontdimen2`) | Lane's forced `\spaceskip` |
|---|---:|---:|
| body, 10.95pt | 2.73749pt | 3.59302pt (**+31%**) |
| 18pt bold heading | 4.5pt | 3.59302pt (**−20%**) |

Every heading is set with word spaces a fifth too tight for its own font, and body text a third
too loose. Lane compensates locally inside `\@makefntext` (`:1775`) but nowhere else, so
headings, captions and any size-shifted text are all affected. This also explains why the
complete package measures tighter than its own modules on heading tests.

**Suggested fix.** Set `\spaceskip` inside a size-aware hook, or drop it and let
`\fontdimen2` do its job.

---

## 10. Widow and orphan penalties take four different values across four modules

**Medium.**

| File:line | Value |
|---|---|
| `paper/lltpaperstyle.sty:710-712` | club / widow / displaywidow = **10000** |
| `paper/modules/lltheadings.sty:212-213` | club / widow = 10000 |
| `paper/modules/lltcompilationfixes.sty:42-43` | club / widow = **9999** |
| `paper/modules/lltheadingsgridlocked.sty:169-170` | club / widow = **5000** |
| `paper/modules/lltmathgridlocked.sty:157-161` | predisplay 8000, postdisplay 3000, displaywidow **8000** |

Which wins is pure load order (`lltcompilationfixes` at `:237`, `lltheadings` at `:252`,
`lltpaperstyle`'s own block at `:710`). Under the default option set the measured result is
`CLUB=10000 WIDOW=10000 DISPWIDOW=10000` — but an adopter passing `[grid]`, which loads
`lltheadingsgridlocked` and `lltmathgridlocked`, gets a different and undocumented answer
depending on ordering. Not a rendering bug in the default configuration, but four independent
claims about the same three registers.

For reference: setting club/widow/displaywidow to 10000 took the adopter's 52-page paper from
three widows/orphans to zero with no repagination.

---

## 11. `\jot` is documented as 6.6pt and ships as 9.9pt

**Medium.**

`paper/lltpaperstyle.sty:2592-2593` and `:2615-2618`:

```tex
% Multi-line equation spacing
\jot=6.6pt  % 0.5 grid units between aligned equations
...
% Ensure consistent spacing around equation numbers
\AtBeginDocument{%
  \addtolength{\jot}{0.25\gridunit}  % Add quarter grid unit between numbered equations
}
```

Measured `\jot` in Lane's build is **9.9pt**. The `\addtolength` is unconditional and global —
despite the comment, it applies to every multi-line display, numbered or not. Lane's own
`grideqnarray` (`:2626-2629`) then sets `\jot` back to `0.5\gridunit` = 6.6pt, so the package
makes three different statements about inter-equation spacing.

---

## 12. `\SetTracking` leaks its numeric argument into PDF bookmarks

**Medium.** One-character fix.

`paper/lltpaperstyle.sty:2411`, inside `\pdfstringdefDisableCommands`:

```tex
  \def\SetTracking#1#2{#2}%    % Remove tracking commands
```

`\SetTracking`'s second argument is the tracking *amount*, so substituting `#2` prints that
number into the bookmark string. Verified — `\section{\headsc{Identification} Strategy}`, using
Lane's own `\headsc` (which is not in the disable list), produces:

```
\BOOKMARK [1][-]{section.1}{1\04060Identification\040Strategy}{}% 1
```

The bookmark reads `1 60Identification Strategy`. Any of `\regsc`, `\itsc`, `\headsc`,
`\inlinebsc`, `\person`, `\smallcapsacro` in a heading triggers it.

**Fix.** `\def\SetTracking#1#2{}`.

---

## 13. Protrusion list declares TS1-only characters in a T1/OT1 list

**Low**, but noisy.

`paper/modules/lltmicrotype.sty:294-311` declares, under `encoding = {T1,OT1}, family = qpl`:

```tex
  \textdagger = {200,300}, \textdaggerdbl = {200,300},
  \textsection = {200,200}, \textparagraph = {,300},
  \textasteriskcentered = {300,300},
  \textdollar = {100,100}, \textsterling = {100,}, \texteuro = {,100},
  \textexclamdown = {300,}, \textquestiondown = {300,},
  \guillemotleft = {400,200}, \guillemotright = {200,400}
```

`\textdagger`, `\textdaggerdbl`, `\textparagraph`, `\textasteriskcentered` and `\texteuro` have
no slot in T1; several more have none in OT1. Compiling Lane's own `main.tex` produces **241**
`Unknown slot number of character` messages — 30 each for `\textparagraph`, `\texteuro`,
`\textdaggerdbl`, `\textdagger`, `\textasteriskcentered`; 13 each for the rest — all demoted to
`Package microtype Info` by `verbose=silent`. The declared protrusion for those characters
never takes effect, and the log line that would say so is suppressed.

---

## 14. `\hfuzz=0.2pt` is commented "tighter" but is looser than the default

**Low.**

`paper/lltpaperstyle.sty:2764` — `\hfuzz=0.2pt  % Tighter overfull tolerance`. LaTeX's default
is 0.1pt, so this *doubles* the tolerance and suppresses overfull reports rather than
tightening them.

---

## 15. Harness targets and docs reference files that do not exist

**Low.**

- `Makefile:221` — `make check-deps` calls `$(SRC_DIR)/sh/check-packages.sh`, which was never
  committed; `src/sh/` holds only `.gitkeep` and `validate_latex_style.sh`. The `|| echo
  "Script not found…"` fallback means the target exits 0 and looks healthy.
- `src/sh/validate_latex_style.sh:158` — `cd "$(dirname "$0")/../.."` resolves two levels up
  from `src/sh/`, i.e. the repo root's *parent*, so `make style-check` runs in the wrong
  directory.
- `Makefile:48` — `$(CHKTEX) $(CHKTEXFLAGS) *.tex` globs the root only, so `make lint` never
  lints `paper/` or `appendices/` — which is where all 3101 lines of `lltpaperstyle.sty` and
  every `.tex` fragment live.
- `docs/technical/TESTING.md:452,481,484` documents a log-parsing toolchain at
  `context/tools/log-parsing/`. `context/` does not exist and is gitignored.

Worth noting alongside this: `tests/check-spacing-integrity.sh` exists but did not catch
findings 1, 6, 9 or 11. Several findings here would make good regression tests — asserting the
*measured* `\baselineskip`, `\jot`, `\footnotesep` and heading widths against declared values
would have caught most of this list mechanically.

---

## Unverified leads

**A. Overleaf may not resolve `paper/modules/*.sty`.** `.latexmkrc` is five lines, entirely
`ensure_path('TEXINPUTS', './paper:./paper/modules:')`, and the `Makefile` exports the same;
there is no other resolution path — every fixture in this report required setting `TEXINPUTS`
by hand. If Overleaf does not honour `.latexmkrc` for `TEXINPUTS`, `\usepackage{lltfonts}` and
friends resolve only when the `.sty` files sit in the project root. This could not be tested
from here. It is worth the maintainer's attention because `README.md` and `INSTALL.md` present
the template as Overleaf-friendly.

**B. Five dangling `Hfootnote.1`–`Hfootnote.5` PDF destinations** appeared in the adopter's
build both before and after the port, so they are probably that paper's own title-page notes
rather than Lane. Flagged only because `\titlefootnotesetup` (`:1664-1691`) does the same
pattern — `\setcounter{footnote}{0}` plus `\thefootnote` → `\fnsymbol`, twice — which is a
plausible generator of duplicate hyperref anchors. Not reproduced against Lane's own title page.

**C. `\renewcommand{\footnote}[2][]` at `:1804-1810`.** The comment says "Prevent footnote
marks from breaking", but the implementation inserts `\nobreak` at the start of the footnote
*text* (`\oldfootnote{\nobreak#2}`), which does nothing to the mark. No misbehaving case was
constructed; reported as a comment/behaviour mismatch in a command every adopter relies on.

---

## Excluded — the adopter's own errors, not Lane's

Listed so the report is not read as assigning everything upstream.

- **Widow/orphan penalties missing after the port.** Lane sets them correctly at `:710-712`;
  the adopter simply omitted them from the port list. Distinct from finding 10, which is about
  Lane's four conflicting values.
- **Flattening `\gridunit` arithmetic into ~95 pre-multiplied literals** in the adopter's
  `preamble.tex`. A porting style choice. It would not have prevented any finding above — Lane
  expresses `\footnotesep` as `0.25\gridunit` and has the identical bug.
- **The adopter's `\pagestyle{empty}` folio loss, `floats/` brace imbalance, and
  cross-reference tilde gaps.** Unrelated to Lane.

ADR 0007's incorrect `11pt/13.2pt` requirement is *not* excluded — it is folded into finding 1,
since Lane's documentation is what it was derived from.
