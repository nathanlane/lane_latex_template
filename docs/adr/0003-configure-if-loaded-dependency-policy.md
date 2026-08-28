---
status: accepted
date: 2026-08-22
---

# Load only owned dependencies; configure third-party behavior narrowly

The Package once loaded or configured packages because its template happened
to use them. That made Lanepaper own document choices, load order, and APIs it
did not need to implement typography.

> **v3 revision (2026-08-28).** The former package lists were transitional and
> are replaced by an ownership rule. "Configure if loaded" is a relationship,
> not a permanent allowlist.

Three rules govern v3:

1. **Load** only a dependency needed to implement retained Lanepaper
   typography. This includes the font and Microtype stack, layout and heading
   owners, colors and captions, required `booktabs`, and `fancyhdr` while the
   retained page style needs it.
2. **Configure if loaded** only when the document has already loaded a package
   and the configured result is Lanepaper typography. The retained cases are
   narrow Hyperref link/bookmark styling and conditional longtable caption
   width; the relation, not those names, is the durable decision.
3. **Neither load nor configure** APIs owned by documents or third parties.
   Cleveref, BibLaTeX, natbib, appendix orchestration, and threeparttable remain
   document-owned; Lanepaper provides no wrappers or fallbacks for them.

Hyperref illustrates the boundary. Loading it would dictate load order and
options to every adopter. When a document loads it, Lanepaper may apply visible
theme link colors and bookmark-safe substitutions for retained Lanepaper
commands, but it does not own bookmark numbering, encoding, borders, or draft
mode.

## Consequences

- A document explicitly loads bibliography, cross-reference, appendix, and
  other content-level packages it chooses.
- Missing third-party features are not repaired with generic wrappers or
  `\providecommand` fallbacks.
- Package lists are re-derived from surviving callers instead of maintained as
  architecture.
