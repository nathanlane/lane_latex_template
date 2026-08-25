# Contributing to Lane LaTeX Template

## Building

```bash
make          # compile demo/main.tex → main.pdf
make clean    # remove generated output, the PDF included
make help     # list every target
```

Requires TeX Live 2020+ with `tgpagella`, `inconsolata`, `newpx`, `mathalfa`,
and `booktabs`. Verify your installation with `make check-deps`.

## Pre-commit Gates

All three must pass before committing, and they are exactly what CI runs:

```bash
make lint     # chktex on demo/*.tex and demo/appendices/*.tex, then the
              # math-spacing checker (src/sh/validate_latex_style.sh)
make build    # latexmk full compile → main.pdf
make test     # python3 -m pytest -q, then bash tests/run-tests.sh
```

`make test` runs both harnesses because issue #51 removed the four separate
test targets: what CI runs and what you run can no longer drift apart. The
shell harness is documented in `docs/technical/TESTING.md`.

The pytest harness requires `pdftotext` (Poppler) for PDF text assertions; it
skips those assertions cleanly when `pdftotext` is unavailable.

## Package Namespace Convention

The package is `lanepaper`; its modules use the `lnp` prefix:

- Main style: `lanepaper` (`lanepaper/lanepaper.sty`)
- Modules: `lnpcolors`, `lnpfonts`, `lnpdimensions`, `lnpheadings`,
  `lnplists`, `lnpmicrotype`, `lnpparagraphs`, `lnphochuli`, etc.

Load packages by name, not by path:

```latex
\usepackage{lanepaper}   % correct
\usepackage{paper/paperstyle} % wrong — legacy path, do not use
```

How package code is written -- naming, message policy, robustness, hooks, lint
policy, and the rule against `\makeatletter` in a `.sty` -- is in
[`CONVENTIONS.md`](CONVENTIONS.md). Read it before changing anything in
`lanepaper/`.

Internal LaTeX identifiers (lengths, counters, private commands) use the
`\lnp@` prefix to avoid conflicts. See
[`docs/PACKAGE_NAMING_CONVENTION.md`](docs/PACKAGE_NAMING_CONVENTION.md) and
[`docs/package/NAMESPACE_CONVENTIONS.md`](docs/package/NAMESPACE_CONVENTIONS.md)
for the full convention.

## Module Documentation

- Per-module docs: `docs/package/*.md` (colors, fonts, dimensions, headings, lists)
- Module index: `docs/package/modules.md`
- Testing guide: `docs/technical/TESTING.md`
