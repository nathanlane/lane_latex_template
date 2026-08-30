# Lane LaTeX Template

A living LaTeX template for academic papers with optimized typography. Actively used and revised.

This template applies classic typographic principles to create scholarly articles. For more on typography principles: [https://github.com/nathanlane/nathanstypographynotes/](https://github.com/nathanlane/nathanstypographynotes/)


---

## ✨ Features

<!-- %% FIX: Keep active feature claims limited to locally verified support. -->
- **Typography** – TeX Gyre Pagella (Palatino-based) with superior small caps, harmonized mathematics, and optimized monospace
- **Spacing Quantum System** – most vertical spacing in multiples of a 13.2pt quantum; body leading measures 16.32pt (see `docs/adr/0004-baseline-grid-is-a-spacing-quantum.md`)
- **Optical Refinements** – The `[optical]` option adds sourced refinements over the defaults, currently last-line runt control (`\parfillskip`)
- **Dynamic Title Page** – Mathematical spacing with golden ratio proportions
- **Document-owned Citations** – load and configure `biblatex` or `natbib` in your document; lanepaper does not load either
- **Floats** – Standard figure/table environments with styled captions and required booktabs rules
- **Lists and Quotes** – Styled standard environments plus one inline list for brief enumerations
- **Color Hierarchy** – restrained roles for text, headings, supporting elements, and links
- **Local Build Workflow** – Verified with local `latexmk`, ChkTeX, pytest, and shell-harness gates

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
make build            # Creates main.pdf
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
- **[Licensing](#licensing)** – License scope and notices
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

### Tested Build Environments

<!-- %% FIX: Keep the documented toolchain tied to the supported CI baseline. -->
Verified locally on August 30, 2026 using **TeX Live 2025** at
`/usr/local/texlive/2025` (all gates: `make lint`, `make build`, `make test`):

- pdfTeX 1.40.28, `latexmk` 4.86a, Biber 2.20, and ChkTeX 1.7.9.

### Quick Setup

```bash
# Install missing packages from the authoritative lists in INSTALL.md.

# Test compilation
make lint
make build
make test
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
   \usepackage[backend=biber,style=authoryear]{biblatex}
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
make build        # Compile the demo document
make clean        # Remove generated output, the PDF included
make lint         # Check the demo sources with ChkTeX
make test         # Run pytest, then the shell harness
make help         # List every target
```

**Repository verification gates**:

```bash
make lint
make build
make test
```

**Direct compilation of the demo**:
```bash
latexmk -pdf -interaction=nonstopmode demo/main.tex
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

**The document owns its bibliography.** The package does not load `biblatex`,
`natbib`, `hyperref`, `cleveref`, `babel` or `appendix`. Bibliography,
cross-reference and appendix packages are entirely document-owned. If loaded,
lanepaper only applies its link styling to `hyperref` and its caption width to
`longtable`; nothing here dictates your citation style.

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

The removed `nobiblatex` and `natbib` package options raise LaTeX's `Unknown
option` error. Load the bibliography package you need in the document instead.

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

**Professional table** (note caption placement and absence of vertical rules):
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
\end{table}
```

For table notes, load `threeparttable` in the document and use its native
`threeparttable` and `tablenotes` environments. `lanepaper` neither loads that
package nor changes `tablenotes`.

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

`\usepackage{lanepaper}` is the only public load path, and it takes two
options:

```latex
\usepackage{lanepaper}             % Standard
\usepackage[optical]{lanepaper}    % Add the sourced optical refinements
\usepackage[nocolor]{lanepaper}    % Grayscale hierarchy, no chroma
```

- `optical` – Optical refinements that have a stated source but are not safe
  to impose on every document. Currently runt control: the last line of a
  paragraph is made to reach at least a third of the measure (Hochuli,
  *Detail in Typography*), at the cost of rebreaking the paragraph. Widow and
  orphan protection is *not* here — that is a default every document gets.
- `nocolor` – Converts the palette through xcolor's gray model. Chroma goes;
  the grayscale hierarchy between heading levels stays.

Anything else is rejected with LaTeX's own `Unknown option` error. v3 removed
the v2 template modes — `grid`, `minimal`, `draft`, `natbib`, `nobiblatex`
and the subsection-barrier pair — without aliases. See
[ADR-0006](docs/adr/0006-one-public-entry-point-and-a-narrow-v3-interface.md).

### Internal Modules

The `lnp*.sty` files are internal owners, not entry points. Loading one
directly is unsupported: they assume `lanepaper` has already set up the
options and load order, and they may be merged or renamed without notice.

| Module | Owns |
|---|---|
| `lnpcolors` | The semantic colour palette |
| `lnpdimensions` | Page geometry, the 13.2pt spacing quantum, and block quotations |
| `lnpfonts` | The Pagella / newpxmath / Inconsolata stack |
| `lnpheadings` | Section heading typography |
| `lnplists` | List typography |
| `lnpmicrotype` | Upstream Pagella protrusion and expansion; small-caps tracking |

---

## Typography System

### Font Configuration

The template uses a carefully selected font stack:

- **Text**: TeX Gyre Pagella (enhanced Palatino)
- **Math**: newpxmath (harmonized with Pagella)
- **Code**: Inconsolata (scaled to 96%)
- **Features**: Real small caps, lining tabular figures by default, ligatures

Microtype uses its shipped Pagella protrusion and default expansion tables.
The package adds only +50 tracking for Pagella small caps. Oldstyle tabular
figures are private to page numbers, top-level list labels, and body-footnote
marks.

### Spacing Quantum

The package states nearly all of its vertical spacing in multiples of one
13.2pt quantum (a spacing unit — the body baseline measures 16.32pt). It is
an internal implementation value, not a grid API: there is no public
`\gridunit` length and no grid helpers. A document that wants a specific
gap writes it:

```latex
\vspace{13.2pt}   % One quantum
\vspace{6.6pt}    % Half a quantum
```

### Emphasis

Use the standard LaTeX emphasis commands:

```latex
\emph{emphasis}           % Italic (toggles in nested context)
\textbf{critical}         % Bold for critical terms
\textsc{Hermann Zapf}     % Person names, acronyms (small caps)
\textit{Book Title}       % Published works
```

> v3 removed the generic `\strongemph`, `\term`, `\person`, `\acro`, `\work`,
> and `\critical` helpers; use the standard commands above (see API_REFERENCE.md
> "Removed in v3").

### Special Characters

Use standard LaTeX and `textcomp`/`csquotes`:

```latex
Typography---the art---is essential   % Em dash
Pages 10--20                          % En dash for ranges
25\textdegree C                       % Degree symbol (textcomp)
\texteuro 100                         % Currency (textcomp)
\copyright 2025                       % Legal symbols
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

### Appendices

Use standard LaTeX appendix mode:

```latex
\appendix
\section{Main Appendix}
\input{appendices/main_appendix.tex}

\section{Technical Appendix}
\input{appendices/tech_appendix.tex}
```

Load an appendix package yourself if the document needs features beyond
standard `\appendix` behavior.

### Mathematical Typography

Optimized for academic papers:

```latex
% Display equations with quantum-derived spacing
\begin{equation}
  f(x) = \int_{-\infty}^{\infty} g(t) e^{-2\pi i x t} \, dt
\end{equation}

% Standard amsmath notation
$x \in \mathbb{R}$              % Real numbers
$\lVert v\rVert = 1$           % Vector norm
$\lvert x\rvert < \epsilon$    % Absolute value
```

> v3 removed the generic `\real`, `\norm`, `\abs`, ... math helpers; use amsmath
> notation and `\DeclareMathOperator` (see API_REFERENCE.md "Removed in v3").

---

## Advanced Customization

### Color Customization

The document owns custom colours:

```latex
\usepackage{lanepaper}
\definecolor{myaccent}{RGB}{0,0,255}
\newcommand{\myaccenttext}[1]{\textcolor{myaccent}{#1}}
```

### Layout Modifications

Adjust margins and spacing:

```latex
\usepackage{lanepaper}
\geometry{margin=2in}                      % Wider margins
\setlength{\parindent}{2em}                % Larger indent
```

### Creating Extensions

Add custom commands in your preamble:

```latex
% After loading lanepaper
\newcommand{\mycommand}[1]{\textcolor{myaccent}{\textbf{#1}}}
\newenvironment{myenv}{\begin{quote}}{\end{quote}}
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
make build        # Full rebuild
```

**Font issues**: check that TeX Gyre Pagella, `newpxmath` and `zi4` are
installed; see the [Required LaTeX Packages](INSTALL.md#required-latex-packages)
section in the installation guide.

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

1. **Typography first**: Don't introduce spacing values off the quantum scale
2. **Test everything**: Run `make test` before commits
3. **Document changes**: Update relevant documentation
4. **Follow style**: One sentence per line in LaTeX

### Testing

```bash
make test         # pytest, then the shell harness
make lint         # ChkTeX over the demo sources
```

### Pull Request Process

1. Fork and create a feature branch
2. Make changes and test thoroughly
3. Update documentation if needed
4. Submit PR with clear description

---

## Licensing

The `lanepaper/` directory is the licensed Work under LPPL 1.3c. The root
[`LICENSE`](LICENSE) is the verbatim LPPL text, and the LPPL scope is limited
to those package files; each one carries its LPPL header.

Every other original project file — including `demo/`, `docs/`, `tests/`, the
`Makefile`, `build.lua`, and the repository documentation — is MIT, copyright
2025-2026 Nathan Lane. See [`licenses/LICENSE-MIT.txt`](licenses/LICENSE-MIT.txt).

The `licenses/LICENSE.txt` file is only the LPPL header template for the
package files and does not expand the licensed Work.

## Technical Reference

### Documentation

- **[API Reference](API_REFERENCE.md)** – Complete command reference
- **[Typography standards](API_REFERENCE.md)** – how to use the system well
- **[Testing Guide](tests/README.md)** – Test framework documentation

### Key Commands

**Typography** (standard LaTeX):
```latex
\emph{}, \textbf{}, \textit{}, \textsc{}, \texttt{}
---, --, \textdegree, \texteuro, \textpm
```

**Structure**:
```latex
\articletitle{}, \articleauthors{}, \articledate{}
\begin{articleabstract}, \articlekeywords{}, \articlejel{}
\sectionopening{Opening words} continuing in the same paragraph
\appendix
```

**Document-owned bibliography and reference commands**:
```latex
\textcite{}, \autocite{}, \cref{}, \Cref{}
```

**Standard and package environments**:
```latex
itemize, enumerate, description, quote, quotation
table, figure, inlineitem, lanepaperfigurenotes
```

The demo's landscape helpers are example-local, not package APIs.

### Dependencies

Package-loaded typography dependencies:
- `tgpagella` – TeX Gyre Pagella fonts
- `newpxmath` – Mathematics
- `booktabs` – Professional tables
- `microtype` – Pagella protrusion, default expansion, and small-caps tracking

Document-owned (load them yourself when needed):
- `biblatex` – Bibliography
- `cleveref` – Smart cross-references
- `threeparttable` – Table-note structure
- `appendix` – Optional appendix features beyond standard `\appendix`

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
- [ ] Emphasis uses `\emph{}` (italic); strong emphasis uses `\textbf{}`
- [ ] Small caps use standard `\textsc{}`
- [ ] Mathematical notation uses amsmath (`\mathbb{R}`, `\lVert\,\rVert`, `\lvert\,\rvert`, `\DeclareMathOperator`)
- [ ] Code typography uses `\texttt{}`
- [ ] Colors use the palette's semantic color names, not manual `\textcolor{}`

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
- [ ] Standard `\appendix` structure used consistently
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
