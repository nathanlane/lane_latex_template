# LaTeX Testing Framework

A simple, maintainable testing system for the academic paper template.

## Quick Start

Run all tests:
```bash
make test
```

`make test` runs `pytest -q` and then the shell harness, which is what CI
runs. To run one harness on its own:
```bash
python3 -m pytest -q                          # regression tests
bash tests/run-tests.sh                       # shell harness
bash tests/run-tests.sh tests/fixtures/minimal.tex   # one fixture
```

Some pytest regression checks inspect generated PDF text. Install Poppler so
`pdftotext` is available, for example `brew install poppler` on macOS.

`tests/compilation/logs/` is treated as a transient output directory.
Harness logs are useful for local debugging but are ignored by git and are not part
of the verification contract.

## Test Structure

```
tests/
├── compilation/     # Basic compilation tests
├── visual/         # PDF output checks (manual)
└── fixtures/       # Test documents
    ├── minimal.tex      # Minimal valid document
    ├── full-features.tex # Tests all features
    └── edge-cases.tex   # Common problems
```

## For New Users

1. **Before submitting changes**, run `make test` to ensure nothing broke
2. **If tests fail**, inspect the latest generated logs in `tests/compilation/logs/`
3. **Visual checks** are manual - compare PDFs in `tests/visual/output/`

## For Advanced Users

Add new test cases by creating `.tex` files in `tests/fixtures/`. The framework automatically tests all fixtures for:
- Successful compilation
- Bibliography processing
- Cross-reference resolution
- No LaTeX errors or warnings

## Design Philosophy

- **Simple**: One command runs everything
- **Fast**: Parallel compilation when possible
- **Clear**: Obvious pass/fail results
- **Helpful**: Detailed logs for debugging
