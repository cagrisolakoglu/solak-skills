# solak-design-ui Stabilization Report

**Date:** 2026-08-02 · **Version:** 1.6.0 → 1.8.0 · **Status:** draft → beta

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

All six have been run, **all in isolated sessions** that saw only the skill path, the user prompt and a purpose-built broken surface — no evaluation file, no expected or forbidden list, no access to this conversation. Every reported outcome below was then re-measured independently rather than taken from the runner's own report.

| Evaluation | Result | References read | Notes |
|------------|--------|-----------------|-------|
| `small-ui-fix` | **PASS** | 3 / 14 | No wireframe, no questions, no scope creep. A third defect reported and deliberately not fixed. Also corrected the routing wording — see below. |
| `unsafe-user-request` | **PASS** | 4 / 14 | Declined the misleading representation, delivered the labelled-total version. Said it skipped `ux-workflow.md` because routing forbids it for a micro fix. |
| `responsive-overflow` | **PASS** | 5 / 14 | Falsified the user's premise — the page overflowed at every width, not only mobile. Hit and named the `overflow: hidden` corner-clip trap. |
| `slow-filter-panel` | **PASS** | 5 / 14 | The dimming trap did not occur: 19 rows retained at `opacity: 1` through a refresh, staleness carried by banner, border and progress line. |
| `table-redesign` | **PASS** | 9 / 14 | Read "minimal" as fewer competing signals and **raised** the type size from 11px to 13px. |
| `dashboard-redesign` | **PASS** | 13 / 14 | From nothing. One primary decision in one sentence; five tiles, not nine; freshness as its own tile. |

**The routing table changes behaviour.** That was the open question, and the reference count answers it: 3, 4, 5, 5, 9, 13 — scaling with scope, from a three-file micro fix to a full redesign. Three runs named the files they deliberately skipped and why. One reported the `design-quality.md` gate as *unchecked rather than met* because routing told it not to load that file — which is precisely what the scoped-gates rule asks for and the behaviour most likely to have been ignored.

### What the runs found that the plan did not anticipate

**Measurement passes go green while screenshots do not.** Three independent runs caught defects by eye that their own assertions had reported clean: a drawer covering the primary action at 1440, an empty banner strip in the success state, skeleton bars invisible against zebra rows. The skill's claim that some breakage appears only in the image is now evidence rather than assertion.

**`hidden` loses to `display: flex`.** Three of five runs hit this independently. A state component with a `display` rule renders as an empty strip in its success state, and the `hidden` attribute silently does nothing. **Now a rule and a blocking gate** (`interaction-and-states.md` §20, base-layer line in `tokens.md`). Audited across ten surfaces afterwards: none was leaking and nine had no guard — the bug is not usually present, it is usually one `display` declaration away, which is what makes it a gate rather than a debugging note. One surface had ended up writing the per-component fix three times; the base-layer line replaces all three.

**A rule that correct behaviour violates is a bad rule.** The micro-fix routing row said *"the surface reference that owns the rule — nothing else"*, singular. The clean re-run named two defects in two rule families and correctly read three references. The wording was wrong, not the run; reworded to *"one per defect, nothing more"*, and the evaluation's own expectation was corrected with it.

**`document.fonts.check()` does not verify font delivery.** The dashboard run reported Inter absent despite the API returning `true`. Confirmed directly: `check('16px Inter')` is `true`, `check('16px "Totally Not A Real Font"')` is **also** `true`, `[...document.fonts].length` is `0`, and both measure an identical 31.1015625px. The obvious way to verify the font-delivery gate verifies nothing. Now encoded in `typography.md` §3 with the width-comparison test that does work — the only rule this pass added, and it came from an evaluation, as the plan requires.

**Adjacent-defect drift.** The responsive run also fixed numeric alignment the fixture never had; the filter run added a token layer, a dark theme and an expanded data stub. Neither is forbidden and both were disclosed, but the pattern is worth a rule: during a refinement, an adjacent defect is reported unless the change already in hand touches it. Not written yet — one observation across two runs is not enough to justify a rule.

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

**Previous:** 1.6.0 · **New:** 1.7.1 · **Status:** `draft` → **`beta`**

`1.7.0` for the stabilization work; `1.7.1` for the `document.fonts.check()` finding, which hardened an existing gate; `1.8.0` for the `hidden`-vs-`display` rule, which adds a **new** blocking gate and a new reference section, plus the micro-fix routing rewording.

The status move is evidence, not volume. Seven of the plan's eight criteria for leaving `draft` are met: validation passes, all six evaluations were run, none has a blocking failure, micro-fix routing is tested, a full redesign is tested, a responsive defect is tested, and the duplicate-rule audit is complete. The eighth — three real project tasks — is not, which is exactly why this is `beta` and not `stable`.

## Remaining risks

- **No real project has used the skill.** Every judgement in it is derived from fixtures built to test it. The evaluations narrow this loop but do not close it — the runners were given a broken file and told a skill existed, which is not the same as someone reaching for it mid-task.
- **The scope classifier is untested against ambiguity.** All six prompts had an unambiguous answer. The interesting case — "just fix the table" on a screen whose information priority is wrong, where the correct move is to say so and widen — was never posed.
- **Adjacent-defect drift is real but under-evidenced.** Two runs fixed things outside the reported defect. Both disclosed it; neither was forbidden. One more occurrence and it earns a rule.
- **Two runs read 9 and 13 of 14 references.** Justifiable for a broad refinement and a from-scratch redesign, but the upper end of routing is looser than the lower end, where discipline was excellent.
- **The examples are constructed, not transcribed.** They demonstrate the expected shape; none is a record of work delivered to a person.
- **The validator checks structure, not correctness.** It confirms a reference has a verification section; it cannot tell whether the section is right.
- **Inter is still not installed locally.** Now measured rather than assumed — the fallback face is what renders — but end-to-end delivery has never been exercised.

## Not implemented

- No `stable` promotion — blocked on real project use, deliberately
- No rule written for adjacent-defect drift — one observation short of justifying one
- No changes to `solak-create-skill` or the skill template; the staged-execution rollout remains a separate, previously deferred task
