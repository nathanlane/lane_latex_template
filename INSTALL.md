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

The lists below are derived from the current `\RequirePackage` and
`\usepackage` statements. They name LaTeX packages/files; a distribution may
group several of them under one installable package. Install a missing item
with `tlmgr install <package-name>` or `mpm --install=<package-name>`.

### Loaded by `lanepaper/`

The package and its internal modules require:

```text
amsmath amssymb array booktabs caption enumitem etoolbox fancyhdr footmisc
geometry graphicx iftex inputenc mathalfa microtype newpxmath textcomp
tgpagella titlesec xcolor zi4
```

### Added by `demo/`

The demo sources add these document-owned packages:

```text
adjustbox babel biblatex cleveref csquotes doi hyperref longtable natbib
pdflscape rotating tabularx threeparttable url
```

The demo's `biblatex` configuration also requires the `biber` executable.

### TeX Live / MacTeX installation

The distribution names differ for some LaTeX files: `fontenc`, `inputenc`, and
`textcomp` come from the LaTeX base; `array`, `longtable`, and `tabularx` come
from the tools bundle; `graphicx` and `rotating` come from the graphics bundle;
`tgpagella`, `newpxmath`, and `zi4` are supplied by `tex-gyre`, `newpx`, and
`inconsolata`. Install the corresponding distribution packages, for example:

```bash
tlmgr install latex amsmath amsfonts tools graphics booktabs caption enumitem \
  etoolbox fancyhdr footmisc geometry iftex mathalpha microtype newpx \
  tex-gyre titlesec xcolor inconsolata adjustbox babel biblatex cleveref \
  csquotes doi hyperref natbib pdflscape threeparttable url biber
```

MiKTeX can install the same dependencies on demand; otherwise use
`mpm --install=<package-name>` for the corresponding MiKTeX package.

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

For a document that only loads `lanepaper`, install every item in the
`lanepaper/` list above. The demo and this repository's fixture suite also need
the packages in the `demo/` list. There is no smaller supported dependency set.

1. **Check the package loads on its own**:
   Create a file `probe.tex`:
   ```latex
   \documentclass[11pt]{article}
   \usepackage{lanepaper}
   \begin{document}
   Your content here
   \end{document}
   ```

2. **Compile with basic pdflatex**:
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
