# LaTeX Review Findings P1/P2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the two review findings: restore the public `\textapprox` / `\textinfty` API and make the microtype ownership claim true.

**Architecture:** Use TDD for the public symbol API before touching package code. Then consolidate remaining active microtype tuning into `paper/modules/lltmicrotype.sty`, leaving `paper/lltpaperstyle.sty` responsible only for orchestration and non-microtype commands. Preserve default visual output with a before/after PDF raster hash check.

**Tech Stack:** LaTeX2e package code, `pdflatex`, `latexmk`, `microtype`, pytest, shell fixture harness, Poppler `pdftoppm`.

---

## File Structure

- Modify: `tests/test_option_contracts.py`
  - Add focused regression coverage for `\textapprox` and `\textinfty`.
- Modify: `tests/fixtures/special-characters-test.tex`
  - Restore the fixture to use the public text-symbol commands instead of raw math fallback syntax.
- Modify: `paper/lltpaperstyle.sty`
  - Fix T1-safe public text-symbol commands.
  - Remove active `microtype` tuning commands from the main package after moving them to the module.
- Modify: `paper/modules/lltmicrotype.sty`
  - Own all active `microtype` package loading, setup, tracking, spacing, protrusion, expansion, and extra kerning.
- Modify: `docs/technical/LATEX_CODE_REVIEW_2026-05-28.md`
  - Mark P1/P2 review follow-up as resolved after verification.
- Modify: `docs/superpowers/plans/2026-05-28-latex-template-maintainability.md`
  - Correct the implementation results to include this follow-up.
- Modify: `CHANGELOG.md`
  - Record the follow-up fixes under `2026-05-28`.

## Checkpoint Rules

- Every LaTeX package fix must include a `%% FIX:` comment with a one-line rationale.
- Do not change margins, fonts, colors, spacing, numbering schemes, or float placement defaults.
- Before moving the remaining microtype commands, capture `main.pdf` raster hashes.
- After moving them, rebuild and compare every raster page byte-for-byte against the captured baseline.
- Required final gates:

```bash
make lint
make build
pytest -q
tests/run-tests.sh
```

---

### Task 1: Reproduce and Test the P1 Symbol API Failure

**Files:**
- Modify: `tests/test_option_contracts.py`
- Modify: `tests/fixtures/special-characters-test.tex`

- [ ] **Step 1: Add a failing pytest contract for text symbols**

Append this test to `tests/test_option_contracts.py`:

```python
def test_text_symbol_commands_compile_in_t1_encoding(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "text-symbol-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage{lltpaperstyle}
        \begin{document}
        The value is \textapprox 3.14159.
        The limit approaches \textinfty.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "Command \\textapprox unavailable in encoding T1" not in log_text
    assert "Command \\textinfty unavailable in encoding T1" not in log_text
```

- [ ] **Step 2: Restore the fixture to test the public API**

In `tests/fixtures/special-characters-test.tex`, replace:

```latex
The value is $\approx$ 3.14159.

The limit approaches $\infty$.
```

with:

```latex
The value is \textapprox 3.14159.

The limit approaches \textinfty.
```

- [ ] **Step 3: Run the focused tests and confirm failure**

Run:

```bash
pytest tests/test_option_contracts.py::test_text_symbol_commands_compile_in_t1_encoding -q
tests/run-tests.sh tests/fixtures/special-characters-test.tex
```

Expected:
- pytest fails with a T1 encoding error for `\textapprox`.
- the fixture harness fails with the same public API failure.

---

### Task 2: Fix the P1 Public Symbol Commands

**Files:**
- Modify: `paper/lltpaperstyle.sty`
- Test: `tests/test_option_contracts.py`
- Test: `tests/fixtures/special-characters-test.tex`

- [ ] **Step 1: Replace the fragile text-symbol definitions**

In `paper/lltpaperstyle.sty`, replace the current `\textapprox` and `\textinfty` definitions:

```latex
\newcommand{\textapprox}{\kern0.08em\ensuremath{\approx}\kern0.08em}
\newcommand{\textinfty}{\kern0.08em\ensuremath{\infty}\kern0.08em}
```

with this encoding-safe form:

```latex
%% FIX: Define text-symbol commands as robust wrappers instead of encoding-bound text commands.
\DeclareRobustCommand{\llttextapprox}{\kern0.08em\ensuremath{\approx}\kern0.08em}
\DeclareRobustCommand{\llttextinfty}{\kern0.08em\ensuremath{\infty}\kern0.08em}
\makeatletter
\@ifundefined{textapprox}{%
  \DeclareRobustCommand{\textapprox}{\llttextapprox}%
}{%
  \DeclareRobustCommand{\textapprox}{\llttextapprox}%
}
\@ifundefined{textinfty}{%
  \DeclareRobustCommand{\textinfty}{\llttextinfty}%
}{%
  \DeclareRobustCommand{\textinfty}{\llttextinfty}%
}
\makeatother
```

Rationale: this avoids `\DeclareTextCommand` encoding-table conflicts and ensures the public commands expand to math-safe glyphs in any text encoding.

- [ ] **Step 2: Run the focused symbol checks**

Run:

```bash
pytest tests/test_option_contracts.py::test_text_symbol_commands_compile_in_t1_encoding -q
tests/run-tests.sh tests/fixtures/special-characters-test.tex
```

Expected:
- pytest passes.
- fixture harness reports `Passed: 3`, `Failed: 0`.

- [ ] **Step 3: Inspect for stale fixture bypasses**

Run:

```bash
rg -n '\$\\approx\$|\$\\infty\$' tests/fixtures/special-characters-test.tex tests/test_option_contracts.py
```

Expected:
- no matches.

---

### Task 3: Capture the Default Visual Baseline Before P2

**Files:**
- No source changes.

- [ ] **Step 1: Build the current default PDF**

Run:

```bash
make build
```

Expected:
- exit code `0`
- `main.pdf` exists

- [ ] **Step 2: Render the visual baseline**

Run:

```bash
mkdir -p /tmp/llt-p1-p2-visual
pdftoppm -r 144 -png main.pdf /tmp/llt-p1-p2-visual/main-before
```

Expected:
- files `/tmp/llt-p1-p2-visual/main-before-01.png` through `/tmp/llt-p1-p2-visual/main-before-41.png` exist.

- [ ] **Step 3: Record baseline hashes**

Run:

```bash
shasum -a 256 /tmp/llt-p1-p2-visual/main-before-*.png > /tmp/llt-p1-p2-visual/main-before.sha256
```

Expected:
- `/tmp/llt-p1-p2-visual/main-before.sha256` contains 41 rows.

---

### Task 4: Move Remaining Active Microtype Tuning Into `lltmicrotype`

**Files:**
- Modify: `paper/lltpaperstyle.sty`
- Modify: `paper/modules/lltmicrotype.sty`

- [ ] **Step 1: Move the remaining active tracking/kerning block**

Move the active microtype commands currently in `paper/lltpaperstyle.sty` around the small-caps tracking section into `paper/modules/lltmicrotype.sty`, after the initial `\microtypesetup` branch and before the protrusion section.

The moved block must include the active commands matching this search:

```bash
rg -n 'SetTracking|SetExtraKerning' paper/lltpaperstyle.sty
```

At minimum, move these command families:

```latex
\SetTracking{...}{...}
\SetExtraKerning[unit=space] {...} {...}
```

Add this comment above the moved block in `paper/modules/lltmicrotype.sty`:

```latex
%% FIX: Keep active tracking and extra-kerning setup in the microtype module.
```

- [ ] **Step 2: Leave only a non-active note in the main package**

Replace the moved block in `paper/lltpaperstyle.sty` with:

```latex
%% FIX: Active microtype tracking and extra-kerning setup lives in lltmicrotype.
% Small-caps and code commands below rely on lltmicrotype for tracking/kerning.
```

- [ ] **Step 3: Confirm `lltpaperstyle` no longer owns active microtype tuning**

Run:

```bash
rg -n 'SetTracking|SetProtrusion|SetExpansion|SetExtraSpacing|SetExtraKerning|microtypesetup|RequirePackage(\[[^]]*\])?\{microtype\}' paper/lltpaperstyle.sty
```

Expected:
- no matches, except comments containing `microtype` are acceptable only if they do not include active command names.

- [ ] **Step 4: Confirm `lltmicrotype` is the sole active owner**

Run:

```bash
rg -n 'SetTracking|SetProtrusion|SetExpansion|SetExtraSpacing|SetExtraKerning|microtypesetup|RequirePackage(\[[^]]*\])?\{microtype\}' paper/modules/lltmicrotype.sty
```

Expected:
- all active microtype setup matches are in `paper/modules/lltmicrotype.sty`.
- `\SetExtraKerning` may appear here only for the active settings moved from `lltpaperstyle`; do not reintroduce the stale module-only `\SetExtraKerning` block that was previously removed.

---

### Task 5: Verify P2 Did Not Change Default Output

**Files:**
- No source changes unless verification fails.

- [ ] **Step 1: Rebuild after the move**

Run:

```bash
make build
```

Expected:
- exit code `0`
- `main.pdf` exists

- [ ] **Step 2: Render the post-move PDF**

Run:

```bash
pdftoppm -r 144 -png main.pdf /tmp/llt-p1-p2-visual/main-after
```

Expected:
- files `/tmp/llt-p1-p2-visual/main-after-01.png` through `/tmp/llt-p1-p2-visual/main-after-41.png` exist.

- [ ] **Step 3: Compare every page raster**

Run:

```bash
zsh -lc 'for before in /tmp/llt-p1-p2-visual/main-before-*.png; do after=${before/main-before/main-after}; cmp -s "$before" "$after" || { echo "DIFF ${before:t}"; exit 1; }; done; echo "visual hashes match"'
```

Expected:

```text
visual hashes match
```

If this fails, stop. Do not accept a visual delta for P2 without explicitly documenting the page-level diff and getting approval.

---

### Task 6: Update Documentation for the Follow-Up Resolution

**Files:**
- Modify: `docs/technical/LATEX_CODE_REVIEW_2026-05-28.md`
- Modify: `docs/superpowers/plans/2026-05-28-latex-template-maintainability.md`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Update the code review report**

In `docs/technical/LATEX_CODE_REVIEW_2026-05-28.md`, add under `Resolution Status`:

```markdown
- Follow-up P1/P2 review findings resolved: `\textapprox` and `\textinfty`
  compile as public package commands, and active microtype tuning is owned by
  `lltmicrotype`.
```

- [ ] **Step 2: Update the maintainability plan results**

In `docs/superpowers/plans/2026-05-28-latex-template-maintainability.md`, add to `Implementation Results`:

```markdown
- Follow-up review resolved the remaining P1/P2 issues: public text-symbol
  commands are tested directly, and active microtype tuning no longer remains in
  `lltpaperstyle.sty`.
```

- [ ] **Step 3: Update the changelog**

In `CHANGELOG.md`, under `2026-05-28`, add:

```markdown
- Fixed follow-up review findings for public text-symbol commands and completed
  active microtype ownership consolidation in `lltmicrotype`.
```

---

### Task 7: Final Verification

**Files:**
- No source changes unless verification fails.

- [ ] **Step 1: Run required gates**

Run:

```bash
make lint
make build
pytest -q
tests/run-tests.sh
```

Expected:
- `make lint` exits `0`
- `make build` exits `0`
- `pytest -q` reports all tests passing
- `tests/run-tests.sh` reports all fixture checks passing

- [ ] **Step 2: Run ownership and fixture-bypass guards**

Run:

```bash
rg -n '\$\\approx\$|\$\\infty\$' tests/fixtures/special-characters-test.tex tests/test_option_contracts.py
rg -n 'SetTracking|SetProtrusion|SetExpansion|SetExtraSpacing|SetExtraKerning|microtypesetup|RequirePackage(\[[^]]*\])?\{microtype\}' paper/lltpaperstyle.sty
rg -n 'SetTracking|SetProtrusion|SetExpansion|SetExtraSpacing|SetExtraKerning|microtypesetup|RequirePackage(\[[^]]*\])?\{microtype\}' paper/modules/lltmicrotype.sty
```

Expected:
- first command: no matches
- second command: no active microtype command matches in `lltpaperstyle.sty`
- third command: active microtype commands exist in `lltmicrotype.sty`

- [ ] **Step 3: Check final diff**

Run:

```bash
git diff --check
git status --short
```

Expected:
- `git diff --check` exits `0`
- `git status --short` shows only intentional source, test, fixture, and documentation changes.

## Self-Review

- Spec coverage: P1 is covered by Tasks 1-2 and Task 7. P2 is covered by Tasks 3-5 and Task 7. Documentation closeout is covered by Task 6.
- Placeholder scan: no placeholders remain; every code step includes concrete replacement text or exact commands.
- Consistency check: the public commands are consistently named `\textapprox` and `\textinfty`; the microtype owner is consistently `paper/modules/lltmicrotype.sty`.

