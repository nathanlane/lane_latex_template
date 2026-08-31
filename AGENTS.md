# AGENTS.md – Rules & Workflow for LaTeX Build‑Doctor Agent
> **Mission**  
> Fix all LaTeX compilation issues and harden the template for local `latexmk`
> **without changing any visual design**.

---

## 📜 Non‑negotiable rules
1. **Do not** alter margins, fonts, colours, spacing, numbering schemes, or figure placement defaults.  
2. Prefer the **smallest possible change** that compiles cleanly on the verified local toolchain.
3. Comment every fix with `%% FIX:` and a one‑line rationale.  
4. Package code in `lanepaper/` follows [`CONVENTIONS.md`](CONVENTIONS.md) — naming, message policy, robustness, hooks, and the rule against `\makeatletter` in a `.sty`. Read it before editing a `.sty` file.  
5. Update `CHANGELOG.md` and relevant sections of `README.md` after any material change.

## 🛠 Tools you must run before proposing a commit

| Command | Purpose | Acceptable exit code |
|---------|---------|----------------------|
| `make lint` | ChkTeX over the demo sources. | 0 |
| `make build` | Full compile; `main.pdf` must be produced. | 0 |
| `make test` | `pytest -q`, then the shell harness. | 0 |

These are the three gates CI runs, in the same order. What each one covers, and
the accepted warnings, are in [`CONTRIBUTING.md`](CONTRIBUTING.md) and
[`tests/README.md`](tests/README.md) — this table does not restate them.

If **any** command fails, fix the cause instead of suppressing it.

## ⚙️ Build targets available
`make help` lists all of them. The three that matter here:

* `make build` – the latexmk command above
* `make lint` – ChkTeX over the demo sources
* `make test` – `pytest -q` then the shell harness, exactly what CI runs

There is no formatting target. Issue #51 deleted the aliases; run the
formatter directly when you want it:

```bash
latexindent -l -w demo/*.tex   # indentation only
```

## 🔄 Workflow
1. `make lint` – fix warnings **unless** they require visual changes.  
2. `make build` – iterate until the build is green.  
3. `make test` – ensure regression tests pass.  
4. Document the change and commit.

## 🏁 Definition of Done
* All tools exit 0.  
* `main.pdf` renders with the verified local `latexmk` workflow.
* `README.md` lists the tested local TeX Live toolchain.
* `CHANGELOG.md` entry added under today’s date.

---

## 1  Project Philosophy  ⬐ 30 sec read

• Focus on **clarity over cleverness**—both in prose and in code.  
• Prefer **standard tools**; add complexity only when it brings visible value (e.g., professional typography).  
• Every change must be **reproducible** and leave the repo healthier than before.

---

## 2  Minimum Repository Layout

```text
/                 – root; this file, README.md, Makefile
/lanepaper/       – LaTeX package and internal modules
/demo/            – curated demo document sources
/tests/           – pytest suite, shell harness, and fixtures
```

Keep extra folders to an absolute minimum.  Empty dirs should contain a `.gitkeep`.

---

## 3  LaTeX Quick Start

1. The document owns its bibliography: load `biblatex`, then `lanepaper`, and
   register the bibliography resource:

   ```latex
   \usepackage[backend=biber,style=authoryear]{biblatex}
   \usepackage{lanepaper}
   \addbibresource{references.bib}
   ```
2. Compile with `make build`.
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
   Examples: `docs: add AGENTS.md`, `style: format lanepaper/`.

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

* Full style spec → [`API_REFERENCE.md`](API_REFERENCE.md), section "Typography standards".  
* OpenAI API docs → <https://platform.openai.com/docs>.  
* Chicago Manual of Style (author-date).  
* Butterick’s *Practical Typography* (for quick reference).

---

© 2025-2026 Nathan Lane. `lanepaper/` is LPPL 1.3c; all other original
repository files are MIT. See `LICENSE` and `licenses/LICENSE-MIT.txt`.
