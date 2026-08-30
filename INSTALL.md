# Installation Guide for Lane LaTeX Template

This guide will help you set up the LaTeX template on your system with all required dependencies.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Required LaTeX Packages](#required-latex-packages)
- [Troubleshooting](#troubleshooting)
- [Minimal Installation](#minimal-installation)

## Prerequisites

### Required Software

**The engine is pdfLaTeX only.** XeLaTeX and LuaLaTeX are not supported: the
font stack is 8-bit and pdfTeX-shaped, with no `fontspec` path, and `microtype`
font expansion is unsupported on XeTeX. Loading `lanepaper` under either
engine stops the run with an explicit error rather than a cascade of font
failures.

1. **TeX Distribution** (one of the following). The LaTeX format must be
   **2020-10-01 or newer**; the package uses `\AddToHook` and declares that
   floor with `\NeedsTeXFormat`:
   - TeX Live 2020 or newer (recommended)
   - MiKTeX 2020 or newer
   - MacTeX 2020 or newer (macOS)

2. **Build Tools**:
   - GNU Make
   - Python 3.8+ (for pytest regression tests)
   - Git (for version control)

3. **PDF Viewer**:
   - Any PDF viewer that auto-refreshes (e.g., Skim on macOS, SumatraPDF on Windows)

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd lane_latex_template
   ```

2. **Review the required package list** in
   [Required LaTeX Packages](#required-latex-packages) below.

> **Overleaf note (unverified):** the template resolves its modules via
> `TEXINPUTS` set in `.latexmkrc` (`./lanepaper`). We could not
> verify whether Overleaf honours `ensure_path('TEXINPUTS', ...)` from
> `.latexmkrc`. If `\usepackage{lanepaper}` fails to find `lnpfonts` and
> friends there, copy `lanepaper/*.sty` into the project
> root as a workaround. Local `latexmk` is the verified path.

3. **Install missing packages** (if any):
   ```bash
   # TeX Live / MacTeX
   tlmgr install <package-name>
   
   # MiKTeX
   mpm --install=<package-name>
   ```

4. **Build the paper**:
   ```bash
   make build
   ```

5. **Run the tests**:
   ```bash
   make test
   ```

## Platform-Specific Instructions

### macOS

1. **Install MacTeX**:
   ```bash
   brew install --cask mactex
   ```

2. **Install build tools**:
   ```bash
   brew install make python git
   ```

### Linux (Ubuntu/Debian)

1. **Install TeX Live**:
   ```bash
   sudo apt-get update
   sudo apt-get install texlive-full
   ```

2. **Install build tools**:
   ```bash
   sudo apt-get install make python3 python3-pip git
   ```

### Windows

1. **Install MiKTeX**:
   - Download from: https://miktex.org/download
   - Choose "Install for all users"
   - Enable "Install packages on-the-fly"

2. **Install Git Bash**:
   - Download from: https://git-scm.com/download/win
   - This provides Unix-like tools including `make`

3. **Install Python**:
   - Download from: https://www.python.org/downloads/
   - Check "Add Python to PATH" during installation

## Required LaTeX Packages

### Core Typography Packages
```bash
# Font packages
tlmgr install tex-gyre tex-gyre-math  # TeX Gyre Pagella and math support
tlmgr install inconsolata             # Monospace font (zi4 package)
tlmgr install newpx                   # newpxmath for mathematics
tlmgr install mathalpha               # Enhanced mathematical symbols
tlmgr install boondox                 # Blackboard, calligraphic, and Fraktur fonts
tlmgr install textcomp                # Additional text symbols

# Typography enhancement
tlmgr install microtype               # Character protrusion, font expansion
tlmgr install fnpct                   # Footnote punctuation management
```

### Essential Packages
```bash
# Document structure
tlmgr install geometry           # Page layout
tlmgr install fancyhdr          # Headers and footers
tlmgr install titlesec         # Section formatting
tlmgr install titletoc         # Table of contents control

# Graphics and tables
tlmgr install graphicx          # Graphics inclusion
tlmgr install booktabs          # Professional tables
tlmgr install tabularx         # Flexible tables
tlmgr install longtable        # Multi-page tables
tlmgr install ltcaption        # Caption support for longtable
tlmgr install adjustbox        # Box adjustments
tlmgr install array            # Enhanced arrays and tables
tlmgr install multirow         # Multi-row cells in tables

# Bibliography
tlmgr install biblatex          # Modern bibliography
tlmgr install biber            # Bibliography backend
tlmgr install biblatex-chicago  # Chicago style (optional)

# Utilities
tlmgr install xcolor           # Color support
tlmgr install hyperref         # Hyperlinks
tlmgr install cleveref         # Smart references
tlmgr install csquotes         # Demo bibliography quotation support
tlmgr install enumitem         # List customization
tlmgr install caption          # Caption customization
tlmgr install subcaption       # Subfigures and subtables

# Float and rotation support
tlmgr install rotating         # Rotation support
tlmgr install pdflscape        # PDF landscape pages
tlmgr install afterpage        # Execute after page break
```

### Install All Required Packages at Once

**TeX Live / MacTeX**:
```bash
# Core collections
tlmgr install collection-latexrecommended collection-fontsrecommended \
  collection-bibtexextra collection-mathscience

# Individual packages
tlmgr install tex-gyre tex-gyre-math inconsolata newpx mathalpha boondox \
  microtype fnpct textcomp \
  geometry fancyhdr titlesec titletoc \
  graphicx booktabs tabularx longtable ltcaption adjustbox array multirow \
  biblatex biber xcolor hyperref cleveref csquotes enumitem \
  caption subcaption rotating pdflscape afterpage \
  amsmath amssymb mathtools etoolbox xstring ifthen
```

**MiKTeX** (automatic installation):
MiKTeX will automatically install packages when first used. To pre-install:
```bash
mpm --install=collection-latexrecommended
mpm --install=tgpagella
# ... etc
```

## Troubleshooting

### Common Issues and Solutions

1. **"Package not found" error**:
   ```bash
   # Update package database
   tlmgr update --self
   tlmgr update --all
   
   # Then install the missing package
   tlmgr install <package-name>
   ```

2. **"make: command not found" (Windows)**:
   - Use Git Bash instead of Command Prompt
   - Or install Make for Windows: http://gnuwin32.sourceforge.net/packages/make.htm

3. **Bibliography not updating**:
   ```bash
   # Clean and rebuild
   make clean
   make build
   ```

4. **Font-related warnings**:
   ```bash
   # Update font maps
   updmap-sys
   
   # If permission denied:
   sudo updmap-sys
   ```

5. **"Overfull hbox" warnings**:
   - These are usually minor spacing issues
   - Check the log file for specific line numbers
   - Consider using `\sloppy` for problematic paragraphs

### Checking for Problems

Compile a minimal package probe:
```bash
pdflatex -interaction=nonstopmode probe.tex
```

### Getting Help

1. Check the log file: `main.log`
2. Look for specific error messages
3. Search the [TeX Stack Exchange](https://tex.stackexchange.com/)
4. File an issue on the repository

## Minimal Installation

If you're having trouble with the full installation, try the minimal setup:

1. **Install only essential packages**:
   ```bash
   tlmgr install latex latex-bin latexmk \
     tgpagella geometry article hyperref
   ```

2. **Check the package loads on its own**:
   Create a file `probe.tex`:
   ```latex
   \documentclass[11pt]{article}
   \usepackage{lanepaper}
   \begin{document}
   Your content here
   \end{document}
   ```

3. **Compile with basic pdflatex**:
   ```bash
   pdflatex probe.tex
   ```

## Verification

After installation, review the [Required LaTeX Packages](#required-latex-packages)
section above, then verify everything works:

```bash
# Check the required LaTeX packages listed above
# Install any missing package with tlmgr or mpm.

# Run the full test suite
make lint
make build
make test

# List every target
make help
```

## Typography System Architecture

`\usepackage{lanepaper}` is the sole public load path (ADR-0006). The
`lnp*.sty` files in `lanepaper/` are internal owners: `lanepaper` loads them,
and loading one directly is unsupported.

| Module | Owns |
|---|---|
| `lnpcolors.sty` | The semantic colour palette, all names `lnp@`-prefixed |
| `lnpdimensions.sty` | Page geometry, the 13.2pt spacing quantum, and block quotations |
| `lnpfonts.sty` | Pagella, Inconsolata, newpxmath, mathalfa |
| `lnpheadings.sty` | Section heading styles and their colour hierarchy |
| `lnplists.sty` | List typography and refined bullets |
| `lnpmicrotype.sty` | Upstream Pagella protrusion and expansion; small-caps tracking |

Customisation happens in the document, after loading:

```latex
\usepackage{lanepaper}
\geometry{margin=2in}   % Override the layout
```

## Next Steps

- Read `README.md` for usage instructions
- See [`API_REFERENCE.md`](API_REFERENCE.md), section "Typography standards", for typography guidelines
- Check `TROUBLESHOOTING.md` for common issues

---

<!-- %% FIX: Avoid naming unverified external platforms in active installation docs. -->
**Note**: This template requires a complete LaTeX installation. If you encounter persistent package issues, use a complete TeX Live, MacTeX, or MiKTeX setup.
