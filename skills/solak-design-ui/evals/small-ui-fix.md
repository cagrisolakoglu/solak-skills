# Micro fix — restraint under a small request

Tests the single behaviour most likely to fail: doing too much. A skill with ten stages and fourteen references has a standing temptation to run all of it.

## Prompt

```text
The amount column is left-aligned and the focus ring is missing.
```

## Scope

`micro-fix` — two named defects, both with a canonical rule, neither implying anything about the screen's purpose.

## Expected

- [ ] Classifies as a micro fix, in one line, without ceremony
- [ ] Inspects the actual component before changing it
- [ ] Reads one reference per named defect and no more — `tables.md` for alignment, whatever owns focus (`interaction-and-states.md`), and `typography.md` if the figure set is touched
- [ ] Fixes alignment with `text-align: end` **and** `tabular-nums lining-nums`, and puts the header on the same axis
- [ ] Restores a visible `focus-visible` ring rather than deleting the `outline: none` and stopping
- [ ] Checks the computed value, not the stylesheet — a class can be present and overridden
- [ ] Verifies both themes, since a focus ring commonly survives one and vanishes in the other
- [ ] Reports the two changes and how each was checked

## Forbidden

- [ ] Producing a wireframe
- [ ] Asking who the primary user is, what the primary task is, or what a mistake costs
- [ ] Running or narrating the ten-stage workflow
- [ ] Rewriting the table's markup, density, or column set
- [ ] Touching files unrelated to the two defects
- [ ] Proposing a token system, a refactor, or a redesign "while we're here"
- [ ] Claiming the full blocking-gate list was verified

## Notes for the reviewer

The interesting failure is not doing nothing — it is doing the fix correctly and then attaching an unrequested redesign proposal. Scope creep with a helpful tone is still scope creep.

A second, subtler failure: fixing `text-align` on the cell but not the header, leaving the number and its label on two different edges.

## Result — 2026-08-02, v1.7.1, clean context

Re-run in an isolated session against a **second** broken surface (`eval-microfix2.html`: a batch-run table with three left-aligned measured columns and `*:focus { outline: none }` commented as a clash with the rounded controls). The runner saw no part of this evaluation and none of the earlier run.

- **Scope classification:** micro fix. Inspect → fix → verify, no wireframe, no stage list.
- **Routing:** `tables.md` for alignment, `typography.md` for the figure set, `interaction-and-states.md` for focus — one owner per named defect. Listed the nine references it deliberately skipped.
- **References loaded:** 3 references + `SKILL.md` + `manifest.yaml`.
- **Expected behaviours met:** all eight.
- **Forbidden behaviours observed:** none. Independently verified in both themes: 18 numeric cells, all `right`, all `lining-nums tabular-nums`; **zero** non-numeric cells wrongly right-aligned; each numeric column collapses to a **single** right edge (614 / 812 / 924) so header, body and total row share one axis; 7 of 7 tabbable controls show a `solid 2px` ring at a 2px offset in the correct per-theme colour; zero page errors.
- **Blocking failures:** none.
- **Result: PASS**
- **Notes:** Read the ambiguity in "the amount column" correctly — fixed all three measured columns because they share one root cause (`th, td { text-align: left }`), reasoning that fixing only Cost leaves the same defect visible twice. Declined to honour the comment that justified removing the ring, on the grounds that "it clashed with the rounded controls" is a cosmetic objection with a solution (`outline-offset`) rather than a requirement.

  Same restraint as the first run: found a third defect — the total row leaves non-summable cells blank where `tables.md` requires `—` — and reported it rather than folding it into a fix that was reported as two.

  Stated 320px and 200% zoom as **unchecked** rather than claiming the gate, with the reason (per-cell alignment inside existing column widths adds no box). That is the scoped-gates rule working as intended.

  **This run changed a rule.** The routing row read *"the surface reference that owns the rule — nothing else"*, singular. This prompt names two defects in two rule families, so three references was the correct answer and the wording was wrong. Reworded to *"the reference that owns each named defect — one per defect, nothing more"*. A rule that correct behaviour violates is a bad rule.

## Earlier result — 2026-08-02, v1.7.0, same-session run (superseded)

Run against a purpose-built broken surface (`eval-microfix.html`: an invoice-line table with left-aligned measured columns, proportional figures, and `button:focus, a:focus { outline: none }` commented as a tidiness change).

- **Scope classification:** micro fix. Stated in one line, no stage list.
- **Routing:** `tables.md` for alignment, `interaction-and-states.md` §3 for focus. Two references.
- **References loaded:** 2 of 14.
- **Expected behaviours met:** measured before changing — `textAlign: left`, `fontVariantNumeric: normal`, `outlineStyle: none` on the focused button in both themes. Fixed with `text-align: right` + `tabular-nums lining-nums` at a specificity that beats the `th, td` base rule; headers carried the same class so the number and its label share an edge; `outline: none` replaced with `:focus-visible` + `:focus:not(:focus-visible)` rather than deleted. Verified by computed value, not by reading the stylesheet: 16 cells at `right`, ring `solid 2px` resolving to the theme accent in light **and** dark.
- **Forbidden behaviours observed:** none. No wireframe, no questions about user or task, no unrelated edits, no redesign proposal.
- **Blocking failures:** none.
- **Result: PASS**
- **Notes:** Two further defects were found and deliberately **not** fixed, only reported: the unit-price column mixes precision (`4,200.00`, `0.004`, `950.00`, `18.50`) against `formatting.md`, and the `Reference` column holds technical identifiers that `tables.md` would set in monospace. Noticing without acting is the behaviour this eval is for.

  **Caveat on the evidence:** performed in the session that wrote the reference, so it did not test whether a cold reader reaches the same routing. Kept for the record because its artefacts were measured rather than judged. The clean-context re-run above supersedes it.
