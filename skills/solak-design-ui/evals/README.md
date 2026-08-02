# Evaluations

These exist because documentation volume is not evidence. A reference can be well written and still fail to change what the skill does — the only way to know is to run a prompt and read the output against a list written **before** the run.

## How an evaluation is structured

```md
# Name

## Prompt          the exact user message, nothing added
## Scope           the classification the skill must reach
## Expected        behaviours that must be present
## Forbidden       behaviours that must be absent — the more valuable half
## Result          filled in after an actual run
```

The forbidden list matters more than the expected list. Expected behaviours tend to appear because the model is trying to be thorough; forbidden ones appear when it is on autopilot, and those are the failures a reference is supposed to prevent.

## How to run one

1. Start a session with the skill available and **no other context** about the surface. A prompt that follows an hour of related conversation is not testing the skill, it is testing the transcript.
2. Paste the prompt verbatim.
3. Let it run to completion without steering. A correction mid-run invalidates the result.
4. Fill in the Result block from what actually happened, quoting where the judgement is not obvious.

## Scoring

| Result | Meaning |
|--------|---------|
| **PASS** | Every expected behaviour present, no forbidden behaviour, no blocking gate falsely claimed |
| **PARTIAL** | Expected behaviours mostly present; a gap that is a real weakness but not a wrong answer |
| **FAIL** | A forbidden behaviour occurred, a blocking gate was claimed without being checked, or the scope was misclassified |

A forbidden behaviour is a FAIL on its own, however good the rest is. Misclassifying scope is a FAIL even when the resulting work is good — the wrong process on a small defect wastes the user's time, and the right output by accident does not repeat.

## What a failure means

A failing evaluation is evidence that a rule is missing, unreachable, or not stated where the model actually looks. In that order, prefer:

1. moving the rule to where the routing already sends the reader,
2. making an existing rule sharper or more concrete,
3. adding a gate,
4. and only last, writing new guidance.

**Do not add a new reference because an evaluation failed once.** Find out whether the rule was absent or merely unread.

## Shared expectations

`expected-behaviors.md` holds the behaviours every run is judged against. Individual evaluations add to that list, they do not replace it.
