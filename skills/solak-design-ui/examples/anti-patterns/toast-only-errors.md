# Toast-only errors

Canonical reference: `interaction-and-states.md`, with the form cases in `forms.md`.

## Bad implementation

Every piece of system feedback goes through one transient channel.

```js
try {
  await saveSettlementRun(payload);
  toast.success('Saved');
} catch (e) {
  toast.error('Something went wrong');       // gone in 4 seconds
}

if (!form.valid)   toast.error('Please check the form');
if (data.isStale)  toast.info('Data may be out of date');
```

## Why it fails

A toast is a **transient, non-modal, low-attention** channel. That makes it correct for exactly one thing: confirming something small that the user already expects to have happened.

- **A dismissed toast is an unrecoverable state.** The user looks away, comes back, and the interface shows a form that appears saved. The only record that it failed has expired.
- **Validation in a toast leaves the user hunting.** "Please check the form" names no field. The information belongs next to the input that is wrong, where the eye already is.
- **Staleness in a toast is worse than no indicator.** Staleness persists; a toast does not. Four seconds later the data is still stale and the screen says nothing, so the user reads old numbers believing they are current.
- **The retry disappears with the toast.** Putting the recovery action inside a component that removes itself on a timer means the recovery is only available to users who react within the timeout.
- **Screen-reader users may never receive it.** A polite live region that fires while focus is elsewhere, competing with other announcements, is easily lost.
- **Stacked toasts hide each other.** Three failures in a bulk operation produce three overlapping cards and one readable message.

## Correct direction

Choose the smallest surface that **persists as long as the state does**:

| State | Surface |
|-------|---------|
| Field is invalid | Field message, `aria-describedby` + `aria-invalid` |
| Save failed | Persistent status by the form actions, with a named retry |
| Data is stale | Banner on the region, with the last-updated time, until a refresh succeeds |
| One row failed | Row-level state, other rows untouched |
| Critical save succeeded | Persistent "Saved · 14:32", not only a toast |
| Small reversible action succeeded | Toast **is** correct here, with the undo inside it |
| A decision is required before continuing | Dialog |

```text
❌ toast: "Something went wrong"

✅ ⚠ The settlement run was not saved.
     The billing service rejected 2 of 6 fields; your entries are unchanged.
     [Retry save]  [Review the 2 fields]
```

Errors say **what failed, why if known, what to do, and whether the user's work survived**. Retry names its target: `Retry meter data`, not `Try again`.

A toast may accompany a persistent record. It may not be the only one.

## Detection checklist

- [ ] Is any error, validation message or stale-data notice delivered **only** as a toast?
- [ ] If the user dismisses every toast, is any state now invisible that is still true?
- [ ] Does any recovery action live inside something that auto-dismisses?
- [ ] Does a toast carry text the user might need to write down or act on later?
- [ ] Is a critical save confirmed anywhere other than a toast?
- [ ] Can a single user action produce more than two toasts?
- [ ] Does an actionable toast pause its timer on hover and focus?
- [ ] Is a validation message anywhere other than next to its field?
