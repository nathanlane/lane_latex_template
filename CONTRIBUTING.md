# Contributing to Lane LaTeX Template

## Building

```bash
make          # compile main.tex → main.pdf
make clean    # remove auxiliary files
```

Requires TeX Live 2020+ with `tgpagella`, `inconsolata`, `newpx`, `mathalfa`,
and `booktabs`. Verify your installation with `make check-deps`.

## Running the Test Suites

Three suites must all pass before committing:

```bash
# 1. Shell harness (LaTeX compilation + compatibility probes)
bash tests/run-tests.sh

# 2. Python regression tests (measured values, contract assertions)
python3 -m pytest -q

# 3. Convenience alias that calls tests/run-tests.sh
make test
```

The pytest harness requires `pdftotext` (Poppler) for PDF text assertions; it
skips those assertions cleanly when `pdftotext` is unavailable.

## Package Namespace Convention

All packages use the `llt` prefix (Lane LaTeX Template):

- Main style: `lltpaperstyle` (`paper/lltpaperstyle.sty`)
- Modules: `lltcolors`, `lltfonts`, `lltdimensions`, `lltheadings`,
  `lltlists`, `lltmicrotype`, `lltparagraphs`, `llthochuli`, etc.

Load packages by name, not by path:

```latex
\usepackage{lltpaperstyle}   % correct
\usepackage{paper/paperstyle} % wrong — legacy path, do not use
```

Internal LaTeX identifiers (lengths, counters, private commands) use the
`\paper@` prefix to avoid conflicts. See
[`docs/PACKAGE_NAMING_CONVENTION.md`](docs/PACKAGE_NAMING_CONVENTION.md) and
[`paper/modules/NAMESPACE_CONVENTIONS.md`](paper/modules/NAMESPACE_CONVENTIONS.md)
for the full convention.

## Module Documentation

- Per-module docs: `paper/modules/*.md` (colors, fonts, dimensions, headings, lists)
- Module index: `paper/modules/README.md`
- Testing guide: `docs/technical/TESTING.md`
