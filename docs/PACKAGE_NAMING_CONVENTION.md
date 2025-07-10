# Lane LaTeX Template (LLT) Package Naming Convention

## Overview

As of July 2025, the Lane LaTeX Template has adopted a systematic naming convention for all packages and modules. This change improves package identification and prevents naming conflicts with other LaTeX packages.

## Naming Convention

All packages now use the `llt` prefix (Lane LaTeX Template):

| Old Name (Path-based) | New Name (Direct) |
|-----------------------|-------------------|
| `paper/paperstyle` | `lltpaperstyle` |
| `paper/modules/colors` | `lltcolors` |
| `paper/modules/fonts` | `lltfonts` |
| `paper/modules/dimensions` | `lltdimensions` |
| `paper/modules/headings` | `lltheadings` |
| `paper/modules/lists` | `lltlists` |
| `paper/modules/paragraphs` | `lltparagraphs` |
| `paper/modules/compilation-fixes-simple` | `lltcompilationfixessimple` |
| `paper/modules/microtype-config` | `lltmicrotypeconfig` |
| `paper/modules/headings-gridlocked` | `lltheadingsgridlocked` |
| `paper/modules/mathematics-gridlocked` | `lltmathematicsgridlocked` |
| `paper/modules/hochuli-refinements` | `llthochulirefinements` |
| `paper/modules/font-features` | `lltfontfeatures` |
| `paper/modules/font-fallbacks` | `lltfontfallbacks` |
| `paper/gridoverlay` | `lltgridoverlay` |

## Migration Guide

### For Documents Using the Main Package

**Old usage:**
```latex
\usepackage{paper/paperstyle}
```

**New usage:**
```latex
\usepackage{lltpaperstyle}
```

### For Documents Using Individual Modules

**Old usage:**
```latex
\RequirePackage{paper/modules/colors}
\RequirePackage{paper/modules/lists}
```

**New usage:**
```latex
\RequirePackage{lltcolors}
\RequirePackage{lltlists}
```

### For Custom Module Loading

**Old usage:**
```latex
% Define custom settings
\definecolor{mycolor}{RGB}{100,100,100}
% Load module with path
\RequirePackage{paper/modules/colors}
```

**New usage:**
```latex
% Define custom settings
\definecolor{mycolor}{RGB}{100,100,100}
% Load module directly
\RequirePackage{lltcolors}
```

## Benefits

1. **Cleaner Syntax**: No path separators needed
2. **Standard Compliance**: Follows LaTeX package naming conventions
3. **Namespace Protection**: `llt` prefix prevents conflicts
4. **Easier Installation**: Can be installed in standard TeX directories
5. **Better Portability**: Works consistently across different systems

## Backward Compatibility

For temporary backward compatibility during migration, you can create symbolic links or wrapper files, but it's recommended to update your documents to use the new naming convention directly.

## Technical Details

The renaming follows these principles:
- Remove path separators (`/`)
- Add `llt` prefix
- Convert hyphens to camelCase where appropriate
- Maintain lowercase convention

All internal module dependencies have been updated to use the new names, so the system remains fully functional with the new naming convention.