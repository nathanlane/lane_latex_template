# Testing and Quality Assurance Guide

This document provides comprehensive documentation for the testing, validation, and debugging infrastructure in the East Asian Miracle Paper project.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Testing Framework](#testing-framework)
3. [Enhanced Error Detection](#enhanced-error-detection)
4. [Style Validation](#style-validation)
5. [Log Analysis Tools](#log-analysis-tools)
6. [Visual Debugging](#visual-debugging)
7. [Continuous Integration](#continuous-integration)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Adding New Tests](#adding-new-tests)

## Quick Start

Run these commands to test your setup:

```bash
# Run all tests
make test

# Quick compilation test
make test-quick

# Validate LaTeX style compliance
make validate

# Test from clean state
make test-clean

# View test results
ls tests/compilation/*.pdf
```

## Testing Framework

### Overview

The project includes a sophisticated bash-based testing framework located in `/tests/` that ensures document compilation, validates features, and catches common errors.

### Directory Structure

```
tests/
├── README.md                    # Quick testing guide
├── TESTING_SUMMARY.md          # Detailed framework documentation
├── run-tests.sh                # Main test runner script
├── fixtures/                   # Test documents
│   ├── minimal.tex            # Basic compilation test
│   ├── full-features.tex      # Comprehensive feature test
│   └── edge-cases.tex         # Edge case and error handling
└── compilation/               # Test outputs
    ├── logs/                  # Compilation logs
    └── *.pdf                  # Generated PDFs for inspection
```

### Test Fixtures

#### 1. **Minimal Test** (`minimal.tex`)
Tests basic document compilation with core features:
- Document class loading
- Custom style package (`paperstyle.sty`)
- Basic sections and paragraphs
- Bibliography integration
- **Purpose**: Quick smoke test to ensure basic functionality
- **Runtime**: ~2 seconds
- **Use case**: Fast feedback during development

#### 2. **Full Features Test** (`full-features.tex`)
Comprehensive test of all typography features:
- Complete heading hierarchy (section through paragraph)
- Emphasis hierarchy (all four levels)
- Mathematical typography with custom commands
- Code typography with all variants
- Lists (all 7 variants: itemize, academicitem, compactitem, displayitem, inlineitem, enumerate, description)
- Tables (booktabs, gridtable, regressiontable, compacttable)
- Figures with grid alignment
- Footnotes with proper spacing
- Citations (textcite, autocite, multiple citations)
- Block quotations and display quotes
- Page numbering styles
- Title page elements
- **Purpose**: Validate all typography features work correctly
- **Runtime**: ~5 seconds
- **Use case**: Pre-commit validation, feature testing

#### 3. **Edge Cases Test** (`edge-cases.tex`)
Tests problematic scenarios:
- Widow/orphan control with forced bad breaks
- Long URLs and line breaking behavior
- Nested emphasis (up to 4 levels)
- Float placement edge cases (multiple consecutive floats)
- Bibliography edge cases (missing citations, malformed entries)
- Special characters and Unicode support
- Deeply nested lists (4+ levels)
- Mixed list types
- Overfull/underfull box scenarios
- **Purpose**: Catch edge cases that break in real documents
- **Runtime**: ~4 seconds
- **Use case**: Regression testing, debugging

### Test Fixture Best Practices

1. **Keep fixtures focused**: Each fixture should test a specific aspect
2. **Include comments**: Document what each section tests
3. **Use meaningful content**: Real-looking text helps spot visual issues
4. **Test both success and failure**: Include cases that should generate warnings
5. **Maintain fixtures**: Update when features change

### Running Tests

#### Basic Test Execution
```bash
# Run all tests with detailed output
./tests/run-tests.sh

# Run specific test
./tests/run-tests.sh minimal

# Run with verbose output
VERBOSE=1 ./tests/run-tests.sh
```

#### Makefile Targets
```bash
make test          # Run complete test suite
make test-quick    # Run minimal test only
make test-compile  # Test LaTeX compilation
make test-clean    # Test from clean state (removes aux files first)
```

### Test Output

The test runner provides color-coded output:
- ✅ Green checkmarks for passed tests
- ❌ Red X marks for failed tests
- 🔍 Detailed error messages with context
- 📊 Summary statistics at the end

Test artifacts are saved in `tests/compilation/`:
- PDF files for visual inspection
- Log files for debugging
- Auxiliary files for analysis

### Test Script Architecture

The `run-tests.sh` script implements a robust testing framework:

```bash
# Core functions
run_latex_test()     # Main test execution function
check_warnings()     # Advanced warning detection
extract_errors()     # Error extraction with context
print_summary()      # Results summary

# Configuration
LOG_DIR="tests/compilation/logs"
OUTPUT_DIR="tests/compilation"
VERBOSE=${VERBOSE:-0}
```

## Enhanced Error Detection

### Overview

The testing framework includes sophisticated error detection capabilities that go beyond simple compilation checking. It identifies and categorizes various types of issues that can occur in LaTeX documents.

### Error Categories

#### 1. **Critical Errors**
These prevent document compilation:
```
- Undefined control sequences
- Missing packages
- Syntax errors in LaTeX commands
- Missing required files
- Invalid document structure
```

#### 2. **Bibliography Errors**
Issues with citations and references:
```
- Missing citations (e.g., "Citation 'undefined' on page 1 undefined")
- Incomplete bibliography entries
- Biber/BibTeX processing failures
- Missing .bib files
- Malformed BibTeX entries
```

#### 3. **Cross-Reference Errors**
Problems with internal document references:
```
- Undefined references (e.g., "Reference 'fig:missing' on page 2 undefined")
- Duplicate labels
- Missing \label commands
- Circular references
```

#### 4. **Typography Warnings**
Issues affecting document appearance:
```
- Overfull hboxes (text extending into margins)
- Underfull hboxes (excessive spacing)
- Font substitutions
- Missing glyphs
- Encoding problems
```

#### 5. **Float Placement Issues**
Problems with figures and tables:
```
- "Too many unprocessed floats"
- Float placement conflicts
- Missing float captions
- Oversized floats
```

### Enhanced Warning Detection

The framework implements intelligent warning filtering to distinguish between harmless and problematic warnings:

#### Filtered (Harmless) Warnings:
```bash
# These are safely ignored:
- "Token not allowed in a PDF string" (hyperref)
- "Fandol font warnings" (font substitution)
- "Empty bibliography" (when intentional)
- "Marginpar on page X moved" (normal behavior)
```

#### Critical Warnings:
```bash
# These require attention:
- Missing references
- Undefined citations  
- Float placement failures
- Font loading errors
- Package conflicts
```

### Error Detection Implementation

The `check_warnings()` function in `run-tests.sh` implements sophisticated pattern matching:

```bash
check_warnings() {
    local log_file="$1"
    local has_warnings=0
    
    # Check for critical LaTeX errors
    if grep -q "! LaTeX Error:" "$log_file"; then
        echo "  ❌ LaTeX errors detected:"
        grep "! LaTeX Error:" "$log_file" | head -5
        has_warnings=1
    fi
    
    # Check for undefined references
    if grep -q "Reference.*undefined" "$log_file"; then
        echo "  ⚠️  Undefined references detected:"
        grep "Reference.*undefined" "$log_file" | sort | uniq | head -5
        has_warnings=1
    fi
    
    # Check for missing citations
    if grep -q "Citation.*undefined" "$log_file"; then
        echo "  ⚠️  Undefined citations detected:"
        grep "Citation.*undefined" "$log_file" | sort | uniq | head -5
        has_warnings=1
    fi
    
    # Check for overfull hboxes (with threshold)
    local overfull_count=$(grep -c "Overfull.*hbox" "$log_file" || true)
    if [ "$overfull_count" -gt 0 ]; then
        echo "  ⚠️  Overfull hboxes detected: $overfull_count instances"
        if [ "$VERBOSE" -eq 1 ]; then
            grep "Overfull.*hbox" "$log_file" | head -3
        fi
        has_warnings=1
    fi
    
    # Advanced pattern detection for other issues...
}
```

### Context-Aware Error Reporting

The framework provides contextual information for errors:

```bash
extract_errors() {
    local log_file="$1"
    echo "Extracting detailed error information from $log_file..."
    
    # Extract error with 5 lines of context
    grep -A 5 -B 5 "! LaTeX Error:" "$log_file" || true
    
    # Show line numbers for undefined references
    grep -n "undefined" "$log_file" | head -10 || true
    
    # Display error summary
    echo "Error summary:"
    grep -E "^!" "$log_file" | sort | uniq -c || true
}
```

### Real-World Error Examples

#### Example 1: Missing Citation
```
LaTeX Warning: Citation 'smith2023' on page 5 undefined on input line 234.

Context: The citation database may be missing this entry, or biber failed to process.
Fix: Add the citation to references.bib or check biber compilation.
```

#### Example 2: Overfull Hbox
```
Overfull \hbox (15.34pt too wide) in paragraph at lines 156--158

Context: Text extends beyond the margin, often due to long unbreakable content.
Fix: Add hyphenation points, use \sloppy, or rewrite the problematic text.
```

#### Example 3: Float Placement
```
LaTeX Warning: 'h' float specifier changed to 'ht'.
LaTeX Warning: Float too large for page by 73.2pt on input line 89.

Context: The figure/table is too large for the requested position.
Fix: Resize the content or use different placement options [tbp].
```

## Style Validation

### LaTeX Style Compliance

The project includes an automated style validator that enforces typography best practices and LaTeX conventions.

#### Running Style Validation
```bash
# Validate all LaTeX files
make validate

# Run validator directly
./src/sh/validate_latex_style.sh

# Validate specific file
./src/sh/validate_latex_style.sh main.tex
```

#### Validation Checks

1. **Formatting Standards**
   - ✓ One sentence per line
   - ✓ Proper indentation (2 spaces)
   - ✓ No trailing whitespace
   - ✓ Consistent spacing

2. **Typography Conventions**
   - ✓ `\emph{}` for emphasis (not `\textit{}`)
   - ✓ Smart quotes via `\enquote{}`
   - ✓ Non-breaking spaces before citations (`~\cite{}`)
   - ✓ Non-breaking spaces before references (`Figure~\ref{}`)

3. **Labeling Conventions**
   ```
   Prefix    | Usage
   ----------|------------------
   sec:      | Sections
   subsec:   | Subsections  
   fig:      | Figures
   tab:      | Tables
   eq:       | Equations
   app:      | Appendices
   ```

4. **Math Typography**
   - ✓ Spaces around operators (`x = y + z`)
   - ✓ Proper delimiter sizing
   - ✓ Consistent notation

5. **Bibliography Validation**
   - ✓ Complete entry fields
   - ✓ Consistent formatting
   - ✓ Valid BibTeX syntax

### Python Code Validation

Python scripts are automatically formatted and checked:

```bash
# Format Python code with black
make format-python

# Check Python style
black --check src/py/
```

## Log Analysis Tools

### Advanced Log Parser

The project includes a sophisticated log parsing system for analyzing LaTeX compilation output.

#### Location
```
context/tools/log-parsing/
├── parse_latex_logs.py      # Python log analyzer
├── check_latex_logs.sh      # Bash wrapper
└── LOG_PARSER_README.md     # Documentation
```

#### Features

1. **Multi-format Support**
   - LaTeX logs (`.log`)
   - Biber logs (`.blg`)
   - Auxiliary files

2. **Issue Categorization**
   - **ERRORS**: Compilation failures
   - **WARNINGS**: Potential issues
   - **OVERFULL**: Overfull hboxes/vboxes
   - **UNDERFULL**: Underfull hboxes/vboxes
   - **INFO**: Informational messages

3. **Smart Filtering**
   - Suppresses harmless warnings
   - Highlights critical issues
   - Provides context for errors

#### Usage

```bash
# Analyze main compilation log
python context/tools/log-parsing/parse_latex_logs.py main.log

# Quick check with wrapper
./context/tools/log-parsing/check_latex_logs.sh

# Summary mode (errors only)
python context/tools/log-parsing/parse_latex_logs.py main.log --summary

# Ignore box warnings
python context/tools/log-parsing/parse_latex_logs.py main.log --no-boxes

# Parse biber log
python context/tools/log-parsing/parse_latex_logs.py main.blg
```

#### Output Examples

```
=== LaTeX Log Analysis ===
File: main.log
Total Issues: 3

ERRORS (1):
  Line 1234: Undefined control sequence \unknowncmd
  Context: "This is \unknowncmd{text} that fails"
  
WARNINGS (2):
  Line 567: Underfull \hbox (badness 10000)
  Line 890: Package hyperref Warning: Token not allowed
  
Summary: 1 error, 2 warnings, 0 overfull, 0 underfull
```

### Automated Error Detection

The test framework automatically detects and reports:
- Compilation failures
- Missing references
- Undefined citations
- Font warnings
- Package conflicts

## Visual Debugging

### Grid Overlay System

The project includes a sophisticated grid overlay system for debugging baseline grid alignment.

#### Loading the Grid System
```latex
% Add to preamble
\usepackage{paper/gridoverlay}

% Or in document
\input{paper/gridoverlay.sty}
```

#### Basic Commands

```latex
% Show grid overlay
\showgrid

% Hide grid overlay  
\hidegrid

% Toggle grid
\togglegrid

% Mark current position
\markposition{label}

% Check alignment
\checkgrid
```

#### Grid Visualization Features

1. **Multi-level Grid Lines**
   - Red lines: Primary 13.2pt grid
   - Blue lines: Secondary grid (2 units)
   - Green lines: Tertiary grid (3 units)
   - Gray lines: Quarter units

2. **Margin Indicators**
   - Dashed lines showing margins
   - Text area boundaries
   - Header/footer regions

3. **Position Information**
   - Current vertical position
   - Distance to next gridline
   - Page dimensions
   - Grid unit counter

#### Advanced Debugging

```latex
% Debug specific element
\begin{gridcheck}
  \section{Test Section}
  This content will show grid alignment
\end{gridcheck}

% Show spacing analysis
\gridanalysis{
  Some content to analyze
}

% Measure vertical space
\measurespace
```

### Typography Debugging

```latex
% Show font information
\fontinfo

% Display current type size
\showfontsize

% Check emphasis hierarchy
\emphtest

% Test small caps tracking
\trackingtest
```

## Continuous Integration

While the project doesn't include CI configuration files, it's designed for easy integration:

### GitHub Actions Example

```yaml
name: LaTeX Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: LaTeX Setup
      uses: xu-cheng/latex-action@v2
      with:
        root_file: main.tex
        latexmk_use_xelatex: true
        
    - name: Run Tests
      run: make test
      
    - name: Validate Style
      run: make validate
      
    - name: Upload PDFs
      uses: actions/upload-artifact@v2
      with:
        name: test-pdfs
        path: tests/compilation/*.pdf
```

### Exit Codes

All test scripts provide proper exit codes:
- `0`: All tests passed
- `1`: Compilation failure
- `2`: Style validation failure
- `3`: Critical errors found

## Best Practices

### 1. **Regular Testing**
```bash
# Before commits
make test-quick
make validate

# Before pull requests  
make test-clean
```

### 2. **Debug Workflow**
```latex
% When debugging alignment
\usepackage{paper/gridoverlay}
\showgrid

% When debugging spacing
\the\baselineskip
\the\parskip
```

### 3. **Log Analysis**
```bash
# After compilation issues
python context/tools/log-parsing/parse_latex_logs.py main.log

# Check for warnings
grep -i "warning" main.log
```

### 4. **Visual Inspection**
Always review generated PDFs:
- Check alignment visually
- Verify typography features
- Test page breaks
- Confirm float placement

## Troubleshooting

### Common Issues

#### 1. **Test Failures**
```bash
# Check specific log
cat tests/compilation/logs/minimal.log

# Run with verbose mode
VERBOSE=1 ./tests/run-tests.sh
```

#### 2. **Style Violations**
```bash
# See detailed report
./src/sh/validate_latex_style.sh main.tex | less

# Fix automatically (where possible)
make format-python
```

#### 3. **Grid Misalignment**
```latex
% Enable grid to see issues
\showgrid

% Check specific elements
\checkgrid
This paragraph should align
\checkgrid
```

#### 4. **Compilation Warnings**
```bash
# Filter harmful warnings
python context/tools/log-parsing/parse_latex_logs.py main.log --no-boxes

# See only errors
python context/tools/log-parsing/parse_latex_logs.py main.log --critical
```

### Getting Help

1. Check test output carefully - error messages are descriptive
2. Review `tests/compilation/logs/` for detailed information
3. Use visual debugging tools to identify issues
4. Run style validator for quick fixes

## Contributing

When adding new features:

1. **Add Test Cases**
   - Update `full-features.tex` with new features
   - Add edge cases to `edge-cases.tex`
   - Create specific test if needed

2. **Update Validation**
   - Add new style rules to validator
   - Document new conventions

3. **Document Changes**
   - Update this guide
   - Add examples to test fixtures
   - Update README.md

## Adding New Tests

### Creating a New Test Fixture

To add a new test case, create a `.tex` file in `tests/fixtures/`:

```latex
% tests/fixtures/my-feature-test.tex
\documentclass[11pt,letterpaper]{article}
\input{paper/preamble.tex}

\begin{document}

% Test your specific feature here
\section{Testing My New Feature}

Your test content...

\end{document}
```

### Registering the Test

The test runner automatically discovers all `.tex` files in the fixtures directory. Simply place your file there and it will be included in the test suite.

### Test Naming Conventions

Follow these naming patterns:
- `feature-name.tex` - For testing a specific feature
- `issue-123.tex` - For regression tests tied to issues
- `integration-xyz.tex` - For integration tests
- `performance-abc.tex` - For performance tests

### Writing Effective Tests

#### 1. **Minimal Reproducible Examples**
```latex
% Good: Tests one specific feature
\section{Test Bold Small Caps}
\bsc{This Should Be Bold Small Caps}

% Bad: Tests multiple unrelated features
\section{Test Everything}
\bsc{Bold small caps} and \emph{emphasis} and $\mathbb{R}$...
```

#### 2. **Include Edge Cases**
```latex
% Test boundary conditions
\begin{itemize}
  \item Regular item
  \begin{itemize}
    \item Nested item
    \begin{itemize}
      \item Deeply nested item
      \begin{itemize}
        \item Maximum nesting level
      \end{itemize}
    \end{itemize}
  \end{itemize}
\end{itemize}
```

#### 3. **Document Expected Behavior**
```latex
% This should produce a 13.2pt indent (exactly 1 grid unit)
\noindent This paragraph has no indent.

This paragraph should have standard classical indent.
```

#### 4. **Test Error Conditions**
```latex
% This citation should trigger a warning
See \cite{nonexistent2023} for details.

% This reference should be undefined
As shown in Figure~\ref{fig:missing}.
```

### Advanced Test Features

#### Custom Test Configuration

Create a test with specific compilation requirements:

```bash
# tests/fixtures/special-test.tex.config
LATEX_ENGINE=xelatex
COMPILE_TIMES=4
BIBER_REQUIRED=true
EXPECTED_WARNINGS=2
```

#### Performance Testing

```latex
% tests/fixtures/performance-floats.tex
% Generate many floats to test placement algorithms
\foreach \n in {1,...,50} {
  \begin{figure}[tbp]
    \centering
    \rule{0.8\textwidth}{3cm}
    \caption{Test Figure \n}
  \end{figure}
}
```

#### Visual Regression Testing

```latex
% tests/fixtures/visual-grid-alignment.tex
\usepackage{paper/gridoverlay}
\showgrid

% Content that must maintain precise alignment
\section{Grid Alignment Test}
This text must align to the baseline grid.
```

### Test Documentation

Each test should include a header comment:

```latex
% Test: Feature Name
% Purpose: What this test validates
% Expected: What should happen
% Author: Your name
% Date: 2025-07-01
% Related: Issue #123, PR #456
```

### Debugging Test Failures

When a test fails:

1. **Check the log file**:
   ```bash
   cat tests/compilation/logs/my-feature-test.log
   ```

2. **Run in verbose mode**:
   ```bash
   VERBOSE=1 ./tests/run-tests.sh my-feature-test
   ```

3. **Examine the PDF output**:
   ```bash
   open tests/compilation/my-feature-test.pdf
   ```

4. **Compare with expected output**:
   ```bash
   diff tests/expected/my-feature-test.pdf tests/compilation/my-feature-test.pdf
   ```

### Test Maintenance

#### Regular Tasks
- Review and update tests when features change
- Remove obsolete tests
- Consolidate similar tests
- Update test documentation

#### Test Coverage Goals
- Each typography feature should have a test
- Each custom command should be tested
- Common error conditions should be covered
- Edge cases should be documented

---

For more information, see:
- `/tests/README.md` - Quick testing guide
- `/tests/TESTING_SUMMARY.md` - Framework details
- `/context/tools/log-parsing/LOG_PARSER_README.md` - Log parser docs
- `/tests/run-tests.sh` - Test runner implementation