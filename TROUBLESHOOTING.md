# Troubleshooting Guide

This guide helps resolve common issues with the Lane LaTeX Template.
<!-- %% FIX: Keep active troubleshooting tied to verified local package names. -->

## Table of Contents
- [Compilation Errors](#compilation-errors)
- [Font Issues](#font-issues)
- [Bibliography Problems](#bibliography-problems)
- [Spacing and Layout Issues](#spacing-and-layout-issues)
- [Float Problems](#float-problems)
- [Typography Issues](#typography-issues)
- [Package Conflicts](#package-conflicts)
- [Testing and Validation](#testing-and-validation)

## Compilation Errors

### Sudden errors after switching TeX Live versions (e.g. cleveref `\@firstoffive`)

**Symptoms**: Dozens of `Undefined control sequence` / `Paragraph ended before
\@firstoffive` errors in a tree that compiled fine before.

**Cause**: stale `.aux`/`.out` files written by a different TeX Live release
are incompatible across kernel versions.

**Solution**: `latexmk -C main.tex` (or `git clean` of build artifacts), then
rebuild. Always clean when switching between TeX Live years.

### "Package not found" Error

**Symptoms**: LaTeX stops with `! LaTeX Error: File 'package.sty' not found`

**Solutions**:
1. Update your TeX distribution:
   ```bash
   # TeX Live / MacTeX
   tlmgr update --self
   tlmgr update --all
   tlmgr install [package-name]
   
   # MiKTeX
   mpm --update
   mpm --install=[package-name]
   ```

### "Undefined control sequence" Error

**Symptoms**: A command like `\articletitle` is not recognized

**Solutions**:
1. Ensure lanepaper is loaded:
   ```latex
   \input{demo/preamble.tex}  % or
   \usepackage{lanepaper}
   ```

2. Check whether v3 removed it. The v2 grid API (`\gridunit`,
   `\halfgridunit`, `\gridspace`, `\gridincludegraphics`, `gridtable` and
   friends) and the semantic colour commands are gone; state the length or
   colour you want directly. See
   [ADR-0006](docs/adr/0006-one-public-entry-point-and-a-narrow-v3-interface.md).

### Compilation Warnings

**"Token not allowed in PDF string"**
- **Status**: Normal, can be ignored
- **Cause**: Hyperref converting headings to PDF bookmarks
- **Fix**: Use `\texorpdfstring{TeX version}{PDF version}` if needed

**"Overfull hbox" warnings**
- **Solution 1**: Add hyphenation points: `meth\-od\-ology`
- **Solution 2**: Use `\sloppy` environment for problematic paragraphs
- **Solution 3**: Adjust with `\tightpar{text}` or `\riverlesspar{text}`

## Font Issues

### Missing TeX Gyre Pagella

**Symptoms**: Font substitution warnings, incorrect appearance

**Solutions**:
1. Install the font package:
   ```bash
   tlmgr install tex-gyre tex-gyre-math
   ```

2. Manual fallback to Palatino:
   ```latex
   \usepackage{palatino}  % Before lanepaper
   \usepackage{lanepaper}
   ```

### Small Caps Not Working

**Symptoms**: `\textsc{}` produces regular capitals

**Solutions**:
1. Ensure T1 encoding:
   ```latex
   \usepackage[T1]{fontenc}
   ```

2. Use standard small caps:
   ```latex
   \textsc{text}
   ```

### Math Font Mismatches

**Symptoms**: Math looks different from text

**Solution**: Ensure newpxmath is loaded (automatic with lanepaper)

## Bibliography Problems

### Citations Not Found

**Symptoms**: `[?]` appears instead of citations

**Solutions**:
1. Run complete compilation:
   ```bash
   make clean
   make  # or: pdflatex + biber + pdflatex + pdflatex
   ```

2. Check biber vs bibtex:
   ```bash
   biber main  # Default (recommended)
   # or
   bibtex main  # Legacy fallback
   ```

3. Verify .bib file is specified:
   ```latex
   \addbibresource{references.bib}  % biblatex
   ```

### DOI/URL Not Appearing

**Solution**: Ensure bibliography entries have DOI/URL fields:
```bibtex
@article{example2023,
  ...
  doi = {10.1000/journal.2023},
  url = {https://example.com}
}
```

## Spacing and Layout Issues

### Spacing Quantum Misalignment

**Symptoms**: Elements don't align to the 13.2pt spacing quantum

**Solutions**:
Note: body lines sit on the true baseline (16.32pt); the 13.2pt quantum is a
spacing unit, not the baseline, so vertical space and line positions are not
expected to coincide. See
`docs/adr/0004-baseline-grid-is-a-spacing-quantum.md`.

1. Adjust the space directly. The quantum is internal to the package, so a
   document states the gap it wants:
   ```latex
   \vspace{13.2pt}   % One quantum
   \vspace{6.6pt}    % Half a quantum
   ```

### Page Count Inflation

**Symptoms**: Document has unexpectedly many pages

**Causes & Solutions**:
1. **Spacing leaks**: Check for missing grouping in emphasis commands
   ```latex
   {\bsc{text}}  % Correct - grouped
   \bsc{text}    % Wrong - may leak spacing
   ```

2. **Float accumulation**: Flush pending floats before a major section:
   ```latex
   \clearpage
   \section{New Section}
   ```

### Lists Too Tight/Loose

**Solutions**:
1. Use a standard list environment:
   ```latex
   \begin{itemize}
     \item First point
     \item Second point
   \end{itemize}
   ```

2. Custom spacing:
   ```latex
   \setlist[itemize]{itemsep=3.3pt}  % Quarter grid unit
   ```

## Float Problems

### Figures/Tables Drifting Too Far

**Solutions**:
1. Use `\clearpage` before a major section when all pending floats must print
2. Adjust placement options:
   ```latex
   \begin{figure}[tbp]  % Standard
   \begin{figure}[htbp] % Include 'here' option
   ```

### Wide Tables Not Fitting

**Solutions**:
1. Load `pdflscape` in the document and use its standard `landscape`
   environment:
   ```latex
   \begin{landscape}
     \begin{table}[tbp]
       % Wide table content
     \end{table}
   \end{landscape}
   ```

2. Reduce `\tabcolsep` or the table font size locally before scaling content.

The demo defines `landscapetable`, `rotatedtable` and `fittable` for its own
examples. They are not `lanepaper` package APIs.

## Typography Issues

### Bold Text Too Heavy

**Symptoms**: Bold headings appear "shouty"

**Solution**: The template already implements:
- Softened colors for bold headings
- No added letterspacing on bold headings — upstream microtype assigns none
- This is the intended design

### Hyphenation Problems

**Solutions**:
1. Add hyphenation exceptions:
   ```latex
   \hyphenation{meth-od-ology anal-y-sis}
   ```

2. Use paragraph commands:
   ```latex
   \nohyphpar{text}  % Disable hyphenation
   \tightpar{text}   % Tighter spacing
   ```

3. Adjust penalties:
   ```latex
   \hyphenpenalty=10000  % Prevent all hyphenation
   ```

### Small Caps Tracking Issues

**Symptoms**: Small caps appear too tight or loose

**Solution**: Use standard small caps:
```latex
\textsc{small caps text}
```

## Package Conflicts

### Microtype Warnings

**Symptoms**: `Package microtype Info:` lines in the log; occasionally an
"Unknown slot number" warning

**Solution**: Read them rather than silencing them. `lanepaper` loads microtype
with `protrusion`, `expansion`, and `tracking` enabled and no other options, so
every normal build reports its settings:

```text
Package microtype Info: Character protrusion enabled (level 2).
Package microtype Info: Using default protrusion set `alltext'.
Package microtype Info: Automatic font expansion enabled (level 2),
Package microtype Info: Tracking enabled.
Package microtype Info: Using default tracking set `smallcaps'.
```

That is the expected output, not a fault. Microtype uses its shipped Pagella
protrusion table (`mt-ppl.cfg`, reached through microtype's own `qpl` -> `ppl`
alias) and its default expansion. The package adds only +50 tracking for Pagella
small caps.

Because the package authors no font tables of its own, a real microtype warning
now points at a real problem — a missing font, an unexpected encoding, or a
package loaded in the wrong order. "Unknown slot number" in particular means a
protrusion or tracking rule met a font it does not describe; check which font is
selected at that point instead of hiding the message.

Do not add `verbose=silent`. It suppresses the diagnostics above together with
the warning you would want to read.

### Babel Language Warnings

**Symptoms**: "The package option 'english' should not be used"

**Solution**: Remove explicit language option:
```latex
% Wrong:
\usepackage[english]{babel}

% Correct:
\usepackage{babel}  % Language detected automatically
```

### Cleveref Conflicts

The document owns both packages. Load `hyperref` before `cleveref`; `lanepaper`
may be loaded before either and applies its link styling when `hyperref` loads.

## Testing and Validation

### Running Tests

```bash
# Full test suite: pytest, then the shell harness
make test

# One fixture
./tests/run-tests.sh tests/fixtures/minimal.tex

# With verbose output
VERBOSE=1 ./tests/run-tests.sh
```

### Common Test Failures

**"Page count mismatch"**
- Expected: ~30 pages for comprehensive test
- If >50 pages: Check for spacing leaks
- If <20 pages: Check if content is missing

**"Undefined citations"**
- Ensure test fixture has matching .bib file
- Run biber on test file

**"Missing packages"**
- Install required packages
- Or use minimal test fixture

### Style Validation

```bash
# chktex, then the math-spacing checker
make lint

# Count overfull and underfull boxes in the last build
grep -c 'Overfull \\hbox' main.log
grep -c 'Underfull \\hbox' main.log
```

## Getting Help

1. **Check the log file**: `main.log` contains detailed error information
2. **Search TeX Stack Exchange**: Most LaTeX issues have solutions
3. **Review test output**: `tests/compilation/logs/` for test failures
4. **File an issue**: Include minimal working example (MWE)

## Quick Fixes Reference

| Problem | Quick Fix |
|---------|-----------|
| Missing package | `tlmgr install [package]` |
| Bad citations | `make clean && make` |
| Float drift | Use `[tbp]`; use `\clearpage` before a major section if needed |
| Overfull hbox | Add `\sloppy` or hyphenation |
| Grid misalignment | Use `\vspace{13.2pt}` |
| Font missing | `tlmgr install tex-gyre` |
| Page inflation | Check emphasis grouping |

## Minimal Reproduction

If nothing else works, reduce to the smallest failing document:
```latex
\documentclass[11pt]{article}
\usepackage{lanepaper}
\begin{document}
Your content here
\end{document}
```

`\usepackage{lanepaper}` is the only supported load path (ADR-0006); the
`lnp*.sty` modules are internal and loading one directly is unsupported.
