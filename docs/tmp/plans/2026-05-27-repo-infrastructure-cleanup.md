# Repo Infrastructure Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restore the repository infrastructure so `AGENTS.md` is the authoritative build contract and the required lint, build, and regression gates can be run repeatably without changing LaTeX visual design.

**Architecture:** Keep the cleanup focused on build/test plumbing, merge-state repair, active package-name references, and documentation. Add a small pytest layer that checks infrastructure contracts and delegates LaTeX regression compilation to the existing shell harness. Preserve all typography, layout, spacing, figure placement, numbering, colors, and fonts.

**Tech Stack:** GNU Make, latexmk, chktex, latexindent, pdflatex/biber, pytest, Bash, LaTeX.

---

## Current Evidence

- `git status --short --branch` reports `UU main.tex` on `main...origin/main [ahead 1, behind 2]`.
- `main.tex:24-29` contains unresolved merge markers around the Quick Reference paragraph.
- `AGENTS.md` requires `make lint`, `make build`, `make fmt`, `chktex -q -n8 -n46 *.tex`, `latexmk -pdf -interaction=nonstopmode main.tex`, and `pytest -q`.
- `Makefile` lacks `lint`, `build`, and `fmt` targets.
- `Makefile:104-105` validates `paper/paperstyle.sty`, but the active package file is `paper/lltpaperstyle.sty`.
- `Makefile:230` writes `\usepackage{paper/paperstyle}` in the diagnostic target.
- Root `CHANGELOG.md` is missing; only `docs/style/CHANGELOG.md` exists.
- `tests/run-tests.sh`, `tests/test-bibliography.sh`, `tests/check-spacing-integrity.sh`, and `src/sh/validate_latex_style.sh` are not executable.
- Several active fixtures still use `\usepackage{../../paper/paperstyle}` even though `paper/paperstyle.sty` is no longer shipped.
- Local TeX evidence from review: TeX Live 2025 at `/usr/local/texlive/2025`, latexmk 4.86a, Biber 2.20.
- Overleaf build evidence is not available locally; final documentation must use the exact current Overleaf project log/build information before claiming Definition of Done.

## File Responsibility Map

- `main.tex`: resolve only the merge conflict block; add a TeX comment with `%% FIX:` and keep the branch's `\safeparagraph` behavior.
- `Makefile`: expose AGENTS aliases, fix stale package validation, update diagnostic package load, and keep legacy targets working.
- `tests/test_infrastructure.py`: pytest contract tests for merge markers, Makefile targets, executable scripts, root changelog, and stale active package references.
- `tests/test_regression_harness.py`: pytest wrapper around the existing LaTeX shell regression harness.
- `pytest.ini`: make `pytest -q` discover only the intended local tests.
- `tests/run-tests.sh`: accept an optional fixture argument, avoid unbound `TEXINPUTS`, and remain callable from Make and pytest.
- `tests/fixtures/*.tex`: update active package loads from `paperstyle` to `lltpaperstyle` without changing document content.
- `CHANGELOG.md`: root changelog required by `AGENTS.md` and linked by `README.md`.
- `README.md`: document the authoritative commands and tested local/Overleaf build evidence.

## Execution Notes

- In TeX files, every implementation fix must use a one-line `%% FIX:` comment immediately above the changed line or block.
- In non-TeX files, use the file's native comment syntax with `FIX:`. Do not insert raw `%%` into Makefiles or shell scripts because that would be invalid syntax.
- Do not change margins, fonts, colors, spacing, numbering schemes, or figure placement defaults.
- Do not suppress failing gates. If a gate fails, fix the cause or stop with the exact remaining failure.
- Because the repository is currently in an unmerged state, finish Task 1 before creating commits for later tasks.

---

### Task 1: Resolve the `main.tex` Merge State

**Files:**
- Modify: `main.tex:24-29`

- [ ] **Step 1: Verify the current merge conflict**

Run:

```bash
git status --short --branch
nl -ba main.tex | sed -n '18,34p'
git diff --check
```

Expected:

```text
UU main.tex
main.tex:24: leftover conflict marker
main.tex:26: leftover conflict marker
main.tex:29: leftover conflict marker
```

- [ ] **Step 2: Replace the conflict block with the current branch's safe paragraph form**

Replace `main.tex:24-29` with exactly:

```latex
%% FIX: Resolve merge marker by keeping the safe paragraph command used throughout the template.
\safeparagraph{Quick Reference} For a complete guide to all commands and environments:
```

Rationale: `\safeparagraph` is already the dominant local pattern and avoids the paragraph-mode issue referenced by recent commits. This preserves the intended branch behavior while removing rendered merge text.

- [ ] **Step 3: Verify conflict markers are gone**

Run:

```bash
rg -n "^(<{7}|={7}|>{7})" main.tex
git diff --check
```

Expected:

```text
rg exits 1 with no matches
git diff --check exits 0
```

- [ ] **Step 4: Mark the merge file resolved**

Run:

```bash
git add main.tex
git status --short
```

Expected:

```text
M  main.tex
```

If `.git/MERGE_HEAD` exists, do not create the merge commit yet. Complete the infrastructure tasks below, then commit all related cleanup together unless the user asks for a separate merge commit.

---

### Task 2: Add Pytest Infrastructure Contract Tests

**Files:**
- Create: `tests/test_infrastructure.py`
- Create: `pytest.ini`

- [ ] **Step 1: Create `pytest.ini`**

Add exactly:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = -ra
```

- [ ] **Step 2: Create `tests/test_infrastructure.py`**

Add exactly:

```python
import os
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_SOURCE_SUFFIXES = {".tex", ".sty", ".sh", ".py"}
ACTIVE_SCAN_ROOTS = ("main.tex", "appendices/", "paper/", "src/", "tests/", "Makefile")


def run_git(args):
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def tracked_active_source_files():
    result = run_git(["ls-files"])
    for rel_path in result.stdout.splitlines():
        path = ROOT / rel_path
        if rel_path.startswith(("archive/", "docs/archive/")):
            continue
        if rel_path == "Makefile" or rel_path.endswith(ACTIVE_SOURCE_SUFFIXES):
            yield rel_path, path


def test_no_unresolved_merge_markers_in_active_sources():
    marker_re = re.compile(r"^(<{7}|={7}|>{7})", re.MULTILINE)
    offenders = []
    for rel_path, path in tracked_active_source_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        if marker_re.search(text):
            offenders.append(rel_path)
    assert offenders == []


def test_makefile_exposes_agents_targets():
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    for target in ("build", "lint", "fmt"):
        assert re.search(rf"^\.PHONY:.*\b{target}\b", makefile, re.MULTILINE)
        assert re.search(rf"^{target}:", makefile, re.MULTILINE)


def test_required_shell_harnesses_are_executable():
    rel_paths = [
        "src/sh/validate_latex_style.sh",
        "tests/run-tests.sh",
        "tests/test-bibliography.sh",
        "tests/check-spacing-integrity.sh",
    ]
    non_executable = [
        rel_path
        for rel_path in rel_paths
        if not os.access(ROOT / rel_path, os.X_OK)
    ]
    assert non_executable == []


def test_root_changelog_exists():
    assert (ROOT / "CHANGELOG.md").is_file()


def test_active_build_inputs_do_not_use_removed_paperstyle_package():
    stale_re = re.compile(r"paper/paperstyle|paperstyle\.sty")
    offenders = []
    for rel_path, path in tracked_active_source_files():
        if rel_path.startswith(("docs/", "archive/")):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if stale_re.search(text):
            offenders.append(rel_path)
    assert offenders == []
```

- [ ] **Step 3: Run the new tests to confirm they fail against current infrastructure**

Run:

```bash
python3 -m pytest tests/test_infrastructure.py -q
```

Expected failures at this point:

```text
test_makefile_exposes_agents_targets
test_required_shell_harnesses_are_executable
test_root_changelog_exists
test_active_build_inputs_do_not_use_removed_paperstyle_package
```

If pytest exits abnormally with no output, run:

```bash
python3 -X faulthandler -m pytest tests/test_infrastructure.py -q
python3 -m pytest --trace-config
```

Expected: one of these commands prints the failing plugin or interpreter issue. Fix that issue before continuing because `pytest -q` is an authoritative gate.

- [ ] **Step 4: Stage the tests**

Run:

```bash
git add pytest.ini tests/test_infrastructure.py
```

Do not commit until Task 6 proves `pytest -q` can run the intended harness.

---

### Task 3: Align `Makefile` Targets with `AGENTS.md`

**Files:**
- Modify: `Makefile:4-13`
- Modify: `Makefile:30-48`
- Modify: `Makefile:100-117`
- Modify: `Makefile:225-236`
- Modify: `Makefile:255-end`

- [ ] **Step 1: Add command variables**

Modify the variable block so it includes exactly these additional variables:

```make
LATEXMK = latexmk
CHKTEX = chktex
LATEXINDENT = latexindent
```

The top variable block should become:

```make
# Variables
MAIN = main
LATEX = pdflatex
BIBER = biber
LATEXMK = latexmk
CHKTEX = chktex
LATEXINDENT = latexindent
LATEXFLAGS = -interaction=nonstopmode -halt-on-error
PYTHON = python3
BLACK = black
```

- [ ] **Step 2: Add authoritative AGENTS aliases after `all: pdf`**

Insert exactly:

```make
# FIX: Mirror AGENTS.md verification commands without changing legacy targets.
.PHONY: build
build:
	$(LATEXMK) -pdf -interaction=nonstopmode $(MAIN).tex

# FIX: Keep the lint gate identical to AGENTS.md.
.PHONY: lint
lint:
	$(CHKTEX) -q -n8 -n46 *.tex

# FIX: Provide the documented indentation-only formatting target.
.PHONY: fmt
fmt:
	$(LATEXINDENT) -l -w $(MAIN).tex $(PAPER_DIR)/*.tex $(APPENDICES_DIR)/*.tex
```

- [ ] **Step 3: Update `validate` to check the renamed package**

Replace:

```make
	@if ! test -f $(PAPER_DIR)/paperstyle.sty; then \
		echo "==> ERROR: paperstyle.sty not found"; exit 1; \
	fi
```

with:

```make
	@if ! test -f $(PAPER_DIR)/lltpaperstyle.sty; then \
		echo "==> ERROR: lltpaperstyle.sty not found"; exit 1; \
	fi
```

Add this native Makefile comment immediately above the check:

```make
	# FIX: Validate the renamed package that is actually shipped.
```

- [ ] **Step 4: Update the diagnostic package load**

Replace:

```make
	@echo "\\usepackage{paper/paperstyle}" >> diagnose.tex
```

with:

```make
	@echo "% FIX: Load the renamed package for diagnostics." >> diagnose.tex
	@echo "\\usepackage{lltpaperstyle}" >> diagnose.tex
```

- [ ] **Step 5: Update `make help` output**

Add the following lines under the compilation targets section:

```make
	@echo "  make build      - AGENTS.md latexmk build gate"
	@echo "  make lint       - AGENTS.md chktex lint gate"
	@echo "  make fmt        - Run latexindent on active TeX sources"
```

- [ ] **Step 6: Verify target availability**

Run:

```bash
make -n build
make -n lint
make -n fmt
make validate
python3 -m pytest tests/test_infrastructure.py::test_makefile_exposes_agents_targets -q
```

Expected:

```text
make -n build prints latexmk -pdf -interaction=nonstopmode main.tex
make -n lint prints chktex -q -n8 -n46 *.tex
make -n fmt prints latexindent -l -w main.tex paper/*.tex appendices/*.tex
make validate exits 0
pytest target test passes
```

- [ ] **Step 7: Stage the Makefile**

Run:

```bash
git add Makefile
```

---

### Task 4: Make Shell Harnesses Executable and Robust

**Files:**
- Modify mode: `src/sh/validate_latex_style.sh`
- Modify mode: `tests/run-tests.sh`
- Modify mode: `tests/test-bibliography.sh`
- Modify mode: `tests/check-spacing-integrity.sh`
- Modify: `tests/run-tests.sh`

- [ ] **Step 1: Add executable bits**

Run:

```bash
chmod +x src/sh/validate_latex_style.sh tests/run-tests.sh tests/test-bibliography.sh tests/check-spacing-integrity.sh
```

- [ ] **Step 2: Make `TEXINPUTS` safe under `set -u`**

In `tests/run-tests.sh`, replace:

```bash
    export TEXINPUTS=".:./paper:./paper/modules:$TEXINPUTS"
```

with:

```bash
    # FIX: Keep direct script runs working when TEXINPUTS is unset.
    export TEXINPUTS=".:./paper:./paper/modules:${TEXINPUTS:-}"
```

- [ ] **Step 3: Make optional fixture arguments actually work**

In `tests/run-tests.sh`, replace the current fixture discovery block:

```bash
    # Find all test fixtures
    local fixtures=($(find "$FIXTURES_DIR" -name "*.tex" -type f | sort))
    
    if [ ${#fixtures[@]} -eq 0 ]; then
        echo -e "${YELLOW}No test fixtures found in $FIXTURES_DIR${NC}"
        exit 0
    fi
```

with:

```bash
    # FIX: Honor explicit fixture arguments for quick regression runs.
    local fixtures=()
    if [ "$#" -gt 0 ]; then
        for fixture_arg in "$@"; do
            if [ ! -f "$fixture_arg" ]; then
                echo -e "${RED}Error: fixture not found: $fixture_arg${NC}"
                exit 1
            fi
            fixtures+=("$fixture_arg")
        done
    else
        while IFS= read -r fixture; do
            fixtures+=("$fixture")
        done < <(find "$FIXTURES_DIR" -name "*.tex" -type f | sort)
    fi

    if [ ${#fixtures[@]} -eq 0 ]; then
        echo -e "${YELLOW}No test fixtures found in $FIXTURES_DIR${NC}"
        exit 0
    fi
```

- [ ] **Step 4: Verify script permissions and quick fixture behavior**

Run:

```bash
ls -l src/sh/validate_latex_style.sh tests/run-tests.sh tests/test-bibliography.sh tests/check-spacing-integrity.sh
python3 -m pytest tests/test_infrastructure.py::test_required_shell_harnesses_are_executable -q
bash tests/run-tests.sh tests/fixtures/minimal-root.tex
make test-quick
```

Expected:

```text
Each listed script mode contains x.
pytest executable-bit test passes.
bash tests/run-tests.sh tests/fixtures/minimal-root.tex tests one fixture only.
make test-quick tests one fixture only.
```

If the fixture compile fails because it uses the removed `paperstyle` package, continue to Task 5 and rerun this step.

- [ ] **Step 5: Stage script changes**

Run:

```bash
git add src/sh/validate_latex_style.sh tests/run-tests.sh tests/test-bibliography.sh tests/check-spacing-integrity.sh
```

---

### Task 5: Remove Active Stale `paperstyle` References

**Files:**
- Modify: `tests/fixtures/float-test.tex`
- Modify: `tests/fixtures/heading-optimization-test.tex`
- Modify: `tests/fixtures/crossref-test.tex`
- Modify: `tests/fixtures/quote-test.tex`
- Modify: `tests/fixtures/opening-test.tex`
- Modify: `tests/fixtures/special-characters-test.tex`
- Modify: `tests/fixtures/caption-test.tex`
- Modify: `tests/fixtures/emphasis-test.tex`
- Modify: `tests/fixtures/hyphenation-test.tex`
- Modify: `tests/fixtures/list-optimization-test.tex`
- Modify: `tests/fixtures/minimal-opening-test.tex`
- Modify: `paper/preamble.tex`
- Modify: `paper/lltpaperstyle.sty`

- [ ] **Step 1: Update fixture package loads**

In each listed fixture, replace:

```latex
\usepackage{../../paper/paperstyle}
```

with:

```latex
%% FIX: Use the renamed package file; paperstyle.sty is no longer shipped.
\usepackage{../../paper/lltpaperstyle}
```

- [ ] **Step 2: Update preamble prose and package load**

In `paper/preamble.tex`, update comments that say `paperstyle.sty` to `lltpaperstyle.sty`.

Replace:

```latex
\usepackage{paper/lltpaperstyle}
```

with:

```latex
%% FIX: Load the renamed package by package name to match \ProvidesPackage.
\usepackage{lltpaperstyle}
```

- [ ] **Step 3: Update the old example comment in `paper/lltpaperstyle.sty`**

Replace:

```latex
%   \usepackage{paper/paperstyle}
```

with:

```latex
%   %% FIX: Document the renamed public package entry point.
%   \usepackage{lltpaperstyle}
```

- [ ] **Step 4: Verify active stale references are gone**

Run:

```bash
rg -n "paper/paperstyle|paperstyle\.sty" Makefile main.tex appendices paper/preamble.tex paper/lltpaperstyle.sty tests src
python3 -m pytest tests/test_infrastructure.py::test_active_build_inputs_do_not_use_removed_paperstyle_package -q
bash tests/run-tests.sh tests/fixtures/minimal-root.tex
```

Expected:

```text
rg exits 1 with no active matches.
pytest stale-reference test passes.
minimal-root fixture compiles successfully.
```

- [ ] **Step 5: Stage package-reference changes**

Run:

```bash
git add tests/fixtures paper/preamble.tex paper/lltpaperstyle.sty
```

---

### Task 6: Make `pytest -q` Run the Regression Harness

**Files:**
- Create: `tests/test_regression_harness.py`
- Modify: `tests/run-tests.sh`

- [ ] **Step 1: Create `tests/test_regression_harness.py`**

Add exactly:

```python
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_minimal_fixture_regression_harness_passes():
    result = subprocess.run(
        ["bash", "tests/run-tests.sh", "tests/fixtures/minimal-root.tex"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
```

- [ ] **Step 2: Run the targeted pytest wrapper**

Run:

```bash
python3 -m pytest tests/test_regression_harness.py -q
```

Expected:

```text
1 passed
```

If this fails with LaTeX warnings from the minimal fixture, inspect `tests/compilation/logs/minimal-root.log` and fix the first real warning or error without changing visual design.

- [ ] **Step 3: Run all pytest tests**

Run:

```bash
pytest -q
```

Expected:

```text
All pytest tests pass, including infrastructure tests and the minimal LaTeX regression harness.
```

- [ ] **Step 4: Stage pytest harness changes**

Run:

```bash
git add pytest.ini tests/test_infrastructure.py tests/test_regression_harness.py tests/run-tests.sh
```

- [ ] **Step 5: Commit the infrastructure harness checkpoint**

Run:

```bash
git status --short
git commit -m "test(infra): add repository infrastructure gates" -m "* add pytest checks for AGENTS.md build contract
* make shell regression harness callable from pytest
* keep package-reference checks focused on active sources"
```

If the repository is still in a merge state and Git asks for a merge commit message, use:

```text
merge: resolve infrastructure cleanup baseline

* keep safe paragraph command in main.tex
* add pytest infrastructure gates
* align active package references with lltpaperstyle
```

---

### Task 7: Restore Root Changelog and README Build Evidence

**Files:**
- Create: `CHANGELOG.md`
- Modify: `README.md`

- [ ] **Step 1: Create root `CHANGELOG.md`**

Add exactly:

```markdown
# Changelog

All notable changes to the Lane LaTeX Template are documented here.

## 2026-05-27

- Restored the repository infrastructure contract so the AGENTS.md lint, build, and regression gates are runnable from the root.
- Resolved the active merge marker in `main.tex` without changing the intended LaTeX layout.
- Updated active build and test references from the removed `paperstyle` package name to `lltpaperstyle`.
- Added pytest coverage for build-target drift, executable shell harnesses, root changelog presence, active package references, and the minimal LaTeX regression harness.
```

- [ ] **Step 2: Add tested environment evidence to `README.md`**

Under `## Installation`, immediately after the prerequisites list, add:

```markdown
### Tested Build Environments

Verified on May 27, 2026:

- **Local**: TeX Live 2025 at `/usr/local/texlive/2025`, `latexmk` 4.86a, Biber 2.20, using `latexmk -pdf -interaction=nonstopmode main.tex`.
- **Overleaf**: Use the exact TeX Live year and build identifier from the current Overleaf compile log before marking this cleanup complete.
```

- [ ] **Step 3: Replace the Overleaf evidence sentence with exact Overleaf data**

Before final commit, compile the project in Overleaf and replace the Overleaf bullet with an evidence-backed line in this exact format:

```markdown
- **Overleaf**: TeX Live YEAR and Overleaf build BUILD_ID, verified on May 27, 2026 with the project Recompile action.
```

Use the actual `YEAR` and `BUILD_ID` from the Overleaf compile log. Do not leave the words `YEAR`, `BUILD_ID`, `current`, `pending`, or `unknown` in `README.md`.

- [ ] **Step 4: Document the authoritative commands in `README.md`**

In the compilation methods section, add this markdown snippet:

````markdown
**Repository verification gates**:

```bash
chktex -q -n8 -n46 *.tex
latexmk -pdf -interaction=nonstopmode main.tex
pytest -q
```
````

- [ ] **Step 5: Verify documentation contract**

Run:

```bash
test -f CHANGELOG.md
rg -n "YEAR|BUILD_ID|pending|unknown|current Overleaf" README.md CHANGELOG.md
python3 -m pytest tests/test_infrastructure.py::test_root_changelog_exists -q
```

Expected:

```text
test -f CHANGELOG.md exits 0.
rg exits 1 with no placeholder or pending Overleaf evidence text.
pytest changelog test passes.
```

- [ ] **Step 6: Stage documentation**

Run:

```bash
git add CHANGELOG.md README.md
```

---

### Task 8: ChkTeX Gate Triage Without Visual Design Changes

**Files:**
- Modify only files reported by `chktex -q -n8 -n46 *.tex`

- [ ] **Step 1: Run the exact AGENTS lint gate**

Run:

```bash
chktex -q -n8 -n46 *.tex
```

Expected before fixes: warnings may remain from source typography examples and command spacing.

- [ ] **Step 2: Fix non-visual warnings first**

Use this decision table:

```text
Warning 1 command terminated with space:
  Remove trailing spaces or add braces where TeX ignores the spacing.

Warning 24 label spacing:
  Move \label immediately after the heading/caption command without changing rendered text.

Warnings caused by merge markers:
  Already fixed in Task 1; any recurrence is a hard failure.

Warnings inside literal command examples:
  Convert the example to a verbatim-safe form only if rendered output is unchanged.

Warnings requiring visible punctuation, quotation, paragraphing, float, table, spacing, or prose changes:
  Stop and report the exact warning. Do not change visual output without user approval.
```

For every TeX source edit, add a one-line `%% FIX:` comment immediately above the changed line or block.

- [ ] **Step 3: Re-run lint after each small batch**

Run:

```bash
chktex -q -n8 -n46 *.tex
```

Expected for completion:

```text
exit 0 with no output
```

- [ ] **Step 4: Stage lint-only source changes**

Run:

```bash
git add main.tex appendices paper tests/fixtures
```

- [ ] **Step 5: Commit lint cleanup**

Run:

```bash
git status --short
git commit -m "fix(latex): clear nonvisual lint blockers" -m "* remove source-only ChkTeX blockers
* preserve typography and layout defaults
* keep AGENTS.md lint gate authoritative"
```

If a warning requires visible output changes, do not run this commit. Record the warning and request user approval.

---

### Task 9: Final Local Build and Regression Verification

**Files:**
- No planned edits unless a gate identifies a concrete defect.

- [ ] **Step 1: Confirm the worktree is staged or clean enough for verification**

Run:

```bash
git status --short --branch
```

Expected:

```text
No unmerged paths.
Only intentional cleanup files are modified or staged.
```

- [ ] **Step 2: Run the exact required gates**

Run:

```bash
chktex -q -n8 -n46 *.tex
latexmk -pdf -interaction=nonstopmode main.tex
pytest -q
```

Expected:

```text
chktex exits 0.
latexmk exits 0 and writes main.pdf.
pytest exits 0.
```

- [ ] **Step 3: Verify no merge text appears in the generated PDF**

Run:

```bash
pdftotext main.pdf - | rg -n "origin/main|merge marker|={7}|>{7}|<{7}"
```

Expected:

```text
rg exits 1 with no matches.
```

- [ ] **Step 4: Inspect LaTeX warnings**

Run:

```bash
make warnings
```

Expected:

```text
No package warnings that contradict AGENTS.md Definition of Done.
Any overfull or underfull boxes are unchanged from the pre-cleanup baseline, or are explicitly documented as existing visual-layout debt outside this infrastructure cleanup.
```

- [ ] **Step 5: Commit final documentation and verification state**

Run:

```bash
git status --short
git add CHANGELOG.md README.md Makefile pytest.ini tests src main.tex paper appendices
git commit -m "chore(infra): align build gates with AGENTS contract" -m "* add documented lint, build, format, and pytest gates
* restore changelog and tested build documentation
* repair active lltpaperstyle references without visual design changes"
```

If previous task commits already captured every staged change, skip this commit and record that the tree is clean.

---

## Self-Review

**Spec coverage:**

- Do not change visual LaTeX output: covered by Execution Notes, Tasks 1, 5, 8, and 9.
- Treat `AGENTS.md` as authoritative: covered by Tasks 3, 6, 8, and 9.
- Fix unresolved `main.tex` merge state: covered by Task 1.
- Align `Makefile` targets with `AGENTS.md`: covered by Task 3.
- Fix stale `paperstyle.sty` references after rename: covered by Task 5.
- Restore/create root `CHANGELOG.md`: covered by Task 7.
- Make shell harnesses executable/callable: covered by Task 4.
- Make `pytest -q` run the regression harness: covered by Tasks 2 and 6.
- Update README with tested local TeX Live and Overleaf build information: covered by Task 7, with an explicit Overleaf evidence blocker.
- End with required gates: covered by Task 9.

**Placeholder scan:**

- The plan intentionally forbids leaving `YEAR`, `BUILD_ID`, `pending`, `unknown`, or `current Overleaf` in committed README content.
- The only external fact not available locally is the Overleaf build identifier; Task 7 blocks completion until that evidence is supplied.

**Type and command consistency:**

- Pytest commands use `pytest -q` for the final gate and `python3 -m pytest` for targeted diagnostics.
- Make targets match `AGENTS.md`: `make lint`, `make build`, and `make fmt`.
- The build gate uses the exact required `latexmk -pdf -interaction=nonstopmode main.tex`.

---

## Execution Handoff

Plan complete and saved to `docs/tmp/plans/2026-05-27-repo-infrastructure-cleanup.md`. Two execution options:

1. **Subagent-Driven (recommended for parallel review)** - dispatch a fresh subagent per task, review between tasks, and keep the visual-output constraint under review.

2. **Inline Execution** - execute tasks in this session using `superpowers:executing-plans`, with checkpoints after Task 1, Task 4, Task 6, and Task 9.

For this repository, inline execution is the better default because the current unmerged state and no-visual-change constraint require tight local control.
