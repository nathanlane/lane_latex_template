# lanepaper

`lanepaper` is a LaTeX2e typography package for academic papers.
It gives ordinary LaTeX documents a considered typeface, hierarchy, spacing,
list treatment, caption style, and footnote treatment without replacing the
document structures that authors, editors, and tools already understand.

This repository contains the package, a curated visual demo, and the tests that
prove the package loads and builds.

## Status and scope

The current work is the v3 development line.
V3 is a deliberate breaking contraction: there is one public entry point and
there are no compatibility aliases for the removed v2 surface.
A v2 document needs source edits; it cannot be made current by adding a flag.
The complete replacement map is in [MIGRATION.md](MIGRATION.md).

Load the package with:

```latex
\usepackage{lanepaper}
```

The only package options are:

```latex
\usepackage[optical]{lanepaper}
\usepackage[nocolor]{lanepaper}
```

`optical` enables the sourced optical refinements.
`nocolor` keeps the hierarchy while converting the palette to grayscale.
Any other option is an error.

**CTAN status:** v3 is not yet on CTAN.
Until the maintainer announces a CTAN release, install it from this GitHub
repository or from a local checkout.

## What the package provides

- TeX Gyre Pagella text, harmonized `newpxmath` mathematics, and scaled
  Inconsolata monospace.
- Microtype's shipped Pagella protrusion and default expansion, plus restrained
  small-caps tracking.
- Styled standard sectioning commands, lists, quotations, figures, tables, and
  footnotes.
- A small title-page family for article title, author, date, abstract, keyword,
  and JEL metadata.
- A 13.2pt internal spacing quantum and 16.32pt body leading, used as
  typographic implementation details rather than a public grid API.
- Optional optical refinements and a grayscale mode, as described above.

The package configures document-owned integrations only where they contribute
to Lanepaper typography.
The document remains responsible for bibliography, language, cross-reference,
appendix, float, table-note, and page-rotation packages.

## Quick start

### Use the package in a paper

The following is a minimal package-first document.
Choose the document's bibliography, language, links, and cross-reference
packages explicitly:

```latex
\documentclass[11pt]{article}

\usepackage{csquotes}
\usepackage[backend=biber,style=authoryear]{biblatex}
\usepackage[english]{babel}
\usepackage{lanepaper}
\usepackage{hyperref}
\usepackage{cleveref}
\addbibresource{references.bib}

\begin{document}

\section{Introduction}
\sectionopening{A page should make structure easy to see,}
and the rest of the paragraph can carry the argument in ordinary prose.

\begin{itemize}
  \item Standard LaTeX structures remain the document's structure.
  \item Lanepaper supplies their typographic treatment.
\end{itemize}

\printbibliography
\end{document}
```

For a title page, the package also provides `\articletitle`,
`\articleauthors`, `\articledate`, the `articleabstract` environment,
`\articlekeywords`, and `\articlejel`.
The complete retained API is in [API_REFERENCE.md](API_REFERENCE.md).

### Build the repository demo

The demo is a visual showcase, not a template to copy for a new paper.
From the repository root:

```bash
make lint
make build
make test
```

`make build` compiles `demo/main.tex` and writes `main.pdf` at the repository
root.
The demo's `demo/preamble.tex` shows one document-owned `biblatex` setup with
Biber, English hyphenation, Hyperref, and cleveref.

## Installing from GitHub

The package is distributed from GitHub while the v3 CTAN release is pending:

```bash
git clone https://github.com/nathanlane/lane_latex_template.git
cd lane_latex_template
```

For a paper that uses a local checkout, add its package directory to the TeX
search path before compiling:

```bash
export TEXINPUTS="/path/to/lane_latex_template/lanepaper:"
pdflatex paper.tex
```

Alternatively, from the checkout, `make install` places the package in
`TEXMFHOME`; `make uninstall` reverses that installation.
Repository builds do not need an installed copy because the Makefile supplies
the local search path.

Do not install `lnp*.sty` modules directly.
They are internal owners loaded by `lanepaper.sty`, not adopter-facing entry
points.

## Supported toolchain

Lanepaper is **pdfLaTeX-only**.
XeLaTeX and LuaLaTeX stop with a package-owned error because the font stack is
8-bit and uses T1 encoding, `inputenc`, Type 1 Pagella, `newpxmath`,
`mathalfa`, and `zi4`.

The format floor is LaTeX2e `2020-10-01`.
The verified production baseline is **TeX Live 2025** at
`/usr/local/texlive/2025`, with:

- pdfTeX 1.40.28;
- latexmk 4.86a;
- Biber 2.20;
- ChkTeX 1.7.9.

Other TeX distributions may work when they provide the same LaTeX2e packages,
but TeX Live 2025 is the supported and tested baseline for this repository.

## Dependencies

The package and repository demo have separate dependency sets.
Distribution package names can group several of these LaTeX files together.

### Loaded by `lanepaper`

The seven files in `lanepaper/` are one public package and six internal
modules.
Their required LaTeX packages are:

```text
amsmath amssymb array booktabs caption enumitem etoolbox fancyhdr footmisc
fontenc geometry graphicx iftex inputenc mathalfa microtype newpxmath
textcomp tgpagella titlesec xcolor zi4
```

The font resources selected through those packages include **boondox**.
It is easy to miss in a package-load grep because
`lnpfonts.sty` selects it through the values of
`\RequirePackage[cal=boondoxo,bb=boondox,frak=boondox]{mathalfa}`.
The distribution package may be named `mathalpha` even though the LaTeX load
name is `mathalfa`.

### Added by the demo

The curated demo owns these document-level packages:

```text
babel babel-english biblatex cleveref csquotes hyperref
```

`babel-english` is also easy to miss in a package-load grep.
It is selected by `\usepackage[english]{babel}` in `demo/preamble.tex` and
provides the English language definition.
The demo's bibliography configuration requires the **Biber** executable.

### Tools for the repository workflow

The build and test gates additionally require:

- `make`;
- Python 3 with `pytest`;
- `latexmk`, `pdflatex`, and Biber;
- ChkTeX for `make lint`;
- Git for obtaining the repository.

On TeX Live or MacTeX, install missing LaTeX dependencies with `tlmgr`.
For example, the distribution names corresponding to the package set include
`latex`, `amsmath`, `amsfonts`, `tools`, `graphics`, `booktabs`, `boondox`,
`caption`, `enumitem`, `etoolbox`, `fancyhdr`, `footmisc`, `geometry`, `iftex`,
`mathalpha`, `microtype`, `newpx`, `tex-gyre`, `titlesec`, `xcolor`,
`inconsolata`, `babel`, `babel-english`, `biblatex`, `cleveref`, `csquotes`,
`hyperref`, and `biber`.
Use the package manager's current name when a distribution bundles or renames
one of these files.

## Document ownership

The package deliberately does not load every package a paper might need.
Load these in the document when their features are wanted:

| Need | Document-owned package or structure |
| --- | --- |
| Bibliography | `biblatex` and Biber, or another explicitly chosen backend |
| Language and hyphenation | `babel` with the language definitions required by the paper |
| Hyperlinks | `hyperref` |
| Smart cross-references | `cleveref` |
| Table notes | `threeparttable` |
| Wide-page rotation | `pdflscape` and its standard `landscape` environment |
| Appendices | Standard `\appendix` and ordinary sectioning |

This boundary keeps `\usepackage{lanepaper}` predictable and avoids making a
typography package own document policy.
See [CONVENTIONS.md](CONVENTIONS.md) for the configure-if-loaded rule and
[MIGRATION.md](MIGRATION.md) for v2 replacements.

## Typography guidance

Use standard LaTeX structures in the paper:

```latex
\begin{quote}
  A quotation can change the measure without changing the document model.
\end{quote}

\begin{table}[tbp]
  \caption{A table caption belongs above the table.}
  \centering
  \begin{tabular}{@{}lr@{}}
    \toprule
    Measure & Value \\
    \midrule
    Example & 1.0 \\
    \bottomrule
  \end{tabular}
\end{table}

\begin{figure}[tbp]
  \centering
  \includegraphics[width=.7\textwidth]{figures/example}
  \caption{A figure caption belongs below the figure.}
\end{figure}
```

Tables use `booktabs` rules without vertical lines.
Figures use standard `figure` and `\includegraphics`.
The package also retains the `lanepaperfigurenotes` environment for a
collision-safe note block attached to a figure.

For mathematics, use `amsmath` environments and standard notation such as
`\mathbb{R}`, `\lVert x\rVert`, and `\DeclareMathOperator`.
For emphasis and quotations, use standard LaTeX commands and environments.
The package's public commands and their signatures are listed in
[API_REFERENCE.md](API_REFERENCE.md); private `\lnp@...` names are not a
document interface.

## Repository layout

```text
lanepaper/              package entry point and internal modules
demo/                   curated visual showcase and its bibliography
tests/                  pytest contracts and LaTeX fixture harness
API_REFERENCE.md        retained v3 API
MIGRATION.md            v2-to-v3 replacement guide
```

The demo is the visual proof of the package.
The test layout and accepted warnings are documented in
[tests/README.md](tests/README.md).

## Troubleshooting

Start with [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
In particular, if Biber exits with status 2 and an empty error log, search for
`Unicode::UCD: failed to find unicore/version`; the guide documents the
macOS PAR-cache repair.

For a v2 paper that fails after loading v3, read
[MIGRATION.md](MIGRATION.md) before adding packages or redefining commands.

## Contributing

Run the same three gates used by CI:

```bash
make lint
make build
make test
```

Package code follows [CONVENTIONS.md](CONVENTIONS.md).
Document-source style and the ownership boundary are in
[CONTRIBUTING.md](CONTRIBUTING.md).
Do not run the CTAN build while the maintainer's CTAN hold is active.

## Licensing

The files in `lanepaper/` are licensed under LPPL 1.3c.
The other original repository files are MIT, under
[`licenses/LICENSE-MIT.txt`](licenses/LICENSE-MIT.txt).

The project is not yet a CTAN release.
GitHub distribution and a later CTAN publication are separate release steps.
