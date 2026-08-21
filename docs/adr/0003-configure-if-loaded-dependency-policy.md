---
status: accepted
date: 2026-08-22
---

# The Package configures third-party packages; it does not load them

The Package currently issues around thirty-seven unconditional `\RequirePackage`
calls. Measured against its own source, `longtable` and `tabularx` are used zero
times, and `rotating`, `pdflscape`, and `adjustbox` exist solely to support
`\begin{landscape}`, `\begin{sideways}`, and one `\adjustbox` wrapper — document
conveniences, not typography.

Three rules now govern what the Package loads:

1. **Load** what implementing the typography requires: `microtype`,
   `letterspace`, `ragged2e`, `titlesec`, `enumitem`, `geometry`, `xcolor`,
   `caption`, `lettrine`, `booktabs`, `fancyhdr`, `placeins`, the fonts.
2. **Configure if loaded**, never load: `hyperref`, `cleveref`, `biblatex`,
   `babel`, `appendix`. The Package styles them via `\@ifpackageloaded` when the
   document has already brought them in.
3. **Neither** — delete outright, or move to the Template: `longtable`,
   `tabularx`, and the landscape/sideways/adjustbox wrappers with their three
   supporting packages.

This lands the Package at roughly twenty-five loads.

Rule 2 matters most. A style package that loads `hyperref` itself dictates load
order to every document that uses it, and forces anyone wanting their own
hyperref options to load first or use `\PassOptionsToPackage`. That is the
single most likely thing to break an adopter, and it is avoidable: the
cross-reference and link typography survive intact under `\@ifpackageloaded`.

`fancyhdr` (running heads) and `placeins` (float barriers, tied to the
`subsectionbarriers` option) were judged typography and stay loaded. `appendix`,
with one use, does not.

## Consequences

- A document that loads none of the configure-if-loaded packages gets less
  styling than before. The Template loads all of them, so papers are unaffected;
  a third party using the Package bare must load what they want styled.
- The reduction is not a tidy-up to be reverted. Anyone re-adding a
  `\RequirePackage{hyperref}` to "fix" missing link colours is undoing this
  decision — configure it under `\@ifpackageloaded` instead.
- Fewer loads means fewer preamble conflicts, fewer `check-deps` entries, and
  faster compiles.
