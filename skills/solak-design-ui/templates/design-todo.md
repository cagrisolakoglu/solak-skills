# Design Implementation TODO

> Copy this file into the working area for the surface being designed and fill it in.
> Stages 0-6 of `references/ux-workflow.md` produce the Context, UX decisions and
> Wireframe sections. Do not start Work items until those three are complete.

## Context

- Surface:
- Primary user:
- Primary task (one sentence):
- Success condition:
- Data volume (typical / worst case):
- Primary device and input:
- Supported minimum width:
- Existing tokens:
- Existing typography:
- Area NOT to change:

## UX decisions

- Main flow:
- Information priority (P0 / P1 / P2):
- Primary action:
- Secondary actions:
- Rare or destructive actions, and where they live:
- Progressive disclosure:
- Responsive strategy (and the measurement behind it):
- Loading strategy:
- Empty strategy (first use vs filtered no-results):
- Error strategy:

## Wireframe

```text

```

## Work items

Every item names a file or component, produces one verifiable result, and carries an
acceptance criterion. Validate before moving on. No item is marked complete on the
strength of "it looks right".

### 1. Structure and semantics
- [ ] …
      *Accept:* …

### 2. Primary flow
- [ ] …
      *Accept:* …

### 3. States
- [ ] Loading — *Accept:* real content height, no layout shift on arrival
- [ ] First use — *Accept:* explains what this is and offers the first action
- [ ] No results (filtered) — *Accept:* separate component, names the responsible filter, offers an exit
- [ ] Error and retry — *Accept:* scoped to the failing region, retry works
- [ ] Partial / stale — *Accept:* incomplete data is not presented as complete

### 4. Responsive
- [ ] Desktop — *Accept:* …
- [ ] Tablet — *Accept:* …
- [ ] 320px — *Accept:* strategy measured, not just declared

### 5. Density and typography
- [ ] Density tokens connected — *Accept:* changing the level touches no component rule
- [ ] Type system applied — *Accept:* existing system used, or the fallback declared
- [ ] Numeric cells — *Accept:* `tabular-nums lining-nums`, right-aligned, constant precision

### 6. Visual tokens
- [ ] Colour and spacing tokens connected — *Accept:* no literal values in components
- [ ] One separator system — *Accept:* zebra or rules, not both
- [ ] Interaction states — *Accept:* hover, focus-visible, active, selected, disabled, readonly
- [ ] Decoration removed — *Accept:* every remaining ornament answers "what does this tell the user?"

### 7. Accessibility
- [ ] Semantic elements — *Accept:* …
- [ ] Keyboard access and focus order — *Accept:* primary task completable by keyboard
- [ ] Accessible names and ARIA relationships — *Accept:* …
- [ ] Colour is not the only indicator — *Accept:* passes the greyscale check
- [ ] Contrast — *Accept:* ≥ 4.5:1, status colours included

### 8. Verification
- [ ] 320 / 768 / 1440 screenshots
- [ ] Loading / empty / error screenshots
- [ ] Scrolled screenshot where anything is sticky
- [ ] Keyboard flow
- [ ] Overflow and long content
- [ ] Realistic dense data

## Decision log

| Decision | Reason | Alternatives rejected |
|----------|--------|-----------------------|
| … | … | … |

## Completion report

- Completed:
- Warnings (done but unverified):
- Blockers:
- Remaining risks:
- Not tested (state explicitly): real users · real devices · dark theme · performance · virtualisation
