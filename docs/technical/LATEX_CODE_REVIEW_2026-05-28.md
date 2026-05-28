# LaTeX Package Code Review - 2026-05-28

## Scope

This review focused on maintainability, package API behavior, and LaTeX coding
style in the active template package files under `paper/` and the regression
harness under `tests/`.

## Verification

- `make lint` - passed
- `make build` - passed and produced `main.pdf`
- `pytest -q` - passed, 7 tests

The build still emits content-level overfull/underfull box warnings in
`main.tex`; those were not treated as package code findings unless the package
implementation caused the behavior.

## Findings

### P1 - `nocolor` is not an effective package option

`lltpaperstyle` skips `lltcolors` when `nocolor` is set, but immediately loads
`lltheadings` and `lltlists`.
Those modules unconditionally require `lltcolors` if it is not already loaded.
As a result, `\usepackage[nocolor]{lltpaperstyle}` still installs the custom
color palette and colored headings/list markers.

Evidence:

- `paper/lltpaperstyle.sty:222` skips `lltcolors` only in the top-level loader.
- `paper/lltpaperstyle.sty:225` and `paper/lltpaperstyle.sty:226` still load
  `lltheadings` and `lltlists`.
- `paper/modules/lltheadings.sty:14` to `paper/modules/lltheadings.sty:18`
  silently reload `lltcolors`.
- `paper/modules/lltlists.sty:13` to `paper/modules/lltlists.sty:18`
  silently reload `lltcolors`.

Recommended fix:

- Always load `lltcolors`, but make the color module option-aware and map the
  semantic colors to black/grayscale in `nocolor` mode.
- Add a fixture that compiles with `[nocolor]` and asserts no colored link or
  semantic color settings survive except explicitly allowed grayscale.

### P1 - `draft` is contradicted by unconditional final microtype settings

The `draft` option passes `draft` to `microtype`, but the package later loads
`microtype` with `final` and calls `\microtypesetup{..., final}`.
This makes the option contract hard to reason about and can defeat draft-mode
diagnostics.

Evidence:

- `paper/lltpaperstyle.sty:130` passes `draft` to `microtype`.
- `paper/lltpaperstyle.sty:589` to `paper/lltpaperstyle.sty:600` load
  `microtype` with `final`.
- `paper/lltpaperstyle.sty:2839` to `paper/lltpaperstyle.sty:2847` force
  `\microtypesetup{..., final}`.

Recommended fix:

- Branch the `microtype` package options and `\microtypesetup` final/draft state
  on `\ifllt@draft`.
- Add a `[draft]` fixture that checks the expected overfull-box and hyperref
  behavior.

### P2 - `natbib` is advertised as an option but does not load natbib

The package and README advertise `natbib` compatibility, but the option only
prevents automatic `biblatex` loading.
It does not load `natbib`, provide natbib commands, or fail with a clear package
warning explaining that users must use `preamble-natbib.tex`.

Evidence:

- `paper/lltpaperstyle.sty:86` to `paper/lltpaperstyle.sty:89` describe
  `natbib` as a package option while also noting it has no effect.
- `paper/lltpaperstyle.sty:150` to `paper/lltpaperstyle.sty:152` only emit a
  package info message and skip `biblatex`.
- `README.md:292` to `README.md:297` list `natbib` beside implemented options.

Recommended fix:

- Either implement the option by loading/configuring `natbib`, or remove it from
  the public option list and document `preamble-natbib.tex` as the only
  supported natbib route.
- Add a fixture for `natbib` mode so this API does not drift again.

### P2 - The main package duplicates module implementation after loading modules

`lltpaperstyle.sty` loads modules such as `lltfonts`, `lltheadings`, and
`lltlists`, but then continues to define or override large parts of the same
systems in the main file.
This undermines the modular architecture because maintainers cannot tell which
file is authoritative, and user attempts to pre-load or override modules may be
overwritten later by the main package.

Evidence:

- `paper/lltpaperstyle.sty:196` to `paper/lltpaperstyle.sty:197` says font
  configuration moved to `lltfonts.sty`, but the main file still contains a
  large font/microtype system.
- `paper/lltpaperstyle.sty:207` to `paper/lltpaperstyle.sty:226` load the core
  modules.
- `paper/lltpaperstyle.sty:708` to `paper/lltpaperstyle.sty:709` then reload
  list/caption infrastructure in the main file.
- `paper/lltpaperstyle.sty:2892` to `paper/lltpaperstyle.sty:3070` duplicate
  microtype configuration that also exists in `paper/modules/lltmicrotype.sty`.

Recommended fix:

- Pick one source of truth per subsystem.
- Leave only option processing and module orchestration in `lltpaperstyle.sty`.
- Move remaining implementation blocks into modules incrementally, with PDF
  regression checks after each move.

### P2 - `\ref` is globally redefined to warn on normal LaTeX usage

The package replaces the core `\ref` command with a wrapper that warns users to
prefer `\cref`.
That is intrusive for a template package: it changes a standard command,
generates warning noise for valid LaTeX, and can interact badly with packages
that expect `\ref` to be stable.

Evidence:

- `paper/lltpaperstyle.sty:2204` saves `\ref`.
- `paper/lltpaperstyle.sty:2205` to `paper/lltpaperstyle.sty:2210` globally
  redefine `\ref` to emit a package warning.

Recommended fix:

- Restore `\ref` unchanged.
- If project authors want a migration warning, put it in a lint script rather
  than in the package runtime.

### P2 - The subsection float-barrier condition is not checking pending floats

The conditional subsection barrier tests `\value{topnumber}>0`, but `topnumber`
is the allowed number of top floats, not a pending-float indicator.
In normal documents it is usually positive, so this behaves like an unconditional
`\FloatBarrier` before every subsection.

Evidence:

- `paper/lltpaperstyle.sty:1287` saves `\subsection`.
- `paper/lltpaperstyle.sty:1288` to `paper/lltpaperstyle.sty:1291` uses
  `\ifnum\value{topnumber}>0` as the pending-float check.

Recommended fix:

- Remove the automatic subsection barrier, or make it an explicit option with
  clear semantics.
- If automatic detection is still desired, use a mechanism that actually tracks
  pending floats, and cover it with a fixture containing floats around
  subsections.

## Test Coverage Gaps

- No focused pytest coverage for `[nocolor]`, `[draft]`, `[natbib]`, and
  `[nobiblatex]` option contracts.
- Regression tests cover only two LaTeX fixtures through pytest; the shell
  harness can compile all fixtures, but that path is not the default Python
  regression gate.
- No test asserts that package options preserve visual defaults while changing
  only the advertised behavior.

## Suggested Next Pass

1. Add option-contract fixtures for `nocolor`, `draft`, `natbib`, and
   `nobiblatex`.
2. Fix the option behavior failures above.
3. Start modular cleanup with one subsystem, preferably microtype, because it is
   currently duplicated and has direct draft/final option conflicts.
4. Remove runtime warnings for normal `\ref` usage and move code-style nudges to
   linting.
