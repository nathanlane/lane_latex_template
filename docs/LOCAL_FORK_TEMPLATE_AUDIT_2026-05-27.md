# Local Fork Template Audit - 2026-05-27

## Scope

This audit filters three large local paper repositories for reusable LaTeX template
work only:

- `/Users/nathanlane/code/kiel_review`
- `/Users/nathanlane/code/eastasia_paper`
- `/Users/nathanlane/code/monopoly_technology`

Excluded by default: paper body text, bibliographies, empirical outputs, project
data, generated figures, and project-specific author/title material.

## Filter

Template-related objects scanned:

- `paper/paperstyle.sty`, `paper/preamble.tex`, `paper/titlepage.tex`
- archived modular style files under `paper/archive/modules/*.sty`
- root `Makefile`
- root and paper-level README/style documentation
- template markers including `paperstyle`, `lltpaperstyle`, `biblatex`,
  `TEXINPUTS`, `latexmk`, `chktex`, `Overleaf`, and package compatibility notes

Current template baseline:

- `/Users/nathanlane/code/lane_latex_template/paper/lltpaperstyle.sty`
- `/Users/nathanlane/code/lane_latex_template/paper/modules/llt*.sty`
- `/Users/nathanlane/code/lane_latex_template/paper/preamble.tex`
- `/Users/nathanlane/code/lane_latex_template/Makefile`

## Repo Inventory

| Repo | Template surfaces found | Git status signal | Notes |
| --- | --- | --- | --- |
| `kiel_review` | `paper/paperstyle.sty`, `paper/preamble.tex`, archived modules, `Makefile`, paper docs | Dirty generated LaTeX outputs plus `main.tex`, `paper/titlepage.tex`, `references.bib` | Contains the full archived modular family and a v1.7 monolithic `paperstyle.sty`. |
| `eastasia_paper` | Same as `kiel_review`, plus `MODULARIZATION_ACTION_PLAN.md` and `docs/style/CHANGELOG.md` | Clean | Archived modules are identical to `kiel_review`; `paperstyle.sty` has a small journal-specific figure-caption extension. |
| `monopoly_technology` | `paper/paperstyle.sty`, `paper/preamble.tex`, `paper/titlepage.tex`, `Makefile`, docs | Untracked `.agents/` and `.codex/` | `paperstyle.sty` is identical to `kiel_review`; no archived modular modules present. |

## Main Finding

The candidate repos mostly represent two template lines:

1. A newer local monolith: `paper/paperstyle.sty` v1.7, dated 2026-03-06.
   It absorbed live core modules and retired the modular public API.
2. The older archived modules: `paper/archive/modules/*.sty`.
   In this repo, those have already been imported/renamed as `paper/modules/llt*.sty`.

The current template is not simply behind the forks. It has already absorbed much
of the archived modular system, added package options, renamed packages under the
`llt` namespace, and added several later fixes. The safest adoption path is not a
bulk import of `paperstyle.sty`; it is selective backporting of behavior-preserving
compatibility fixes from the monolith.

## Adoption Matrix

| Source | Object | Change | Why it matters | Visual impact | Recommendation |
| --- | --- | --- | --- | --- | --- |
| all three | `paper/paperstyle.sty` appendix wrapper | Forks preserve `\section*{...}` and `\section[short]{long}` inside `\startappendices`; current `lltpaperstyle` only wraps one mandatory argument. | Current template can break starred or optional appendix section forms and lose short TOC titles. | None expected for ordinary appendices; preserves existing LaTeX API. | Adopt as a focused compatibility patch. |
| all three | `paper/paperstyle.sty` footnote wrapper | Forks preserve optional footnote marks via `\renewcommand{\footnote}[2][]{...}`; current `lltpaperstyle` only accepts one mandatory argument. | Current template can break `\footnote[<mark>]{...}`. | None for normal footnotes; preserves optional API. | Adopt as a focused compatibility patch. |
| all three | `paper/paperstyle.sty` appendix finish | Forks reset `\paperstylesectionsavedfalse` after restoring `\section`; current template restores `\section` but leaves the flag true. | Avoids stale internal state if appendices are opened/closed by helper environments or future tests. | None. | Adopt with the appendix patch. |
| all three | `paper/paperstyle.sty` sideways caption hooks | Forks apply table/figure caption setup to `sidewaystable` and `sidewaysfigure`; current template applies table, figure, and longtable hooks only. | Improves consistency for rotating floats if `rotating` environments are used. | Possible caption-spacing effect on sideways floats only. | Review manually; adopt only with a fixture that proves intended output. |
| `eastasia_paper` | `paper/paperstyle.sty` top-caption figure support | Adds `\paperstyletopfigurecaptionsetup`, `topfignotes`, and `topcaptionfigure`. | Useful for journal-specific figure requirements. | Yes: permits/encourages figure captions above figures. | Reject by default under current no-visual-change rule. Could become an opt-in extension later. |
| `kiel_review`, `eastasia_paper` | `paper/archive/modules/*.sty` | Archived modules are identical across those repos and mostly match current `paper/modules/llt*.sty` after namespace renaming. | Confirms current repo already imported the reusable modular layer. | None. | No import. Current versions are equal or newer. |
| all three | monolithic `paperstyle.sty` v1.7 | Retires modular public API and inlines module code. | Reduces module loading complexity in paper repos. | High risk; large behavioral surface and conflicts with current package namespace design. | Do not bulk import. Selectively backport only compatibility fixes. |
| all three | `paper/preamble.tex` | Forks load `paper/paperstyle` before manual `biblatex`; current template loads `lltpaperstyle`, which auto-loads `biblatex` unless disabled. | Represents a different package-loading model, not a simple improvement. | Potential bibliography behavior change. | Do not import wholesale. Keep current `nobiblatex` escape hatch. |
| `eastasia_paper` | root `Makefile` | Has project lint/validate targets, but not the AGENTS gates exactly. | Current template already has `build`, `lint`, and `fmt` gates matching AGENTS.md. | None. | No import. |
| `kiel_review`, `monopoly_technology` | root `Makefile` | Simpler or project-specific targets. | Less complete than current template gates. | None. | No import. |

## Clear Best Practices to Carry Forward

- Preserve standard LaTeX command APIs when wrapping core commands.
  The footnote and appendix wrappers are the clearest examples.
- Keep project-specific journal variants opt-in.
  `eastasia_paper`'s top-caption figure support is useful, but it should not alter
  the default figure rule.
- Prefer compatibility patches over architecture reversals.
  The monolith is useful evidence, but this repo has intentionally moved to a
  namespaced modular package layout.
- Require fixture coverage before adopting float/caption changes.
  Sideways captions are plausible, but they need a regression fixture because they
  can affect layout.

## Proposed Import Order

1. Add a regression fixture for optional footnotes and appendix `\section` forms.
2. Patch `lltpaperstyle.sty` to preserve optional footnote marks.
3. Patch `lltpaperstyle.sty` to preserve starred and optional appendix sections,
   and reset `\paperstylesectionsavedfalse` during `\finishappendices`.
4. Run `make lint`, `make build`, and `pytest -q`.
5. Separately evaluate sideways caption hooks with a rotating-float fixture.

## Non-Adopted Items

- Bulk replacement with v1.7 monolithic `paperstyle.sty`.
- East Asia top-caption figure defaults.
- Paper-specific Makefile targets, project audit scripts, and content workflows.
- Archived modules that are already present under the `llt` namespace.

