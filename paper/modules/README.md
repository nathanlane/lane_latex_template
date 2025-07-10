# LLT Style Modules

This directory contains the modular components of the lltpaperstyle LaTeX package. Each module provides specific functionality and can be used independently or as part of the complete lltpaperstyle system.

> **Note**: As of July 2025, all modules have been renamed following the Lane LaTeX Template (LLT) naming convention. Module files now use the `llt` prefix (e.g., `lltcolors.sty` instead of `colors.sty`).

## Module Overview
(The Lists module is now fully active as of v1.6.)

| Module | Purpose | Dependencies |
|--------|---------|--------------|
| `lltfonts.sty` | Font configuration and math typography | fontenc, tgpagella, zi4, newpxmath |
| `lltcolors.sty` | Professional color system | xcolor |
| `lltdimensions.sty` | Page geometry and grid system | geometry |
| `lltheadings.sty` | Section and heading formatting | titlesec, lltcolors, lltdimensions |
| `lltlists.sty` | List typography and environments | enumitem, lltcolors, lltdimensions |

## Quick Start

### Using All Modules (Recommended)

```latex
\usepackage{lltpaperstyle}
```

### Using Individual Modules

```latex
% Just the color system
\RequirePackage{lltcolors}
```
% Just the list styles
\RequirePackage{lltlists}

% Change first-level bullet to an en-dash
\setlist[itemize,1]{label=\dashmark}
```

## Module Documentation

- [Fonts Module](fonts.md) - Typography and font configuration (`lltfonts.sty`)
- [Colors Module](colors.md) - Color definitions and usage (`lltcolors.sty`)
- [Dimensions Module](dimensions.md) - Page layout and spacing (`lltdimensions.sty`)
- [Headings Module](headings.md) - Section formatting (`lltheadings.sty`)
- [Lists Module](lists.md) - List environments and styles (`lltlists.sty`)

## Design Principles

All modules follow these core principles:

1. **Baseline Grid Alignment**: All vertical spacing aligns to a 13.2pt grid
2. **Professional Typography**: Based on Butterick, Brown, and Hochuli
3. **Modular Independence**: Each module can function standalone
4. **Graceful Degradation**: Fallbacks for missing dependencies
5. **Overleaf Compatibility**: Tested on cloud LaTeX platforms

## Version History

- v1.0 (2025-07-03): Initial modular release