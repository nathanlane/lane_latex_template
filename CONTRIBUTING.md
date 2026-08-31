# Contributing to lanepaper

## Building

```bash
make build    # compile demo/main.tex → main.pdf
make clean    # remove generated output, the PDF included
make help     # list every target
```

The verified baseline is TeX Live 2025 with pdfLaTeX, latexmk, Biber, and
ChkTeX.
The authoritative package, demo, and tool dependency lists are in
[README.md](README.md#dependencies).

## Pre-commit Gates

All three must pass before committing, and they are exactly what CI runs:

```bash
make lint     # ChkTeX on the demo sources
make build    # latexmk full compile → main.pdf
make test     # python3 -m pytest -q, then bash tests/run-tests.sh
```

`make test` runs both harnesses because issue #51 removed the four separate
test targets: what CI runs and what you run can no longer drift apart. The
shell harness is documented in [`tests/README.md`](tests/README.md).

## Package Namespace Convention

The package is `lanepaper`; its modules use the `lnp` prefix:

- Main style: `lanepaper` (`lanepaper/lanepaper.sty`)
- Modules: `lnpcolors`, `lnpfonts`, `lnpdimensions`, `lnpheadings`,
  `lnplists`, `lnpmicrotype`.

Load only the public package by name:

```latex
\usepackage{lanepaper}                  % the sole public load path
\usepackage[optical,nocolor]{lanepaper} % the two supported options
```

Do not load an `lnp*.sty` module directly.
The modules are internal owners loaded by `lanepaper`.

How package code is written -- naming, message policy, robustness, hooks, lint
policy, and the rule against `\makeatletter` in a `.sty` -- is in
[`CONVENTIONS.md`](CONVENTIONS.md). Read it before changing anything in
`lanepaper/`.

Internal LaTeX identifiers (lengths, counters, private commands) use the
`\lnp@` prefix to avoid conflicts. `CONVENTIONS.md` section 3 is the full
convention; there is no second naming document.

## Module Documentation

- Commands, systems and typography standards: [`API_REFERENCE.md`](API_REFERENCE.md)
- Module list and dependencies: [`CONVENTIONS.md`](CONVENTIONS.md) section 3
- Testing guide: [`tests/README.md`](tests/README.md)

## Document source style

This document codifies the LaTeX source code formatting standards for this project, ensuring consistency, maintainability, and professional quality.

### Core Formatting Principles

#### 1. Line Length and Breaking
- **One sentence per line** for clean version control diffs
- **Maximum line length:** 100 characters for code examples
- **Break long commands** at logical points with proper indentation

#### 2. Indentation
- **Use 2 spaces** for all environment indentation
- **No tabs** - configure editor to convert tabs to spaces
- **Align environment delimiters** vertically

```latex
\begin{itemize}
  \item First item with proper indentation
  \item Second item maintaining consistency
  \begin{enumerate}
    \item Nested with additional 2-space indent
    \item Maintaining hierarchical structure
  \end{enumerate}
\end{itemize}
```

#### 3. Spacing Conventions

##### Vertical Spacing
- **Single blank line** between major sections
- **No blank lines** within environments
- **Double blank line** before `\section` commands (optional for clarity)

##### Horizontal Spacing
- **Space after commas** in lists: `{item1, item2, item3}`
- **Space around operators** in math: `$x = y + z$` not `$x=y+z$`
- **No space before punctuation** in text mode

#### 4. Comments
- **Use `%` followed by single space** for comments
- **Section dividers:** 80 character lines of `%` for major sections
- **Inline comments:** Align to column 50+ when possible

```latex
\section{Introduction}  % Major section beginning
\label{sec:intro}       % Systematic label

% This comment explains the following complex command
\somecommand[option1,   % First option explanation
            option2]    % Second option explanation
           {argument}
```

#### 5. Mathematical Typography

##### Inline Mathematics
- **Use `$...$`** for inline math (not `\(...\)`)
- **Add thin spaces** around operators when needed: `$x\,=\,y$`
- **Standard amsmath notation** for common constructs: `\mathbb{R}`, `\lVert x\rVert`.
  See [MIGRATION.md](MIGRATION.md) when converting older documents.

##### Display Mathematics
- **Use `\[...\]`** for unnumbered display equations
- **Use `equation` environment** for numbered equations
- **Align multi-line equations** properly:

```latex
\begin{align}
  f(x) &= ax^2 + bx + c \\
       &= a(x - h)^2 + k
\end{align}
```

#### 6. Environments and Commands

##### Environment Usage
```latex
\begin{figure}[tbp]  % Always use [tbp] placement
  \centering
  \includegraphics[width=0.8\textwidth]{figures/example.pdf}
  \caption{Descriptive Caption Below Figure}  % Caption BELOW for figures
  \label{fig:descriptive-name}
\end{figure}

\begin{table}[tbp]
  \caption{Table Caption Above Content}  % Caption ABOVE for tables
  \label{tab:descriptive-name}
  \centering
  \begin{tabular}{@{}lrr@{}}  % Remove outer column spacing
    \toprule
    % Table content
    \bottomrule
  \end{tabular}
\end{table}
```

##### Custom Commands
- **Define in preamble** or separate style file
- **Use descriptive names**: `\articletitle` not `\mytitle`
- **Document with comments**:

```latex
% A document-specific command with a descriptive name
% Usage: \paperhighlight{Your highlighted text}
\newcommand{\paperhighlight}[1]{%
  {\bfseries #1\par}%
  \vspace{1em}%
}
```

#### 7. Labeling Conventions

Systematic prefixes for all labels:

| Element | Prefix | Example |
|---------|--------|---------|
| Section | `sec:` | `\label{sec:introduction}` |
| Subsection | `subsec:` | `\label{subsec:methodology}` |
| Figure | `fig:` | `\label{fig:results-plot}` |
| Table | `tab:` | `\label{tab:summary-stats}` |
| Equation | `eq:` | `\label{eq:main-model}` |
| Algorithm | `alg:` | `\label{alg:optimization}` |
| Appendix | `app:` | `\label{app:technical}` |

#### 8. Citation Style
- **Narrative citations** use `\textcite`: `results~\textcite{author2023}`
- **Parenthetical citations** use `\autocite`: `the result~\autocite{author2023}`
- **Page numbers** use a double dash: `\autocite[45--48]{author2023}`
- **Multiple citations** are comma-separated: `\autocite{smith2023,jones2023}`

#### 9. Special Characters
- **Quotation marks**: Use `\enquote{text}` for smart quotes
- **Dashes**: hyphen `-`, en-dash `--`, em-dash `---`
- **Ellipsis**: Use `\ldots` not `...`
- **Percent**: Use `\%` in text mode

#### 10. Package Loading Order

Keep document-owned packages explicit and load links after the packages they
refer to:
```latex
% 1. Document class options
\documentclass[11pt]{article}

% 2. Document-owned language and bibliography
\usepackage{csquotes}
\usepackage{biblatex}
\usepackage[english]{babel}

% 3. Typography
\usepackage{lanepaper}

% 4. Links and cross-references
\usepackage{hyperref}
\usepackage{cleveref}
```

### File Organization

#### LaTeX Source Files
- **Curated demo**: `demo/main.tex`
- **Package entry point**: `lanepaper/lanepaper.sty`
- **Preamble**: `demo/preamble.tex`
- **Title page**: `demo/titlepage.tex`

#### Package Loading Convention
- Main package: `\usepackage{lanepaper}`
- Internal modules: `\RequirePackage{lnpcolors}`, `\RequirePackage{lnpfonts}`, etc.
- Documents must not load the internal modules directly.

#### Naming Conventions
- **Use lowercase** with hyphens: `main-appendix.tex`
- **Descriptive names**: `regression-results.tex` not `table1.tex`
- **No spaces** in filenames

### Quality Checklist

Before committing LaTeX files:

- [ ] One sentence per line
- [ ] Proper 2-space indentation
- [ ] Systematic labels with correct prefixes
- [ ] Non-breaking spaces before citations/references
- [ ] Consistent math spacing
- [ ] No unexpected overfull hboxes (check log)
- [ ] All floats use [tbp] placement
- [ ] Captions above tables, below figures
- [ ] Comments explain complex constructs
- [ ] Package loading order maintained

### Common Pitfalls to Avoid

1. **Don't use `[h]` float placement** - causes poor page layout
2. **Don't use vertical lines in tables** - violates booktabs principles
3. **Don't hide document-owned spacing** - use an explicit `\vspace` length
4. **Don't use `\\` for line breaks** in text - proper paragraph breaks
5. **Don't mix `\cite` and `\autocite`** - choose one citation style

### Validation Tools

Run these checks before finalizing:

```bash
make lint
make build
make test
```

---

*This document is part of the lanepaper project style guide.*
