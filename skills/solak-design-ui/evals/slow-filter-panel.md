# Slow filter panel — asynchronous state

Tests the behaviour that separates a usable query surface from an unusable one: what is on screen while the answer is being fetched.

## Prompt

```text
The filters are slow and users think the table is empty.
```

## Scope

`component-refinement`. Note what the user reported: not "slow", but *"users think the table is empty"*. The complaint is a state-communication failure that speed alone would not fix.

## Expected

- [ ] Reads the complaint correctly — the problem is what the screen says during the wait, not only the wait
- [ ] Keeps the previous result on screen while the new query runs (stale-while-revalidate)
- [ ] Announces staleness in text, with a last-updated time
- [ ] Shows a pending state that says what is pending, not a bare spinner
- [ ] Keeps applied filters visible at all times, including their values
- [ ] Separates loading from filtered no-results — different components, different recovery
- [ ] No-results names the restrictive criterion and offers a way back
- [ ] Debounces typed input, or uses an explicit Apply for an expensive query, and shows that unapplied changes exist
- [ ] Result count stays consistent with what is displayed
- [ ] Provides retry on failure that does not clear the existing result
- [ ] One live region — one action does not produce three announcements

## Forbidden

- [ ] `opacity` on the result region to signal staleness
- [ ] Emptying the table on every query
- [ ] Hiding active filters inside a drawer with no summary outside it
- [ ] Using the same empty component for "no data yet" and "no matches"
- [ ] A spinner as the only pending feedback
- [ ] Treating this as a backend performance ticket and returning no interface change
- [ ] Announcing every intermediate update to assistive technology

## Notes for the reviewer

The dimming failure is the one to watch. It is the first idea most people have, it looks considerate, and it drops every value in the table below the contrast threshold — asking the user to read numbers that are no longer readable, in exchange for information one line of text carries better.

Second: a correct stale-while-revalidate implementation with the filter chips hidden is still a failure, because the user cannot tell which query produced the numbers they are reading.

## Result — 2026-08-02, v1.7.0, clean context

Surface: a panel behind a `Filters (3)` button, three defaults applied on mount and rendered nowhere, a per-keystroke `input → runQuery` binding, the result region replaced by a spinner on every query, one `No records found` component for both empty conditions, and a count from a separate endpoint.

- **Scope classification:** component refinement. Not a micro fix — the defects span query behaviour, the count contract and five absent states. Not a redesign — the criteria and column sets were right.
- **Routing:** `filters.md` + `interaction-and-states.md` exactly as the table prescribes, plus `ux-workflow.md` and the TODO template. Explicitly did not open `tables.md`, `typography.md`, `formatting.md`, `responsive-grid.md` or `design-quality.md`.
- **References loaded:** 5 of 14.
- **Expected behaviours met:** all eleven. Read the complaint correctly — identified that "users think the table is empty" is a state-communication failure that speed alone would not fix, and said so before changing anything.
- **Forbidden behaviours observed:** none. Verified independently by driving the page: editing a criterion fires **no** query (state stayed `idle`, an unapplied-changes notice appeared); pressing Apply put the region into `refreshing` with **all 19 previous rows still present**, `opacity: 1` on both the rows and the region, a warning border, a progress line, and a banner reading *"Applying filters — showing the previous result from 04:07 PM until the new one arrives"*; exactly **one** `aria-live` region; three chips visible with the panel closed, each carrying its value and labelled `· default`; no horizontal overflow at 320 / 600 / 768 / 1440; numeric cells `right` with `lining-nums tabular-nums`; zero page errors.
- **Blocking failures:** none.
- **Result: PASS**
- **Notes:** The dimming trap — the failure this evaluation exists to catch — did not occur. Staleness is carried by banner, border and progress line at full contrast.

  Chose explicit Apply over debounce with a stated reason: 1.5–6s per criterion is not rescuable by debouncing. Computed the responsible filter for the no-results copy rather than listing all of them ("removing it would show 19 records"). Put filter state in the URL.

  Went well beyond the reported defect: a token layer, a dark theme, container queries, a card fold, and an expanded 288-record stub with `?fail=1 ?nocount=1 ?empty=1` flags so each state is demonstrable. Defensible for a refinement whose subject is states, but it is the widest of the five runs and worth watching.

  Notably honest: reported the `design-quality.md` gate as **unchecked rather than met**, because routing told it not to load that file for a refinement. That is the exact behaviour the scoped-gates rule asks for.
