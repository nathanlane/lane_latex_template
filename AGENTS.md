# AGENTS.md – Rules & Workflow for LaTeX Build‑Doctor Agent
> **Mission**  
> Fix all LaTeX compilation issues and harden the template for both local `latexmk`
> **and** the current Overleaf container **without changing any visual design**.

---

## 📜 Non‑negotiable rules
1. **Do not** alter margins, fonts, colours, spacing, numbering schemes, or figure placement defaults.  
2. Prefer the **smallest possible change** that compiles cleanly on both platforms.  
3. Comment every fix with `%% FIX:` and a one‑line rationale.  
4. Update `CHANGELOG.md` and relevant sections of `README.md` after any material change.

## 🛠 Tools you must run before proposing a commit
| Command | Purpose | Acceptable exit code |
|---------|---------|----------------------|
| `chktex -q -n1 -n3 -n8 -n11 -n13 -n18 -n24 -n36 -n39 -n42 -n46 -n48 *.tex` | Catch obvious bad constructs while ignoring intentional template/prose warnings that require visual-output changes. | 0 |
| `latexmk -pdf -interaction=nonstopmode main.tex` | Full compile; output PDF must be produced. | 0 |
| `pytest -q` | Runs regression harness (`tests/`) that diff‑checks layout hashes. | 0 |

If **any** command fails, fix the cause instead of suppressing it.

## ⚙️ Build targets available
* `make build` – alias for the latexmk command above  
* `make lint` – runs the chktex line above  
* `make fmt` – runs `latexindent -l -w` (no layout impact, indentation only)

## 🔄 Workflow
1. `make lint` – fix warnings **unless** they require visual changes.  
2. `make build` – iterate until the build is green.  
3. `pytest` – ensure regression tests pass.  
4. Document the change and commit.

## 🏁 Definition of Done
* All tools exit 0.  
* `main.pdf` renders without warnings on Overleaf **and** locally.  
* `README.md` lists the tested TeX Live and Overleaf build numbers.  
* `CHANGELOG.md` entry added under today’s date.

---

*You may create additional helper scripts, but keep them in `scripts/` and document them in the README.*

---

## 1  Project Philosophy  ⬐ 30 sec read

• Focus on **clarity over cleverness**—both in prose and in code.  
• Prefer **standard tools**; add complexity only when it brings visible value (e.g., professional typography).  
• Every change must be **reproducible** and leave the repo healthier than before.

---

## 2  Minimum Repository Layout

```text
/                 – root; this file, README.md, main.tex
/paper/           – LaTeX style + modules (lltpaperstyle.sty, etc.)
/src/             – code (python/, sh/)
/data/            – datasets (raw/, processed/)
/figures/         – generated graphics
```

Keep extra folders to an absolute minimum.  Empty dirs should contain a `.gitkeep`.

---

## 3  LaTeX Quick Start

1. In your document preamble load the template style, then register the bibliography:

   ```latex
   \usepackage{lltpaperstyle} % master template; auto-loads default biblatex
   \addbibresource{references.bib}
   ```

   For custom `biblatex` options, load `biblatex` yourself and disable the
   template's automatic bibliography loading:

   ```latex
   \usepackage[backend=biber,style=authoryear]{biblatex}
   \addbibresource{references.bib}
   \usepackage[nobiblatex]{lltpaperstyle}
   ```
2. Compile with `latexmk -pdf -synctex=1 main.tex` (local) or just click *Recompile* on Overleaf.
3. Obey Chicago author-date citation style (`\textcite`, `\autocite`).
4. Follow these **non-negotiable typographic rules**:
   • Tables use `booktabs`, no vertical rules.  
   • Figures: caption **below**; Tables: caption **above**.  
   • One sentence per line in `.tex` for clean diffs.

---

## 4  Python / Shell Standards

• Python: PEP 8 + Black (line-length = 88).  
• Shell: Google Bash Style Guide.  
• Never commit notebooks; export results to `/figures` or `/data/processed`.

---

## 5  Git Workflow (3 rules)

1. **Branch per task** → descriptive name (`feat/grid-overlay`, `fix/ref-bib`).
2. Run `git status` & `pytest` (or relevant checks) before every commit.  
3. Commit message format:
   ```text
   type(scope): short summary

   * bullet explaining what & why (wrap 72)
   ```
   Examples: `docs: add AGENTS.md`, `style: black-format src/`.

---

## 6  OpenAI Agent Operating Guidelines

| Goal                      | Action                                                        |
|---------------------------|---------------------------------------------------------------|
| **Answer a question**     | Provide concise, source-linked explanation.                   |
| **Modify code**           | Use exact `patch` diff (no ellipses). Preserve formatting.    |
| **Create a file**         | Supply full path & complete content.                          |
| **Run a command**         | Explain first, add `--no-pager` where relevant, then execute. |
| **Update docs**           | Keep examples in sync with current API & package names.       |

Always prefer **clarity**, **minimalism**, and **reversibility**.

---

## 7  Resources

* Full style spec → `CLAUDE.md` (for typography deep-dive).  
* OpenAI API docs → <https://platform.openai.com/docs>.  
* Chicago Manual of Style (author-date).  
* Butterick’s *Practical Typography* (for quick reference).

---

© 2025 Lane LaTeX Template Project.  Licensed under the LaTeX Project Public License v1.3c.
