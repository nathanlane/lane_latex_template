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
The fixed vertical rhythm every element aligns to. The Package's organising
constraint — spacing decisions are expressed as multiples of it, not in points.
_Avoid_: leading grid, vertical grid, rhythm

**Quantum**:
The smallest unit of vertical space the grid admits. Spacing is stated in whole
or half quanta.
_Avoid_: unit, step, tick

**Grid-locked**:
Describes a Module that forces its output onto the baseline grid rather than
merely respecting it — currently headings and mathematics.
_Avoid_: aligned, snapped
