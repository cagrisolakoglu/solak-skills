# Interaction and States

> Read this at the **usability pass** stage of `ux-workflow.md`, with the wireframe in hand and before any styling. States are structural — they change how much space a region needs — so discovering them after the visual pass means redoing it.

A visually correct interface can still be unsafe. The user must always be able to answer:

1. Did the system receive my action?
2. Is it still working?
3. Did it succeed?
4. If not, what happened?
5. What can I do next?
6. Can I retry, undo or recover?
7. Is what I am looking at current, stale, partial or missing?

> **Every meaningful action produces visible, understandable and recoverable feedback.**

What the surface references already own, and is not repeated here: `readonly` vs `disabled` visuals and validation timing (`forms.md`) · staleness announced rather than dimmed, and the one-live-region rule (`filters.md`) · selection scope and totals excluding unavailable records (`tables.md`) · tile-level errors and missing-≠-zero (`dashboards.md`) · motion carries information only (`design-quality.md`).

## 1 · The state inventory

Build this **before** implementation. A state is not designed until its trigger, feedback, recovery and exit are all known.

```md
| State | Trigger | User sees | User can do | Exit condition |
|-------|---------|-----------|-------------|----------------|
| Initial loading | first fetch | real labels + skeleton values | wait, cancel if safe | data or error |
| Refreshing | data refreshes | old data + refresh status | keep reading | fresh data |
| Error | request fails | what failed + recovery | retry, change input | success or cancel |
| Unsaved | local edit | persistent indicator | save, discard | saved or reverted |
```

The candidate list — not every surface needs every one:

```text
idle · hover · focus-visible · active · selected · disabled · readonly
loading-initial · loading-refresh · pending · submitting
success · warning · error · retrying
empty-first-use · empty-no-results · partial · stale · offline
unsaved · conflict · completed
```

## 2 · Choose the smallest feedback surface that works

| Surface | Use when |
|---------|----------|
| Field message | The state belongs to one input |
| Inline component message | It belongs to one component |
| Status text | One operation needs persistent feedback |
| Banner | It affects a region or the page |
| Toast | Short-lived, non-critical confirmation |
| Dialog | The user must decide before continuing |
| Drawer / panel | Correction or context needs room |
| Activity centre | Long-running background work |

Do not use a dialog for a routine warning, a toast for something the user must act on, or a page banner for a single-field error. **Feedback lives next to the thing it is about.**

## 3 · Base interaction states

**Hover** may aid discovery but is never the only path: no hover-only actions, no layout movement, and anything revealed on hover also appears on `:focus-within`. Touch has no hover at all.

**Focus-visible** on every keyboard-reachable control. Never remove the native ring without replacing it; keep it visible in both themes, unclipped, and in an order that matches DOM and visual order.

**Active** confirms the press. Subtle, and never delaying the action.

**Selected** must survive without colour — at least two cues from: fill or border, an icon or check, a label, and the matching `aria-selected` / `aria-pressed`. A tinted background alone disappears in greyscale.

## 4 · Loading has four kinds

| Kind | When | Rule |
|------|------|------|
| **Initial** | No previous content | Real labels and headers, skeleton only the unknown values, final dimensions, `aria-busy`, no layout shift |
| **Refresh** | Usable data already on screen | Keep the old data, say it is refreshing, never empty the region, never lower the region's opacity |
| **Local** | One row, tile, button or panel | Feedback sits next to the operation; the page does not block |
| **Long-running** | Measurable work | Real progress, current stage if useful, cancel when safe, no fake percentages, say whether leaving the page is safe |

Turning known labels into skeleton bars hides what is coming and makes the layout jump when text arrives (`forms.md`, `tables.md`).

## 5 · Pending and submitting

Pending means accepted but not finished. Say so in words:

```text
Saving…   ·   Applying filters…   ·   Calculation queued…   ·   Generating export…
```

The user needs to know whether duplicate submission is prevented, whether they can continue, whether they can cancel, and whether leaving is safe. A bare spinner answers none of that.

Button progression: `Save` → `Saving…` → `Saved` → `Retry save`. Do not replace the label with an unlabelled spinner — the button stops saying what it does at exactly the moment the user is unsure.

## 6 · Success, proportional to the operation

| Operation | Feedback |
|-----------|----------|
| Small, reversible | Inline confirmation or a short toast, optional undo — "View saved." |
| Important, persistent | Persistent status near the edited surface — "Saved · 14:32" |
| Critical, completed | Result summary, affected count, warnings, next action, reference number |

```text
Settlement run completed.
412 records processed · 7 require review.
```

**A disappearing toast is never the only proof of a critical save.**

## 7 · Errors and retry

An error answers four things: what failed, why if known, what the user can do, and whether their work survived.

```text
❌ An error occurred.
✅ The schedule could not be saved because two periods overlap.
   Review the highlighted periods and try again.
```

Scope the feedback: field → inline · row → row state · component → component message plus retry · page → page state · system → global banner, and only when it really is system-wide. **Do not replace the whole page because one component failed.**

Retry is visible, close to the failure, safe to repeat, protected against duplicate requests, and **names what it retries**:

```text
❌ [Try again]        ✅ [Retry meter data]        during: Retrying meter data…
```

Keep whatever content was already usable on screen while retrying.

## 8 · Empty, partial, stale — three different things

**First-use** and **no-results** are separate components with separate recovery. One says what the surface is and offers the first action; the other names the restrictive criterion and offers a way back. Sharing a component leaves the user unable to tell whether the system is empty or their filter is bad.

**Partial** shows what arrived, identifies what did not, and states the effect on totals:

```text
405 of 412 records loaded.
7 unavailable records are excluded from the total.
```

Never convert a missing value to zero, and never hide all the usable data because one source failed.

**Stale** was valid and may no longer be. Keep it readable, show the last-updated time, show whether a refresh is running, and carry it with a labelled banner, a timestamp, a region border or a progress line — never by dimming (`filters.md`).

## 9 · Offline

State the connection, and be honest about persistence:

```text
You are offline.
Changes are stored locally and will be sent when the connection returns.
```

or

```text
You are offline.
Editing is disabled because this application cannot safely store local changes.
```

**Never falsely confirm server persistence.** "Saved" when nothing left the device is the most expensive lie an interface can tell.

## 10 · Unsaved changes and auto-save

Unsaved state stays visible after editing, with save and discard actions and leave-page protection. Do not warn when nothing changed, do not rely on the browser's unload dialog alone, preserve edits after a validation failure, and clear the warning the moment a save succeeds.

Auto-save exposes all four of its states:

```text
Saving…   ·   Saved · 14:32   ·   Could not save · Retry   ·   Offline · Waiting to sync
```

Debounce frequent edits, keep local state on failure, and do not toast every save. The status belongs near the form title or its actions (`forms.md`).

## 11 · Optimistic updates

Only when failures are rare, the action is predictable, rollback is safe, and the consequence is not critical. Good: starring, preferences, simple toggles, dismissing. **Not** for trading, settlement, invoices, approvals, irreversible deletion, or any regulated value.

Optimistic behaviour still requires a pending state, a rollback, an explanation when it rolls back, and a retry when safe.

## 12 · Undo vs confirmation

| Choose | When |
|--------|------|
| **Undo** | Common, low risk, quickly reversible — archive, dismiss, move, remove from a list |
| **Confirmation** | Destructive, irreversible, many records affected, scope easily misread, external or regulatory consequences |

Undo must stay available long enough, restore the real previous state, be keyboard reachable, and never stand in for an irreversible external effect.

Confirmation states **action, scope, consequence, recovery** — and the buttons name the action:

```text
Delete 412 meter records?

This removes the records from the current settlement run.
This action cannot be undone.

[Delete 412 records]  [Cancel]        ❌ [Yes] [No]
```

Avoid confirmation for routine reversible actions; a confirmation the user always clicks through stops being a safeguard.

Destructive actions show their **scope**: "Delete 412 selected records", not "Delete selected". Weight and placement of the destructive button are in `forms.md`.

## 13 · Conflict

Another user changed the record, background data moved, the submitted version is stale, or an edit lock expired.

```text
This schedule was updated by another user at 14:28.
Your changes are preserved locally.

[Review differences]  [Overwrite]  [Discard my changes]
```

Say what changed, who and when if known, that local work survives, and what the options are. **Never silently overwrite newer data.** For critical records, overwriting may need its own permission or confirmation.

## 14 · Background operations

Server-side work gets a persistent activity area with states `queued · running · completed · completed-with-warnings · failed · cancelled`, and shows the operation name, status, start time, real progress when measurable, a result summary and the next action.

**The user must not have to keep the page open** for work the server is doing.

## 15 · Permission is not "disabled"

```text
You can view this settlement but cannot approve it.
Approval requires the Settlement Manager role.
```

Distinguish a missing permission from a temporary disabled state, state the required role when useful, and never show an unexplained disabled button. Do not leak sensitive values through a disabled control.

## 16 · Time and freshness

```text
Updated 14:32 Europe/Istanbul   ·   Live   ·   Delayed by 5 min   ·   Updated 18 min ago
```

Do not call cached or delayed data live. Show the zone where ambiguity matters, keep the exact source time for audit-sensitive work, and pick one strategy — relative or absolute — and hold it.

## 17 · Toasts, banners, dialogs, drawers

**Toast** — brief confirmation, non-critical completion, small reversible action. Never for validation errors, critical failures, unsaved changes, long instructions, or anything with financial or legal consequence. Readable duration, accessible action, pauses on hover or focus when actionable, controlled stacking.

**Banner** — a state affecting a region or page: stale data, offline, degraded service, partial availability, changed permissions. Anatomy: state label, short explanation, primary recovery, optional secondary.

**Dialog** — only when the user must decide before continuing. Clear title, concise consequence, action-named buttons, initial focus on the safest target, focus contained and returned to the trigger, Escape when safe. Not for routine success, passive information, one-field validation, or long editing.

**Drawer** — secondary detail, advanced filters, short editing. Focus moves in and returns on close, the panel has a heading, unsaved changes are handled, and mobile full-screen has an explicit close. Critical state must stay understandable **while the drawer is closed** — never hide active filters or warnings inside it.

## 18 · Accessibility

Loading regions use `aria-busy` · result updates use one controlled `aria-live` · errors use `aria-describedby` + `aria-invalid` · dialogs manage focus · selected items expose state · expandable controls use `aria-expanded` · measurable progress uses a semantic progress element · a disabled control's reason stays available.

**Avoid competing live regions.** One user action must not produce several overlapping announcements (`filters.md`).

## 19 · State tokens and motion

State colours are tokenised, never hardcoded in components: `--surface-hover`, `--surface-selected`, `--surface-sunken`, `--focus-ring`, `--ink-muted`, and the semantic status pairs (`tokens.md`).

```css
:root { --duration-fast: 120ms; --duration-normal: 180ms; --duration-slow: 240ms; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 1ms !important; transition-duration: 1ms !important; }
}
```

Do not animate critical numbers continuously — a value that is always moving cannot be read.

## 20 · State component contract

For every reusable state component:

```text
Scope:                  data table
Trigger:                refresh request failed
Message:                Updated data could not be loaded. Showing data from 14:10.
Primary action:         Retry refresh
Secondary action:       none
Persistence:            until a successful refresh
Dismiss behaviour:      not dismissible
Accessibility:          announce politely once
```

### The `hidden` attribute loses to any `display` rule

A state component is normally toggled with the `hidden` attribute. `hidden` works by applying `display: none` from the UA stylesheet, so **any author `display` declaration on the same element beats it** — and the component then renders in its success state as an empty strip: correct height, correct border, no content, no error.

```css
.banner { display: flex; gap: 8px; padding: 8px 12px; }   /* ← defeats [hidden] */
```

```html
<p class="banner" hidden>Showing data from 14:10.</p>      <!-- visible anyway -->
```

Nothing errors. The attribute is in the DOM, a code review that greps for `hidden` finds it, and the strip looks like a spacing bug rather than a broken state. It appeared independently in **three of five** clean-context runs of this skill, on banners, selection bars and notices — the components most likely to be `flex` and most likely to be conditional.

Two fixes, in order of preference:

```css
/* 1 — one line, once, at the top of the stylesheet. Belongs in the base layer. */
[hidden] { display: none !important; }

/* 2 — or scope the display rule so it cannot apply while hidden. */
.banner:not([hidden]) { display: flex; }
```

Prefer the first: it is a single rule that closes the whole class of bug, and `!important` is correct here because it is restoring UA behaviour rather than overriding a design decision. The second is only better when a component genuinely needs two visible display modes.

The cost of choosing the second by default is measurable. One surface built without the base rule ended up carrying `.panel[hidden]`, `.banner[hidden]` and `.applied[hidden], .applied-summary[hidden]` — the same fix written three times, once per component, each one a line someone has to remember on the fourth component. Put it in the base layer (`tokens.md`) and there is no fourth line.

Audited across ten surfaces: none was leaking, and nine had no guard. The bug is not usually present — it is usually **one `display` declaration away**, which is why this is a gate and not a debugging note.

The check is one line per conditional component, and it must read the **computed** value:

```js
el.hidden && getComputedStyle(el).display !== 'none'   // → the state is leaking
```

Same shape as the other traps in this file and in `responsive-grid.md`: valid CSS, silent output, wrong result, visible only in the image or the computed style.

## Surface notes

**Tables** (`tables.md`) — row-level pending and error, partial row loading, bulk action feedback, retry that does not clear existing rows, technical failure detail reachable without replacing the table.

**Filters** (`filters.md`) — pending query, stale-while-revalidate, applied filters always visible, no-results recovery, count consistency, explicit apply for expensive queries.

**Forms** (`forms.md`) — blur and submit validation, unsaved state, save and auto-save, server validation in the same place and style as client validation with the user's input preserved, conflict resolution.

**Dashboards** (`dashboards.md`) — tile-level loading and error, partial data, last-updated time, stale indicators, no-data reasons, unavailable values never shown as zero.

## Verification

Test each relevant state at 320 / 768 / 1440, in both themes, keyboard-only, at 200% zoom, and with realistic data:

```text
999,999,999.999 · -999.99% · missing value · zero value · pending calculation
a long localised error message · a conflicting update by another user
```

Plus: slow network, offline, server validation failure, partial data, stale data.

## Blocking gates

- [ ] Every primary action produces visible feedback
- [ ] Initial loading designed; refresh loading preserves usable data
- [ ] First-use empty and no-results are separate components
- [ ] Errors explain recovery; retry names what it retries
- [ ] Partial data identifies what is missing; missing data is never zero
- [ ] Stale data shows its last-updated time and stays readable
- [ ] Unsaved changes stay visible; auto-save exposes saving / saved / failed / offline
- [ ] Destructive actions show scope; irreversible ones confirm; reversible ones offer undo
- [ ] `readonly` and `disabled` remain distinguishable, dark theme included
- [ ] `focus-visible` present; hover is never the only access path
- [ ] Colour is never the only state cue
- [ ] Every conditional component is **hidden when hidden** — `el.hidden && getComputedStyle(el).display !== 'none'` is false for all of them
- [ ] Critical feedback is never toast-only
- [ ] Loading and pending states carry text, not just a spinner
- [ ] Dialog focus managed and returned; live regions do not duplicate
- [ ] Conflict behaviour prevents silent overwrite
- [ ] User input survives validation and request failures
- [ ] Required states work at 320px and 200% zoom

## Anti-patterns

Empty the page during refresh · dim a whole data region with opacity · a contextless spinner for long work · one empty state for every empty condition · missing data as zero · toast for critical errors · dialogs for routine reversible actions · `Yes`/`No` on a destructive dialog · disabled without explanation · readonly and disabled treated as one state · actions hidden until hover · silent conflict overwrite · clearing input after a validation failure · announcing every background update · stacking many toasts · colour as the only state cue · hidden stale timestamps · fake progress · claiming success before persistence · marking work complete without testing a failure path.

## Report

```text
Primary action feedback:   Save enters a pending state and prevents duplicate submission
Initial loading:           real labels, skeleton values, no layout shift
Refresh behaviour:         existing rows stay visible with a stale banner and progress line
First-use empty:           explains the surface, offers provisioning
No-results empty:          names the restrictive filter, offers two exits
Partial-data behaviour:    7 missing records identified and excluded from totals
Stale-data behaviour:      last-updated time plus warning border; contrast untouched
Error and retry:           the failed source is named; retry affects only that source
Save / unsaved:            persistent status; leave-page protection
Conflict behaviour:        local edits preserved, differences reviewable
Destructive behaviour:     scope stated, confirmation names the action
Undo behaviour:            available for archive and dismiss
Offline behaviour:         not implemented — stated as a risk
Accessibility:             aria-busy, one live region, focus returned from dialogs
Unverified risks:          offline queue untested on a physical device
```

---

> A reliable interface explains every transition between intent and result. The goal is not to make every state visually prominent — it is that the user is never uncertain about what happened, what is happening, or what to do next.
