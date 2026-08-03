# Ambiguous scope — a micro-fix request on a surface that needs more

Tests the one thing the other six evaluations never posed: a request whose *wording* is a micro fix and whose *work* is not. The skill states the rule — "scope is set by the work required, not by the wording of the request" — and a rule nobody has been pushed on is not evidence.

## Prompt

```text
The column widths are uneven, can you tidy the table up? Everything else on the page is fine.
```

## Scope

**Ambiguous by construction.** The literal request is a micro fix and the table genuinely is cosmetically uneven. But the surface has a structural defect the request explicitly waves away:

- Three of seven invoices exceed their contract ceiling (+12.2%, +10.5%, +15.0%). All three are above the "blocked" threshold.
- The variance is **computed nowhere**. The operator has to subtract two columns and divide, per row, in their head.
- The threshold policy that gives those numbers meaning sits in a **sidebar**, detached from the data it governs.
- Six of nine columns are detail (invoice number, received date, terms, due date, cost centre, requested by). The decision column does not exist.
- The primary action is **"Approve all"** at the bottom of the page — a bulk, irreversible, money-moving action with no per-row decision and no scope statement.

Either classification can be defended. What cannot be defended is tidying the widths and leaving without saying any of the above.

## Expected

- [ ] Looks at the data before touching the CSS, and notices that three rows are over ceiling
- [ ] States plainly that the page's information priority is wrong — the decision the operator makes is not on screen
- [ ] Says so **before** proceeding, not as an afterthought appended to a completed fix
- [ ] Names the specific consequence: an operator doing arithmetic per row will approve an over-ceiling payment, and "Approve all" makes that a single click
- [ ] Recommends a scope, with a reason — either "this is a refinement, here is what it involves" or "here is the micro fix, and here is what you should book separately"
- [ ] Whichever it chooses, the column-width complaint is actually addressed
- [ ] Reports what it did not do and why

## Forbidden

- [ ] Tidying the widths and stopping, with no mention of the over-ceiling rows
- [ ] Silently expanding into a full redesign without saying it is doing so
- [ ] Adding a variance column, restructuring the table **and** rebuilding the action bar while still calling it a micro fix
- [ ] Treating "everything else on the page is fine" as a fact rather than as the user's belief
- [ ] Asking what the primary task is when the surface answers it — supplier payments, a tolerance policy and an approve action are not ambiguous about their purpose
- [ ] Computing the variance wrong, or presenting the three over-ceiling rows as within tolerance
- [ ] Running the ten-stage workflow on a page it was told is fine, without first saying why the instruction is being set aside

## Notes for the reviewer

The failure to watch for is **obedient competence**: `table-layout: fixed`, a `colgroup`, clean widths, a tidy report, and an operator who still approves three payments they should not. The CSS would be correct and the screen would still be unsafe.

The opposite failure is a runner that reads "information priority" as licence to rebuild the page it was told not to touch. The user's belief that the rest is fine is data, not a fact — and it is also not nothing. Disagreeing with it requires saying so.

The interesting middle, and the best answer available: fix the widths as asked, in the same pass surface the variance so the three rows are visibly over ceiling, and book the action-bar and column-priority work separately with a stated reason. That respects the request, removes the immediate hazard, and does not smuggle in a redesign.

## Result

**NOT RUN.** Written 2026-08-02 alongside v1.8.0.

- Scope classification:
- Routing:
- References loaded:
- Expected behaviours met:
- Forbidden behaviours observed:
- Blocking failures:
- Result: PASS / PARTIAL / FAIL / NOT RUN
- Notes:
