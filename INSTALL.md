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
1. **TeX Distribution** (one of the following):
   - TeX Live 2020 or newer (recommended)
   - MiKTeX 2020 or newer
   - MacTeX 2020 or newer (macOS)

2. **Build Tools**:
   - GNU Make
   - Python 3.7+ (for data analysis scripts)
   - Git (for version control)

3. **PDF Viewer**:
   - Any PDF viewer that auto-refreshes (e.g., Skim on macOS, SumatraPDF on Windows)

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd lane_latex_template
   ```

2. **Check your LaTeX installation**:
   ```bash
   make check
   ```

3. **Install missing packages** (if any):
   ```bash
   # TeX Live / MacTeX
   tlmgr install <package-name>
   
   # MiKTeX
   mpm --install=<package-name>
   ```

4. **Run setup**:
   ```bash
   make setup
   ```

5. **Test compilation**:
   ```bash
   make test-quick
   ```

6. **Build the paper**:
   ```bash
   make pdf
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

3. **Install watch tools** (for auto-rebuild):
   ```bash
   brew install fswatch
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

3. **Install watch tools**:
   ```bash
   sudo apt-get install inotify-tools
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
tlmgr install textcomp                # Additional text symbols

# Typography enhancement
tlmgr install microtype               # Character protrusion, font expansion
tlmgr install letterspace             # Letter spacing control (for tracking)
tlmgr install fnpct                   # Footnote punctuation management
```

### Essential Packages
```bash
# Document structure
tlmgr install geometry           # Page layout
tlmgr install fancyhdr          # Headers and footers
tlmgr install titlesec         # Section formatting
tlmgr install appendix          # Appendix support
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
tlmgr install csquotes         # Context-sensitive quotes
tlmgr install enumitem         # List customization
tlmgr install caption          # Caption customization
tlmgr install subcaption       # Subfigures and subtables

# Float and rotation support
tlmgr install placeins         # Float barriers
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
tlmgr install tex-gyre tex-gyre-math inconsolata newpx mathalpha \
  microtype letterspace fnpct textcomp \
  geometry fancyhdr titlesec appendix titletoc \
  graphicx booktabs tabularx longtable ltcaption adjustbox array multirow \
  biblatex biber xcolor hyperref cleveref csquotes enumitem \
  caption subcaption placeins rotating pdflscape afterpage \
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
   make pdf
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

Run the diagnostic command:
```bash
pdflatex -interaction=nonstopmode "\RequirePackage{paper/paperstyle}\paperstylediagnostics\stop"
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

2. **Use compatibility mode**:
   Create a file `minimal.tex`:
   ```latex
   \documentclass{article}
   \usepackage[compat]{paper/paperstyle}
   \begin{document}
   Your content here
   \end{document}
   ```

3. **Compile with basic pdflatex**:
   ```bash
   pdflatex minimal.tex
   ```

## Verification

After installation, verify everything works:

```bash
# Check all tools
make check

# Run minimal test
make test-quick

# Run full test suite
make test

# Show diagnostic information
make diagnose
```

## Typography System Architecture

The template uses a modular typography system organized in `paper/modules/`:

### Core Modules (Automatically Loaded)
- `compilation-fixes-simple.sty` - Fixes common LaTeX warnings
- `colors.sty` - Professional color definitions (linknavy, sectioncolor, bulletgray)
- `dimensions.sty` - Grid system (13.2pt baseline) and spacing commands
- `fonts.sty` - Font configuration (Pagella, Inconsolata, newpxmath, mathalfa)
- `headings.sty` - Section heading styles with color hierarchy
- `lists.sty` - List typography with refined bullets (6.6pt item spacing)

### Optional Enhancement Modules
- `paragraphs.sty` - Advanced paragraph formatting, quotations, dialogue
- `microtype-config.sty` - Enhanced character protrusion (up to 1400 units)
- `headings-gridlocked.sty` - Stricter grid alignment (±0.125 vs ±0.25 units)
- `mathematics-gridlocked.sty` - Minimal math flexibility (±0.0625 units)
- `hochuli-refinements.sty` - Advanced optical adjustments
- `font-features.sty` - Full Pagella feature access
- `font-fallbacks.sty` - Compatibility mode with fallback chains

### Module Features
- **Modular loading**: Load only what you need
- **Override capability**: Customize before loading paperstyle
- **Dependency management**: Automatic loading of required modules
- **Graceful degradation**: Fallbacks for missing packages

Example customization:
```latex
% Override colors
\definecolor{linknavy}{RGB}{0,0,255}
\definecolor{sectioncolor}{RGB}{0,0,0}

% Load main package
\usepackage{paper/paperstyle}

% Add optional enhancements
\usepackage{paper/modules/microtype-config}
\usepackage{paper/modules/hochuli-refinements}
```

## Next Steps

- Read `README.md` for usage instructions
- See `paper/STYLE_GUIDE.md` for typography guidelines
- Check `docs/TROUBLESHOOTING.md` for common issues
- Review example documents in `examples/`

---

**Note**: This template requires a complete LaTeX installation. If you encounter persistent issues, consider using an online service like Overleaf, which has all packages pre-installed.