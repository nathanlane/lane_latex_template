# Simplification Example: Quote System

This example shows how we can reduce brittleness and complexity while keeping all features.

## Current Implementation (Complex)

```latex
% 4 separate environments with duplicated code:

\renewenvironment{quote}{%
  \vspace{13.2pt}%     % Hardcoded grid value
  \begin{list}{}{%
    \setlength{\leftmargin}{26.4pt}%       % Hardcoded
    \setlength{\rightmargin}{26.4pt}%      % Hardcoded
    \setlength{\topsep}{0pt}%
    \setlength{\partopsep}{0pt}%
    \setlength{\parsep}{6.6pt}%            % Hardcoded
    \setlength{\itemsep}{0pt}%
    \setlength{\listparindent}{\parindent}%
    \fontsize{10.5}{13.2}\selectfont%      % Hardcoded
    \color{quotegray}%
  }%
  \item\relax
}{%
  \endlist
  \vspace{13.2pt}%     % Hardcoded
  \@afterindentfalse%
}

\renewenvironment{quotation}{%
  % ... nearly identical code with minor differences ...
}

\newenvironment{emphasisquote}{%
  % ... nearly identical code with different spacing ...
}

\newenvironment{blockquote}{%
  % ... nearly identical code ...
}

% Plus attribution command:
\newcommand{\quoteattribution}[1]{%
  \par\vspace{6.6pt}%  % Hardcoded
  \hfill\textemdash\space\fontsize{10}{12}\selectfont\color{gray}#1%
}
```

## Simplified Implementation (Robust)

```latex
% Single parameterized environment with all features:

\NewDocumentEnvironment{blockquote}{O{} m}{%
  % Parse options with defaults
  \setkeys{blockquote}{%
    spacing=normal,
    style=standard,
    indent=2,
    color=quotegray,
    size=0.95,
    #1%  % User options
  }%
  
  % Calculate based on grid unit
  \vspace{\blockquote@before\gridunit}%
  \begin{list}{}{%
    \setlength{\leftmargin}{\blockquote@indent\gridunit}%
    \setlength{\rightmargin}{\blockquote@indent\gridunit}%
    \setlength{\topsep}{0pt}%
    \setlength{\partopsep}{0pt}%
    \setlength{\parsep}{\blockquote@parsep\gridunit}%
    \setlength{\itemsep}{0pt}%
    \IfStrEq{\blockquote@style}{quotation}{%
      \setlength{\listparindent}{\parindent}%
    }{%
      \setlength{\listparindent}{0pt}%
    }%
    \fontsize{\blockquote@size\@ptsize}{\gridunit}\selectfont%
    \color{\blockquote@color}%
    \blockquote@style@hook%  % For custom styling
  }%
  \item\relax
  #2%  % Quote content
}{%
  \endlist
  \vspace{\blockquote@after\gridunit}%
  \IfValueT{\blockquote@attribution}{%
    \par\vspace{0.5\gridunit}%
    \hfill\textemdash\space
    \fontsize{0.9\@ptsize}{\gridunit}\selectfont
    \color{gray}\blockquote@attribution%
  }%
  \@afterindentfalse%
}

% Define style presets:
\define@key{blockquote}{style}{%
  \IfStrEqCase{#1}{%
    {standard}{%
      \def\blockquote@indent{2}%
      \def\blockquote@before{1}%
      \def\blockquote@after{1}%
      \def\blockquote@parsep{0.5}%
    }%
    {emphasis}{%
      \def\blockquote@indent{3}%
      \def\blockquote@before{1.5}%
      \def\blockquote@after{1.5}%
      \def\blockquote@parsep{0.5}%
      \def\blockquote@style@hook{\itshape}%
    }%
    {compact}{%
      \def\blockquote@indent{1.5}%
      \def\blockquote@before{0.5}%
      \def\blockquote@after{0.5}%
      \def\blockquote@parsep{0}%
    }%
  }[% Default
    \def\blockquote@indent{2}%
    \def\blockquote@before{1}%
    \def\blockquote@after{1}%
    \def\blockquote@parsep{0.5}%
  ]%
}

% Optional attribution:
\define@key{blockquote}{attribution}{\def\blockquote@attribution{#1}}

% Backward compatibility:
\newenvironment{quote}{\begin{blockquote}}{\end{blockquote}}
\newenvironment{quotation}{\begin{blockquote}[style=quotation]}{\end{blockquote}}
\newenvironment{emphasisquote}{\begin{blockquote}[style=emphasis]}{\end{blockquote}}
```

## Usage Examples

```latex
% Simple quote (same as before):
\begin{blockquote}
  Typography exists to honor content.
\end{blockquote}

% Quote with attribution:
\begin{blockquote}[attribution={Robert Bringhurst}]
  Typography exists to honor content.
\end{blockquote}

% Emphasis quote:
\begin{blockquote}[style=emphasis]
  This is a key point that deserves special attention.
\end{blockquote}

% Custom configuration:
\begin{blockquote}[
  style=emphasis,
  color=darkgray,
  size=1.1,
  attribution={Custom Author}
]
  A fully customized quotation with all features.
\end{blockquote}

% Old syntax still works:
\begin{quote}
  Backward compatible!
\end{quote}
```

## Benefits of This Approach

### 1. Single Point of Truth
- Grid values defined once
- Spacing relationships clear
- Easy to modify globally

### 2. Feature Complete
- All original features available
- Actually MORE flexible
- Attribution built-in

### 3. Less Code
- 4 environments → 1
- ~200 lines → ~80 lines
- No duplicated logic

### 4. More Robust
- Grid-relative sizing
- Parameterized options
- Graceful defaults

### 5. Better User Experience
- Intuitive key-value options
- Mix and match features
- Backward compatible

### 6. Easier Maintenance
- Change behavior in one place
- Add new styles easily
- Clear structure

## This Pattern Applies To:

1. **List environments** - One configurable list instead of 7
2. **Emphasis commands** - One with style parameter instead of 6
3. **Spacing commands** - One with multiplier instead of 10
4. **Section commands** - One with level parameter
5. **Float helpers** - Trust LaTeX or one smart command

## Conclusion

By parameterizing instead of proliferating, we can:
- Reduce code by 60-70%
- Make the system more flexible
- Eliminate brittleness
- Keep all features
- Actually improve usability

This is the path to a robust, maintainable framework.