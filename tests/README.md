# LaTeX Testing Framework

A simple, maintainable testing system for the academic paper template.

## Quick Start

Run all tests:
```bash
make test
```

Run specific test types:
```bash
make test-compile    # Test LaTeX compilation
make test-quick      # Quick compilation check (no bibliography)
make test-clean      # Test from clean state
```

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
2. **If tests fail**, check the log files in `tests/compilation/logs/`
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