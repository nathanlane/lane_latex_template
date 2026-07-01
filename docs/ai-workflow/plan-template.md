---
topic: <kebab-case-slug>
created: YYYY-MM-DD
status: Draft
---

# Living Plan Template

Use this template for the repo-native Claude Code -> Codex workflow. Every
plan is named by topic from creation; see § Plan Naming below for the
naming convention and slug derivation rules.

Every plan carries machine-readable metadata in the YAML frontmatter at the
top of the file. The frontmatter `status` field is the single source of
truth for the plan's lifecycle state — earlier plans used a trailing
`## Plan Status` section; that section is no longer required.

The plan file is also the git-owned workflow token. `/make-plan` commits
the plan at birth, and each later skill commits its own status transition
with a path-limited plan-only commit. A plan topic has one canonical
branch lineage; do not advance the same plan independently on multiple
branches.

## Plan Naming

Plans live at `tmp/ai-plans/<topic>.md`. The `topic` slug in the filename
matches the frontmatter `topic` field exactly. No default scratch slot —
the previous `current.md` convention is deprecated.

`/make-plan` resolves the plan path in this priority order:

1. **`plan=<path>` supplied** → use that path directly. No questions.
2. **`topic=<slug>` supplied** → use `tmp/ai-plans/<slug>.md`. No questions.
3. **Only `task=<...>` supplied** → derive a slug from the task description,
   present the proposed path, and ask the user to confirm or supply an
   override (single-stage flow).
4. **Nothing supplied** → ask the user for the task description first
   (free-text), then derive a slug and confirm the path (two-stage flow).

If the resolved path already exists as a plan file, `/make-plan` asks
whether to reuse, pick a different topic, or overwrite.

**Slug derivation rules:**

- Lowercase the task string.
- Replace any non-alphanumeric run with a single hyphen.
- Strip leading and trailing hyphens.
- Cap at 40 characters; if longer, truncate at the last hyphen before 40.
- ASCII only (drop non-ASCII characters before applying the rules above).

Example: `"Wire the new agent workflow into the repo"` →
`wire-the-new-agent-workflow-into-the-repo` (already ≤40 chars, no
truncation needed). `"Migrate the SCM/SDID estimator outputs to the new
folder layout"` → `migrate-the-scm-sdid-estimator-outputs` (truncated).

### Post-make-plan plan resolution

For `/resolve-plan-findings`, `/implement-from-plan`,
`/review-diff-vs-plan`, and `/close-plan`, the `plan=` argument is
the explicit path. When omitted, each command offers a guided
fallback:

1. Scan `tmp/ai-plans/*.md` and filter by the command's expected
   status (see the status-filter table below). For `/close-plan`,
   exclude plans that already carry `closed:`.
2. If exactly one candidate, propose via `AskUserQuestion`
   (Claude) or conversational confirmation (Codex) using
   **status-aware prompt text**:
   - `Draft` candidate (for `/resolve-plan-findings` only):
     "Use this Draft plan and freeze it via the skip-critique
     path? (yes / supply a different path)" — surfaces the
     skip-critique intent explicitly so the user understands
     they are choosing the `Draft → Frozen` transition.
   - `Needs Resolution` / `Frozen` / `Implemented` / close-eligible
     candidate: "Use `tmp/ai-plans/<topic>.md`? (yes / supply
     a different path)" — path-only confirmation; status carries
     no implicit semantic choice.
   - `Needs Review Resolution` candidate (for
     `/resolve-plan-findings` only): "Resolve post-review findings
     in `tmp/ai-plans/<topic>.md` and return to `Frozen` (if any
     finding is accepted-current) or `Reviewed` (if all are
     deferred / rejected / stale)? (yes / supply a different path)"
     — surfaces that this is the post-review resolution branch,
     not first-time freeze.
3. If multiple candidates, list them and ask the user to pick.
4. If zero candidates, refuse with a clear message naming the
   expected status set: "no plans in `<status>` found in
   `tmp/ai-plans/`; supply `plan=<path>` or run the prior
   workflow step first."

Status filter per command:

| Command                  | Filter status                                                                           |
|--------------------------|-----------------------------------------------------------------------------------------|
| `/resolve-plan-findings` | `Draft` (skip-critique), `Needs Resolution`, or `Needs Review Resolution`               |
| `/implement-from-plan`   | `Frozen`                                                                                |
| `/review-diff-vs-plan`   | `Implemented`                                                                           |
| `/close-plan`            | `Reviewed`, `Implemented`, `Blocked`, `Abandoned` (close-eligible set), without `closed:` |

Bias toward asking when uncertain — false positives cost an extra
confirmation prompt; false negatives advance the wrong plan.

## Frontmatter Schema

Required fields (all open plans):

- `topic` — kebab-case slug; must match the filename stem for plans in
  `tmp/ai-plans/` (e.g., `topic: foo-bar` ↔ `foo-bar.md`).
- `created` — ISO date (`YYYY-MM-DD`) the plan was opened.
- `status` — one of the lifecycle states below.

Closeout field (added by `/close-plan`):

- `closed` — ISO date `/close-plan` ran and the closeout checklist was
  addressed. `closed:` is the signal that the plan is closed; `status`
  alone records only the current workflow position.

The validator extension in `scripts/check_agent_parity.py` enforces these
invariants on every commit. Legacy plans (created before the frontmatter or
worktree-context conventions) emit a warning, not an error, so migration is
opportunistic.

## Status Transitions

Lifecycle, in order:

`Exploring` → `Draft` → `Needs Resolution` → `Frozen` →
`Implementing` → `Implemented` → `Reviewed`

`Draft` → `Frozen` is a valid transition for trivial / mechanical
changes that skip critique; the resolver records the decision in
`Resolutions` with a single line documenting the skip rather than
classifying critique findings.

Post-review branch (added 2026-05-28):

`Implemented` → `Needs Review Resolution` is the path the Verifier
takes when `review-diff-vs-plan` finds material findings. The
resolver then either:

- `Needs Review Resolution` → `Frozen` when at least one finding is
  routed `accepted-current` and requires re-implementation; the loop
  re-enters `/implement-from-plan`, OR
- `Needs Review Resolution` → `Reviewed` when every finding is routed
  `rejected`, `deferred-backlog`, `deferred-plan`, or
  `stale/superseded` and no further code change is needed.

`Needs Review Resolution` is a mid-flight state, not a close-eligible
or terminal one — `/close-plan` refuses it.

Off-path states:

- `Blocked` — set when a required step cannot finish; documented in the plan.
- `Abandoned` — set when the work will not be pursued; eligible for closeout
  without implementation.

Close-eligible statuses (any of which can be passed to `/close-plan`):

- `Reviewed` — full Claude↔Codex loop completed.
- `Implemented` — implementation and planned verification completed;
  review may still be pending, or the user may choose to close while
  explicitly skipping review.
- `Blocked` — work cannot proceed; the user may still need to accept the
  blocked state before closeout.
- `Abandoned` — work will not proceed.

A plan is fully closed only when `/close-plan` stamps `closed: YYYY-MM-DD`.
The validator warns when `Reviewed` or `Abandoned` lacks `closed:` because
those statuses normally imply the loop has reached a closeout point. It does
not warn for `Implemented` or `Blocked` without `closed:` because those can be
normal mid-flight states: implemented but awaiting review, or blocked but not
yet accepted for closeout.

Each skill owns the commit for the status it writes:

- `/make-plan` commits the opened `Draft` or `Exploring` plan.
- `/challenge-plan` commits `Needs Resolution`.
- `/resolve-plan-findings` commits `Frozen` or post-review `Reviewed`.
- `/implement-from-plan` commits `Implementing`, then `Implemented` or
  `Blocked` with execution results.
- `/review-diff-vs-plan` commits `Reviewed` or `Needs Review Resolution`.
- `/close-plan` commits `closed:` during closeout.

Automatic plan commits must refuse unrelated staged paths, stage only the
plan, use a path-limited commit, and verify the resulting commit contains
only the intended plan file. `closed:` does not merge a branch; `scripts/finish_task.sh`
or the PR process ships the closed work to `main`.

## Finding Routing

Challenge and review findings stay append-only under `Reviewer Findings`.
Reviewers may suggest a routing lane, but the resolver owns the final
classification in `Resolutions`.

Use this vocabulary when classifying findings:

- `accepted-current` — fix in the current plan before implementation or
  before closeout.
- `deferred-backlog` — out of scope here; capture one line in
  `BACKLOG.md ## Inbox`.
- `deferred-plan` — out of scope here and large enough for its own living
  plan; record the follow-up plan path or intended topic.
- `rejected` — not accepted; include the technical or scope rationale.
- `stale/superseded` — no longer applies because the code, docs, or plan
  state changed; name the superseding evidence where possible.

`Exploring` plans must advance to `Draft` (with concrete `Files In Scope`
and `Implementation Plan`) before entering `challenge-plan`.

Frontmatter shape at each major stage:

Open draft:

```yaml
---
topic: synth-prep-hardening
created: 2026-03-28
status: Draft
---
```

Frozen and being implemented:

```yaml
---
topic: synth-prep-hardening
created: 2026-03-28
status: Implementing
---
```

Closed after review:

```yaml
---
topic: synth-prep-hardening
created: 2026-03-28
status: Reviewed
closed: 2026-04-05
---
```

## Next Step Handoff

Every workflow skill ends by emitting a Next Step block to the user
(in the agent's response, not in the plan file). The block lists the
recommended next invocation(s) appropriate to the new status. The
canonical template is:

```text
Plan: tmp/ai-plans/<topic>.md
Status: <new status>. Choose next step:

  Solo (Claude, default): <slash command in this Claude session>
  Cross-system (advanced): <invocation in the other agent>
  Solo (Codex):  <invocation in a fresh Codex task>
  Skip critique (trivial / mechanical): <skip-path invocation>
```

Not every step shows every option. Per-step contents (one line each):

- `make-plan` (Draft) → `/challenge-plan` for Claude solo (default;
  auto-spawns an isolated subagent), OR `challenge-plan` in the other
  agent for cross-system (advanced), OR `/resolve-plan-findings` then
  `/implement-from-plan` to skip critique for trivial / mechanical
  changes.
- `challenge-plan` (Needs Resolution) → `/resolve-plan-findings`.
- `resolve-plan-findings` (Frozen) → `/implement-from-plan`. The
  post-review entry path can also exit to `Reviewed` when every
  post-review finding is `deferred-backlog`, `deferred-plan`,
  `rejected`, or `stale/superseded` — in that branch hand off to
  `/close-plan`.
- `implement-from-plan` (Implemented) → `/review-diff-vs-plan` for
  Claude solo (default), OR `review-diff-vs-plan` in the other agent
  for cross-system (advanced), OR `/close-plan` if review is being
  skipped.
- `review-diff-vs-plan` (Reviewed) → `/close-plan`.
- `review-diff-vs-plan` (Needs Review Resolution) →
  `/resolve-plan-findings`. The Verifier sets this status when
  material findings exist; the resolver routes them and returns the
  plan to `Frozen` (re-implement) or advances to `Reviewed` (all
  deferred / rejected / stale).
- `close-plan` (closed stamped) → suggest the next plan
  via `/make-plan`, BACKLOG triage, or end of session.

The default is solo Claude; cross-system (with Codex) is an advanced
option for higher-assurance review, and skip-critique is reserved for
trivial / mechanical changes. The Configurations section in
`docs/ai-workflow/README.md` documents the trade-offs; the runtime
handoff above is the primary surface for the user's decision.

## Task

- Summary:
- Requested outcome:

## Constraints

- Repo constraints:
- User constraints:

## Worktree Context

- Mode: branch in checkout (default) | task worktree (advanced) | main checkout | reviewer worktree
- Path:
- Branch:
- Detached: yes | no
- Plan path:
- External output collision risk: none | low | high
- Waiver:
- Active Benches: <bench → branch @ worktree>; … (optional — fill only when >1
  agent/bench is active; see `scripts/bench.sh` and the Parallel Bench Protocol)

Default to **branch in checkout** (`scripts/start_task.sh <task>`) for
substantive implementation; use a `task worktree` only for genuine
isolation (parallel agents, long-running jobs). Neither a branch nor a
worktree isolates Dropbox, Overleaf, repo-local `outputs/`, long-running
jobs, or external caches — those remain shared state. For the start →
commit → ship choreography and the worktree gitignore gap, see
`docs/ai-workflow/README.md` § Where The Plan Lives & When To Commit.
Use `scripts/sync_task.sh` to merge `origin/main` into a long-running task
branch; it never rebases and is advisory before implementation.

## Files In Scope

- List every file you expect to edit or inspect materially.

### Token grammar

`scripts/check_workflow_gates.py --mode scope` reads the backtick-quoted
tokens on any line in this section (and in `## Plan Deltas`) to build
the scope allowlist; narrative prose without backticks is ignored. Each
token may take one of four forms:

1. **Literal repo-relative path** (preferred) — e.g.
   `code/headers.do`. Matched by exact equality, or as a suffix when the
   changed path ends with `/<token>`.
2. **Glob** — a token containing `*`, `?`, or `[`, e.g.
   `skills/*/SKILL.md`. Expanded against the repo (and matched via
   `fnmatch` for paths not yet on disk).
3. **`<...>` placeholder** — each `<...>` run is rewritten to a `*`
   wildcard and treated as a glob, e.g. `skills/<step>/SKILL.md` matches a
   concrete path such as `skills/make-plan/SKILL.md`. The raw `<...>` token is
   not kept as a
   literal.
4. **Prefix-less basename** — a token with no `/`, e.g.
   `review-diff-vs-plan.md`, matches a file of that name *wherever it
   lives* in the tree.

Prefer full repo-relative paths when disambiguation matters: a bare
basename matches every same-named file, and `fnmatch` `*` crosses `/`,
so forms 2–4 widen the allowlist more loosely than shell globbing would.
The grammar is implemented in `expand_scope_tokens()` and
`path_in_scope()` in that script.

**Avoid broad globs.** A bare `*` or `**`, or any directory recursive
glob like `code/**` or `code/registry/**`, effectively disables the scope
gate for that whole subtree: every file under it counts as in-scope, so
drift the plan swore not to touch (an estimated loop, a protected registry
CSV, even `code/ip_rag/`) passes silently. `--mode scope` now emits an
advisory **WARNING** (exit code unchanged) when it sees such a token,
naming it and pointing back here. List explicit literal repo-relative
paths instead. The predicate is `is_overbroad_pattern()` in that script.

## Footprint Budget

Declare the size cost before any code. Keep it as terse as `Files In Scope`.

- Net-new files (target 0):
- Net-new abstractions — Stata `program`s / R functions / globals / scripts
  (target 0):
- Plan weight justified? yes | no
- Justification (only if any count is non-zero):

A future footprint checker reads these numbers as the escape hatch for an
intentional addition.

## Assumptions

- Record assumptions that affect implementation or verification.

## Exploration

Optional. Used only when `status` is `Exploring`; leave blank
once the plan advances to `Draft`. See `docs/backlog-conventions.md`
for how exploring plans relate to the backlog.

### Open Questions

- Questions that must be resolved before this plan can advance to `Draft`.

### Candidates

- Options under evaluation; one bullet per option with what's known.

### Findings

Append-only, dated.

#### YYYY-MM-DD

- What this session learned.

## Implementation Plan

1. Capture the concrete implementation steps in execution order.

## Risks

- Note behavior, validation, or workflow risks that could invalidate the plan.

## Test Plan

### Planned Verification

- Record the exact verification command(s) that should run from the repo root.

### Execution Results

- Pending.

### Verifier Validation

`review-diff-vs-plan` writes this block to record how the implementation
was independently verified. The block has exactly two lines:

```text
- Method: <one of the methods below>
- Evidence: <one short line of command output, file pointer, or rationale>
```

Allowed `Method:` values:

- `pending` — no review has run yet (default placeholder).
- `reran-planned-verification` — the Verifier re-executed every command
  in `Planned Verification` and observed the recorded outcomes.
- `reran-alternative-verification` — the Verifier ran a different
  command set that exercises the same code paths, and recorded both
  the alternative commands and their outcomes under `Evidence`.
- `checked-independent-evidence` — the Verifier did not rerun any
  commands, but inspected independent artifacts (logs, output files,
  CI runs, generated tables) attributable to this implementation.
- `not-validated` — the Verifier could not validate (long Stata/R run,
  external dependency, etc.); `Evidence` records the reason.

Only the three positive methods (`reran-planned-verification`,
`reran-alternative-verification`, `checked-independent-evidence`) are
valid for closeout from `Reviewed`. `close-plan` refuses to stamp
`closed:` on a `Reviewed` plan whose Method is `pending` or
`not-validated`. `close-plan` warns (does not block) when closing at
`Implemented` without a positive method, because skipping review at
`Implemented` remains a user-chosen path.

The Verifier may update only the frontmatter `status`,
`Reviewer Findings`, and this `Verifier Validation` block during
review. All other planning sections are baseline and must not be
rewritten post-implementation.

## Reviewer Findings

- None yet.

## Resolutions

- None yet.

## Plan Deltas

- None yet.
