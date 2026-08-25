---
status: accepted
date: 2026-08-22
---

# l3build for packaging, pytest for tests

l3build is the LaTeX Project's build tool. It ships with TeX Live, so it is
already present both locally and in the CI container, and it is not an expl3
tool — plenty of LaTeX2e packages use it. Its targets divide cleanly into
packaging (`install`, `tag`, `ctan`, `upload`, `manifest`) and testing
(`check`, `save`). We adopt the first half and decline the second.

## Packaging: adopt

Four targets map directly onto decisions already made: `install` is the chosen
adoption path, `tag` stamps one version and date into every `\ProvidesPackage`,
`ctan` builds the archive in the layout CTAN expects, and `upload` submits it
with metadata read from `build.lua` so the submission cannot drift from the
source. That replaces four scripts we would otherwise write and maintain.

`make release VERSION=x.y.z` wraps `l3build tag && l3build ctan`; the Makefile
stays the entry point for humans and agents.

## Testing: decline

`l3build check` compiles a test document and diffs its normalised log against a
saved `.tlg`. Two things make it a poor fit here:

**Log-diffing is brittle in proportion to dependency count, and ours is large.**
The Package loads roughly twenty-five third-party packages whose warnings land
in the log and therefore in the `.tlg`. l3build normalises dates, paths, and
format versions, but not third-party chatter — so every TeX Live update forces
mass `.tlg` regeneration, and regenerating expected output wholesale is how real
regressions get approved by accident.

**The existing tests assert things a log diff cannot express.** Of 31 passing
tests, 18 are semantic: `test_option_contracts.py` checks that each package
option does what it claims, and `test_measured_values.py` checks computed TeX
dimensions. Typographic regressions are additionally caught by per-page raster
comparison at 150dpi, which is a stronger check for this domain than any log
diff.

Multi-engine checking, l3build's other draw, is moot while the Package is
pdfLaTeX-only.

So `build.lua` declares no test files — a normal configuration — and CI keeps
running `python3 -m pytest -q` unchanged. This supersedes the l3build migration
planned in `docs/PACKAGE_ROADMAP.md` (T-402), which is withdrawn. That file was
deleted on 2026-08-25 by issue #52; the withdrawal stands, and the roadmap is in
git history.

## Consequences

- Two tools, but no overlap: neither knows about the other, and deleting
  `build.lua` would not affect the test suite.
- If the Package ever supports XeLaTeX or LuaLaTeX, multi-engine testing has to
  be built rather than configured. Revisit this ADR at that point.
- CTAN acceptance is unaffected either way — no reviewer inspects a test harness.
  l3build makes release mechanics repeatable, not approval easier.
