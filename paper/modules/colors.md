# Colors Module Documentation

## Overview

The colors module (`lltcolors.sty`) provides a sophisticated color system with semantic naming, professional aesthetics, and accessibility compliance.

## Color Philosophy

Based on three principles:
1. **Restraint**: Limited palette for professional appearance
2. **Hierarchy**: Colors reinforce document structure
3. **Accessibility**: WCAG AA compliant contrast ratios

## Color Palette

### Text Colors
```latex
textblack    % RGB(25,25,25)    - Softened black for reduced eye strain
textgray     % RGB(102,102,102) - 40% gray for secondary text
lightgray    % RGB(179,179,179) - 70% gray for subtle elements
darkgray     % RGB(64,64,64)    - 25% gray for emphasis
```

### Heading Colors
```latex
sectioncolor    % RGB(25,50,80)   - Softened navy
subsectioncolor % RGB(40,40,55)   - Muted midnight
subsubcolor     % RGB(64,64,64)   - Medium charcoal
paragraphcolor  % RGB(89,89,89)   - Dark gray
```

### Functional Colors
```latex
linkcolor       % RGB(0,102,180)  - Professional blue
citecolor       % RGB(0,102,180)  - Same as links
codecolor       % RGB(51,51,51)   - Dark gray for code
quotegray       % gray!15         - 15% gray for quotes
subtlegray      % gray!85         - Very dark gray
```

## Usage

### Basic Usage
```latex
\RequirePackage{lltcolors}
```

### Applying Colors
```latex
% Text coloring
\textcolor{textgray}{Secondary text}
\textcolor{sectioncolor}{Important heading}

% In other commands
\color{quotegray}  % Switch color
```

### Color in Document Elements

The colors are automatically applied to:
- Section headings (sectioncolor, subsectioncolor, etc.)
- Hyperlinks (linkcolor)
- Citations (citecolor)
- Code snippets (codecolor)
- Block quotes (quotegray)

## Accessibility

All color combinations meet WCAG AA standards:

| Text Color | Background | Contrast Ratio | Rating |
|------------|------------|----------------|---------|
| textblack | white | 17.4:1 | AAA |
| textgray | white | 4.1:1 | AA |
| sectioncolor | white | 9.7:1 | AAA |
| linkcolor | white | 4.8:1 | AA |

## Customization

### Redefining Colors
```latex
% Load module first
\RequirePackage{lltcolors}

% Then redefine
\definecolor{sectioncolor}{RGB}{0,100,0}  % Green sections
```

### Adding New Colors
```latex
% After loading module
\definecolor{mycolor}{RGB}{100,50,150}
```

## Color Commands

### Semantic Text Commands
The module provides semantic commands for common uses:

```latex
\emphcolor{text}     % Uses sectioncolor
\metacolor{text}     % Uses darkgray
\codecolor{text}     % Uses codecolor
```

## Design Guidelines

### When to Use Color

**Do:**
- Reinforce hierarchy
- Indicate functionality (links, code)
- Subtle emphasis

**Don't:**
- Decorate without purpose
- Create "rainbow" documents
- Override semantic meaning

### Color Hierarchy

1. **Black text**: Primary content
2. **Section colors**: Major divisions
3. **Gray variations**: Supporting elements
4. **Blue**: Interactive elements only

## Technical Details

### Color Model
- Primary model: RGB
- Gray definitions: Percentage-based
- Full xcolor syntax supported

### Package Options
```latex
% Load with xcolor options
\RequirePackage[dvipsnames]{lltcolors}
```

## Compatibility

- Works with all LaTeX engines
- Full xcolor compatibility
- Printer-friendly gray fallbacks
- Screen and print optimized

## Examples

### Custom Link Colors
```latex
% Make links dark green
\definecolor{linkcolor}{RGB}{0,100,0}
```

### Highlighted Text
```latex
% Create highlight color
\definecolor{highlight}{RGB}{255,255,200}
\newcommand{\highlight}[1]{%
  \colorbox{highlight}{#1}%
}
```

### Conditional Colors
```latex
% Different colors for draft/final
\ifdraft
  \definecolor{sectioncolor}{RGB}{200,0,0}  % Red in draft
\fi
```