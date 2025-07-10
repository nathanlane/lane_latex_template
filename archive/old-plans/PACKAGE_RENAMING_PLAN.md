# Package Renaming Plan for CTAN Compatibility

## Overview
To make the Lane LaTeX Template CTAN-compatible, we need to remove path dependencies and rename generic package names. This document outlines the renaming strategy.

## Naming Convention
We'll use the prefix `llt` (Lane LaTeX Template) for all packages to ensure uniqueness.

## Package Renaming Map

### Main Packages
| Current Name | New Name | File Location |
|--------------|----------|---------------|
| `paper/paperstyle` | `lltpaperstyle` | `paper/paperstyle.sty` |
| `paper/paperstyle-minimal` | `lltpaperstyleminimal` | `paper/paperstyle-minimal.sty` |
| `paper/gridoverlay` | `lltgridoverlay` | `paper/gridoverlay.sty` |

### Module Packages
| Current Name | New Name | File Location |
|--------------|----------|---------------|
| `paper/modules/colors` | `lltcolors` | `paper/modules/colors.sty` |
| `paper/modules/compilation-fixes-simple` | `lltcompilationfixes` | `paper/modules/compilation-fixes-simple.sty` |
| `paper/modules/dimensions` | `lltdimensions` | `paper/modules/dimensions.sty` |
| `paper/modules/font-fallbacks` | `lltfontfallbacks` | `paper/modules/font-fallbacks.sty` |
| `paper/modules/font-features` | `lltfontfeatures` | `paper/modules/font-features.sty` |
| `paper/modules/fonts` | `lltfonts` | `paper/modules/fonts.sty` |
| `paper/modules/headings` | `lltheadings` | `paper/modules/headings.sty` |
| `paper/modules/headings-gridlocked` | `lltheadingsgridlocked` | `paper/modules/headings-gridlocked.sty` |
| `paper/modules/hochuli-refinements` | `llthochuli` | `paper/modules/hochuli-refinements.sty` |
| `paper/modules/lists` | `lltlists` | `paper/modules/lists.sty` |
| `paper/modules/mathematics-gridlocked` | `lltmathgridlocked` | `paper/modules/mathematics-gridlocked.sty` |
| `paper/modules/microtype-config` | `lltmicrotype` | `paper/modules/microtype-config.sty` |
| `paper/modules/paragraphs` | `lltparagraphs` | `paper/modules/paragraphs.sty` |

## Changes Required

### 1. In Each .sty File
- Change `\ProvidesPackage{paper/...}` to `\ProvidesPackage{llt...}`
- Update all `\RequirePackage{paper/...}` to `\RequirePackage{llt...}`

### 2. In .tex Files
- Change `\usepackage{paper/paperstyle}` to `\usepackage{lltpaperstyle}`
- Update any other package references

### 3. In Test Files
- Update all package references in test fixtures

## Implementation Options

### Option A: Keep Directory Structure
- Keep files in current locations
- Only change package names internally
- Pros: Minimal file movement
- Cons: Installation more complex

### Option B: Flatten Structure
- Move all .sty files to single directory
- Simpler for users to install
- Pros: Standard CTAN structure
- Cons: Loses organizational hierarchy

## Recommendation
Start with Option A (keep structure) to minimize changes. Can flatten later if needed for CTAN.

## Usage After Renaming

### Old Usage:
```latex
\usepackage{paper/paperstyle}
```

### New Usage:
```latex
\usepackage{lltpaperstyle}
```

## Alternative Prefix Options
If `llt` is not preferred, consider:
- `laneacademic` - More descriptive but longer
- `lane` - Shorter but might be too generic
- `lanetype` - Indicates typography focus
- `academictype` - Describes purpose

## Next Steps
1. Decide on prefix (recommend `llt`)
2. Run the renaming script
3. Test compilation
4. Update documentation
5. Add LPPL headers