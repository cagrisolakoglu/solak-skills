# solak-design-ui Stabilization Report

**Date:** 2026-08-02 · **Version:** 1.6.0 → 1.7.0 · **Status:** draft (unchanged, deliberately)

## Summary

The skill had enough design guidance and no way to tell whether it was being applied correctly. This pass added the parts that make it trustworthy rather than larger: a scope classifier so a focus-ring fix does not trigger a ten-stage workflow, an explicit routing table so a small task loads two references instead of fourteen, a machine-readable manifest, a validation script wired to CI, six evaluations, four worked examples and five anti-patterns.

**No new design reference was created.** Two references gained a verification section they were missing (`forms.md`, `density-and-direction.md`) — required by the validator, not by taste.

## Scope triage

Four classes in `SKILL.md`, with the process for each: micro fix (inspect → fix → verify), component refinement (local task → local review → short TODO → implement), screen redesign (full workflow), product-wide system (out of scope).

Three supporting changes make the classification real rather than decorative:

- The Inputs table now says required means *required for a redesign* — a micro fix needs none of them.
- The Workflow section states it **is** the redesign process; a refinement runs five of the ten stages, a micro fix none.
- Gates are scoped: a micro fix answers the gates its own change touches plus "nothing regressed", not the whole list. Claiming an unchecked gate is called out as worse than reporting it unchecked.

## Reference routing

A ten-row routing table maps situation → smallest safe reference set. `ux-workflow.md` is now explicitly excluded from micro fixes and `design-quality.md` is no longer "always" read — it was the only reference marked unconditional.

Each surface reference opens with a **Read with** list, replacing the ad-hoc "type treatment comes from typography.md" line each had accumulated.

A **canonical ownership** table names one home for each rule. The audit found no duplicated blocks to remove — mention counts already followed ownership (stale/retry concentrated in `interaction-and-states.md`, figures in `typography.md`, `opacity: 0.45` only in `filters.md`) — so this documents the existing state rather than changing it.

## Files added

```
manifest.yaml
scripts/validate_skill.py
evals/README.md
evals/expected-behaviors.md
evals/{table-redesign,small-ui-fix,responsive-overflow,slow-filter-panel,dashboard-redesign,unsafe-user-request}.md
examples/{dense-energy-table,slow-filter-panel,long-data-entry-form,operations-dashboard}.md
examples/anti-patterns/{card-everything,unreadable-dense-table,hidden-filter-state,toast-only-errors,arbitrary-breakpoints}.md
.github/workflows/validate-solak-design-ui.yml        (repo root)
```

## Files updated

- `SKILL.md` — scope triage, reference routing, canonical ownership, scoped gates, surface-contract pointer, v1.7.0
- `references/{tables,filters,forms,dashboards}.md` — Read with sections
- `references/forms.md`, `references/density-and-direction.md` — verification sections added
- `references/ux-workflow.md` — scope classification at Stage 0, surface contract
- `templates/design-todo.md` — Context section became the surface contract, four fields added
- `registry.json`, `README.md`, `.gitattributes` (py/yaml/yml pinned to LF)

## Files renamed

None. The audit found no naming drift: the `typography-system` and `responsive-grid-system` variants were considered during development and never created. Both are listed in `manifest.yaml` under `retired_names`, and the validator now fails if either appears on disk or in a reference.

## Duplicate rules removed

None removed. The audit measured where each cross-cutting rule is mentioned and found the canonical owner holds the substance in every case; other mentions are one-line cross-references, which is the intended pattern. Ownership is now documented in `SKILL.md` so a future addition has somewhere to belong.

## Evaluations

| Evaluation | Result | Notes |
|------------|--------|-------|
| `small-ui-fix` | **PASS** | Actually run against a purpose-built broken surface. Both defects fixed and verified by computed value in both themes; no wireframe, no questions, no scope creep. Two further defects reported and deliberately not fixed. |
| `table-redesign` | NOT RUN | Needs a clean session |
| `responsive-overflow` | NOT RUN | Needs a clean session |
| `slow-filter-panel` | NOT RUN | Needs a clean session |
| `dashboard-redesign` | NOT RUN | Needs a clean session |
| `unsafe-user-request` | NOT RUN | Needs a clean session |

Five are marked NOT RUN rather than self-graded. A run performed in the session that wrote the expectations tests recall, not routing, and recording it as PASS would make the evaluation suite look like evidence when it is not.

The one that was run is genuine because its criteria are **measured**: `textAlign`, `fontVariantNumeric` and `outlineStyle` read from the computed style before and after, in light and dark. Before: `left` / `normal` / `none`. After: `right` / `lining-nums tabular-nums` / `solid 2px` resolving to the theme accent.

## Validation

```bash
python skills/solak-design-ui/scripts/validate_skill.py
```

```text
solak-design-ui validation passed
Files checked: 32
References checked: 123
Warnings: 0
Errors: 0
```

Negative-tested by injecting four faults into a throwaway copy — all four failed the run: invalid semver (`1.6`), an empty reference, a retired filename on disk, and a reference missing its verification section. Separately confirmed that a link to a non-existent reference and a link escaping the skill directory both fail.

The report you are reading was itself caught by the validator on its first run: it quoted the retired filenames and the test links as prose, and every one of them was reported. The check does not distinguish a reference from a mention, which is the conservative behaviour — a stale name in prose is how a stale name comes back.

The hand-rolled manifest parser (standard library only, so CI needs no install step) was diffed against PyYAML on the real manifest: **identical output**.

## CI

`.github/workflows/validate-solak-design-ui.yml` — the repository had no CI, so this is a new, deliberately narrow workflow: `pull_request` and `push` filtered to `skills/solak-design-ui/**`, plus manual dispatch. Checkout, Python 3.12, one command. No secrets. Parsed with PyYAML to confirm the triggers and steps resolve as intended.

## Version decision

**Previous:** 1.6.0 · **New:** 1.7.0 · **Status:** stays `draft`

Minor, not major: everything added is additive and no existing rule changed meaning. The plan's own criteria for leaving draft are not met — five evaluations are unrun and the skill has not been used on a real project. Promoting to `beta` on the strength of new documentation would be exactly the mistake the plan warns about.

## Remaining risks

- **Five evaluations are unrun.** This is the largest gap and the one that decides whether the routing table changes behaviour or only describes an intention.
- **No real project has used the skill.** Every judgement in it is derived from fixtures built to test it, which is a closed loop.
- **The scope classifier is untested against ambiguity.** "Just fix the table" on a screen with a broken information priority is the interesting case, and nothing has probed it.
- **The examples are constructed, not transcribed.** They demonstrate the expected shape; none is a record of work actually delivered to someone.
- **The validator checks structure, not correctness.** It can confirm a reference has a verification section; it cannot tell whether the section is right.
- **Inter is still not installed locally,** so font delivery has never been verified end to end.

## Not implemented

- Clean-context runs of five evaluations (above)
- No status promotion, by design
- No changes to `solak-create-skill` or the skill template — the staged-execution rollout remains a separate, previously deferred task
