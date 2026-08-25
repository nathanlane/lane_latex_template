---
status: accepted
date: 2026-08-22
---

# Package-first, with the template as a separate repository

This repository grew as a paper template that happened to contain a style
package, and the two were never separated. That single ambiguity produced most
of the repository's problems: two READMEs, two style guides, three drifted
version namespaces, and a style package that loads `longtable` and `tabularx`
without ever using them.

We are splitting the two. The **Package** (`lanepaper`) owns everything that
changes how text looks. The **Template** — a separate repository, extracted once
the Package is stable — owns everything that decides what a document contains or
which document-level packages to load. A minimal **Demo** stays in the Package
repository as the CI fixture; it is not a starting point for real papers.

The deciding argument was adoption across projects. A template is forked, and
forks drift — this already happened once here, which is why
`docs/LOCAL_FORK_TEMPLATE_AUDIT_2026-05-27.md` had to be written (deleted
2026-08-25 by issue #52; it is in git history). A package is
installed once and upgraded in place. Only the second has an upgrade path.

## The name

`lltpaperstyle` becomes `lanepaper`, and the four competing internal prefixes
(`\paper@`, `\llt@`, `\lltpaperstyle@`, `\lltfontfeatures@`) collapse to a single
`\lnp@`, matching how CTAN packages actually do it — `\MT@` for microtype, `\Hy@`
for hyperref, `\Gm@` for geometry.

> **Erratum (2026-08-24).** The count above is one short. Implementing this in
> #46 found a fifth prefix, `\paperstyle@` (6 occurrences), which was retired
> with the other four. The decision is unchanged — all of them collapse to
> `\lnp@` — but anything citing "four" is citing this sentence, not the code.
> `CONVENTIONS.md` and `docs/package/NAMESPACE_CONVENTIONS.md` say five, and
> the guard in `tests/test_infrastructure.py` covers all five. The original
> sentence is left as written because an accepted ADR is a record of what was
> decided, not a live description.

`paper` was the obvious name and is unavailable: `paper.sty` already ships in
TeX Live. `-latex` and `-style` suffixes were rejected as redundant inside a
LaTeX style package, and the `-latex` suffix additionally reads on CTAN as
marking documentation *about* LaTeX. The rename is mechanical now and would be
permanent-with-a-deprecated-alias after CTAN, so it happens before submission.

## Distribution

`l3build install` copies the Package into `TEXMFHOME`, after which any local
document resolves `\usepackage{lanepaper}`. Environments that cannot install
into a texmf tree — Overleaf, co-authors' machines — vendor the `.sty` files
into a Template checkout via `git subtree`, which also lets an in-progress paper
pull upstream fixes.

CTAN is the endgame and has no date. It is what retires vendoring and what makes
Overleaf work without manual uploads, so issue #34 is closed as won't-fix until
then rather than being solved twice.

## Consequences

- Nothing an author currently uses is lost. `\begin{landscape}`,
  `\begin{sideways}`, and the `\adjustbox` wrapper move to the Template, where
  they always belonged; they keep working in papers.
- Until CTAN, Overleaf has no zero-setup path. Vendoring is a recurring
  per-project cost, and it stops paying at roughly three concurrent papers, or
  at the first co-author, or the first time one fix must reach everything at
  once.
- Package-first is a layout decision, not a commitment to CTAN. Choosing it now
  keeps the door open; skipping it would mean reorganising the repository again
  later.
