# Troubleshooting Guide

This guide helps resolve common issues when using the East Asia Paper LaTeX template.

## Table of Contents
- [Compilation Errors](#compilation-errors)
- [Warning Messages](#warning-messages)
- [Spacing and Layout Issues](#spacing-and-layout-issues)
- [Font Problems](#font-problems)
- [Bibliography Issues](#bibliography-issues)
- [Quick Fixes](#quick-fixes)

## Compilation Errors

### "Package not found" Error
**Symptom**: `! LaTeX Error: File 'package.sty' not found`

**Solution**:
```bash
# TeX Live / MacTeX
tlmgr install [package-name]

# MiKTeX (Windows)
mpm --install=[package-name]
```

### "Undefined control sequence" Error
**Symptom**: `! Undefined control sequence`

**Common Causes**:
1. Missing package that defines the command
2. Typo in command name
3. Using internal commands (with @) incorrectly

**Solution**:
- Check spelling of the command
- Ensure required packages are loaded
- Don't use internal commands (containing @) in document

## Warning Messages

### Overfull hbox Warnings
**Symptom**: `Overfull \hbox (XXXpt too wide)`

**Solutions**:
1. **For headings**: Use shorter titles or allow hyphenation
   ```latex
   \section{Very Long Title That Causes \\ Overfull Box}
   ```

2. **For tables**: Use smaller font or landscape orientation
   ```latex
   \begin{landscapetable}
     % Wide table content
   \end{landscapetable}
   ```

3. **For URLs**: Allow line breaks
   ```latex
   \url{https://very-long-url.com/that/needs/to/break}
   ```

### Biblatex Warnings

#### "Using fall-back bibtex backend"
**Symptom**: `Package biblatex Warning: Using fall-back bibtex backend`

**Solution**: This is normal when using bibtex backend. To use biber:
```latex
% In preamble.tex, change:
backend=bibtex
% to:
backend=biber
```

Then compile with:
```bash
pdflatex main
biber main
pdflatex main
```

#### "Conflicting options"
**Symptom**: `Package biblatex Warning: Conflicting options`

**Solution**: Already fixed in preamble.tex with `uniquename=init`

### Hyperref Glyph Warnings
**Symptom**: `Package hyperref Warning: Glyph not defined in PU encoding`

**Cause**: Special characters in section headings

**Solutions**:
1. Use `\texorpdfstring` for headings with special characters:
   ```latex
   \section{\texorpdfstring{Title with \LaTeX}{Title with LaTeX}}
   ```

2. Avoid commands that don't translate to PDF bookmarks:
   - Replace `\textsc{...}` with plain text in headings
   - Avoid math mode in section titles

## Spacing and Layout Issues

### Inconsistent Spacing
**Symptom**: Irregular vertical spacing between elements

**Solution**: The template uses a 13.2pt baseline grid. Use grid units:
```latex
\vspace{\gridunit}      % 13.2pt
\vspace{\halfgridunit}  % 6.6pt
\vspace{2\gridunit}     % 26.4pt
```

### Page Breaks in Wrong Places
**Solution**: Use float barriers:
```latex
\FloatBarrier  % Force all floats to appear before this point
```

## Font Problems

### Missing Fonts
**Symptom**: Font substitution warnings

**Solution**: Install TeX Gyre Pagella:
```bash
tlmgr install tex-gyre tex-gyre-math
```

### Small Caps Not Working
**Symptom**: `\textsc` produces regular capitals

**Solution**: TeX Gyre Pagella has true small caps. Ensure T1 encoding:
```latex
\usepackage[T1]{fontenc}  % Already in paperstyle.sty
```

## Bibliography Issues

### Missing Citations
**Symptom**: `[?]` in text instead of citation

**Solutions**:
1. Ensure reference exists in `references.bib`
2. Run full compilation:
   ```bash
   make clean
   make pdf
   ```

### Bibliography Not Appearing
**Solution**: Check that you have:
```latex
\printbibliography  % At end of document
```

## Quick Fixes

### Reset Everything
```bash
make distclean
make pdf
```

### Test Minimal Document
Create `test.tex`:
```latex
\documentclass[11pt]{article}
\usepackage{lltpaperstyle}
\begin{document}
Test
\end{document}
```

Compile with:
```bash
pdflatex test
```

### Disable Problematic Features
In your document preamble:
```latex
% Disable microtype if causing issues
\PassOptionsToPackage{draft}{microtype}

% Use simpler bibliography
\usepackage[style=numeric]{biblatex}
```

### Emergency Fallback
If nothing works, use minimal style:
```latex
\documentclass{article}
% Don't load lltpaperstyle.sty
\begin{document}
Your content
\end{document}
```

## Module-Related Issues

### Module Not Loading
**Symptom**: `! LaTeX Error: File 'lltxxx.sty' not found` (where xxx is a module name)

**Solution**: Ensure all LLT packages are properly installed. The new naming convention uses direct package names:
```bash
# Old path-based loading:
# \usepackage{paper/paperstyle}
# \RequirePackage{paper/modules/colors}

# New direct loading:
\usepackage{lltpaperstyle}
\RequirePackage{lltcolors}
```

### Color Override Not Working
**Symptom**: Custom colors not taking effect

**Solution**: Define colors BEFORE loading lltpaperstyle:
```latex
% Correct order
\definecolor{linknavy}{RGB}{0,0,255}
\usepackage{lltpaperstyle}

% Wrong order (won't work)
\usepackage{lltpaperstyle}
\definecolor{linknavy}{RGB}{0,0,255}
```

### List Spacing Too Tight/Loose
**Symptom**: Lists appear cramped or too spread out

**Solution**: The default is 6.6pt (0.5 grid units). For tighter lists:
```latex
\begin{compactitem}  % 0pt spacing
\item First
\item Second
\end{compactitem}
```

### Grid Alignment Drift
**Symptom**: Text gradually drifts off the baseline grid

**Solution**: Use grid-locked modules for stricter alignment:
```latex
\usepackage{lltheadingsgridlocked}
\usepackage{lltmathematicsgridlocked}
```

Or check grid alignment with:
```latex
\usepackage{lltgridoverlay}
\showgrid  % Shows grid lines
```

## Getting Help

1. **Check the log file**: `main.log` contains detailed error information
2. **Search error messages**: Most LaTeX errors have solutions online
3. **Minimal example**: Create smallest document that shows the problem
4. **File an issue**: Include your minimal example and error message

## Common Error Messages

| Error | Likely Cause | Quick Fix |
|-------|-------------|-----------|
| `Missing $ inserted` | Math mode needed | Wrap in `$...$` |
| `\begin{document} ended by \end{figure}` | Mismatched environments | Check braces |
| `Undefined control sequence` | Unknown command | Check spelling |
| `File ended while scanning` | Missing closing brace | Count `{` and `}` |
| `Missing number` | Command expects number | Check syntax |
| `Package clash` | Incompatible packages | Change load order |

## Prevention Tips

1. **Compile frequently** - Don't wait until you have 20 pages
2. **Use version control** - Git helps track what changed
3. **Keep backups** - Before major changes
4. **Read error messages** - First error is usually the real problem
5. **Comment out sections** - Isolate problems by commenting code