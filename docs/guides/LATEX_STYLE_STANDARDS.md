# LaTeX Style Standards for East Asian Miracle Paper

This document codifies the LaTeX source code formatting standards for this project, ensuring consistency, maintainability, and professional quality.

## Core Formatting Principles

### 1. Line Length and Breaking
- **One sentence per line** for clean version control diffs
- **Maximum line length:** 100 characters for code examples
- **Break long commands** at logical points with proper indentation

### 2. Indentation
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

### 3. Spacing Conventions

#### Vertical Spacing
- **Single blank line** between major sections
- **No blank lines** within environments
- **Double blank line** before `\section` commands (optional for clarity)

#### Horizontal Spacing
- **Space after commas** in lists: `{item1, item2, item3}`
- **Space around operators** in math: `$x = y + z$` not `$x=y+z$`
- **No space before punctuation** in text mode

### 4. Comments
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

### 5. Mathematical Typography

#### Inline Mathematics
- **Use `$...$`** for inline math (not `\(...\)`)
- **Add thin spaces** around operators when needed: `$x\,=\,y$`
- **Semantic commands** for common constructs: `\real`, `\norm{x}`

#### Display Mathematics
- **Use `\[...\]`** for unnumbered display equations
- **Use `equation` environment** for numbered equations
- **Align multi-line equations** properly:

```latex
\begin{align}
  f(x) &= ax^2 + bx + c \\
       &= a(x - h)^2 + k
\end{align}
```

### 6. Environments and Commands

#### Environment Usage
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

#### Custom Commands
- **Define in preamble** or separate style file
- **Use descriptive names**: `\articletitle` not `\mytitle`
- **Document with comments**:

```latex
% Professional title formatting with modular scale sizing
% Usage: \articletitle{Your Title Here}
\newcommand{\articletitle}[1]{%
  {\fontsize{18pt}{22pt}\selectfont\bfseries #1\par}%
  \vspace{\titlespacemajor}%
}
```

### 7. Labeling Conventions

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

### 8. Citation Style
- **Non-breaking space** before citations: `results~\cite{author2023}`
- **Page numbers** with double dash: `\cite[45--48]{author2023}`
- **Multiple citations** comma-separated: `\cite{smith2023,jones2023}`

### 9. Special Characters
- **Quotation marks**: Use `\enquote{text}` for smart quotes
- **Dashes**: hyphen `-`, en-dash `--`, em-dash `---`
- **Ellipsis**: Use `\ldots` not `...`
- **Percent**: Use `\%` in text mode

### 10. Package Loading Order

Maintain systematic order in preamble:
```latex
% 1. Document class options
\documentclass[11pt]{article}

% 2. Encoding and fonts
\usepackage[T1]{fontenc}
\usepackage{tgpagella}

% 3. Layout and geometry  
\usepackage{geometry}

% 4. Typography packages
\usepackage{microtype}

% 5. Math packages
\usepackage{amsmath,amssymb}

% 6. Graphics and tables
\usepackage{graphicx}
\usepackage{booktabs}

% 7. Bibliography
\usepackage{biblatex}

% 8. hyperref (must be near end)
\usepackage{hyperref}

% 9. cleveref (must be after hyperref)
\usepackage{cleveref}
```

## File Organization

### LaTeX Source Files
- **Main document**: `main.tex`
- **Style definitions**: `lltpaperstyle.sty` (formerly `paper/paperstyle.sty`)
- **Preamble**: `paper/preamble.tex`
- **Title page**: `paper/titlepage.tex`
- **Appendices**: `appendices/*.tex`

### Package Loading Convention
As of July 2025, the Lane LaTeX Template uses a new naming convention:
- Main package: `\usepackage{lltpaperstyle}` (not `\usepackage{paper/paperstyle}`)
- Modules: `\RequirePackage{lltcolors}`, `\RequirePackage{lltfonts}`, etc.
- No path prefixes needed with the new naming system

### Naming Conventions
- **Use lowercase** with hyphens: `main-appendix.tex`
- **Descriptive names**: `regression-results.tex` not `table1.tex`
- **No spaces** in filenames

## Quality Checklist

Before committing LaTeX files:

- [ ] One sentence per line
- [ ] Proper 2-space indentation
- [ ] Systematic labels with correct prefixes
- [ ] Non-breaking spaces before citations/references
- [ ] Consistent math spacing
- [ ] No overfull hboxes (check log)
- [ ] All floats use [tbp] placement
- [ ] Captions above tables, below figures
- [ ] Comments explain complex constructs
- [ ] Package loading order maintained

## Common Pitfalls to Avoid

1. **Don't use `[h]` float placement** - causes poor page layout
2. **Don't use vertical lines in tables** - violates booktabs principles
3. **Don't hardcode spacing** - use systematic commands
4. **Don't use `\\` for line breaks** in text - proper paragraph breaks
5. **Don't mix `\cite` and `\autocite`** - choose one citation style

## Validation Tools

Run these checks before finalizing:

```bash
# Check for common LaTeX issues
lacheck main.tex

# Check for style compliance
chktex main.tex

# Ensure clean compilation
pdflatex main.tex && echo "Success"
```

---

*This document is part of the East Asian Miracle Paper project style guide.*