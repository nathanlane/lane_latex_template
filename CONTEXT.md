# lanepaper

Typography for academic papers, distributed as a LaTeX2e package. This file is
the project's glossary: it fixes what each term means so that documentation,
issues, and code use one word per concept.

## Language

### Artifacts

**Package**:
The `lanepaper` style files — the typography itself, installed once and reused
across documents. Public GitHub release and later CTAN publication are separate
events.
_Avoid_: style, stylesheet, lltpaperstyle, the paper package

**Template**:
The repository forked once per paper, carrying document scaffolding and the
author's own conveniences. Depends on the Package; contains none of it.
_Avoid_: starter, boilerplate, skeleton

**Demo**:
The curated visual document inside the Package repository, compiled by CI to
prove the Package works. Not a starting point for real papers — that is the
Template.
_Avoid_: example, sample paper, main.tex

**Module**:
An internal owner for one coherent area of Package typography. It is not a
separate adopter-facing package or load path.
_Avoid_: public module, entry point, component, submodule, include

### Loading

**Configure-if-loaded**:
The ownership relation in which the Package may style behavior of a third-party
package only after the document has loaded it and only where the behavior is
part of Lanepaper typography. It never transfers ownership of the third-party
API to Lanepaper.
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
The private 13.2pt scale from which some internal vertical spaces are drawn.
It is not the baseline, does not divide it, and is not a public unit or grid
system (ADR-0005, ADR-0006).
_Avoid_: public grid unit, baseline unit, step, tick, grid
