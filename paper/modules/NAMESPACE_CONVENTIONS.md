# LaTeX Package Namespace Conventions

This document outlines the namespace conventions used in the paper template modules to ensure robustness and prevent conflicts with other packages.

## Overview

All internal package variables and commands should use the `\paper@` prefix to create a protected namespace. This follows standard LaTeX package development best practices.

## Naming Conventions

### Internal Variables (Use `\paper@` prefix)

```latex
% Lengths
\newlength{\paper@listhalfbaseline}    % Good: namespaced
\newlength{\listhalfbaseline}           % Bad: could conflict

% Commands  
\newcommand{\paper@internalhelper}{}    % Good: namespaced
\newcommand{\internalhelper}{}          % Bad: too generic

% Counters
\newcounter{paper@tempcount}            % Good: namespaced
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
\newlength{\paper@listhalfbaseline}

% Compatibility alias (mark as deprecated)
\let\listhalfbaseline\paper@listhalfbaseline  % Will be removed in v2.0
```

## Current Status

### ✅ Completed
- **lists.sty**: All internal lengths now use `\paper@` prefix
  - `\paper@listhalfbaseline`, `\paper@listquarterbaseline`, etc.
  - Compatibility aliases provided for backward compatibility

### 🔄 To Be Updated

The following files contain variables that could benefit from namespacing:

#### dimensions.sty
- Current: `\gridunit`, `\halfgridunit`, `\quartergridunit`, etc.
- Proposed: `\paper@gridunit`, `\paper@halfgridunit`, etc.
- Reason: While relatively specific, "gridunit" could be used by other grid-based packages

#### colors.sty  
- Current: Direct color definitions are fine (they use xcolor's namespace)
- Commands like `\maincolor`, `\secondarycolor` could potentially conflict
- Proposed: Keep as-is (low risk, descriptive names)

#### paragraphs.sty
- Current: `\noindentpar`, `\forceindent`, `\centeredpar`, `\dialogue`
- Assessment: These are user-facing commands with descriptive names, low conflict risk
- Recommendation: Keep as-is

#### headings.sty
- Current: Style commands like `\spacioussections`, `\moderatesections`
- Assessment: User-facing commands with specific names
- Recommendation: Keep as-is

## Implementation Guidelines

### When to Use Namespacing

Use the `\paper@` prefix for:
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

1. **Always use `\makeatletter`/`\makeatother`** when defining `@` commands:
   ```latex
   \makeatletter
   \newlength{\paper@internallength}
   \makeatother
   ```

2. **Document deprecated aliases**:
   ```latex
   % Compatibility alias - DEPRECATED, will be removed in v2.0
   \let\oldname\paper@newname
   ```

3. **Use descriptive names** even with namespacing:
   ```latex
   \newlength{\paper@listitemspacing}    % Good: clear purpose
   \newlength{\paper@temp}                % Bad: too generic
   ```

4. **Group related definitions**:
   ```latex
   % List spacing parameters
   \newlength{\paper@listhalfbaseline}
   \newlength{\paper@listquarterbaseline}
   \newlength{\paper@listbaselineskip}
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
