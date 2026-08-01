# Data-Entry Form

> Before applying these rules, complete the user-task, information-priority and layout stages in `ux-workflow.md`. This reference refines an approved layout — field order follows the user's mental model established there, and fields that support no decision should already have been removed.

Label, help-text, error, readonly and disabled type treatment comes from `typography.md`; this file adds the form behaviour around it.

## Grouping and rhythm

Split fields into semantic groups (`fieldset` + `legend`); spacing between groups is **at least twice** the spacing between fields. Uniform spacing turns a long form into an unreadable list.

```css
.form-field { margin-block-end: var(--space-field); }  /* 16px */
.form-group { margin-block-end: var(--space-group); }  /* 40px */
```

Grouping is expressed by **space and a group label**, not by a box around each group. A form where every group is a card has no hierarchy, only frames (`design-quality.md`).

## Labels above

Label above the field, left-aligned. This is the fastest layout to scan and it does not break with long labels.

A left-side layout (label left, field right) holds the column width hostage to the label. A placeholder label is **not a label** — it disappears on focus and the user cannot verify what they entered. Placeholders are for format hints only: `DD.MM.YYYY`.

## Marking requiredness

**If most fields are required, mark the optional ones** — not the other way round. A star beside every field carries no information.

```html
<label for="note">Note <span class="field-optional">(optional)</span></label>
```

## Validation timing

- **Validate on `blur`** — not on every keystroke. Showing an error mid-typing accuses the user in the middle of their sentence.
- If a field is in error and the user is fixing it, **clear the error the moment it becomes valid** — here immediate feedback is correct.
- On submit, show all errors and focus the first one.
- Server-side validation results land in the same place, in the same form; do not build a second error channel.

## Error messages

**Below** the field, tied to it with `aria-describedby`, phrased as what to do.

| ❌ | ✅ |
|----|-----|
| "Invalid value" | "Date must be in DD.MM.YYYY format" |
| "Error: field required" | "Select a customer" |
| "Format error" | "Tax ID must be 10 digits — currently 9" |

```html
<input id="tax" aria-describedby="tax-error" aria-invalid="true">
<p id="tax-error" class="field-error">Tax ID must be 10 digits — currently 9.</p>
```

Error colour cannot be the only indicator: an icon or text must accompany it.

In a long form, also add a summary block at the top: how many errors, each linking to its field.

## disabled vs read-only

| State | Meaning | Visual |
|-------|---------|--------|
| `disabled` | Cannot be changed right now, **and the reason must be stated** | Faded, not focusable |
| `readonly` | The value exists as information, cannot be changed | Normal contrast, focusable, copyable |

Making a displayed value `disabled` renders it unreadable — if it is there to be read, use `readonly`. Beside a `disabled` field, write why it is closed: "Select a customer before choosing a plan".

### Painting both the same grey is the most common mistake

If both get "sunken surface plus faded border", the distinction survives only in text colour and is invisible. Spread the distinction across **three axes**:

```css
/* readonly = a printed value, not a control: no fill, full-contrast ink */
input[readonly] { background: transparent; border-color: var(--line); color: var(--ink-strong); }
input[readonly]:hover { border-color: var(--line); }   /* does not respond like a control */

/* disabled = a closed control: sunken fill + faded ink + DASHED border */
input[disabled], select[disabled] {
  background: var(--surface-sunken);
  border: 1px dashed var(--line-strong);
  color: var(--ink-muted);
  cursor: not-allowed;
}
```

The dashed border is not decoration, it is a **dark-theme necessity.** In light theme the fill difference does the work; in dark theme the input surface sits at 27.5%, the card at 24% and the sunken surface at 21% — all three resolve to the same dark grey and the brightness difference vanishes. Closedness has to be carried by a colour-independent cue (dashed border, lock icon, reason text). The same argument applies to greyscale printouts and dim screens.

Verification is one step: **take a dark-theme screenshot and compare a readonly and a disabled field side by side.** If you cannot tell them apart, neither can the user.

## Field width matches content

Fixed-length fields such as postcode, tax ID or amount are **never full width.** The width communicates the expected character count and reduces mistakes.

This does not break column alignment: the grid decides the cell's left edge, `max-inline-size` decides how much of the cell the field fills. Division of labour in `grid.md`.

```css
.field-postcode { max-inline-size: 8ch; }
.field-amount   { max-inline-size: 12ch; font-variant-numeric: tabular-nums lining-nums; text-align: right; }
.field-name     { inline-size: 100%; max-inline-size: 40ch; }
```

Note the cell carrying help or error text needs its own measure (≥ ~34ch) even when the input inside it stays narrow — see `grid.md`.

## Action hierarchy

- The primary action (Save) is emphasised and **singular**
- Secondary (Cancel) is low-emphasis; beside the primary but far enough not to be hit by accident
- **The destructive action (Delete) lives elsewhere**, not next to the primary; it asks for confirmation
- **Its weight flips in the confirmation dialog.** In the form's action row Delete is quiet and distant, because the primary action there is Save. In the dialog that follows, the destructive action **is** the primary action — the user came there to confirm it — so it takes solid weight in the danger colour. Left low-emphasis there, "Cancel" becomes the visually stronger button and the screen pushes the user away from what they asked for
- In a long form the save action may be sticky; then an unsaved-changes indicator must exist too
- During submission, disable the button and show the state — prevent double submission

## Auto-save

If saving happens automatically, **show the state**: "Saved · 14:32". Silent auto-save makes users believe their work was lost. With explicit saving, warn before leaving the page with unsaved changes.

## States

| State | Design |
|-------|--------|
| Empty form | Defaults are sensible and visible; no hidden defaults |
| Loading (fetching an existing record) | Field skeletons at real field height — **the label is not a skeleton** |
| Submitting | Button busy state; form locked but content still readable |
| Partial failure (server) | Clear which fields saved and which did not |
| Saved | Confirmation visible and persistent; a vanishing toast is not enough |

### A skeleton hides only the unknown

The label is not loading — it is already known. Turning it into a grey bar hides from the user what is coming, and the layout jitters when the text appears.

```html
<!-- ❌ label is a skeleton too, and the field is hidden from screen readers entirely -->
<div class="field" aria-hidden="true">
  <span class="skeleton-label"></span>
  <span class="skeleton"></span>
</div>

<!-- ✅ real label; only the value is pending -->
<div class="field">
  <label for="avg">Trailing average (GB)</label>
  <div id="avg" aria-busy="true" aria-describedby="avg-hint">
    <span class="skeleton w-index"></span>
  </div>
  <p class="field-hint" id="avg-hint">Fetching the last 6 periods…</p>
</div>
```

`aria-busy` instead of `aria-hidden`: the screen reader knows the field exists and is pending. With `aria-hidden` the field behaves as if it does not exist and then appears out of nowhere when data arrives.

The skeleton's width should also match the expected value — a full-width skeleton for a 16-character field promises something that will not arrive.

## Accessibility

- Every field tied to a `label` via `for`/`id`
- Errors via `aria-describedby` + `aria-invalid`
- Groups via `fieldset`/`legend`
- Fillable from start to end by keyboard; focus order matches visual order
- Autofocus only on a screen whose single job is the form; otherwise it tears a screen-reader user out of context
