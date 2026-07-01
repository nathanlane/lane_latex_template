# Academic Paper LaTeX Template

**By Nathan Lane / Industrial Policy Group**

A (not yet) production-grade LaTeX template for academic papers with optimized typography. 

This (living) template applies classic typographic principles to create scholarly articles. For more on typography principles: [https://github.com/nathanlane/nathanstypographynotes/](https://github.com/nathanlane/nathanstypographynotes/)


---

## ✨ Features

- **Typography** – TeX Gyre Pagella (Palatino-based) with superior small caps, harmonized mathematics, and optimized monospace
- **Baseline Grid System** – 13.2pt rhythm with systematic proportional relationships
- **Optically Refined Typo** - Using typographic principles
- **Grid Optimization** – Optional modules reduce drift while maintaining typography quality
- **Dynamic Title Page** – Mathematical spacing with golden ratio proportions
- **Smart Citations** – biblatex with Chicago style, DOI/URL linking, and native natbib mode
- **Floats** – Comprehensive figure/table system with booktabs, tabularx, and smart placement
- **Lists** – Multiple environments with refined bullets and optimal spacing
- **Accessibility** – WCAG 2.1 AA compliant colors with semantic emphasis commands
- **Cross-Platform** – Works with local LaTeX and Overleaf

---

## 🚀 Quick Start

```bash
# 1. Clone this template
git clone <this-repo> my-paper
cd my-paper

# 2. Write your paper
edit main.tex         # Your content goes here
edit references.bib   # Your citations go here

# 3. Compile
make                  # Creates main.pdf
```

That's it! You now have a professionally typeset academic paper.

---

## 📋 Table of Contents

- **[Installation](#installation)** – System requirements and setup
- **[Getting Started](#getting-started)** – Create your first document
- **[Basic Usage](#basic-usage)** – Essential commands and features
- **[Document Structure](#document-structure)** – File organization and architecture
- **[Typography System](#typography-system)** – Fonts, spacing, and grid
- **[Academic Writing](#academic-writing)** – Citations, figures, and scholarly features
- **[Advanced Customization](#advanced-customization)** – Modify and extend the template
- **[Troubleshooting](#troubleshooting)** – Common issues and solutions
- **[Contributing](#contributing)** – Development guidelines
- **[Technical Reference](#technical-reference)** – Complete API documentation
- **[Version History](#version-history)** – Updates and changelog

---

## Installation

### Prerequisites

- **LaTeX Distribution**: TeX Live 2020+, MiKTeX, or MacTeX
- **Bibliography Backend**: Biber (included with modern distributions)
- **Build Tool**: Make (optional but recommended)
- **Regression Test Helper**: `pdftotext` from Poppler for PDF text assertions in the pytest regression harness

### Tested Build Environments

Verified locally on May 28, 2026; Overleaf evidence must come from the project compile log:

- **Local**: TeX Live 2025 at `/usr/local/texlive/2025` (`tlmgr` revision 76773), pdfTeX 1.40.28, `latexmk` 4.86a, Biber 2.20, using `latexmk -pdf -interaction=nonstopmode main.tex`.
- **Overleaf**: TeX Live 2024 annual release; the exact Overleaf build identifier is not available in this local checkout and must be copied from the Overleaf compile log before claiming Overleaf Definition of Done.

### Quick Setup

```bash
# Verify your LaTeX installation
make check

# Install missing packages (if any)
tlmgr install tgpagella inconsolata newpx mathalfa booktabs

# Test compilation
make lint
make build
pytest -q
```

### Platform Notes

- **macOS**: Use MacTeX or install via Homebrew
- **Linux**: Install texlive-full from your package manager
- **Windows**: Use MiKTeX or WSL with TeX Live
- **Overleaf**: Works automatically without configuration

### Environment Variables (Optional)

If you're using the AI-assisted features or data analysis scripts, create a `.env` file:

```bash
# Copy the example file
cp .env.example .env

# Edit with your API keys (never commit real keys!)
GEMINI_API_KEY=your_api_key_here
```

**Note**: The `.env` file is git-ignored to protect your credentials. Never commit API keys to version control.

---

## Getting Started

### Creating Your First Document

1. **Start with the template structure**:
   ```
   my-paper/
   ├── main.tex          # Your document
   ├── references.bib    # Your citations
   ├── paper/            # Style files (don't edit)
   └── figures/          # Your images
   ```

2. **Edit main.tex**:
   ```latex
   \documentclass[11pt]{article}
   \input{paper/preamble.tex}
   
   \begin{document}
   % Your content here
   \end{document}
   ```

3. **Add your content** and compile

### Compilation Methods

**Using Make** (recommended):
```bash
make              # Full compilation with bibliography
make quick        # Fast compilation (skip bibliography)
make clean        # Remove temporary files
make watch        # Auto-recompile on changes
```

**Repository verification gates**:

```bash
chktex -q -n1 -n3 -n8 -n11 -n13 -n18 -n24 -n36 -n39 -n42 -n46 -n48 *.tex
latexmk -pdf -interaction=nonstopmode main.tex
pytest -q
```

`tests/check-spacing-integrity.sh main.pdf` is run as a diagnostic in this lane:
`tests/check-spacing-integrity.sh main.pdf || true`.

**Manual compilation**:
```bash
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

**Overleaf**: Just click the Recompile button

---

## Basic Usage

### Title Page

Create a professional title page with mathematical spacing:

```latex
\thispagestyle{empty}
\titlefootnotesetup
\begin{center}
  \vspace*{\titlespaceminor}
  \articletitle{Your Paper Title}
  \articleauthors{Jane Smith\footnote{University, email@example.edu} 
    \authorspace John Doe\footnote{Institute, john@example.edu}}
  \articledate{\today}
  \begin{articleabstract}
    Your abstract text here...
  \end{articleabstract}
  \articlekeywords{keyword1, keyword2, keyword3}
  \articlejel{A10, B20, C30}
\end{center}
\clearpage
\titlefootnotereset
```

### Citations and Bibliography

The template uses biblatex with Chicago author-date style. The standard preamble
loads `lltpaperstyle`, which auto-loads the default biblatex configuration; then
it registers `references.bib`:

```latex
\usepackage{lltpaperstyle}
\addbibresource{references.bib}
```

For custom biblatex options, load biblatex manually and disable automatic
loading:

```latex
\usepackage[backend=biber,style=authoryear]{biblatex}
\addbibresource{references.bib}
\usepackage[nobiblatex]{lltpaperstyle}
```

```latex
% In your text
As shown by \textcite{smith2023}...        % Smith (2023) shows...
Recent work \autocite{smith2023} found...  % Recent work (Smith 2023) found...

% In references.bib
@article{smith2023,
  title = {An Important Finding},
  author = {Smith, Jane},
  journal = {Journal Name},
  year = {2023},
  volume = {10},
  pages = {1--20},
  doi = {10.1234/example}
}
```

### Figures and Tables

**Professional figure**:
```latex
\begin{figure}[tbp]
  \centering
  \includegraphics[width=0.8\textwidth]{figures/myplot.pdf}
  \caption{Description of your figure}
  \label{fig:myplot}
\end{figure}
```

**Professional table** (note caption placement):
```latex
\begin{table}[tbp]
  \caption{Regression Results}
  \label{tab:results}
  \centering
  \begin{tabular}{lcc}
    \toprule
    Variable & Model 1 & Model 2 \\
    \midrule
    X & 0.5*** & 0.4*** \\
      & (0.1)  & (0.1)  \\
    \bottomrule
  \end{tabular}
  \begin{tablenotes}
    \tabnote{Standard errors in parentheses}
    \tabstars
  \end{tablenotes}
\end{table}
```

### Cross-References

Smart references with cleveref:

```latex
See \cref{fig:results}...        % see figure 1...
\Cref{tab:data} shows...         % Table 2 shows...
\cref{fig:a,fig:b,fig:c}         % figures 1, 2 and 3
\crefrange{fig:a}{fig:d}         % figures 1–4
```

---

## Document Structure

### Directory Organization

```
your-paper/
├── main.tex              # Main document
├── references.bib        # Bibliography
├── paper/
│   ├── preamble.tex      # Document setup
│   ├── lltpaperstyle.sty # Main style (don't edit)
│   └── modules/          # Modular components
├── appendices/           # Supplementary material
│   ├── main_appendix.tex
│   └── tech_appendix.tex
├── figures/              # Images and plots
└── data/                 # Data files (optional)
```

### Package Options

Load the style with options:

```latex
\usepackage{lltpaperstyle}           % Standard (all features)
\usepackage[grid]{lltpaperstyle}     % Show baseline grid
\usepackage[minimal]{lltpaperstyle}  % Essential features only
\usepackage[draft]{lltpaperstyle}    % Draft mode
```

Available options:
- `grid` / `nogrid` – Show/hide baseline grid overlay
- `minimal` – Load only essential features
- `natbib` – Load native `natbib` author-year citation support instead of automatic `biblatex`
- `nocolor` – Map semantic template colors to black/grayscale values
- `draft` – Enable draft-mode diagnostics, including draft-mode `microtype`
- `nobiblatex` – Disable automatic biblatex loading
- `subsectionbarriers` / `nosubsectionbarriers` – Enable/disable automatic float barriers before subsections
- `nocolor` – Disable all custom colors
- `draft` – Enable draft mode
- `nobiblatex` – Disable automatic biblatex loading after you load biblatex manually

### Modular Architecture

The style system is fully modularized:

**Core modules** (automatically loaded):
- `lltcolors` – Professional color palette
- `lltdimensions` – Grid system and spacing
- `lltfonts` – Font configuration
- `lltheadings` – Section heading styles
- `lltlists` – List typography
- `lltmicrotype` – Enhanced character protrusion, expansion, and spacing

**Optional modules**:
- `lltparagraphs` – Advanced paragraph formatting
- `llthochuli` – Advanced optical adjustments

---

## Typography System

### Font Configuration

The template uses a carefully selected font stack:

- **Text**: TeX Gyre Pagella (enhanced Palatino)
- **Math**: newpxmath (harmonized with Pagella)
- **Code**: Inconsolata (scaled to 96%)
- **Features**: Real small caps, oldstyle figures, ligatures

### Baseline Grid

All vertical spacing follows a 13.2pt grid:

```latex
\vspace{\gridunit}        % 13.2pt (1 unit)
\vspace{\halfgridunit}    % 6.6pt (0.5 units)
\vspace{2\gridunit}       % 26.4pt (2 units)
```

### Emphasis Hierarchy

Semantic commands for different emphasis levels:

```latex
\emph{emphasis}           % Smart italic/roman
\strongemph{critical}     % Bold for critical terms
\term{baseline grid}      % Technical terms
\person{Hermann Zapf}     % Person names (small caps)
\acro{PDF}               % Acronyms (small caps)
\work{Book Title}        % Published works
\critical{WARNING}       % Maximum emphasis
```

### Special Characters

Professional typography for special characters:

```latex
Typography\emdash the art\emdash is essential
Pages 10--20              % En dash for ranges
25\degrees C              % Degree symbol
\texteuro 100            % Currency symbols
\copyright 2025          % Legal symbols
```

---

## Academic Writing

### Citation Standards

Follow Chicago Manual of Style guidelines:

```latex
% Primary commands
\textcite{author2023}          % Author (2023) argues...
\autocite{author2023}          % ...(Author 2023).
\textcite[45]{author2023}      % Author (2023, 45)
\citeauthor{author2023}        % Author
\citeyear{author2023}          % 2023

% Multiple citations
\textcite{smith2023,jones2023} % Smith (2023) and Jones (2023)
```

### Figure and Table Guidelines

**Best practices**:
- Figures: Caption below, use vector formats (PDF/EPS)
- Tables: Caption above, use booktabs (no vertical rules)
- Placement: Use `[tbp]`, avoid `[h]`
- References: Always use `\cref{}` or `\Cref{}`

### Appendix Management

Professional appendix system with automatic formatting:

```latex
\begin{documentAppendices}
  \input{appendices/main_appendix.tex}
  \input{appendices/tech_appendix.tex}
\end{documentAppendices}
```

Features:
- Automatic numbering (A, B, C...)
- Smart detection (single vs. multiple)
- Full cross-reference support
- Consistent typography

### Mathematical Typography

Optimized for academic papers:

```latex
% Display equations with grid alignment
\begin{equation}
  f(x) = \int_{-\infty}^{\infty} g(t) e^{-2\pi i x t} \, dt
\end{equation}

% Semantic math commands
$x \in \real$              % Real numbers
$\norm{v} = 1$            % Vector norm
$\abs{x} < \epsilon$      % Absolute value
```

---

## Advanced Customization

### Color Customization

Override colors before loading the style:

```latex
\definecolor{linknavy}{RGB}{0,0,255}      % Custom link color
\definecolor{sectioncolor}{RGB}{0,0,0}    % Black headings
\usepackage{lltpaperstyle}
```

### Layout Modifications

Adjust margins and spacing:

```latex
\geometry{margin=2in}                      % Wider margins
\setlength{\parindent}{2em}               # Larger indent
\usepackage{lltpaperstyle}
```

### Creating Extensions

Add custom commands in your preamble:

```latex
% After loading lltpaperstyle
\newcommand{\mycommand}[1]{\textcolor{linknavy}{\textbf{#1}}}
\newenvironment{myenv}{\begin{quote}}{\end{quote}}
```

### Grid-Locked Modules

For strict baseline adherence:

```latex
\usepackage{paper/modules/lltheadingsgridlocked}
\usepackage{paper/modules/lltmathgridlocked}
```

---

## Troubleshooting

### Common Issues

**Missing packages**:
```bash
# TeX Live / MacTeX
tlmgr install [package-name]

# MiKTeX
mpm --install=[package-name]
```

**Compilation errors**:
```bash
make clean        # Clear temporary files
make              # Full rebuild
```

**Font issues**:
```latex
% Use minimal mode for compatibility
\usepackage[minimal]{lltpaperstyle}
```

### Platform-Specific Notes

**Overleaf**:
- All features work automatically
- Use "TeX Live 2023" or later in Menu → Settings

**Windows**:
- Use WSL for Make commands
- Or compile manually with pdflatex/biber

**Local installation**:
```bash
# Set TEXINPUTS if needed
export TEXINPUTS=".:./paper//:"
```

### Getting Help

1. Check the [API Reference](API_REFERENCE.md)
2. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions
3. Review test files in `tests/fixtures/`
4. Open an issue on GitHub

---

## Contributing

### Development Guidelines

1. **Typography first**: Don't break the baseline grid
2. **Test everything**: Run `make test` before commits
3. **Document changes**: Update relevant documentation
4. **Follow style**: One sentence per line in LaTeX

### Testing

```bash
make test         # Full test suite
make test-quick   # Quick compilation test
make validate     # Style validation
```

### Pull Request Process

1. Fork and create a feature branch
2. Make changes and test thoroughly
3. Update documentation if needed
4. Submit PR with clear description

---

## Technical Reference

### Documentation

- **[API Reference](API_REFERENCE.md)** – Complete command reference
- **[Style Guide](paper/STYLE_GUIDE.md)** – Typography standards
- **[Code Review Report](docs/technical/LATEX_CODE_REVIEW_2026-05-28.md)** – Maintainability and package API findings
- **[Maintainability Fix Plan](docs/superpowers/plans/2026-05-28-latex-template-maintainability.md)** – Checkpointed implementation plan for review findings
- **[Testing Guide](tests/README.md)** – Test framework documentation
- **[CLAUDE.md](CLAUDE.md)** – Development philosophy

### Key Commands

**Typography**:
```latex
\emph{}, \strongemph{}, \term{}, \person{}, \acro{}
\emdash, \degrees, \texteuro, \textpm
```

**Structure**:
```latex
\articletitle{}, \articleauthors{}, \articledate{}
\begin{articleabstract}, \articlekeywords{}, \articlejel{}
```

**References**:
```latex
\textcite{}, \autocite{}, \cref{}, \Cref{}
```

**Environments**:
```latex
itemize, enumerate, quote, quotation
gridtable, landscapetable, documentAppendices
```

### Dependencies

Core packages:
- `tgpagella` – TeX Gyre Pagella fonts
- `newtxmath` – Mathematics
- `biblatex` – Bibliography
- `booktabs` – Professional tables
- `cleveref` – Smart references
- `microtype` – Microtypography

---

## Version History

Current Release: v0.1.0-beta

**Version v0.1.0-beta (July 2025)**
- Public repository
- All preamble files and documentation
- Migration guides and README files
- API reference and appendices
- Module documentation
- Version history sections

**Version v1.4-alpha:v1.6-alpha (July 2025)**
- Added `llt` package naming convention
- Implemented modular architecture
- Enhanced grid system with visual overlay
- Improved cross-platform compatibility

**Version v1.0-alpha:v1.3-alpha (June 2025)**
- Professional appendix management system
- Enhanced optical margin alignment
- Sophisticated list typography
- QJE-style table notes

### Versioning 

Historical Versions: All old development versions are now labeled as alpha:
•  v1.6-alpha (was v1.6)
•  v1.5-alpha (was v1.5) 
•  v1.4-alpha (was v1.4)
•  v1.3-alpha (was v1.3)
•  v1.2-alpha (was v1.2)
•  v1.1-alpha (was v1.1)
•  v1.0-alpha (was v1.0)

### Migration Notes

If upgrading from an older version:
- `\usepackage{paper/paperstyle}` → `\usepackage{lltpaperstyle}`
- All module names now have `llt` prefix
- See [MIGRATION.md](paper/MIGRATION.md) for details

### Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete version history.

---

**License**: LaTeX Project Public License v1.3c

**Credits**: Typography based on principles from Butterick's *Practical Typography*, Brown's *Modular Scale*, and Hochuli's *Detail in Typography*.
