# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Sophisticated list typography system with multiple environments
- Professional testing framework with visual output validation
- Comprehensive typography documentation
- Grid-aligned table system
- Enhanced citation support with biblatex
- Professional footnote system optimized for TeX Gyre Pagella
- Testing infrastructure with Make targets
- Repository audit documentation

### Changed
- Updated from Bembo (fbb) to TeX Gyre Pagella font system
- Bullet colors adjusted from 45% to 20% gray for better visibility
- Renamed `\endashmark` to `\dashmark` to avoid conflicts
- Improved section heading typography with color and tracking

### Fixed
- LaTeX compilation errors with duplicate command definitions
- Cross-reference warnings in test fixtures
- Bibliography processing in test suite
- Overleaf "Incomplete \iffalse" error by properly protecting @ commands in user macros
- Microtype warnings for unavailable character slots (now gracefully handled)

## [0.1.0] - 2024-06-30

### Added
- Initial LaTeX template with sophisticated typography
- TeX Gyre Pagella font integration
- Modular scale typography system
- Chicago Manual of Style citation support
- Professional appendix management
- Baseline grid implementation

[Unreleased]: https://github.com/yourusername/lane_latex_template/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/lane_latex_template/releases/tag/v0.1.0