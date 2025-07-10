# Lists Module Documentation

## Overview

The lists module (`lists.sty`) implements sophisticated list typography with multiple styles, perfect grid alignment, and professional aesthetics.

## List Types

### Standard Lists

#### Itemize (Bullets)
```latex
\begin{itemize}
\item First item with gray bullet
\item Second item
  \begin{itemize}
  \item Nested with en-dash
  \item Another nested item
  \end{itemize}
\end{itemize}
```

#### Enumerate (Numbers)
```latex
\begin{enumerate}
\item First item with oldstyle numeral
\item Second item
  \begin{enumerate}
  \item Nested with letter (a)
  \item Another nested (b)
  \end{enumerate}
\end{enumerate}
```

#### Description (Terms)
```latex
\begin{description}
\item[Term] Definition with small caps label
\item[Concept] Extended explanation
\end{description}
```

### Specialized List Environments

#### Compact Lists
Minimal spacing for dense information:
```latex
\begin{compactitem}
\item Reference one
\item Reference two
\item Reference three
\end{compactitem}
```

#### Display Lists
Emphasized items with generous spacing:
```latex
\begin{displayitem}
\item \textbf{Key Finding:} Important result
\item \textbf{Innovation:} Novel contribution
\end{displayitem}
```

#### Academic Lists
En-dash bullets following university style:
```latex
\begin{academicitem}
\item First scholarly point
\item Second scholarly point
\end{academicitem}
```

#### Readable Lists
Enhanced spacing for improved readability:
```latex
\begin{readableitem}
\item First point with breathing room
\item Second point clearly separated
\end{readableitem}
```

#### Inline Lists
For brief enumerations within text:
```latex
The three principles are:
\begin{inlineitem}
\item clarity
\item consistency  
\item precision
\end{inlineitem}.
```

## List Customization

### Global Spacing Commands

Change spacing for all lists:
```latex
\tightlists      % Minimal spacing
\normallists     % Default spacing (restore)
\spaciouslists   % Generous spacing
```

### Bullet Style Commands

Change bullet appearance globally:
```latex
\dashbullets      % Switch to en-dashes
\trianglebullets  % Switch to triangles
\defaultbullets   % Restore gray bullets
```

### Manual Bullet Control
```latex
\begin{itemize}
\itembullet First item with bullet
\itemdash Second item with dash
\itemdiamond Third item with diamond
\itemsquare Fourth item with square
\itemtriangle Fifth item with triangle
\end{itemize}
```

## Spacing System

All list spacing aligns to the baseline grid (13.2pt):

| Spacing Type | Value | Grid Units |
|--------------|-------|------------|
| Item separation | 3.3pt | 0.25 units |
| List top/bottom | 6.6pt | 0.5 units |
| Nested indent | 13.2pt | 1 unit |
| Hanging indent | 26.4pt | 2 units |

## Typography Details

### Bullet Hierarchy
1. **Level 1**: Gray bullet (scaled 90%)
2. **Level 2**: Gray en-dash
3. **Level 3**: Gray diamond (scaled 70%)

### Number Styles
- **Level 1**: Oldstyle figures with period
- **Level 2**: Lowercase letters with parenthesis
- **Level 3**: Lowercase roman numerals with period

### Label Formatting
- **Description**: Small caps with 15% gray
- **Display**: Bold text
- **Academic**: Regular text with en-dash

## Advanced Usage

### Custom List Definitions
```latex
% Create a new list type
\newlist{mylist}{itemize}{3}
\setlist[mylist,1]{
  label=\textcolor{sectioncolor}{$\star$},
  leftmargin=2em,
  itemsep=\halfgridunit
}
```

### Mixed List Styles
```latex
\begin{itemize}
\item Regular item
\begin{compactitem}  % Switch to compact
\item Nested compact item
\item Another compact item
\end{compactitem}
\item Back to regular spacing
\end{itemize}
```

### Resuming Lists
```latex
\begin{enumerate}
\item First item
\item Second item
\end{enumerate}

Some intervening text...

\begin{enumerate}[resume]
\item Continues at third
\item Fourth item
\end{enumerate}
```

## Integration with Content

### After Headings
Lists after headings automatically have appropriate spacing:
```latex
\subsection{Key Points}
\begin{itemize}
\item First paragraph after list is flush left
\item Spacing is grid-aligned
\end{itemize}
No indent here due to list above.
```

### In Quotations
```latex
\begin{quote}
Key principles include:
\begin{compactitem}
\item Brevity
\item Clarity
\item Precision
\end{compactitem}
\end{quote}
```

## Best Practices

### Choosing List Types

**Use itemize when:**
- Order doesn't matter
- Items are equally important
- Showing options or examples

**Use enumerate when:**
- Order is significant
- Showing steps or sequence
- Referencing items later

**Use description when:**
- Defining terms
- Explaining concepts
- Creating glossaries

### Spacing Guidelines

**Use compact lists for:**
- References
- Brief items
- Space-constrained areas

**Use display lists for:**
- Key findings
- Important points
- Executive summaries

**Use readable lists for:**
- Detailed explanations
- Teaching materials
- When clarity is paramount

## Common Patterns

### References List
```latex
\begin{compactitem}
\item Butterick, M. (2019). \emph{Practical Typography}.
\item Brown, T. (2018). \emph{Flexible Typographic Systems}.
\item Hochuli, J. (1987). \emph{Detail in Typography}.
\end{compactitem}
```

### Methodology Steps
```latex
\begin{enumerate}
\item Data collection
  \begin{academicitem}
  \item Survey design
  \item Participant recruitment
  \item Response validation
  \end{academicitem}
\item Analysis
\item Interpretation
\end{enumerate}
```

### Feature Comparison
```latex
\begin{description}
\item[Performance] 50\% faster processing
\item[Accuracy] 95\% precision rate
\item[Usability] Improved user satisfaction
\end{description}
```

## Troubleshooting

### Inconsistent Spacing
- Check for manual `\vspace` commands
- Ensure consistent list environment usage
- Verify no paragraph breaks in items

### Alignment Issues
- Use `\item` properly
- Don't add blank lines between items
- Check for stray spaces

### Nested List Problems
- Maximum nesting: 3 levels
- Use consistent environment types
- Verify proper \end{} matching