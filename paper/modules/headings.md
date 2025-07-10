# Headings Module Documentation

## Overview

The headings module (`lltheadings.sty`) provides sophisticated section and heading formatting with perfect baseline grid alignment and professional typography.

## Heading Hierarchy

### Design Principles
- **Tim Brown's Modular Scale**: Perfect Fourth ratio (1.333)
- **Grid Alignment**: All spacing in baseline units (13.2pt)
- **Visual Hierarchy**: Size, weight, color, and spacing

### Heading Specifications

| Level | Size | Leading | Color | Style |
|-------|------|---------|-------|-------|
| Section | 18pt | 26.4pt | Softened navy | Bold + 8% tracking |
| Subsection | 14pt | 19.8pt | Muted midnight | Bold + 6% tracking |
| Subsubsection | 12pt | 13.2pt | Charcoal | Bold |
| Paragraph | 11pt | 13.2pt | Dark gray | Bold italic |

## Usage

### Basic Usage
```latex
\RequirePackage{lltheadings}
```

### Standard Commands
```latex
\section{Section Title}
\subsection{Subsection Title}
\subsubsection{Subsubsection Title}
\paragraph{Paragraph Title}
```

### Section Spacing Styles

The module provides four spacing presets:

```latex
\spacioussections   % Generous: 2 units before, 1 after
\moderatesections   % Default: 1.5 units before, 1 after
\compactsections    % Compact: 1 unit before, 1 after
\tightsections      % Tight: 1 unit before, 0.5 after
```

#### Spacing Details

**Spacious** (Original generous spacing):
- Before section: 26.4pt (2 grid units)
- After section: 13.2pt (1 grid unit)
- Best for: Books, reports with ample space

**Moderate** (Default):
- Before section: 19.8pt (1.5 grid units)
- After section: 13.2pt (1 grid unit)
- Best for: Standard academic papers

**Compact**:
- Before section: 13.2pt (1 grid unit)
- After section: 13.2pt (1 grid unit)
- Best for: Dense technical documents

**Tight**:
- Before section: 13.2pt (1 grid unit)
- After section: 6.6pt (0.5 grid units)
- Best for: Space-constrained documents

## Special Commands

### Section Breaks
```latex
\sectionbreak  % Add 2 grid units of space
\spacebreak    % Alias for \sectionbreak
```

### Safe Paragraph Heading
For Overleaf compatibility:
```latex
\safeparagraph{Heading Text}
% Use instead of \paragraph when errors occur
```

### Alternative Paragraph Styles
```latex
\paragraphsc      % Bold small caps variant
\displayparagraph{Heading}  % Display style
```

## Advanced Features

### Section Numbering
```latex
% Control numbering depth (default: 3)
\setcounter{secnumdepth}{2}  % Number only to subsection

% Remove numbers
\section*{Unnumbered Section}
```

### Custom Spacing
```latex
% Temporary spacing change
{
\compactsections
\section{Tight Section}
\subsection{Tight Subsection}
}
% Returns to previous spacing
```

### First Paragraph Control
First paragraphs after headings are automatically flush left (no indent).

## Typography Details

### Tracking (Letter Spacing)
- Sections: +8% for elegant bold
- Subsections: +6% for readability
- Subsubsections: Normal tracking
- Small caps: Context-dependent (3-12%)

### Color Application
All heading colors are defined in the colors module:
- `sectioncolor`: RGB(25,50,80)
- `subsectioncolor`: RGB(40,40,55)
- `subsubcolor`: RGB(64,64,64)
- `paragraphcolor`: RGB(89,89,89)

## Customization

### Changing Heading Colors
```latex
% After loading module
\definecolor{sectioncolor}{RGB}{0,100,0}  % Green sections
```

### Modifying Spacing
```latex
% Custom section spacing
\titlespacing*{\section}
  {0pt}                              % Left indent
  {30pt plus 5pt minus 5pt}          % Before
  {15pt plus 2pt minus 0pt}          % After
```

### Adding New Heading Levels
```latex
\titleformat{\subparagraph}
  {\normalfont\fontsize{10}{12}\selectfont\itshape}
  {}
  {0em}
  {}
\titlespacing*{\subparagraph}
  {0pt}
  {\halfgridunit}
  {\quartergridunit}
```

## Integration with Document Classes

### Article Class
Default settings work perfectly with standard article class.

### Book Class
```latex
\spacioussections  % Recommended for chapters
```

### Report Class
```latex
\moderatesections  % Good balance
```

## Best Practices

### Heading Usage
1. **Logical Hierarchy**: Don't skip levels
2. **Consistent Style**: Use one spacing style throughout
3. **Meaningful Titles**: Descriptive, not decorative

### Spacing Consistency
- Match heading spacing to document type
- Consider total page count
- Account for figures and tables

## Troubleshooting

### Overleaf "Missing \item" Error
Use `\safeparagraph{Title}` instead of `\paragraph{Title}`

### Inconsistent Spacing
- Check for manual `\vspace` commands
- Verify consistent spacing style
- Look for `\paragraph` placement

### Color Not Applying
Ensure colors module is loaded:
```latex
\RequirePackage{lltcolors}
\RequirePackage{lltheadings}
```

## Examples

### Academic Paper Structure
```latex
\moderatesections  % Default

\section{Introduction}
First paragraph is flush left...

\subsection{Background}
Subsequent paragraphs indented...

\paragraph{Key Concept}
Inline paragraph heading style...
```

### Compact Technical Document
```latex
\compactsections

\section{Algorithm}
\subsection{Implementation}
\subsubsection{Data Structures}
```

### Book Chapter
```latex
\spacioussections

\section{The Beginning}
\sectionbreak
\section{The Middle}
\sectionbreak
\section{The End}
```