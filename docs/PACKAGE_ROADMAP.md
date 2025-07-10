# EastAsia_Paper LaTeX Package – Comprehensive Roadmap

> This document expands upon the high-level action plan outlined previously.  It is **the single source of truth** for the package’s near-term direction, milestones, and decision-making history.  Update this file whenever scope or sequencing changes.

---

## 1. Vision

Design and maintain a robust, opinionated LaTeX package that dramatically simplifies the creation of publication-ready, East-Asian-typeset research papers while enforcing grid-aligned, baseline-consistent typography.

Key outcomes:
1. ⚡ **Faster authoring** – reduce boiler-plate LaTeX by ≥ 60 %.  
2. 🪄 **Consistent appearance** – grid-aligned layouts with predictable whitespace.  
3. 🛠️ **Extensible foundation** – clear APIs for custom blocks (figures, code, tables).  
4. 📦 **Seamless distribution** – CI-driven releases to CTAN & GitHub.

---

## 2. Guiding Principles

* **Minimal surprises** – honour classic LaTeX defaults unless there is a clear net benefit.  
* **Single-responsibility** – each macro/style file should do *one* thing well.  
* **Orthogonality** – enabling one feature must not silently alter others.  
* **Documentation-first** – every public macro is accompanied by usage + rationale.

---

## 3. Phase Plan & Milestones

| Phase | Code-name | Goal | ETA | Exit Criteria |
|-------|-----------|------|-----|---------------|
| 0 | "Groundwork" | Complete baseline audit, create test harness, define metrics | **T₀ + 0 w** | Audit report approved; CI smoke tests green |
| 1 | "Typography" | Enforce baseline grid, improve font setup, spacing, lists | **T₀ + 2 w** | All sample docs pass visual diff; `\aselinegridtrue` macro public |
| 2 | "Grid Layout" | General-purpose grid system (N-column, modular scale); Integrate repository structure changes | **T₀ + 5 w** | `grid.sty` 1.0 exported; 90 % coverage in visual tests; Structure changes implemented |
| 3 | "Components" | Figure, table, code-block environments built on grid APIs | **T₀ + 8 w** | `figure*`, `tablegrid`, `codeblock` stable |
| 4 | "Packaging" | Automate versioning, docs, CTAN release, GitHub Actions | **T₀ + 9 w** | Tagged v1.0 on GitHub; package on CTAN; CTAN readiness steps implemented |
| 5 | "Polish & Docs" | Author guide, changelog, migration notes | **T₀ + 10 w** | README, quick-start, full manual published |

### Narrative Overview

Our roadmap is intentionally phased to decouple pure **infrastructure** work (build, CI, repository layout) from **typographic** and **API-level** innovation.  The table above captures high-level timing; the paragraphs below provide the "story" of how we evolve from the current template into a polished CTAN package.

**Phase 0 – Groundwork.**  We treat the existing codebase strictly as *input* and focus on repeatable builds.  Outcomes include a minimal GitHub Action running `latexmk` against a smoke-test document and a visual-diff harness that protects against regressions once we start refactoring.  No functional changes land in this phase.

**Phase 1 – Typography.**  Driven directly by audit items *T-101* and *T-102*, we stabilise the **baseline grid** and font setup.  The grid overlay becomes an opt-in feature (`\GridOverlayOn`) and the macro `\baselinegridtrue` enters the public API.  When this phase exits, all historical sample documents typeset identically (or better) compared with `main.pdf` today.

**Phase 2 – Grid Layout.**  The repository restructuring from the technical audit happens here.  We create `tex/latex/eastasia/` and migrate `.sty` modules while simultaneously extracting common grid maths into `grid.sty` (*T-201*).  Automated tests reach ≥ 90 % coverage of layout primitives.  Successful completion means the codebase can be installed via `TEXMFHOME` and consumed like any other package.

**Phase 3 – Components.**  Using the now-stable grid APIs, we rewrite higher-level environments—figures, tables, code blocks—to guarantee baseline alignment (*T-301*).  This is also the point where colour and dimension parameters become key–value options, satisfying audit goals for `colors.sty` and `dimensions.sty`.

**Phase 4 – Packaging.**  We introduce `eastasia.dtx`, `eastasia.ins`, and `l3build.lua`.  Version numbers are unified, change-log entries are generated, and CI begins producing CTAN-ready `.zip` bundles.  The CTAN readiness checklist embedded in Section 6 must be fully green before we tag `v1.0.0`.

**Phase 5 – Polish & Docs.**  The final sprint focuses on outward-facing collateral: README, quick-start sample, full implementation manual, and migration notes for template users.  On exit, the package is *boring* to install and pleasant to read.

*Dates assume a start (T₀) of 2025-07-07 and one 40 h FTE.  Adjust as capacity changes.*

---

## 4. Detailed Task Breakdown

### Code Refactor Checklist
- Adopt a unique namespace (e.g., `\east@` or `\east_`).
- Add `\ProvidesExplPackage` lines with date, version, description in every module (or in the merged `.dtx`).
- Consolidate versioning: one semantic version across all modules.
- Replace legacy TeX primitives (`\def`, `@ifundefined`) with LaTeX3 interfaces where feasible: `\cs_new:Npn`, `\bool_if:NTF`, `\prop_new:N`, etc.
- Remove stray `\makeatletter` / `\makeatother` pairs by switching to `expl3` where possible.
- Use `\msg_new:nnn` (LaTeX3) or `\PackageWarning` / `\PackageError` for diagnostics instead of `\typeout`.

#### Module-Specific Tasks
- **colors.sty / dimensions.sty**: Convert magic numbers to key–val options (`xkeyval` or `l3keys`). Document every color/length in the `.dtx` docs section.
- **headings-gridlocked.sty, mathematics-gridlocked.sty**: Ensure catcode safety and no global assignments for `\everypar` / `\preto`. Parameterise grid-spacing.
- **font-family modules**: De-duplicate font selection code by consolidating into a `fontfeatures` module.
- **hochuli-refinements.sty & microtype-config.sty**: Validate microtype sets for LuaTeX vs pdfTeX; add `\IfMicrotypeLoaded` conditionals.
| ID | Title | Owner | Status | Depends | Notes |
|----|-------|-------|--------|---------|-------|
| T-001 | CI skeleton (GitHub Actions) | NL | ✅ | – | `latexmk`, l3build, PDF artifact |
| T-002 | Visual diff harness | NL | 🔄 | T-001 | Use `latexdiff-vc` + `pdfcrop` |
| T-101 | Baseline grid macros | NL | ⏳ | T-002 | `\baselinegridtrue/false`, grid overlay |
| T-102 | Fontspec presets | TBD | ⏳ | T-101 | Ship Noto + fallback stack |
| T-201 | `grid.sty` core | TBD | ⏳ | T-101 | Column math, length helpers |
| T-202 | Grid unit tests | TBD | ⏳ | T-201 | Visual + length diff |
| T-301 | Figure environment rewrite | TBD | ⏳ | T-201 | Baseline aligned captions |
| T-401 | Release script | TBD | ⏳ | T-301 | `l3build ctan` wrapper |
| T-402 | CI Build Enhancement | TBD | ⏳ | T-401 | Setup `l3build`: set `test_type = "typeset"`, `check-engines = {"pdftex","xetex","luatex"}` and run on every push. |
| T-501 | Full manual (`.tex`) | TBD | ⏳ | T-301 | Leverage docstrip |

Legend: ✅ complete, 🔄 in-progress, ⏳ pending, ❌ blocked.

---

## 5. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| luatex behaviour drift | Medium | Low | Pin TeXLive yearly docker image |
| Visual diff flakiness | High | Med | Rasterise to PNG before compare |
| Package brittleness due to over-riding core LaTeX | High | Med | Maintain shim layer, document opting-out |
| CTAN review delays | Medium | Low | Pre-submit to `ctan-upload` dry-run |

---

## 6. Governance & Decision Log

* Decisions recorded chronologically in `docs/DECISIONS.md` (create if absent).  
* Significant API changes require an *ADR* entry.

---

## 7. Contribution Process

1. Fork, create feature branch following `feat/<slug>` convention.  
2. Run `make test lint docs` locally – all must pass.  
3. Write descriptive commit message (imperative mood).  
4. Open PR – use template, link to roadmap task ID.  
5. At least one approval + passing CI merges.

---

## 8. References

## 9. Public Interface Stability

### 3. User API Design

**Package options (draft proposal):**
- `baselinegrid`, `colorprofile=`, `lang=`, `maths=grid|plain`, `font=system|latex`,
- `style=minimal|journal`, `headings=tight|loose`, …

Provide sane defaults – `\usepackage{eastasia}` should succeed with no options.

**Expose public commands:**
- `\TitlePage{}`, `\GridOverlayOn`, `\GridOverlayOff`, `\SetPaperInfo{<key>=<value>, …}`
* Baseline Grid Audit → `docs/typography/BASELINE-GRID.md`  
* Brittleness Analysis → `docs/technical/PACKAGE_BRITTLENESS_ANALYSIS.md`  
* Grid Construction Process → `docs/development/grid/GRID-CONSTRUCTION-PROCESS.md`

---

## Appendix A: Technical Audit & Migration Plan (2025-07-07)

Below is a first-pass technical audit and migration plan for turning the current “lane_latex_template” template into a formally documented LaTeX package that is ready for CTAN submission and easy downstream use.

### 1  Repository structure

**KEEP**
• `docs/`, `tests/`, `appendices/`, `examples/` (fixtures) – valuable collateral.

**MOVE / RENAME**
• All `.sty` files → `tex/latex/eastasia/` (or another unique bundle name)  
• All user-facing `.tex` examples → `doc/latex/eastasia/`  
• `README`, `CHANGELOG`, `LICENSE` → top level (or `/doc` if you choose `l3build`).  
• Optional: retain `paper/` as private working directory, but strip from CTAN build.

**ADD**
• `eastasia.dtx` – single documented source (generated from existing `.sty` files).  
• `eastasia.ins` – docstrip driver that extracts `.sty`, `.cfg`, etc.  
• `l3build.lua` – build/test script (preferred by CTAN team).  
• `MANIFEST.md` – file list with install location.

### 2  Code-level review & refactor checklist

**GLOBAL**
- [ ] Adopt a unique namespace (e.g. `\east@` or `\east_`).  
- [ ] Add `\ProvidesExplPackage` lines with date, version, description in every module (or in the merged `.dtx`).  
- [ ] Consolidate versioning: one semantic version across all modules.  
- [ ] Replace legacy TeX primitives (`\def`, `@ifundefined`) with LaTeX3 interfaces where feasible: `\cs_new:Npn`, `\bool_if:NTF`, `\prop_new:N`, etc.  
- [ ] Remove stray `\makeatletter` / `\makeatother` pairs by switching to `expl3` where possible.  
- [ ] Use `\msg_new:nnn` (LaTeX3) or `\PackageWarning` / `\PackageError` for diagnostics instead of `\typeout`.

**MODULE-SPECIFIC HIGHLIGHTS**
• **colors.sty / dimensions.sty**  
  – Convert magic numbers to key–val options (`xkeyval` or `l3keys`).  
  – Document every color/length in the `.dtx` docs section.

• **headings-gridlocked.sty, mathematics-gridlocked.sty**  
  – Heavy reliance on `\everypar` / `\preto`. Ensure catcode safety and no global assignments.  
  – Parameterise grid-spacing so users can override.

• **font-family modules**  
  – De-duplicate font selection code; consolidate into a `fontfeatures` module using `fontspec` under Xe/LuaTeX and NFSS for pdfLaTeX fallback.

• **hochuli-refinements.sty & microtype-config.sty**  
  – Validate microtype sets for LuaTeX vs pdfTeX; supply `\IfMicrotypeLoaded` conditionals.

### 3  User API design

Package options (draft proposal):  
`baselinegrid`, `colorprofile=`, `lang=`, `maths=grid|plain`, `font=system|latex`,  
`style=minimal|journal`, `headings=tight|loose`, …

Provide sane defaults – `\usepackage{eastasia}` should succeed with no options.

Expose public commands:  
`\TitlePage{}`, `\GridOverlayOn`, `\GridOverlayOff`, `\SetPaperInfo{<key>=<value>, …}`

### 4  Documentation plan

• `dtx` preamble: purpose, quick-start, dependency table, option table, changelog.  
• Tutorial section: replicate `minimal.tex` and `full-features.tex` as verbatim listings with rendered output.  
• Implementation section: each module separated with `\StopEventually{}` markers.  
• PDF doc should build with:
```bash
pdflatex eastasia.dtx
makeindex -s gind.ist eastasia.idx
texindy eastasia
pdflatex eastasia.dtx
```

### 5  Testing & CI

• Keep `tests/fixtures` as **l3build** “testfiles”.  
• Add `.l3build` file setting — `test_type = "typeset"`, `check-engines = {"pdftex","xetex","luatex"}`  
• GitHub Actions / GitLab CI: run `l3build check && l3build doc` on every push.

### 6  CTAN readiness checklist

- [ ] LICENSE (LPPL 1.3c or later).  
- [ ] README with short summary, installation, bug tracker link.  
- [ ] `\changes` entries in the dtx.  
- [ ] Ensure all files contain only ASCII/UTF-8 without BOM.  
- [ ] No generated PDFs except `README.pdf` and package manual.  
- [ ] Tag a versioned release (e.g., `v0.9.0`).

### 7  Next steps

1. Create `eastasia.dtx` and `eastasia.ins` (can be mostly auto-generated from the existing `.sty` files).  
2. Introduce **l3build** and migrate current fixtures.  
3. Run `l3build doc`; fix compilation warnings.  
4. Iterate on API and documentation; freeze `v1.0.0`.  
5. Submit to CTAN.

---

_Last updated: 2025-07-07_
