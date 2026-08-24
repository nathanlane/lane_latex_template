# LaTeX Package Namespace Conventions

This document outlines the namespace conventions used in the paper template modules to ensure robustness and prevent conflicts with other packages.

## Overview

All internal package variables and commands should use the `\lnp@` prefix to create a protected namespace. This follows standard LaTeX package development best practices.

## Naming Conventions

### Internal Variables (Use `\lnp@` prefix)

```latex
% Lengths
\newlength{\lnp@listhalfbaseline}    % Good: namespaced
\newlength{\listhalfbaseline}           % Bad: could conflict

% Commands  
\newcommand{\lnp@internalhelper}{}    % Good: namespaced
\newcommand{\internalhelper}{}          % Bad: too generic

% Counters
\newcounter{lnp@tempcount}            % Good: namespaced
\newcounter{tempcount}                  % Bad: could conflict
```

### Public API (No prefix needed)

```latex
% User-facing commands don't need prefixes
\newcommand{\tightlists}{}              % OK: specific to our package
\newcommand{\spacioussections}{}        % OK: descriptive name
\newcommand{\displayparagraph}{}        % OK: unlikely to conflict
```

### Compatibility Aliases

When updating existing packages, provide temporary aliases:

```latex
% Internal definition
\newlength{\lnp@listhalfbaseline}

% Compatibility alias (mark as deprecated)
\let\listhalfbaseline\lnp@listhalfbaseline  % Will be removed in v2.0
```

## Why `\lnp@`

`lnp` abbreviates `lanepaper`, and the same abbreviation names both the internal
macros and the module files (`lnpcolors.sty`, `lnpfonts.sty`). It is deliberately
short because that is how CTAN packages do it: `\MT@` for microtype, `\Hy@` for
hyperref, `\Gm@` for geometry, `\ttl@` for titlesec. `biblatex` is the closest
match to this package's layout — CTAN name `biblatex`, shipped files `blx-*.sty`,
internal macros `\blx@`.

`\lanepaper@` was rejected as too long for something that appears on every
internal identifier. `\lane@` was rejected because it drops half the package
name. `lnp` is less immediately readable than either, and that cost was accepted
deliberately in exchange for matching the convention a CTAN reviewer expects.
See ADR-0001.

## Current state

Every internal identifier uses `\lnp@`. The prefixes it replaced — `\paper@`,
`\llt@`, `\lltpaperstyle@`, `\lltfontfeatures@`, `\paperstyle@` — are retired,
and `tests/test_infrastructure.py` fails if any reappears in an active source
file.

Public commands stay prefix-free per the rule above: `\tightlists`,
`\spacioussections`, `\centeredpar`, `\textapprox`. The exception is the
package's own diagnostic entry points, `\lanepaperdiagnostics` and
`\lanepaperinfo`, which carry the package name because that is what a user types.

Known gap: prefix-free public names are safe inside one repository but weaker in
a shared texmf tree, where `\centeredpar` or `\dialogue` could collide with
another package. Worth revisiting before CTAN submission.

## Implementation Guidelines

### When to Use Namespacing

Use the `\lnp@` prefix for:
1. **Internal lengths and dimensions** that control layout
2. **Temporary variables** used in calculations
3. **Helper commands** not intended for user access
4. **Internal counters** and boxes
5. **Any variable with a generic name** (e.g., `\temp`, `\spacing`, `\indent`)

### When NOT to Use Namespacing

Don't use prefixes for:
1. **User-facing commands** that are part of the public API
2. **Environment names** (LaTeX handles these differently)
3. **Color definitions** (xcolor handles its own namespace)
4. **Variables with highly specific names** unlikely to conflict

### Best Practices

1. **Never use `\makeatletter`/`\makeatother` inside a `.sty` file.** A `.sty`
   already has `@` as a letter by construction, so a stray `\makeatother`
   revokes it for the rest of the file. Just write the definition:
   ```latex
   \newlength{\lnp@internallength}
   ```
   This reverses the advice that stood here until #46, where 137 such lines
   caused `Command \lnp already defined` the moment the prefix contained an
   `@`. They are correct only in a `.tex` document. See `CONVENTIONS.md` §6.

2. **Document deprecated aliases**:
   ```latex
   % Compatibility alias - DEPRECATED, will be removed in v2.0
   \let\oldname\lnp@newname
   ```

3. **Use descriptive names** even with namespacing:
   ```latex
   \newlength{\lnp@listitemspacing}    % Good: clear purpose
   \newlength{\lnp@temp}                % Bad: too generic
   ```

4. **Group related definitions**:
   ```latex
   % List spacing parameters
   \newlength{\lnp@listhalfbaseline}
   \newlength{\lnp@listquarterbaseline}
   \newlength{\lnp@listbaselineskip}
   ```

## Migration Strategy

When updating existing modules:

1. **Phase 1**: Add namespaced versions, keep originals as aliases
2. **Phase 2**: Mark aliases as deprecated in documentation
3. **Phase 3**: Remove aliases in next major version

## Testing

After implementing namespace changes:

1. Compile all test documents
2. Check for undefined control sequence errors
3. Verify spacing and layout remain unchanged
4. Test with common conflicting packages (geometry, enumitem, etc.)

## Benefits

- **Robustness**: Prevents conflicts with other packages
- **Professionalism**: Follows LaTeX community standards
- **Maintainability**: Clear distinction between internal and public API
- **Future-proofing**: Allows safe evolution of the package

## References

- [LaTeX2e for class and package writers](https://www.latex-project.org/help/documentation/clsguide.pdf)
- [Best practices for LaTeX package development](https://tex.stackexchange.com/questions/8351/)
- Examples from major packages: geometry, hyperref, tikz
