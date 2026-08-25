# lanepaper

Typography for academic papers, distributed as a LaTeX2e package. This file is
the project's glossary: it fixes what each term means so that documentation,
issues, and code use one word per concept.

## Language

### Artifacts

**Package**:
The `lanepaper` style files — the typography itself, installed once and reused
across documents. The only thing that ships to CTAN.
_Avoid_: style, stylesheet, lltpaperstyle, the paper package

**Template**:
The repository forked once per paper, carrying document scaffolding and the
author's own conveniences. Depends on the Package; contains none of it.
_Avoid_: starter, boilerplate, skeleton

**Demo**:
The minimal document inside the Package repository, compiled by CI to prove the
Package works. Not a starting point for real papers — that is the Template.
_Avoid_: example, sample paper, main.tex

**Module**:
One `.sty` file inside the Package covering a single area of typography — fonts,
headings, lists, the grid. Loaded by name, never by path.
_Avoid_: component, submodule, include

### Loading

**Configure-if-loaded**:
The rule that the Package styles a third-party package when the document has
already loaded it, but never loads it itself. Applies to `hyperref`, `cleveref`,
`biblatex`, `babel`, and `appendix`.
_Avoid_: optional dependency, soft dependency

**Vendoring**:
Copying the Package's `.sty` files into a Template checkout, for environments
that cannot install into a texmf tree. A temporary measure that CTAN retires.
_Avoid_: bundling, embedding

### Typography

**Baseline grid**:
The 16.32pt line grid running text actually sits on (`\linespread{1.20}` on
the class's 13.6pt baseline). Descriptive, not an organising constraint:
nothing forces elements onto it (ADR-0004, ADR-0005).
_Avoid_: leading grid, vertical grid, rhythm

**Quantum**:
The 13.2pt unit vertical space values are drawn from (`\gridunit`). Spacing
is stated in whole or fractional quanta. The quantum is not the baseline and
does not divide it; spacing in quanta does not produce vertical rhythm
(ADR-0005).
_Avoid_: unit, step, tick, grid
