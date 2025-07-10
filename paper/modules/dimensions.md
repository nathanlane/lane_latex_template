# Dimensions Module Documentation

## Overview

The dimensions module (`lltdimensions.sty`) manages page geometry and implements a sophisticated baseline grid system for perfect vertical rhythm.

## Grid System

### Foundation
- **Base unit**: 13.2pt (derived from 11pt × 1.20 leading)
- **Grid philosophy**: All vertical spacing in multiples of base unit
- **Purpose**: Consistent vertical rhythm throughout document

### Grid Units
```latex
\gridunit         % 13.2pt (1 unit)
\halfgridunit     % 6.6pt (0.5 units)
\quartergridunit  % 3.3pt (0.25 units)
```

## Page Geometry

### Default Layout
- **Page size**: US Letter (8.5 × 11 inches)
- **Margins**: 1.25 inches all sides
- **Text width**: ~6 inches (optimal 65 characters/line)
- **Text height**: ~8.5 inches

### Geometry Settings
```latex
% Current settings (US Letter)
\geometry{
  letterpaper,
  left=1.25in,
  right=1.25in,
  top=1.25in,
  bottom=1.25in,
  headsep=\gridunit,
  footskip=26.4pt  % 2 grid units
}
```

## Usage

### Basic Usage
```latex
\RequirePackage{lltdimensions}
```

### Spacing Commands

#### Adding Vertical Space
```latex
\halfbaselinespace    % Add 6.6pt (0.5 units)
\fullbaselinespace    % Add 13.2pt (1 unit)
\gridspace{2}         % Add 2 grid units (26.4pt)
```

#### Custom Spacing
```latex
% Add 1.5 grid units
\vspace{1.5\gridunit}

% Flexible spacing
\vspace{\gridunit plus \quartergridunit minus \quartergridunit}
```

### Paragraph Styles

The module provides three paragraph formatting styles:

```latex
\classicalparagraphs  % Default: 13.2pt indent, 0pt spacing
\modernparagraphs     % Modern: 0pt indent, 6.6pt spacing  
\hybridparagraphs     % Hybrid: 9.9pt indent, 3.3pt spacing
```

#### Classical (Default)
- First-line indent: 13.2pt (1 grid unit)
- Paragraph spacing: 0pt
- Flush left after headings

#### Modern
- First-line indent: 0pt
- Paragraph spacing: 6.6pt (0.5 units)
- Visual separation through spacing

#### Hybrid
- First-line indent: 9.9pt (0.75 units)
- Paragraph spacing: 3.3pt (0.25 units)
- Balanced approach

## Grid Development Tools

### Visualizing the Grid
```latex
% In document preamble
\usepackage{lltdimensions}
\usepackage{paper/gridoverlay}

% In document
\showgrid  % Display grid lines
\hidegrid  % Hide grid lines
```

### Grid-Aligned Elements
```latex
% Ensure element height is grid-multiple
\begin{gridbox}
  Content automatically sized to grid
\end{gridbox}

% Manual grid alignment
\vspace{\gridunit minus 3.3pt}  % Snap to grid
```

## Page Layout Options

### A4 Paper
```latex
% Before loading module
\PassOptionsToPackage{a4paper}{geometry}
\RequirePackage{lltdimensions}
```

### Custom Margins
```latex
% Load module first
\RequirePackage{lltdimensions}

% Then adjust
\geometry{margin=1in}
```

### Two-Column Layout
```latex
\documentclass[twocolumn]{article}
\usepackage{lltdimensions}
% Grid system adapts automatically
```

## Advanced Features

### Grid Calculations
```latex
% Calculate grid-aligned dimensions
\newlength{\myheight}
\setlength{\myheight}{10\gridunit}  % 132pt

% Conditional spacing
\ifdim\pagetotal<20\gridunit
  \vspace{\gridunit}
\fi
```

### Custom Grid Unit
```latex
% Must set before loading module
\newlength{\gridunit}
\setlength{\gridunit}{12pt}  % Custom grid
\RequirePackage{lltdimensions}
```

## Best Practices

### Maintaining Grid Alignment

1. **Use grid units** for all vertical spacing
2. **Avoid arbitrary dimensions** like `\vspace{1cm}`
3. **Test with grid overlay** during development
4. **Account for line height** in custom environments

### Common Patterns
```latex
% Section spacing
\vspace{2\gridunit}  % Major break
\vspace{\gridunit}   % Standard break
\vspace{\halfgridunit}  % Minor break

% Float spacing
\setlength{\floatsep}{\gridunit}
\setlength{\textfloatsep}{1.5\gridunit}
```

## Troubleshooting

### Broken Grid Alignment
- Check for non-grid spacing
- Verify font size changes maintain grid
- Use `\showgrid` to visualize

### Page Overfull/Underfull
- Adjust flexible spacing
- Use `\raggedbottom` for variable content
- Check float placement

## Examples

### Grid-Perfect Figure
```latex
\begin{figure}[tb]
  \centering
  \includegraphics[height=10\gridunit]{image}
  \caption{Grid-aligned figure}
\end{figure}
```

### Custom Environment
```latex
\newenvironment{gridquote}{%
  \vspace{\gridunit}%
  \begin{quote}%
}{%
  \end{quote}%
  \vspace{\gridunit}%
}
```