# Troubleshooting Guide

This guide helps resolve common issues with the Lane LaTeX Template.

## Table of Contents
- [Compilation Errors](#compilation-errors)
- [Font Issues](#font-issues)
- [Bibliography Problems](#bibliography-problems)
- [Spacing and Layout Issues](#spacing-and-layout-issues)
- [Float Problems](#float-problems)
- [Typography Issues](#typography-issues)
- [Package Conflicts](#package-conflicts)
- [Overleaf-Specific Issues](#overleaf-specific-issues)
- [Testing and Validation](#testing-and-validation)

## Compilation Errors

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

2. For Overleaf: The package might not be available. Use compatibility mode:
   ```latex
   \usepackage[compat]{paper/paperstyle}
   ```

### "Undefined control sequence" Error

**Symptoms**: Commands like `\articletitle` or `\gridunit` not recognized

**Solutions**:
1. Ensure paperstyle is loaded:
   ```latex
   \input{paper/preamble.tex}  % or
   \usepackage{paper/paperstyle}
   ```

2. Check module loading order - some commands require specific modules:
   ```latex
   \usepackage{paper/modules/dimensions}  % For \gridunit
   ```

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

2. Use font fallback module:
   ```latex
   \usepackage{paper/modules/font-fallbacks}
   \enablecompatibilitymode
   ```

3. Manual fallback to Palatino:
   ```latex
   \usepackage{palatino}  % Before paperstyle
   \usepackage{paper/paperstyle}
   ```

### Small Caps Not Working

**Symptoms**: `\textsc{}` produces regular capitals

**Solutions**:
1. Ensure T1 encoding:
   ```latex
   \usepackage[T1]{fontenc}
   ```

2. Use the refined small caps commands:
   ```latex
   \refinedsc{text}      % Regular small caps
   \refinedscbold{text}  % Bold small caps
   ```

### Math Font Mismatches

**Symptoms**: Math looks different from text

**Solution**: Ensure newpxmath is loaded (automatic with paperstyle)

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

### Baseline Grid Misalignment

**Symptoms**: Elements don't align to 13.2pt grid

**Solutions**:
1. Use grid visualization:
   ```latex
   \usepackage{paper/gridoverlay}
   \showgrid
   ```

2. Use grid-locked modules for stricter alignment:
   ```latex
   \usepackage{paper/modules/headings-gridlocked}
   \usepackage{paper/modules/mathematics-gridlocked}
   ```

3. Manual adjustment with grid units:
   ```latex
   \vspace{\gridunit}      % 13.2pt
   \vspace{\halfgridunit}  % 6.6pt
   ```

### Page Count Inflation

**Symptoms**: Document has unexpectedly many pages

**Causes & Solutions**:
1. **Spacing leaks**: Check for missing grouping in emphasis commands
   ```latex
   {\bsc{text}}  % Correct - grouped
   \bsc{text}    % Wrong - may leak spacing
   ```

2. **Float accumulation**: Add barriers before sections:
   ```latex
   \FloatBarrier
   \section{New Section}
   ```

### Lists Too Tight/Loose

**Solutions**:
1. Use appropriate list environment:
   ```latex
   \begin{itemize}      % Standard with 6.6pt spacing
   \begin{compactitem}  % No spacing between items
   \begin{displayitem}  % Generous spacing
   ```

2. Custom spacing:
   ```latex
   \setlist[itemize]{itemsep=3.3pt}  % Quarter grid unit
   ```

## Float Problems

### Figures/Tables Drifting Too Far

**Solutions**:
1. Use `\FloatBarrier` before new sections
2. Adjust placement options:
   ```latex
   \begin{figure}[tbp]  % Standard
   \begin{figure}[htbp] % Include 'here' option
   ```
3. Use specialized commands:
   ```latex
   \tryherefigure{...}    % Attempts here placement
   \forceherefigure{...}  % Forces here placement
   ```

### Wide Tables Not Fitting

**Solutions**:
1. Use landscape environment:
   ```latex
   \begin{landscapetable}[tbp]
     % Wide table content
   \end{landscapetable}
   ```

2. Use adjustable tables:
   ```latex
   \begin{fittable}[tbp]{1.2\textwidth}
     % Auto-scaled content
   \end{fittable}
   ```

3. Rotate single tables:
   ```latex
   \begin{rotatedtable}[tbp]
     % 90-degree rotation
   \end{rotatedtable}
   ```

## Typography Issues

### Bold Text Too Heavy

**Symptoms**: Bold headings appear "shouty"

**Solution**: The template already implements:
- Softened colors for bold headings
- Generous tracking (6-8%)
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

**Solution**: Use size-specific commands:
```latex
\textsc{body text}      % 3% tracking
\titlesc{title text}    % 8-12% tracking
\refinedscbold{bold}    % 4.5% tracking
```

## Package Conflicts

### Microtype Warnings

**Symptoms**: "Unknown slot number" warnings

**Solution**: These are harmless and can be ignored. To suppress:
```latex
\usepackage[verbose=silent]{microtype}
```

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

**Solution**: Load cleveref last:
```latex
\usepackage{paper/paperstyle}
% ... other packages ...
\usepackage{cleveref}  % Must be near end
\usepackage{hyperref}  % Must be last
```

## Overleaf-Specific Issues

### "Incomplete \iffalse" Error

**Symptoms**: Overleaf compilation fails with:
```
! Incomplete \iffalse; all text was ignored after line 20.
```

**Cause**: Overleaf's LaTeX environment handles catcodes and package initialization differently than local installations.

**Status**: **Under investigation** - Works locally but fails on Overleaf

**Solution**:
Use the Overleaf-compatible version:

```latex
\documentclass{article}
\input{paper/preamble-overleaf.tex}
\begin{document}
Your content here
\end{document}
```

**Alternative**: Load the style directly:
```latex
\usepackage{paper/paperstyle-overleaf}
```

**Benefits of Overleaf version**:
- No @ symbols in user-facing code
- Simplified internal mechanisms  
- Maintains core typography features
- Reliable on all cloud platforms

**See OVERLEAF_COMPATIBILITY.md** for detailed information

**Technical Details**: 
- Overleaf renames files to `output.tex` internally
- Stricter catcode handling for `@` symbols
- Different package expansion timing
- Issue occurs at `\begin{document}` during initialization

### Compilation Timeout

**Solutions**:
1. Use draft mode for editing:
   ```latex
   \documentclass[draft]{article}
   ```

2. Disable microtype temporarily:
   ```latex
   \usepackage[draft]{microtype}
   ```

3. Use quick compilation:
   - Menu → Recompile → Fast [draft]

### Font Not Available

**Solution**: Overleaf has all fonts, but ensure:
```latex
\usepackage[T1]{fontenc}  % Before fonts
```

## Testing and Validation

### Running Tests

```bash
# Quick validation
make test-quick

# Full test suite  
make test

# Specific test
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
# Check for common issues
make validate

# Analyze warnings
make warnings

# Show diagnostics
make diagnose
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
| Float drift | Add `\FloatBarrier` |
| Overfull hbox | Add `\sloppy` or hyphenation |
| Grid misalignment | Use `\vspace{\gridunit}` |
| Font missing | Use fallback module |
| Compilation slow | Use draft mode |
| Page inflation | Check emphasis grouping |

## Emergency Minimal Mode

If nothing else works:
```latex
\documentclass{article}
\usepackage{paper/paperstyle-minimal}
\begin{document}
Your content here
\end{document}
```

This loads only essential features with maximum compatibility.