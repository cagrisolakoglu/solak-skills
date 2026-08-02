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

## Result

**NOT RUN.** Written 2026-08-02 alongside v1.7.0; no clean-context execution yet.

A run performed in the session that authored the expectations is not evidence — the routing decision would be recalled rather than reached. This one needs a fresh session with the skill installed and no prior conversation about the surface.

- Scope classification:
- Routing:
- References loaded:
- Expected behaviours met:
- Forbidden behaviours observed:
- Blocking failures:
- Result: PASS / PARTIAL / FAIL / NOT RUN
- Notes:
