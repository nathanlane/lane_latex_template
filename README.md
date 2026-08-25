# Lane LaTeX Template

A living LaTeX template for academic papers with optimized typography. Actively used and revised.

This template applies classic typographic principles to create scholarly articles. For more on typography principles: [https://github.com/nathanlane/nathanstypographynotes/](https://github.com/nathanlane/nathanstypographynotes/)


---

## ✨ Features

<!-- %% FIX: Keep active feature claims limited to locally verified support. -->
- **Typography** – TeX Gyre Pagella (Palatino-based) with superior small caps, harmonized mathematics, and optimized monospace
- **Spacing Quantum System** – most vertical spacing in multiples of a 13.2pt quantum; body leading measures 16.32pt (see `docs/adr/0004-baseline-grid-is-a-spacing-quantum.md`)
- **Optical Refinements** – Optional `lnphochuli` module; when loaded, automatically applies custom Pagella kerning pairs and last-line length control (`\parfillskip`); also provides opt-in commands for selective ligature suppression and hanging punctuation at paragraph openings
- **Grid Optimization** – Optional modules reduce drift while maintaining typography quality
- **Dynamic Title Page** – Mathematical spacing with golden ratio proportions
- **Smart Citations** – styles `biblatex` or `natbib` when your document loads one; it never loads one for you
- **Floats** – Comprehensive figure/table system with booktabs, tabularx, and smart placement
- **Lists** – Multiple environments with refined bullets and optimal spacing
- **Accessibility** – WCAG 2.1 AA compliant colors with semantic emphasis commands
- **Local Build Workflow** – Verified with local `latexmk`, `chktex`, and pytest gates

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

- **Engine**: pdfLaTeX only. XeLaTeX and LuaLaTeX are not supported and the
  package stops with an explicit error on them - the font stack is 8-bit
  (T1 `fontenc`, `utf8` `inputenc`, `newpxmath`, `mathalfa`, `zi4`, Type1
  `tgpagella`), there is no `fontspec` path, and `microtype` font expansion
  is unsupported on XeTeX.
- **LaTeX Distribution**: TeX Live 2020+, MiKTeX, or MacTeX. The LaTeX format
  must be **2020-10-01 or newer** — the package uses the format-native hook
  system (`\AddToHook`), and both entry points declare that floor.
- **Bibliography Backend**: Biber (included with modern distributions)
- **Build Tool**: Make (optional but recommended)
- **Regression Test Helper**: `pdftotext` from Poppler for PDF text assertions in the pytest regression harness

### Tested Build Environments

<!-- %% FIX: Remove unsupported external build claims and keep the local toolchain explicit. -->
Verified locally on August 12, 2026 (all gates: `make lint`, `make build`,
`make check-deps`, `make test`):

- **TeX Live 2026** at `/usr/local/texlive/2026`, pdfTeX 1.40.29, using
  `latexmk -pdf -interaction=nonstopmode main.tex`.
- **TeX Live 2022** at `/Library/TeX/texbin`, pdfTeX 1.40.24, `latexmk` 4.77,
  Biber 2.17, ChkTeX 1.7.6 (the `make lint` gate probes `-n48` support and
  drops it on binaries older than ChkTeX 1.7.7).

Poppler is part of the verified local setup (August 24, 2026): `pdftotext`
26.08.0 and `pdfinfo` on PATH, so the PDF-text assertions in
`tests/test_regression_harness.py` run rather than skip, and
`tests/check-spacing-integrity.sh` runs instead of exiting 1. Verified with
`pytest -q` reporting 0 skipped.

Earlier verification (July 4, 2026): TeX Live 2025, pdfTeX 1.40.28,
`latexmk` 4.86a, Biber 2.20.

### Quick Setup

```bash
# Verify your LaTeX installation
make check-deps

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

---

## Getting Started

### Creating Your First Document

1. **Start with the template structure**:
   ```
   my-paper/
   ├── main.tex          # Your document
   ├── references.bib    # Your citations
   ├── lanepaper/        # Style files (don't edit)
   └── figures/          # Your images
   ```

2. **Edit main.tex**:
   ```latex
   \documentclass[11pt]{article}
   \usepackage{lanepaper}
   \addbibresource{references.bib}
   
   \begin{document}
   % Your content here
   \end{document}
   ```

3. **Add your content** and compile

### Compilation Methods

**Using Make** (recommended):
```bash
make              # Compile the demo document
make clean        # Remove generated output, the PDF included
make watch        # Auto-recompile on changes
make help         # List every target
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

**The document owns its bibliography.** Since issue #48 the package does not
load `biblatex`, `natbib`, `hyperref`, `cleveref`, `babel` or `appendix` — it
styles them if you load them (ADR-0003). Nothing here dictates your load order
or your citation style.

Load biblatex with whatever options you want:

```latex
\usepackage[
  backend=biber, style=authoryear, natbib=true, sorting=nyt,
  maxcitenames=2, maxbibnames=99, giveninits=true, uniquename=init,
  doi=true, url=true, isbn=false
]{biblatex}
\usepackage{lanepaper}
\addbibresource{references.bib}
```

Those are the options the package used to impose on every document; `demo/preamble.tex`
carries them so the demo renders as before. Change any of them freely — that is
the point of the change.

The `nobiblatex` and `natbib` options are **deprecated and do nothing**: there is
no automatic loading left to disable. They are still accepted, with a warning,
so existing documents do not fail on an unknown option.

For legacy natbib-based documents, use the dedicated preamble:

```latex
\input{demo/preamble-natbib.tex}
```

It loads `natbib` itself, then `lanepaper`, and provides the `\textcite` and
`\autocite` compatibility aliases expected by older documents (`\citeauthor`
and `\citeyear` come natively from natbib).

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
├── lanepaper/            # The package - don't edit
│   ├── lanepaper.sty     # Main style
│   └── lnp*.sty          # Feature modules
├── appendices/           # Supplementary material
│   ├── main_appendix.tex
│   └── tech_appendix.tex
├── figures/              # Images and plots
└── data/                 # Data files (optional)
```

### Package Options

Load the style with options:

```latex
\usepackage{lanepaper}           % Standard (all features)
\usepackage[grid]{lanepaper}     % Show grid overlay (baseline + quantum lines)
\usepackage[minimal]{lanepaper}  % Essential features only
\usepackage[draft]{lanepaper}    % Draft mode
```

Available options:
- `grid` / `nogrid` – Show/hide the grid overlay (true-baseline and quantum lines)
- `minimal` – Load only essential features
- `natbib` – **Deprecated, inert.** The package no longer loads a bibliography package; load `natbib` yourself
- `draft` – Enable draft-mode diagnostics, including draft-mode `microtype`
- `nobiblatex` – **Deprecated, inert.** There is no automatic biblatex loading left to disable
- `subsectionbarriers` / `nosubsectionbarriers` – Enable/disable automatic float barriers before subsections
- `mathredefs` – Opt in to variant math glyphs (`\le`→`\leqslant`, `\ge`→`\geqslant`, `\epsilon`→`\varepsilon`, `\phi`→`\varphi`, `\vec`→bold). Off by default: the redefinitions change mathematical meaning, so standard LaTeX semantics ship unless requested. Assumes full (non-`minimal`) mode, where the symbol fonts are loaded
- `nocolor` – Disable all custom colors

Note: `\usepackage[minimal]{lanepaper}` and
`\usepackage{lnpminimal}` are distinct surfaces.
The former uses the main package with reduced module loading; the latter loads the
separate lightweight package.

### Modular Architecture

The style system is fully modularized:

**Core modules** (automatically loaded):
- `lnpcolors` – Professional color palette
- `lnpdimensions` – Grid system and spacing
- `lnpfonts` – Font configuration
- `lnpheadings` – Section heading styles
- `lnplists` – List typography
- `lnpmicrotype` – Enhanced character protrusion, expansion, and spacing

**Optional modules**:
- `lnpmathgridlocked` – Grid-locked equation spacing hooks
- `lnpparagraphs` – Advanced paragraph formatting
- `lnphochuli` – Advanced optical adjustments

Load optional modules such as `lnpparagraphs` before `lanepaper`.
Loading `lnpparagraphs` after `lanepaper` is unsupported unless the reverse
order is fully guarded.

---

## Typography System

### Font Configuration

The template uses a carefully selected font stack:

- **Text**: TeX Gyre Pagella (enhanced Palatino)
- **Math**: newpxmath (harmonized with Pagella)
- **Code**: Inconsolata (scaled to 96%)
- **Features**: Real small caps, oldstyle figures, ligatures

### Spacing Quantum

All vertical spacing follows a 13.2pt quantum (a spacing unit — the body
baseline measures 16.32pt):

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
\usepackage{lanepaper}
```

### Layout Modifications

Adjust margins and spacing:

```latex
\geometry{margin=2in}                      % Wider margins
\setlength{\parindent}{2em}               % Larger indent
\usepackage{lanepaper}
```

### Creating Extensions

Add custom commands in your preamble:

```latex
% After loading lanepaper
\newcommand{\mycommand}[1]{\textcolor{linknavy}{\textbf{#1}}}
\newenvironment{myenv}{\begin{quote}}{\end{quote}}
```

### Grid-Locked Modules

For strict baseline adherence:

```latex
\usepackage{lnpheadingsgridlocked}
\usepackage{lnpmathgridlocked}
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
\usepackage[minimal]{lanepaper}
```

### Platform-Specific Notes

**Windows**:
- Use WSL for Make commands
- Or compile manually with pdflatex/biber

**Local installation**:

To use the package from your own documents, anywhere on the system, install it
into your home texmf tree:

```bash
make install     # copies lanepaper into TEXMFHOME; make uninstall reverses it
```

`\usepackage{lanepaper}` then resolves from any directory. Working inside this
repository needs no install -- the Makefile puts `./lanepaper` first on
`TEXINPUTS`, so the working tree always wins over an installed copy. To compile
by hand from the repository without Make:

```bash
export TEXINPUTS=".:./lanepaper//:"
```

### Getting Help

1. Check the [API Reference](API_REFERENCE.md)
2. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions
3. Review test files in `tests/fixtures/`
4. Open an issue on GitHub

---

## Contributing

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for build instructions, test commands, and the `\lnp@` namespace convention.

### Development Guidelines

1. **Typography first**: Don't break the spacing quantum rhythm
2. **Test everything**: Run `make test` before commits
3. **Document changes**: Update relevant documentation
4. **Follow style**: One sentence per line in LaTeX

### Testing

```bash
make test         # pytest, then the shell harness
make lint         # chktex, then the math-spacing checker
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
- **[Typography standards](API_REFERENCE.md)** – how to use the system well
- **[Testing Guide](tests/README.md)** – Test framework documentation

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
- `newpxmath` – Mathematics
- `biblatex` – Bibliography
- `booktabs` – Professional tables
- `cleveref` – Smart references
- `microtype` – Microtypography

---

## Version History

<!-- %% FIX: Separate repository release status from the bundled package version. -->
Repository release: `v2.1.0`.

Bundled package version: `lanepaper` reports `v2.0` in
`lanepaper/lanepaper.sty`.

v2.0.0 was the breaking-change release following the adopter defect report
(previously repo `v0.1.0-beta` vs package `v1.7`). Repository and package
versions may diverge; see the files above for current values.

### Versioning 

Historical package-development versions are alpha snapshots:
- `v1.6-alpha` (was `v1.6`)
- `v1.5-alpha` (was `v1.5`)
- `v1.4-alpha` (was `v1.4`)
- `v1.3-alpha` (was `v1.3`)
- `v1.2-alpha` (was `v1.2`)
- `v1.1-alpha` (was `v1.1`)
- `v1.0-alpha` (was `v1.0`)

### Migration Notes

If upgrading from an older version:
- `\usepackage{paper/paperstyle}` → `\usepackage{lanepaper}`
- All module names now have the `lnp` prefix

### Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete version history.

---

**License**: LaTeX Project Public License v1.3c

**Credits**: Typography based on principles from Butterick's *Practical Typography*, Brown's *Modular Scale*, and Hochuli's *Detail in Typography*.

## Quality checklist

**Pre-Submission Verification for Professional Academic Documents**

Use this comprehensive checklist to ensure your academic paper meets the highest standards for professional publication.

### ✅ Typography and Formatting Quality

#### Title and Caption Standards
- [ ] All titles use headline-style capitalization (verified with title case checker)
- [ ] Section and subsection headings follow capitalization rules
- [ ] Figure captions placed below figures with proper capitalization
- [ ] Table captions placed above tables with proper capitalization
- [ ] Hyphenated words capitalized correctly (e.g., "Learning-Based Approach")
- [ ] Special cases handled correctly (e.g., "X-ray" not "X-Ray")

#### Typography Standards
- [ ] All emphasis uses semantic commands (`\emph{}`, not `\textit{}`)
- [ ] Small caps use provided commands (`\bsc{}`, `\headsc{}`, `\balancedbsc{}`)
- [ ] Mathematical notation uses semantic commands (`\real`, `\norm{}`, `\abs{}`)
- [ ] Code typography uses appropriate commands for context
- [ ] Colors use semantic commands, not manual `\textcolor{}`

#### Professional Cross-Referencing
- [ ] All labels use systematic prefixes (`tbl:`, `fig:`, `sec:`, `subsec:`, `alg:`, `app:`)
- [ ] Labels are descriptive, not generic (`fig:system-architecture`, not `fig1`)
- [ ] Non-breaking spaces used before all citations (`~\cite{}`)
- [ ] Non-breaking spaces used before all references (`Figure~\ref{}`, `Table~\ref{}`)
- [ ] "Figure" and "Table" capitalized in cross-references
- [ ] Enhanced cross-referencing used when appropriate (`\cref{}`, `\Cref{}`)

### ✅ Reproducibility and Research Integrity

#### Technical Documentation
- [ ] Complete software version documentation provided
- [ ] Programming languages and library versions specified
- [ ] Random seeds documented for reproducible results
- [ ] Computational environment described (hardware, OS)
- [ ] Code availability statement included
- [ ] Data availability and access procedures documented

#### Experimental Design Clarity
- [ ] Dataset splits clearly described (train/validation/test)
- [ ] Sampling methods documented (stratified, random, etc.)
- [ ] Hyperparameter tuning procedures explained
- [ ] Cross-validation strategies detailed
- [ ] Baseline comparisons appropriately chosen
- [ ] Evaluation metrics justified for the task

#### Citation and Reference Quality
- [ ] Appropriate citation density throughout document
- [ ] Citations integrated with contextual analysis
- [ ] Primary sources cited for original claims
- [ ] Recent and relevant literature included
- [ ] Citation format consistent (Chicago author-date)
- [ ] Bibliography complete and properly formatted
- [ ] Self-citations used appropriately (not excessive)

### ✅ Document Structure and Organization

#### Systematic Organization
- [ ] Section hierarchy follows logical progression
- [ ] Modular appendix organization with separate files
- [ ] Consistent labeling conventions throughout
- [ ] Professional appendix system used (`documentAppendices`)
- [ ] Table of contents reflects document structure accurately

#### Version Control and Collaboration
- [ ] Meaningful commit messages for all changes
- [ ] LaTeX auxiliary files excluded from version control
- [ ] Systematic file organization with clear naming
- [ ] Regular compilation checks performed
- [ ] Shared bibliography management implemented

### ✅ Technical Quality Assurance

#### LaTeX Compilation
- [ ] Document compiles without errors in two passes
- [ ] All cross-references resolve correctly
- [ ] Appendix numbering appears correctly (A, B, C... or single "Appendix")
- [ ] Bibliography appears and formats correctly
- [ ] Mathematical expressions render properly
- [ ] Figures and tables appear in correct positions

#### Final Document Quality
- [ ] PDF meets accessibility standards
- [ ] Professional typography throughout
- [ ] Consistent spacing and alignment
- [ ] No orphaned headings or awkward page breaks
- [ ] Professional color scheme maintained
- [ ] Links and bookmarks function correctly

### ✅ Publication Readiness

#### Content Completeness
- [ ] Abstract accurately summarizes contributions
- [ ] Introduction clearly motivates the problem
- [ ] Related work demonstrates field knowledge
- [ ] Methodology enables reproduction
- [ ] Results directly address research questions
- [ ] Discussion interprets findings appropriately
- [ ] Conclusion summarizes contributions and future work

#### Professional Presentation
- [ ] Author information and affiliations complete
- [ ] Keywords representative and searchable
- [ ] Acknowledgments appropriate and complete
- [ ] Appendices provide necessary detail without cluttering main text
- [ ] Bibliography comprehensive and current
- [ ] Document length appropriate for venue

---

### Final Verification Steps

1. **Complete Compilation Test**:
   ```bash
   rm *.aux *.bbl *.bcf *.blg *.log *.out *.toc *.run.xml
   pdflatex main.tex && biber main && pdflatex main.tex && pdflatex main.tex
   ```

2. **Cross-Reference Verification**: Check all `\ref{}`, `\cite{}`, and `\cref{}` commands resolve correctly

3. **Typography Review**: Verify consistent formatting, proper emphasis, and professional appearance

4. **Academic Standards Check**: Confirm citation quality, statistical reporting, and reproducibility documentation

5. **Accessibility Verification**: Test PDF with screen readers and color-blind simulation tools

This checklist ensures your academic paper meets professional publication standards while maintaining the typography excellence of the lanepaper system.
