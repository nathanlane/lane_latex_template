# Testing

`pytest` is the regression harness and a bash script drives LaTeX fixture
compilation. l3build's `check` is deliberately not used; see
[ADR-0002](../docs/adr/0002-l3build-for-packaging-pytest-for-tests.md).

## Quick start

```bash
make test
```

That is `python3 -m pytest -q` followed by `bash tests/run-tests.sh`, and it is
exactly what CI runs. To run one harness on its own:

```bash
python3 -m pytest -q                                 # regression tests
bash tests/run-tests.sh                              # shell harness
bash tests/run-tests.sh tests/fixtures/minimal.tex   # one fixture
```

The pytest suite checks package contracts by compiling focused documents and
reading TeX logs; it also invokes the manual biber bibliography probe because
`run-tests.sh` does not run that script. The shell harness owns bulk fixture
compilation, and neither retained check depends on external PDF-text extraction.

## Gates

| Command | Purpose | Blocking |
|---------|---------|----------|
| `make lint` | ChkTeX over the demo sources | yes |
| `make build` | `latexmk -pdf -interaction=nonstopmode demo/main.tex` | yes |
| `make test` | pytest, then the shell fixture and compatibility harness | yes |

## Layout

```
tests/
├── run-tests.sh                # shell harness; compiles every fixture
├── test-bibliography.sh        # bibliography probe invoked by pytest
├── test_infrastructure.py      # repository invariants and decision guards
├── test_option_contracts.py    # package and document contracts
├── test_measured_values.py     # computed TeX dimensions
├── test_engine_guard.py        # the pdfTeX-only guard, incl. xelatex/lualatex
├── fixtures/                   # 20 .tex documents, compiled by run-tests.sh
├── compilation/                # generated PDFs and logs (git-ignored)
└── visual/output/              # rendered pages for manual comparison
```

`tests/compilation/logs/` is transient. The logs help locally but are not part
of the verification contract.

## Accepted warnings

`main.log` warnings that are known and accepted:

- `LaTeX Warning: Command \showhyphens`
- `Overfull` / `Underfull` lines whose fixes need typography or prose changes
- `Package microtype Info: Unknown slot number`

Anything else should be eliminated rather than suppressed. Useful greps after a
build:

```bash
grep -n "^!" main.log                      # errors
grep -c 'Overfull \\hbox' main.log         # box problems
grep -n "Warning" main.log main.blg        # everything else
```

## Adding a fixture

`run-tests.sh` discovers every `.tex` file in `tests/fixtures/`, so adding one
is enough to register it:

```latex
\documentclass[11pt,letterpaper]{article}
\usepackage{lanepaper}
\begin{document}
\section{Testing one thing}
\bsc{Bold small caps}
\end{document}
```

Name it for what it covers: `feature-name.tex`, `issue-123.tex` for a
regression tied to an issue. Keep each fixture to one feature — a fixture that
exercises everything tells you nothing about what broke.

Fixtures that need the demo's bibliography or preamble use `\input{preamble.tex}`
and rely on `TEXINPUTS` covering `./lanepaper` and `./demo`, which the Makefile
and the harness both set.

## Visual checks

`tests/visual/output/` holds rendered pages and is regenerated on every
`run-tests.sh` run. Comparison is manual. For a real rendering proof, compare
page by page rather than eyeballing totals:

```bash
pdftoppm -r 150 -png before.pdf a/p
pdftoppm -r 150 -png after.pdf  b/p
for f in a/*.png; do compare -metric AE "$f" "b/$(basename $f)" null: 2>&1; done
```

Then crop and look at every page that differs. A count alone has passed for
"no change" here before, and been wrong.
