# Documentation Index

<!-- %% FIX: Replace stale generated-looking links with a curated index of tracked docs. -->

This directory collects active user guides, maintainer notes, historical audits,
and archived implementation plans for the Lane LaTeX Template.

## Active User Guides

- [Bibliography Guide](guides/BIBLIOGRAPHY_GUIDE.md) - Citation and bibliography workflow.
- [LaTeX Style Standards](guides/LATEX_STYLE_STANDARDS.md) - Source-formatting and typography conventions.
- [Package Naming Convention](PACKAGE_NAMING_CONVENTION.md) - Current `llt` package naming rules.
- [Grid System Reference](GRID_SYSTEM_REFERENCE.md) - Grid commands and layout concepts.

## Active Maintainer References

- [Testing Guide](technical/TESTING.md) - Local build, lint, pytest, and shell-harness checks.
- [Deep Review Findings](technical/DEEP_REVIEW_FINDINGS_2026-07-01.md) - Consolidated review findings that drive the current lane roadmap.
- [LaTeX Code Review](technical/LATEX_CODE_REVIEW_2026-05-28.md) - Maintainability and package API findings.
- [Package Brittleness Analysis](technical/PACKAGE_BRITTLENESS_ANALYSIS.md) - Package reliability risks and recommendations.
- [Grid Unit Conversion Audit](technical/GRID_UNIT_CONVERSION_AUDIT.md) - Grid-unit conversion details.

## Roadmaps And Workflow Notes

- [Package Roadmap](PACKAGE_ROADMAP.md) - Historical package roadmap and future packaging ideas.
- [Deep Review Roadmap](superpowers/plans/2026-07-01-deep-review-roadmap.md) - Current serialized lane plan for review remediation.
- [AI Workflow Plan Template](ai-workflow/plan-template.md) - Living-plan lifecycle and status conventions.
- [Style Changelog](style/CHANGELOG.md) - Legacy style-package changelog.

## Typography And Grid Notes

- [Baseline Grid](typography/BASELINE-GRID.md) - Baseline-grid design notes.
- [Blockquote/List Optimization](typography/BLOCKQUOTE_LIST_OPTIMIZATION.md) - Historical quote/list typography work.
- [Cross-Reference Typography](typography/CROSS_REFERENCE_TYPOGRAPHY_OPTIMIZATION.md) - Cross-reference typography notes.
- [Spacing Optimization](typography/SPACING_OPTIMIZATION_NOTES.md) - Spacing-system notes.
- [Grid Development Notes](development/grid/README.md) - Development notes and experiments for grid tooling.

## Historical Audits And Archives

- [Local Fork Template Audit](LOCAL_FORK_TEMPLATE_AUDIT_2026-05-27.md)
- [Typography Audit Report](TYPOGRAPHY_AUDIT_REPORT.md)
- [LaTeX Template Review](LATEX_TEMPLATE_REVIEW.md)
- [Archived Plans](archive/)
- [Legacy Troubleshooting Guide](archive/TROUBLESHOOTING-legacy.md)

## Package Naming Convention

The current main style package is `lltpaperstyle`.
Module packages use the `llt` prefix, such as `lltcolors`, `lltfonts`, and
`lltlists`.
Load packages by package name rather than path prefix.

## Documentation Standards

- Use Markdown with clear section headers.
- Prefer links to tracked files.
- Mark historical or proposal documents clearly when they are not current user
  guidance.
- Use ISO dates (`YYYY-MM-DD`) when dates are needed.
