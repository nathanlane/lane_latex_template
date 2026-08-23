# Contributing to Lane LaTeX Template

## Building

```bash
make          # compile main.tex → main.pdf
make clean    # remove auxiliary files
```

Requires TeX Live 2020+ with `tgpagella`, `inconsolata`, `newpx`, `mathalfa`,
and `booktabs`. Verify your installation with `make check-deps`.

## Pre-commit Gates

All four must pass before committing (`make lint`, `make build`, and
`python3 -m pytest -q` are gated by `AGENTS.md`; the shell harness is
documented in `docs/technical/TESTING.md`):

```bash
make lint              # chktex on demo/*.tex, demo/appendices/*.tex
make build             # latexmk full compile → main.pdf
bash tests/run-tests.sh  # shell harness: LaTeX fixtures + compatibility probes
python3 -m pytest -q   # regression tests: measured values, contract assertions
```

`make test` is a convenience alias for `bash tests/run-tests.sh`.

The pytest harness requires `pdftotext` (Poppler) for PDF text assertions; it
skips those assertions cleanly when `pdftotext` is unavailable.

## Package Namespace Convention

The package is `lanepaper`; its modules use the `lnp` prefix:

- Main style: `lanepaper` (`paper/lanepaper.sty`)
- Modules: `lnpcolors`, `lnpfonts`, `lnpdimensions`, `lnpheadings`,
  `lnplists`, `lnpmicrotype`, `lnpparagraphs`, `lnphochuli`, etc.

Load packages by name, not by path:

```latex
\usepackage{lanepaper}   % correct
\usepackage{paper/paperstyle} % wrong — legacy path, do not use
```

Internal LaTeX identifiers (lengths, counters, private commands) use the
`\lnp@` prefix to avoid conflicts. See
[`docs/PACKAGE_NAMING_CONVENTION.md`](docs/PACKAGE_NAMING_CONVENTION.md) and
[`docs/package/NAMESPACE_CONVENTIONS.md`](docs/package/NAMESPACE_CONVENTIONS.md)
for the full convention.

## Module Documentation

- Per-module docs: `docs/package/*.md` (colors, fonts, dimensions, headings, lists)
- Module index: `docs/package/modules.md`
- Testing guide: `docs/technical/TESTING.md`
