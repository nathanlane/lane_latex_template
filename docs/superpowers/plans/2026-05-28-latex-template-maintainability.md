# LaTeX Template Maintainability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the package maintainability and option-contract issues reported in `docs/technical/LATEX_CODE_REVIEW_2026-05-28.md` without changing the default visual design.

**Architecture:** Add focused option-contract tests first, then make the smallest package changes needed to align implementation with documented behavior. Preserve current default output by keeping default options visually equivalent and using regression gates after every code task.

**Tech Stack:** LaTeX2e package code, `pdflatex`, `latexmk`, `chktex`, pytest, shell fixture harness, `biblatex`, `natbib`, `microtype`, `xcolor`, `hyperref`, `cleveref`.

---

## Resolution Status

- `accepted-current`: Resolve all reviewer findings in this plan before implementation.
- `accepted-current`: Make `lltmicrotype` the only owner of microtype package loading and tuning during the consolidation task.
- `accepted-current`: Add a before/after PDF raster hash checkpoint for default-output changes before and after microtype consolidation.
- `accepted-current`: Define `natbib` mode as native natbib command support, not full biblatex command emulation.
- `accepted-current`: Add tests for `nosubsectionbarriers` and `[minimal,nocolor]`.
- `accepted-current`: Add `tests/run-tests.sh` as the supplemental package-code compile gate.

## Plan Deltas

- Task 1 now includes option-contract tests for native natbib optional arguments, `nosubsectionbarriers`, and `[minimal,nocolor]`.
- Task 3 no longer references a non-existent `\microtypesetup` block in `lltmicrotype`.
- Task 4 no longer installs weak one-argument biblatex aliases in natbib mode.
- Task 6 verifies both enabled and disabled subsection barrier modes.
- Task 7 is now a replacement/consolidation task with explicit before/after visual regression commands.
- Every package-code task now runs `tests/run-tests.sh` in addition to the root lint/build/pytest gates.

## File Structure

- Create: `tests/test_option_contracts.py`
  - Pytest contract tests for `nocolor`, `draft`, `natbib`, `nobiblatex`, normal `\ref`, and float-barrier option behavior.
- Modify: `paper/lltpaperstyle.sty`
  - Correct option handling, remove runtime `\ref` warning, make subsection float barriers explicit, and route microtype through one authoritative path.
- Modify: `paper/modules/lltcolors.sty`
  - Make semantic color definitions respect `\ifllt@nocolor` while remaining standalone-loadable.
- Modify: `paper/modules/lltmicrotype.sty`
  - Become the authoritative microtype configuration module, with draft/final branching.
- Modify: `README.md`
  - Correct documented option behavior and note the contract tests.
- Modify: `CHANGELOG.md`
  - Record each material fix under `2026-05-28`.

## Checkpoint Rules

- After every test-writing step, run the targeted pytest command and confirm the test fails for the expected reason.
- After every implementation step, run the targeted pytest command and confirm it passes.
- After each task, run:

```bash
make lint
make build
pytest -q
tests/run-tests.sh
```

- Do not accept a package-code change if it changes default visual output unless the change is explicitly documented and approved.
- Before and after microtype consolidation, render `main.pdf` to PNG raster files with `pdftoppm` and compare SHA-256 hashes.
  If `pdftoppm` is unavailable, stop and install Poppler or explicitly record a waived visual-regression checkpoint before continuing.
- Every LaTeX code fix must include a `%% FIX:` comment with a one-line rationale.

---

### Task 1: Add Option-Contract Regression Tests

**Files:**
- Create: `tests/test_option_contracts.py`

- [ ] **Step 1: Add the pytest helper and failing contract tests**

Create `tests/test_option_contracts.py` with this content:

```python
import os
import re
import subprocess
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def compile_latex(tmp_path, name, source):
    tex_file = tmp_path / f"{name}.tex"
    tex_file.write_text(textwrap.dedent(source), encoding="utf-8")
    env = os.environ.copy()
    env["TEXINPUTS"] = f".:{ROOT / 'paper'}:{ROOT / 'paper/modules'}:{env.get('TEXINPUTS', '')}"
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_file.name],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    log_text = (tmp_path / f"{name}.log").read_text(
        encoding="utf-8", errors="ignore"
    )
    return result, log_text


def assert_compiles(result, log_text):
    assert result.returncode == 0, result.stdout + result.stderr + log_text


def test_nocolor_maps_semantic_colors_to_black(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "nocolor-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage[nocolor]{lltpaperstyle}
        \makeatletter
        \newcommand{\showcolorhex}[2]{%
          \convertcolorspec{named}{#1}{HTML}{#2}%
        }
        \makeatother
        \begin{document}
        \showcolorhex{sectioncolor}{\lltsectionhex}
        \showcolorhex{linknavy}{\lltlinkhex}
        \typeout{LLT_SECTION_HEX=\lltsectionhex}
        \typeout{LLT_LINK_HEX=\lltlinkhex}
        \section{No Color}
        Body text.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "LLT_SECTION_HEX=000000" in log_text
    assert "LLT_LINK_HEX=000000" in log_text


def test_minimal_nocolor_compiles(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "minimal-nocolor-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage[minimal,nocolor]{lltpaperstyle}
        \begin{document}
        \typeout{LLT_MINIMAL_NOCOLOR_OK}
        Minimal no-color contract.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "LLT_MINIMAL_NOCOLOR_OK" in log_text


def test_draft_option_reports_microtype_draft_mode(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "draft-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage[draft]{lltpaperstyle}
        \begin{document}
        Draft mode contract.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert re.search(r"Package llt(paperstyle|microtype) Info: microtype draft mode active", log_text)


def test_natbib_option_provides_native_natbib_commands(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "natbib-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage[natbib]{lltpaperstyle}
        \begin{document}
        Natbib cite commands compile:
        \citet[chap.~2]{smith2020} and \citep[see][45]{smith2020}.
        \begin{thebibliography}{9}
        \bibitem[Smith(2020)]{smith2020} Smith, A. 2020. Title.
        \end{thebibliography}
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "Undefined control sequence" not in log_text


def test_nobiblatex_does_not_load_biblatex(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "nobiblatex-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage[nobiblatex]{lltpaperstyle}
        \begin{document}
        No automatic bibliography package.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "biblatex.sty" not in log_text


def test_plain_ref_does_not_emit_package_warning(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "plain-ref-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage{lltpaperstyle}
        \begin{document}
        \section{Target}\label{sec:target}
        Plain reference: \ref{sec:target}.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "Direct \\ref usage detected" not in log_text


def test_subsection_barriers_are_explicitly_reported(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "barrier-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage{lltpaperstyle}
        \begin{document}
        \section{One}
        \subsection{Two}
        Body text.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert re.search(
        r"Package lltpaperstyle Info: subsection float barriers (enabled|disabled)",
        log_text,
    )


def test_nosubsectionbarriers_reports_disabled_mode(tmp_path):
    result, log_text = compile_latex(
        tmp_path,
        "no-subsection-barrier-contract",
        r"""
        \documentclass[11pt]{article}
        \usepackage[nosubsectionbarriers]{lltpaperstyle}
        \begin{document}
        \section{One}
        \subsection{Two}
        Body text.
        \end{document}
        """,
    )
    assert_compiles(result, log_text)
    assert "Package lltpaperstyle Info: subsection float barriers disabled" in log_text
```

- [ ] **Step 2: Run the focused tests and verify failures**

Run:

```bash
pytest tests/test_option_contracts.py -q
```

Expected: FAIL, with failures covering the currently broken contracts: `nocolor`, `draft`, `natbib`, plain `\ref`, and `nosubsectionbarriers`.
If `[minimal,nocolor]` already compiles, keep that test as regression coverage.

- [ ] **Step 3: Checkpoint**

Run:

```bash
git diff -- tests/test_option_contracts.py
```

Expected: only the new test file is present.

---

### Task 2: Make `nocolor` an Effective Option

**Files:**
- Modify: `paper/lltpaperstyle.sty`
- Modify: `paper/modules/lltcolors.sty`
- Test: `tests/test_option_contracts.py`

- [ ] **Step 1: Always load the semantic color module before mode-specific modules**

In `paper/lltpaperstyle.sty`, load `lltcolors` immediately after the core
`lltcompilationfixes` and `lltdimensions` modules, before the `\ifllt@minimal`
branch:

```latex
%% FIX: Always load semantic colors so nocolor and minimal mode share definitions.
\@ifpackageloaded{lltcolors}{}{\RequirePackage{lltcolors}}
```

Then remove the old full-mode-only conditional `lltcolors` load.
Keep the `lltheadings` and `lltlists` loads after this line.

- [ ] **Step 2: Make `lltcolors` option-aware**

In `paper/modules/lltcolors.sty`, wrap the semantic color definitions in a package-aware conditional:

```latex
\makeatletter
%% FIX: Allow standalone module loading while honoring lltpaperstyle's nocolor flag.
\@ifundefined{ifllt@nocolor}{\newif\ifllt@nocolor}{}
\ifllt@nocolor
  \definecolor{textblack}{gray}{0}
  \definecolor{sectioncolor}{gray}{0}
  \definecolor{subsectioncolor}{gray}{0}
  \definecolor{subsubcolor}{gray}{0}
  \definecolor{paragraphcolor}{gray}{0}
  \definecolor{subtlegray}{gray}{0}
  \definecolor{bulletgray}{gray}{0}
  \definecolor{dashgray}{gray}{0}
  \definecolor{circlegray}{gray}{0}
  \definecolor{linknavy}{gray}{0}
  \definecolor{linkdark}{gray}{0}
  \definecolor{internalgray}{gray}{0}
  \definecolor{codecolor}{gray}{0}
  \definecolor{commentgray}{gray}{0}
  \definecolor{emphasisblue}{gray}{0}
  \definecolor{warningred}{gray}{0}
\else
  \definecolor{textblack}{gray}{0.05}
  \definecolor{sectioncolor}{RGB}{25,50,80}
  \definecolor{subsectioncolor}{RGB}{40,40,55}
  \definecolor{subsubcolor}{gray}{0.25}
  \definecolor{paragraphcolor}{gray}{0.15}
  \definecolor{subtlegray}{gray}{0.45}
  \definecolor{bulletgray}{gray}{0.25}
  \definecolor{dashgray}{gray}{0.30}
  \definecolor{circlegray}{gray}{0.35}
  \definecolor{linknavy}{RGB}{0,68,136}
  \definecolor{linkdark}{RGB}{0,51,102}
  \definecolor{internalgray}{RGB}{80,80,80}
  \definecolor{codecolor}{RGB}{25,25,25}
  \definecolor{commentgray}{gray}{0.35}
  \definecolor{emphasisblue}{RGB}{0,34,68}
  \definecolor{warningred}{RGB}{140,30,30}
\fi
\makeatother
```

- [ ] **Step 3: Run the focused checkpoint**

Run:

```bash
pytest tests/test_option_contracts.py::test_nocolor_maps_semantic_colors_to_black -q
pytest tests/test_option_contracts.py::test_minimal_nocolor_compiles -q
```

Expected: both pass.

- [ ] **Step 4: Run the task checkpoint**

Run:

```bash
make lint
make build
pytest -q
tests/run-tests.sh
```

Expected: all commands exit 0.

---

### Task 3: Make `draft` Control Microtype Draft/Final State

**Files:**
- Modify: `paper/lltpaperstyle.sty`
- Test: `tests/test_option_contracts.py`

- [ ] **Step 1: Stop passing an early conflicting microtype option**

In `paper/lltpaperstyle.sty`, change the `draft` option declaration to:

```latex
\DeclareOption{draft}{\llt@drafttrue}
```

- [ ] **Step 2: Branch the main microtype load**

Replace the current `\RequirePackage[...] {microtype}` block in `paper/lltpaperstyle.sty` with:

```latex
%% FIX: Keep microtype draft/final state aligned with the package draft option.
\ifllt@draft
  \PackageInfo{lltpaperstyle}{microtype draft mode active}%
  \RequirePackage[
    activate={true,nocompatibility},
    draft,
    tracking=true,
    kerning=true,
    spacing=true,
    factor=1050,
    stretch=15,
    shrink=15,
    protrusion=false,
    verbose=silent
  ]{microtype}
\else
  \PackageInfo{lltpaperstyle}{microtype final mode active}%
  \RequirePackage[
    activate={true,nocompatibility},
    final,
    tracking=true,
    kerning=true,
    spacing=true,
    factor=1050,
    stretch=15,
    shrink=15,
    protrusion=false,
    verbose=silent
  ]{microtype}
\fi
```

- [ ] **Step 3: Branch the later `\microtypesetup`**

Replace the unconditional `final` entry in the later `\microtypesetup` block with:

```latex
  \ifllt@draft draft\else final\fi
```

If TeX rejects the conditional inside the key list, split the setup into two complete blocks guarded by `\ifllt@draft`.

- [ ] **Step 4: Run the focused checkpoint**

Run:

```bash
pytest tests/test_option_contracts.py::test_draft_option_reports_microtype_draft_mode -q
```

Expected: PASS.

- [ ] **Step 5: Run the task checkpoint**

Run:

```bash
make lint
make build
pytest -q
tests/run-tests.sh
```

Expected: all commands exit 0.

---

### Task 4: Implement Native `natbib` Mode

**Files:**
- Modify: `paper/lltpaperstyle.sty`
- Modify: `README.md`
- Test: `tests/test_option_contracts.py`

- [ ] **Step 1: Implement the advertised `natbib` option**

In the bibliography option block of `paper/lltpaperstyle.sty`, replace the `natbib compatibility mode - not loading biblatex` branch with:

```latex
      %% FIX: Implement the documented natbib option instead of silently skipping bibliography support.
      \@ifpackageloaded{natbib}{%
        \PackageInfo{lltpaperstyle}{natbib detected - using existing configuration}%
      }{%
        \PackageInfo{lltpaperstyle}{Loading natbib compatibility mode}%
        \RequirePackage[authoryear,round]{natbib}%
      }%
```

- [ ] **Step 2: Keep `nobiblatex` behavior unchanged**

Do not load `natbib` when the user passes only `nobiblatex`.
The `nobiblatex` contract is "load no bibliography package automatically."
Do not emulate full biblatex citation commands in natbib mode; the supported
natbib-mode public API is native `\citet`, `\citep`, and other commands supplied
by `natbib`.

- [ ] **Step 3: Update README option text**

In `README.md`, update the package-option bullet for `natbib` so it says:

```markdown
- `natbib` – Load native natbib author-year mode instead of automatic biblatex; use `\citet` and `\citep` in this mode.
```

- [ ] **Step 4: Run focused checkpoints**

Run:

```bash
pytest tests/test_option_contracts.py::test_natbib_option_provides_native_natbib_commands -q
pytest tests/test_option_contracts.py::test_nobiblatex_does_not_load_biblatex -q
```

Expected: both pass.

- [ ] **Step 5: Run the task checkpoint**

Run:

```bash
make lint
make build
pytest -q
tests/run-tests.sh
```

Expected: all commands exit 0.

---

### Task 5: Stop Redefining Core `\ref` at Runtime

**Files:**
- Modify: `paper/lltpaperstyle.sty`
- Test: `tests/test_option_contracts.py`

- [ ] **Step 1: Remove the runtime warning wrapper**

In `paper/lltpaperstyle.sty`, delete the block that saves `\oldref` and renews
`\ref` to emit a package warning.

Replace it with a comment only:

```latex
%% FIX: Leave LaTeX's core \ref unchanged; style nudges belong in linting.
% Prefer \cref and \Cref in template prose, but do not alter \ref at runtime.
```

- [ ] **Step 2: Run the focused checkpoint**

Run:

```bash
pytest tests/test_option_contracts.py::test_plain_ref_does_not_emit_package_warning -q
```

Expected: PASS.

- [ ] **Step 3: Run the task checkpoint**

Run:

```bash
make lint
make build
pytest -q
tests/run-tests.sh
```

Expected: all commands exit 0.

---

### Task 6: Make Subsection Float Barriers Explicit and Honest

**Files:**
- Modify: `paper/lltpaperstyle.sty`
- Test: `tests/test_option_contracts.py`

- [ ] **Step 1: Add explicit barrier options without changing default layout**

Add this option flag near the existing package option booleans:

```latex
\newif\ifllt@subsectionbarriers
\llt@subsectionbarrierstrue
```

Add these option declarations:

```latex
\DeclareOption{subsectionbarriers}{\llt@subsectionbarrierstrue}
\DeclareOption{nosubsectionbarriers}{\llt@subsectionbarriersfalse}
```

- [ ] **Step 2: Replace the incorrect pending-float condition**

Replace the current subsection wrapper with:

```latex
%% FIX: Make subsection float-barrier behavior explicit; topnumber is not a pending-float test.
\let\originalsubsection\subsection
\renewcommand{\subsection}{%
  \ifllt@subsectionbarriers
    \FloatBarrier
  \fi
  \originalsubsection
}
```

This preserves the current default behavior because the old condition was
effectively true in normal documents.

- [ ] **Step 3: Report the active barrier mode**

Add after the wrapper:

```latex
\AtBeginDocument{%
  \ifllt@subsectionbarriers
    \PackageInfo{lltpaperstyle}{subsection float barriers enabled}%
  \else
    \PackageInfo{lltpaperstyle}{subsection float barriers disabled}%
  \fi
}
```

- [ ] **Step 4: Run the focused checkpoint**

Run:

```bash
pytest tests/test_option_contracts.py::test_subsection_barriers_are_explicitly_reported -q
pytest tests/test_option_contracts.py::test_nosubsectionbarriers_reports_disabled_mode -q
```

Expected: both pass.

- [ ] **Step 5: Run the task checkpoint**

Run:

```bash
make lint
make build
pytest -q
tests/run-tests.sh
```

Expected: all commands exit 0.

---

### Task 7: Consolidate Microtype Into One Authoritative Module

**Files:**
- Modify: `paper/lltpaperstyle.sty`
- Modify: `paper/modules/lltmicrotype.sty`
- Test: `tests/test_option_contracts.py`

- [ ] **Step 1: Capture the pre-refactor compile and visual baseline**

Run:

```bash
make build
mkdir -p /tmp/llt-visual-baseline
pdftoppm -r 144 -png main.pdf /tmp/llt-visual-baseline/main-before
shasum -a 256 /tmp/llt-visual-baseline/main-before-*.png | awk '{print $1}' > /tmp/llt-visual-baseline/main-before.sha256
pytest -q
tests/run-tests.sh
```

Expected:

- `make build`, `pytest -q`, and `tests/run-tests.sh` pass.
- `/tmp/llt-visual-baseline/main-before.sha256` exists.
- If `pdftoppm` is unavailable, stop and install Poppler before continuing.

- [ ] **Step 2: Replace `lltmicrotype` with the authoritative active configuration**

Replace the current body of `paper/modules/lltmicrotype.sty`.
Do not keep the existing module's stale `\SetExtraKerning` block.
The module must:

- define `\ifllt@draft` when loaded standalone,
- load `microtype` with the same package keys currently active in
  `paper/lltpaperstyle.sty`,
- branch `draft`/`final` on `\ifllt@draft`,
- contain exactly one active `\microtypesetup` path,
- contain the active `\SetProtrusion`, `\SetExpansion`, and `\SetExtraSpacing`
  blocks moved from `paper/lltpaperstyle.sty`,
- not contain `\SetExtraKerning`.

Use this header and ownership block at the top of `paper/modules/lltmicrotype.sty`:

```latex
\ProvidesPackage{lltmicrotype}[2026/05/28 v1.1 Microtype Configuration]

\makeatletter
%% FIX: Make lltmicrotype standalone-safe while honoring lltpaperstyle draft mode.
\@ifundefined{ifllt@draft}{\newif\ifllt@draft}{}
\makeatother

%% FIX: Centralize microtype package loading in the microtype module.
\ifllt@draft
  \PackageInfo{lltmicrotype}{microtype draft mode active}%
  \RequirePackage[
    activate={true,nocompatibility},
    draft,
    tracking=true,
    kerning=true,
    spacing=true,
    factor=1050,
    stretch=15,
    shrink=15,
    protrusion=false,
    verbose=silent
  ]{microtype}
\else
  \PackageInfo{lltmicrotype}{microtype final mode active}%
  \RequirePackage[
    activate={true,nocompatibility},
    final,
    tracking=true,
    kerning=true,
    spacing=true,
    factor=1050,
    stretch=15,
    shrink=15,
    protrusion=false,
    verbose=silent
  ]{microtype}
\fi

%% FIX: Keep microtype runtime mode aligned with package draft/final state.
\ifllt@draft
  \microtypesetup{
    protrusion=true,
    expansion=true,
    kerning=true,
    tracking=true,
    spacing=true,
    babel=true,
    draft
  }
\else
  \microtypesetup{
    protrusion=true,
    expansion=true,
    kerning=true,
    tracking=true,
    spacing=true,
    babel=true,
    final
  }
\fi
```

After this header, move the active `\SetProtrusion`, `\SetExpansion`, and
`\SetExtraSpacing` blocks from `paper/lltpaperstyle.sty`.
Use the active main-package values, not the pre-existing module values.

- [ ] **Step 3: Replace the main package microtype implementation with a module load**

In `paper/lltpaperstyle.sty`, replace both the microtype package-load block and
the later active `\microtypesetup`/`\SetProtrusion`/`\SetExpansion`/
`\SetExtraSpacing` blocks with one module load:

```latex
%% FIX: Delegate microtype configuration to the authoritative module.
\@ifpackageloaded{lltmicrotype}{}{\RequirePackage{lltmicrotype}}
```

Keep public user commands such as `\tightpar`, `\loosepar`, and related
paragraph helper commands in `lltpaperstyle.sty` unless they are already defined
in another loaded module.

- [ ] **Step 4: Verify microtype ownership**

Run:

```bash
! rg -n "SetExtraKerning" paper/modules/lltmicrotype.sty
! rg -n "SetProtrusion|SetExpansion|SetExtraSpacing|microtypesetup|RequirePackage(\\[[^]]*\\])?\\{microtype\\}" paper/lltpaperstyle.sty
rg -n "RequirePackage\\{lltmicrotype\\}|microtype draft mode active|microtype final mode active" paper/lltpaperstyle.sty paper/modules/lltmicrotype.sty
```

Expected:

- No `\SetExtraKerning` remains in `paper/modules/lltmicrotype.sty`.
- No active microtype package load or tuning blocks remain in `paper/lltpaperstyle.sty`.
- The main package loads `lltmicrotype`, and the module reports draft/final mode.

- [ ] **Step 5: Run focused and full checkpoints**

Run:

```bash
pytest tests/test_option_contracts.py::test_draft_option_reports_microtype_draft_mode -q
make lint
make build
pytest -q
tests/run-tests.sh
```

Expected: all commands exit 0, with no new warnings caused by duplicate
microtype setup.

- [ ] **Step 6: Compare default visual regression output**

Run:

```bash
pdftoppm -r 144 -png main.pdf /tmp/llt-visual-baseline/main-after
shasum -a 256 /tmp/llt-visual-baseline/main-after-*.png | awk '{print $1}' > /tmp/llt-visual-baseline/main-after.sha256
diff -u /tmp/llt-visual-baseline/main-before.sha256 /tmp/llt-visual-baseline/main-after.sha256
git diff -- paper/lltpaperstyle.sty paper/modules/lltmicrotype.sty
pytest -q
```

Expected:

- The visual hash diff is empty.
- The source diff shows ownership movement only.
- `pytest -q` still passes.

If the visual hash diff is not empty, stop and inspect rendered pages before
continuing.
Either restore the previous output or document the exact accepted visual delta
in `docs/technical/LATEX_CODE_REVIEW_2026-05-28.md` and `CHANGELOG.md`.

---

### Task 8: Documentation and Final Review

**Files:**
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `docs/technical/LATEX_CODE_REVIEW_2026-05-28.md`

- [ ] **Step 1: Update README option documentation**

Document these option contracts in `README.md`:

```markdown
- `nocolor` – Remap semantic template colors to black while preserving layout.
- `draft` – Enable draft link borders and microtype draft mode.
- `natbib` – Load native natbib author-year mode instead of automatic biblatex; use `\citet` and `\citep` in this mode.
- `nobiblatex` – Do not load a bibliography package automatically.
- `nosubsectionbarriers` – Disable automatic subsection float barriers.
```

- [ ] **Step 2: Update the code review report status**

In `docs/technical/LATEX_CODE_REVIEW_2026-05-28.md`, add a short "Resolution
Status" section mapping each finding to the commit or final diff once the work
is complete.

- [ ] **Step 3: Update the changelog**

Under `2026-05-28`, add bullets for:

```markdown
- Added option-contract regression tests for `nocolor`, `draft`, `natbib`, `nobiblatex`, `\ref`, and subsection float barriers.
- Fixed package option handling for color, draft microtype mode, natbib compatibility, and subsection float barriers without changing default visual design.
- Consolidated microtype ownership into the module layer.
```

- [ ] **Step 4: Run final verification**

Run:

```bash
make lint
make build
pytest -q
tests/run-tests.sh
git status --short
```

Expected:

- `make lint` exits 0.
- `make build` exits 0 and produces `main.pdf`.
- `pytest -q` exits 0.
- `tests/run-tests.sh` exits 0.
- `git status --short` shows only intentional source, test, and documentation changes.

---

## Final Self-Review Checklist

- [x] `nocolor` no longer reloads colored semantic values through dependent modules.
- [x] `draft` no longer conflicts with unconditional microtype `final` settings.
- [x] `natbib` compiles native natbib commands with optional arguments; full biblatex command emulation is not promised.
- [x] `nobiblatex` remains a no-automatic-bibliography option.
- [x] `\ref` is not redefined at package runtime.
- [x] Subsection float barriers are explicit and documented.
- [x] `lltpaperstyle.sty` has less duplicate subsystem ownership after microtype consolidation.
- [x] Microtype ownership is singular: active tuning lives in `lltmicrotype`, and `lltpaperstyle` only loads the module.
- [x] Default visual raster hashes match before and after microtype consolidation, or the accepted visual delta is documented.
- [x] Every LaTeX fix has a `%% FIX:` rationale.
- [x] README and changelog match the implemented behavior.
- [x] `make lint`, `make build`, `pytest -q`, and `tests/run-tests.sh` pass.

## Implementation Results

- Focused option-contract tests were added in `tests/test_option_contracts.py`.
- The initial red test run exposed failures in `nocolor`, `draft`, `natbib`,
  subsection barrier reporting, and `nosubsectionbarriers`.
- Microtype consolidation preserved default visual output: all 41 `main.pdf`
  page rasters matched byte-for-byte before and after the move.
- Follow-up review resolved the remaining P1/P2 issues: public text-symbol
  commands are covered directly, and active tracking/extra-kerning setup no
  longer remains in `paper/lltpaperstyle.sty`.
- The final gates passed: `make lint`, `make build`, `pytest -q` with 16 tests,
  and `tests/run-tests.sh` with 29 fixture files / 87 checks.

## Reviewer Findings

### P1 - Task 3 references a non-existent module `\microtypesetup` block

Task 3 says to "use the same draft/final branch around the module's
`\microtypesetup`," but `paper/modules/lltmicrotype.sty` currently has no
`\microtypesetup` block and does not load `microtype`.
It only errors if `microtype` was not already loaded.
As written, the implementer cannot execute this step literally, and the plan may
leave the real draft/final conflict in `paper/lltpaperstyle.sty` only partially
fixed.

Resolution requirement: rewrite Task 3 or Task 7 so `lltmicrotype` first becomes
responsible for loading/configuring `microtype`, then branch draft/final state in
that one authoritative module.

Resolution: `accepted-current`.
Task 3 now handles only the immediate main-package draft/final conflict, and
Task 7 makes `lltmicrotype` the authoritative loader/configuration module.

### P1 - Task 7 can leave duplicate and stale microtype settings in place

Task 7 tells the implementer to copy active microtype configuration from
`paper/lltpaperstyle.sty` into `paper/modules/lltmicrotype.sty`, but the module
already contains independent protrusion, expansion, spacing, and
`\SetExtraKerning` settings.
The main package comments say `\SetExtraKerning` was removed due compilation
issues, so a copy-only consolidation can preserve stale settings and introduce
duplicate definitions rather than creating one source of truth.

Resolution requirement: make Task 7 a replacement, not a copy.
Specify the exact post-task ownership rule: `lltmicrotype` contains one complete
microtype configuration, and `lltpaperstyle` contains only the module load.

Resolution: `accepted-current`.
Task 7 now requires replacing the stale module body, removing `\SetExtraKerning`,
and verifying that no active microtype tuning remains in `lltpaperstyle`.

### P1 - The plan lacks a real visual-regression checkpoint for a no-design-change goal

The plan repeatedly states that default visual design must not change, but its
checkpoints rely on `make lint`, `make build`, and `pytest -q`.
The current pytest suite mostly checks compilation and a few text assertions; it
does not prove that the default PDF layout or typography is unchanged.
This is especially risky for Task 7, which moves microtype configuration and can
change line breaks, protrusion, spacing, and overfull boxes.

Resolution requirement: add an explicit default-output guard before and after
Task 7, such as a documented PDF hash/text-position regression, the existing
layout-hash harness if available, or a narrowly scoped accepted-diff procedure.

Resolution: `accepted-current`.
The checkpoint rules and Task 7 now require before/after `pdftoppm` raster hashes
for `main.pdf`, with an explicit stop/waiver path if Poppler is unavailable.

### P2 - `natbib` compatibility is under-specified and the proposed aliases are too weak

Task 4 implements only one-argument aliases for `\textcite`, `\autocite`, and
`\parencite`.
That may pass the proposed smoke test, but it does not cover common citation
forms used by this template's documentation and examples, including optional
page arguments and starred citation forms.

Resolution requirement: either reduce the contract to "simple natbib commands
only" and update docs accordingly, or add tests and implementation for optional
arguments such as `\textcite[45]{key}` and `\parencite[see][45]{key}`.

Resolution: `accepted-current`.
Task 4 now defines natbib mode as native natbib command support, tests optional
arguments on `\citet` and `\citep`, and removes weak biblatex aliases.

### P2 - `nosubsectionbarriers` is documented but not tested

Task 6 adds a new `nosubsectionbarriers` option, but the only planned test checks
that some barrier mode is reported.
It does not verify that `nosubsectionbarriers` selects the disabled branch, so
the option could be misspelled, ignored, or overridden while tests still pass.

Resolution requirement: add a focused test using
`\usepackage[nosubsectionbarriers]{lltpaperstyle}` and assert that the log
contains `subsection float barriers disabled`.

Resolution: `accepted-current`.
Task 1 now adds `test_nosubsectionbarriers_reports_disabled_mode`, and Task 6
runs it as a focused checkpoint.

### P2 - `nocolor` coverage misses combined option and minimal-mode behavior

Task 2 tests plain `[nocolor]`, but the package also advertises combinable
options such as `[minimal,nocolor]`.
The planned implementation changes the full-mode module loader, while minimal
mode still skips `lltcolors` and later package code can define commands that
reference semantic color names such as `subtlegray`.

Resolution requirement: add a compile fixture for `[minimal,nocolor]` or state
explicitly that `nocolor` is supported only in full mode.

Resolution: `accepted-current`.
Task 1 now adds `test_minimal_nocolor_compiles`, and Task 2 runs it as a focused
checkpoint.

### P3 - Package-code lint remains too narrow for this change set

The mandatory `make lint` target checks only root `*.tex` files, not the `.sty`
files being edited.
That is acceptable as the project gate, but it is not enough as a plan-specific
quality check for package-code changes.

Resolution requirement: add a supplemental style-file check or an all-fixtures
compile checkpoint, for example `tests/run-tests.sh`, after package-code tasks.

Resolution: `accepted-current`.
The checkpoint rules and all package-code tasks now include `tests/run-tests.sh`.
