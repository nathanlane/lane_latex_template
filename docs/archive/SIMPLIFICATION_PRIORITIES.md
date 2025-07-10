# Simplification Priorities for Production-Ready Repository

**Date:** July 3, 2025  
**Current State:** Severely over-engineered academic template  
**Goal:** Simple, maintainable, production-ready repository

## Priority 1: Critical Simplifications (Do First)

### 1.1 Replace Custom Typography System
**Current:** 3,080-line paperstyle.sty with complex baseline grid  
**Action:** Use standard LaTeX article class with minimal customization
```latex
\documentclass[11pt]{article}
\usepackage{geometry}  % margins
\usepackage{graphicx}  % figures
\usepackage{booktabs}  % tables
\usepackage{amsmath}   % math
\usepackage[style=authoryear]{biblatex}  % citations
```
**Impact:** Remove 95% of complexity, maintain professional appearance

### 1.2 Eliminate Package Modules
**Current:** 5 separate module files (fonts.sty, colors.sty, etc.)  
**Action:** Delete modules directory, use standard packages directly  
**Impact:** -200 lines of code, -5 files, easier debugging

### 1.3 Remove Custom Commands
**Current:** 50+ custom typography commands (\emdash, \figuredash, etc.)  
**Action:** Use standard LaTeX commands  
**Impact:** Eliminate learning curve, improve portability

## Priority 2: Documentation Cleanup

### 2.1 Consolidate Documentation
**Current:** 46 documentation files across multiple directories  
**Action:** Keep only:
- `README.md` - Basic usage instructions
- `SETUP.md` - Installation guide
- Delete all others
**Impact:** -44 files, -10,000+ lines of documentation

### 2.2 Simplify Instructions
**Current:** 3,000+ line CLAUDE.md "constitution"  
**Action:** Replace with 1-page style guide  
**Impact:** Easier onboarding, less maintenance

## Priority 3: Test Framework Reduction

### 3.1 Remove Excessive Tests
**Current:** 26 test fixtures for edge cases  
**Action:** Keep only:
- `tests/compile-test.tex` - Basic compilation check
- `tests/bibliography-test.tex` - Citation check
**Impact:** -24 test files, faster validation

### 3.2 Eliminate Complex Test Scripts
**Current:** Automated spacing leak detection, page count validation  
**Action:** Simple make targets: `make test`, `make pdf`  
**Impact:** Remove brittleness, simplify CI/CD

## Priority 4: File Structure Simplification

### 4.1 Flatten Directory Structure
**Current:**
```
/paper/modules/
/paper/styles/
/appendices/
/docs/planning/
/docs/technical/
/tests/fixtures/
/tests/visual/
```
**Action:**
```
/main.tex
/references.bib
/figures/
/README.md
```
**Impact:** -10 directories, clearer structure

### 4.2 Remove Generated Files
**Current:** Multiple .aux, .log, .out files tracked  
**Action:** Proper .gitignore, clean repository  
**Impact:** Cleaner git history, smaller repo

## Priority 5: Bibliography Simplification

### 5.1 Remove Bibliography Customizations
**Current:** Complex biblatex configurations with custom formatting  
**Action:** Vanilla biblatex or natbib  
**Impact:** Better journal compatibility

### 5.2 Simplify Reference Management
**Current:** Categorized references with extensive annotations  
**Action:** Simple .bib file with standard entries  
**Impact:** Easier maintenance

## Quick Wins (Can Do Immediately)

1. **Delete these directories now:**
   - `/docs/` (except basic README)
   - `/scripts/`
   - `/tests/visual/`
   - `/paper/modules/`

2. **Remove these files:**
   - All `.log`, `.aux`, `.out` files
   - `CLAUDE.md`
   - All planning documents
   - All audit documents

3. **Simplify main.tex:**
   - Remove custom commands
   - Use standard sectioning
   - Remove special environments

## Expected Outcomes

After simplification:
- **Files:** From 200+ to ~10
- **Lines of Code:** From 15,000+ to ~500
- **Packages:** From 44 to 6-8
- **Compilation Time:** 5x faster
- **Maintenance:** 90% reduction
- **Learning Curve:** Near zero

## The 80/20 Rule

**Keep:** Basic LaTeX best practices that cover 80% of needs
**Remove:** Complex customizations that add 20% value but 80% complexity

## Final Recommendation

This repository should be a simple academic paper template, not a typography framework. Journal styles will override most customizations anyway. Focus on content, not typography engineering.