---
status: accepted
date: 2026-08-28
---

# A narrow v3 package with one public entry point

Lanepaper v3 is a typography package, not a library of writing shortcuts or a
document framework. Its sole public load path is `\usepackage{lanepaper}`;
the `lnp*.sty` modules are internal owners that may change without becoming
separate adopter-facing packages.

This ADR defines the v3 target. Issue #82 tracks the transition, so current v2
surfaces may remain until their dependency-ordered child lands.

This is an intentional breaking contraction before CTAN. Generic writing,
maths, reference, float, appendix, paragraph-mode, grid, and package-wrapper
APIs are removed rather than preserved behind aliases. Standard LaTeX and
third-party packages keep their own commands. Lanepaper loads a dependency
only when its typography requires it, and configures an already-loaded package
only where Lanepaper owns the resulting typographic behavior.

Only `[optical]` and `[nocolor]` remain as options. Core paragraph behavior,
including widow protection, belongs to the default package; `[optical]` is
reserved for separately sourced refinements such as runt control. The 13.2pt
spacing quantum remains an internal implementation value, not a public grid
system or unit API.

The supported production baseline is pdfTeX with TeX Live 2025. The package
honors class-selected A4 or Letter paper while retaining its established
11pt article typography and centered six-inch text block.

The GitHub v3.0.0 release is manual and points to one exact CI-green
`origin/main` commit. CTAN submission is a separate decision and remains on
hold. Release preparation must not add a general readiness score, new test
suite, complex gate, screenshot automation, or release workflow: use the
existing focused checks, simplify the implementation, and review each change.

## Consequences

- v3 provides migration notes, not compatibility aliases.
- Internal module boundaries follow coherent ownership and may be simplified
  without expanding the public API.
- Documents remain responsible for bibliography, cross-reference, appendix,
  and other content-level package choices.
- GitHub issue #82 is the operational plan; this ADR records only the durable
  boundary and constraints.
