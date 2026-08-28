---
status: accepted
date: 2026-08-22
---

# l3build for packaging, existing harnesses for tests

l3build is the LaTeX Project's build tool. It ships with TeX Live, so it is
already present both locally and in the CI container, and it is not an expl3
tool — plenty of LaTeX2e packages use it. Its targets divide cleanly into
packaging (`install`, `tag`, `ctan`, `upload`, `manifest`) and testing
(`check`, `save`). We adopt the first half and decline the second.

> **v3 revision (2026-08-28).** `build.lua` remains the packaging description
> and install/CTAN tool if CTAN work later resumes. It does not own the GitHub
> release: issue #88 must remove `make release` and the tag-triggered workflow
> before v3 is published manually from an exact CI-green commit. Until then,
> those legacy release surfaces must not be used. CTAN remains on hold. Testing
> keeps the existing pytest suite plus shell harness; no replacement suite or
> release threshold is added.

## Packaging: adopt

Four targets map directly onto decisions already made: `install` is the chosen
adoption path, `tag` stamps one version and date into every `\ProvidesPackage`,
`ctan` builds the archive in the layout CTAN expects, and `upload` submits it
with metadata read from `build.lua` so the submission cannot drift from the
source. That replaces four scripts we would otherwise write and maintain.

Issue #88 removes the `make release` wrapper before v3. A future CTAN decision
may use l3build's packaging commands directly, while GitHub release mechanics
stay manual and separate.

## Testing: decline

`l3build check` compiles a test document and diffs its normalised log against a
saved `.tlg`. Two things make it a poor fit here:

**Log-diffing is brittle in proportion to dependency count, and ours is large.**
The Package loads roughly twenty-five third-party packages whose warnings land
in the log and therefore in the `.tlg`. l3build normalises dates, paths, and
format versions, but not third-party chatter — so every TeX Live update forces
mass `.tlg` regeneration, and regenerating expected output wholesale is how real
regressions get approved by accident.

**The existing tests assert things a log diff cannot express.** Pytest checks
semantic option and measured-value contracts; `tests/run-tests.sh` compiles the
focused LaTeX fixtures. Visual comparison remains an ad hoc proof when a change
needs it, not a new general gate.

Multi-engine checking, l3build's other draw, is moot while the Package is
pdfLaTeX-only.

So `build.lua` declares no test files — a normal configuration — and the v3
target keeps `make test` as pytest followed by `tests/run-tests.sh`, each as one
suite. During the transition, pytest still invokes controlled harness fixtures;
issue #88 removes that duplication after the retained coverage is settled. This
supersedes the l3build migration planned in `docs/PACKAGE_ROADMAP.md` (T-402),
which is withdrawn. That file was deleted on 2026-08-25 by issue #52; the
withdrawal stands, and the roadmap is in git history.

## Consequences

- Packaging and testing remain separate: `build.lua` does not define the test
  suite, and the test harnesses do not publish releases.
- If the Package ever supports XeLaTeX or LuaLaTeX, multi-engine testing has to
  be built rather than configured. Revisit this ADR at that point.
- CTAN acceptance is unaffected either way — no reviewer inspects a test
  harness. L3build makes CTAN packaging repeatable if that separate work resumes;
  it does not justify GitHub release automation.
