# Documentation Index

This directory contains all project documentation organized by category.

## Directory Structure

### 📊 audits/
Comprehensive audits and analysis reports:
- `AUDIT_FINDINGS.md` - Initial project audit findings
- `EMPHASIS_HIERARCHY_AUDIT.md` - Typography emphasis system analysis
- `MATHEMATICAL_TYPOGRAPHY_AUDIT.md` - Mathematical typesetting review
- `PROFESSIONAL_AUDIT_SUMMARY.md` - Overall professional assessment
- `REPOSITORY_AUDIT.md` - Repository structure analysis
- `TITLE_FOOTNOTE_AUDIT.md` - Title page footnote system audit
- `title_page_grid_audit.md` - Title page grid alignment analysis
- `typography-audit-report.md` - Complete typography system audit

### 📚 guides/
User guides and how-to documentation:
- `BIBLIOGRAPHY_GUIDE.md` - Bibliography and citation system guide
- `LATEX_STYLE_STANDARDS.md` - LaTeX coding standards and conventions
- `OVERLEAF_WARNING_SUPPRESSION_GUIDE.md` - Guide to handling Overleaf warnings

### 📋 plans/
Optimization and implementation plans:
- `BIBLIOGRAPHY_OPTIMIZATION_PLAN.md` - Bibliography system improvements
- `CAPTION_OPTIMIZATION_PLAN.md` - Caption typography enhancements
- `CODEBASE_CLEANUP_ROADMAP.md` - Repository cleanup strategy
- `CODE_STYLE_HYGIENE_PLAN.md` - Code quality improvement plan
- `FINAL_MICRO_ADJUSTMENTS_PLAN.md` - Final typography refinements
- `FLOAT_OPTIMIZATION_PLAN.md` - Figure and table placement optimization
- `HEADING_OPTIMIZATION_PLAN.md` - Section heading improvements
- `HYPHENATION_OPTIMIZATION_PLAN.md` - Hyphenation system enhancements
- `INITIAL_CAPS_PLAN.md` - Drop caps and initial capitals design
- `LATEX_PACKAGE_OPTIMIZATION_ROADMAP.md` - Package refactoring strategy
- `LIST_OPTIMIZATION_PLAN.md` - List typography improvements
- `PAPERSTYLE_CLEANUP_PLAN.md` - Style package cleanup strategy
- `PARAGRAPH_OPTIMIZATION_PLAN.md` - Paragraph formatting enhancements
- `SPECIAL_CHARACTERS_OPTIMIZATION_PLAN.md` - Special character handling

### 🎨 style/
Style specifications and changelog:
- `CHANGELOG.md` - Project version history and changes

### 🔧 technical/
Technical documentation and summaries:
- `CODE_HYGIENE_SUMMARY.md` - Code quality report
- `COMPILATION_ERRORS_MASTER_LIST.md` - Known compilation issues
- `DIRECTORY_CLEANUP_SUMMARY.md` - Cleanup operation results
- `FINAL_COMPILATION_STATUS.md` - Final build status report
- `PAPERSTYLE_CLEANUP_SUMMARY.md` - Style package cleanup results
- `TESTING.md` - Testing procedures and results
- `TITLE_FOOTNOTE_FIX.md` - Title footnote implementation fix

### 📐 typography/
Typography-specific documentation:
- `BASELINE-GRID.md` - Baseline grid system specification
- `BLOCKQUOTE_LIST_OPTIMIZATION.md` - Quote and list formatting
- `CROSS_REFERENCE_TYPOGRAPHY_OPTIMIZATION.md` - Cross-reference styling
- `SPACING_OPTIMIZATION_NOTES.md` - Spacing system documentation

## Quick Links

- **Getting Started**: See [guides/LATEX_STYLE_STANDARDS.md](guides/LATEX_STYLE_STANDARDS.md)
- **Current Status**: See [technical/FINAL_COMPILATION_STATUS.md](technical/FINAL_COMPILATION_STATUS.md)
- **Optimization Roadmap**: See [plans/LATEX_PACKAGE_OPTIMIZATION_ROADMAP.md](plans/LATEX_PACKAGE_OPTIMIZATION_ROADMAP.md)
- **Typography System**: See [typography/BASELINE-GRID.md](typography/BASELINE-GRID.md)
- **Package Naming**: See [PACKAGE_NAMING_CONVENTION.md](PACKAGE_NAMING_CONVENTION.md)

## Package Naming Convention

As of July 2025, the Lane LaTeX Template (LLT) packages use a systematic naming convention:
- Main style package: `lltpaperstyle` (formerly `paper/paperstyle`)
- Module packages: `llt{modulename}` (e.g., `lltcolors`, `lltfonts`, `lltlists`)
- Loading method: Direct package names without path prefixes

## Documentation Standards

All documentation follows these conventions:
- **File Names**: UPPERCASE with underscores for word separation
- **Format**: Markdown with clear section headers
- **Status**: Documents marked as PLAN are proposals; others are implemented features
- **Dates**: ISO format (YYYY-MM-DD) when applicable