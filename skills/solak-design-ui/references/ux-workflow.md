# UX-First Workflow

The stages below run **before** any visual decision. Density, typography, tokens and surface rules are not removed — they move to the end, where they belong.

Layout lives in `layout-and-information-architecture.md`; this file covers everything around it.

## Why layout comes before styling

A screen that is beautiful and wrong is still wrong, and the cost of finding out is highest at the end. Three concrete reasons, in order of how much money they save:

1. **Style decisions made early get defended.** Once a palette and card treatment exist, the layout gets bent to fit them. Deciding structure first means style serves the task rather than the task serving the style.
2. **Most "make it prettier" requests are layout complaints.** "This screen is cluttered" almost never means the colours are wrong; it means the information has no priority order. Restyling a screen with no hierarchy produces a prettier screen with no hierarchy.
3. **States are structural, not decorative.** Loading, empty, error and partial data change how much space a region needs. Discovering them after the visual pass means redoing the visual pass.

Shortcut allowance: when fixing a small, obvious defect in an existing component — a misaligned number, a missing focus ring, a wrong figure set — go straight to it. The stages exist for screens, not for one-line fixes.

---

## Stage 0 — Scope and the existing system

### Tasks

- [ ] Identify the target screen or component
- [ ] Detect the framework in use
- [ ] Locate existing design-token files (`tokens.md` has the search commands)
- [ ] Locate the existing typography system
- [ ] Review comparable screens in the same product
- [ ] Identify existing navigation, page shell, dialog, table and form patterns
- [ ] Determine mobile, tablet and desktop support
- [ ] Identify existing accessibility and testing infrastructure
- [ ] Decide whether the task is a component or a whole page

### Output

```text
Scope:
Technology:
Existing token system:
Existing typography:
Comparable screens:
Primary device:
Minimum supported width:
Area to change:
Area NOT to change:
```

The last line matters as much as the others. A design task without a stated boundary expands until it touches everything.

### Gate

Do not proceed until three things are known: **which** screen changes, **what user problem** it solves, and whether the existing visual system must be preserved.

---

## Stage 1 — User, task and decision

Complete these five sentences. They are not a formality; each one later removes a design argument.

```text
The primary user of this screen is __________.
The user comes here to __________.
The result they must reach before leaving is __________.
Their most frequent action is __________.
The most costly mistake or wrong decision is __________.
```

### Task table

```md
| Priority | User task | Frequency | Criticality | Success criterion |
|----------|-----------|-----------|-------------|-------------------|
| P0 | ... | daily | high | ... |
| P1 | ... | weekly | medium | ... |
| P2 | ... | rare | low | ... |
```

Also establish: what the user **compares**, whether they **scan / read / enter**, their expertise level, and the risk carried by late, missing or wrong data.

### One primary task per screen

A screen may support many functions but has exactly one primary task.

```text
❌ Display data · Filter · Edit · Report
✅ Find anomalous usage records and start investigating them
```

Filters, tables, metrics and actions are tools that serve the task. They are not the purpose of the screen. If the primary task needs two sentences joined by "and", the scope is two screens.

### Gate

**If the primary task cannot be written in one sentence, do not design a layout.**

If the answers cannot be inferred from the repository or the request, ask only the questions that genuinely block the design — and ask them together, in one message.

---

## Stage 2 — Content inventory and information priority

### Classify everything on the screen

| Class | What it is |
|-------|------------|
| Identity | Which record is this |
| Decision | The value the user came for |
| Supporting detail | Everything else that is occasionally needed |
| Status | What the system or the record is doing |
| Primary action | The one thing the screen exists to let them do |
| Secondary action | Supports the primary flow |
| Rare / destructive | Needed occasionally, expensive to undo |

### Inventory

```md
| Item | User value | Priority | Visible initially? | Notes |
|------|------------|----------|--------------------|-------|
| ... | ... | P0/P1/P2 | Yes/No | ... |
```

### Elimination questions

Ask all five of every item. One "no" is usually enough to move or drop it.

1. Which decision does this support?
2. Can the task still be completed without it?
3. Must it be visible **at all times**?
4. Could it live on a more appropriate detail surface?
5. Is the same message already said elsewhere?

Merging duplicates is the cheapest density win available: two chips saying the same filter, a count repeated in the header and the toolbar, a status shown as both a colour and a column.

### Gate

Do not start the wireframe while any initially-visible item has no stated decision it supports.

---

## Stage 3 — Task flow and friction

### Flow

```text
Entry
  → understand context
  → apply the necessary filter
  → scan the result
  → select a record
  → inspect the detail
  → decide / act
  → verify the result
```

Write the real one, not this one. Mark where the user **waits**, where they are **likely to err**, and where they must **not lose context**.

### Friction log

```md
| Step | Friction | Impact | Resolution |
|------|----------|--------|------------|
| ... | ... | low/medium/high | ... |
```

### Ease-of-use targets

- The primary task takes the fewest reasonable steps
- The most frequent control stays visible
- Rare controls do not crowd the primary flow
- Destructive actions do not sit beside the primary action
- The user never loses current context or applied filters
- System state is understandable without relying on colour
- Usable data already on screen does not disappear while new data loads

That last one has a specific implication: staleness is announced, never signalled by lowering contrast (`filters.md`).

### Gate

No wireframe until the primary task has a clear entry, an ordered action sequence and a completion state.

---

## Stage 4 — Rough layout

See `layout-and-information-architecture.md`. Return here afterwards.

---

## Stage 5 — Usability pass

The wireframe exists. Now check whether it actually makes the task easier, before any styling.

### Heuristic review

Answer all ten. A "no" is a layout revision, not a note for later.

1. Does the user know where they are?
2. Can they see which filters are active?
3. Do they know whether the system is loading, updating or in error?
4. Is the primary action clearly distinct from the others?
5. Can the user undo or correct an action?
6. Are wrong data and missing data distinguishable?
7. Do rare controls slow down the primary task?
8. Does important information disappear during scroll or narrowing?
9. Does the screen empty itself while the user waits?
10. Do error messages say what to do next?

### Also decide

- How many interactions the primary task costs, and whether that number can drop
- Whether defaults are safe **and** useful — a default that is merely safe still costs a step
- Shortcuts, saved views or bulk actions for repeated work
- Field order against the user's mental model (`forms.md`)
- Identity and decision column priority in tables (`tables.md`)
- The question each dashboard tile answers (`dashboards.md`)
- Auto-save versus explicit save, and how completion is acknowledged
- Focus order against visual order; touch-target size on touch devices

### Gate

If the wireframe does not visibly make the primary task easier, revise the layout. Do not proceed to styling to compensate.

---

## Stage 6 — Density, typography and direction

Apply `density-and-direction.md` and `typography.md` now that data volume and usage behaviour are known.

### Minimalism reduction order

When a screen feels cluttered, reduce in this order — and stop as soon as it reads:

1. Unnecessary content
2. Repeated controls
3. Unnecessary colour
4. Unnecessary emphasis
5. Unnecessary frames and separators
6. Decorative whitespace
7. Density token — only after all of the above

**Shrinking the text is not on this list.** It converts clutter into illegibility, and it is the most common wrong answer (`typography.md`, rule 8).

### Gate

Do not start implementation until the density choice is justified by data volume and usage behaviour, in one sentence.

---

## Stage 7 — Implementation TODO

Mandatory before writing code. The list always exists; where it lives depends on size.

| Work items | Artefact |
|-----------|----------|
| **5 or more** | Fill in `templates/design-todo.md` — the run needs a place to record decisions and progress across many steps |
| **Fewer than 5** | An inline list in the response is enough |

The **discipline is identical** in both cases: dependency order, one verifiable result per item, an acceptance criterion on each, validate before moving on. Only the artefact changes. A short list is not permission to skip the criteria — it is permission to skip the file.

Reworking one existing screen usually lands under the threshold; building a surface from scratch usually lands over it. Count the items before deciding, not after.

### Rules

- Every item produces **one verifiable result**
- Order by dependency; structural work precedes visual work
- State and accessibility work is not postponed to the end
- Name the file or component in the item
- Split large items
- No vague items ("fix the UI", "polish", "improve UX")
- Every item carries an acceptance criterion
- Validate the current item before starting the next

### Mandatory order

```md
### 1. Structure and semantics
- [ ] Create semantic page regions
- [ ] Place title, context, primary action, main data surface
- [ ] Validate DOM order against mobile reading order

### 2. Primary user flow
- [ ] Make the primary action work
- [ ] Implement the minimum interactions the primary task needs
- [ ] Separate secondary and rare actions

### 3. Data and state model
- [ ] Loading state
- [ ] First-use empty state
- [ ] Filtered no-results state (separate component)
- [ ] Error and retry flow
- [ ] Partial and stale-data states

### 4. Responsive layout
- [ ] Desktop layout
- [ ] Tablet breakpoint
- [ ] 320px narrowing strategy
- [ ] Validate the sticky / fold / hide / horizontal-scroll decision

### 5. Density and typography
- [ ] Connect density tokens
- [ ] Apply the existing font system, or the Inter Variable fallback
- [ ] Align numeric cells
- [ ] Apply weight and type-scale tokens

### 6. Visual system
- [ ] Connect existing colour and spacing tokens
- [ ] One separator system
- [ ] hover / focus-visible / selected / disabled / readonly
- [ ] Remove unnecessary decoration

### 7. Accessibility
- [ ] Semantic elements
- [ ] Keyboard access
- [ ] Focus order
- [ ] Accessible names and ARIA relationships
- [ ] Colour is not the only indicator
- [ ] Contrast

### 8. Verification
- [ ] 320 / 768 / 1440 screenshots
- [ ] Loading / empty / error screenshots
- [ ] Keyboard flow
- [ ] Overflow and long content
- [ ] Realistic dense data
```

---

## Stage 8 — Execute the TODO step by step

### Loop, per item

```text
1. Read the relevant existing files
2. Restate the acceptance criterion
3. Apply the smallest scoped change
4. Run lint / type-check / tests
5. Validate the visual or behavioural result
6. Mark the item complete
7. Record the decision and any deviation, briefly
8. Move on
```

### Prohibited

- Combining many unrelated design changes into one step
- Rewriting a component before reading it
- Adding a UI or grid library that was not requested
- Breaking working behaviour to simplify appearance
- Hiding a state-management problem with CSS
- Rendering missing data as zero
- Postponing mobile behaviour to the end
- Treating accessibility as final polish
- Marking an item complete before validating it

### Progress report

```text
Completed: 3.2 — Filtered no-results state
Changed files:
  ~ src/components/ResultTable.*
  + src/components/NoFilterResults.*

Decision:
  Separated first use from filtered no-results.

Validation:
  ✅ Applied filters stay visible
  ✅ Clear-filters action works
  ✅ Keyboard reachable

Next: 3.3 — Error and retry flow
```

---

## Approval policy

Do **not** ask the user to decide every micro-detail. Ask only when the answer materially changes the result:

| Ask | Decide yourself |
|-----|-----------------|
| Primary user or task unknown | Spacing details, token names |
| Two layouts produce meaningfully different workflows | Hover and focus treatment |
| Existing brand system vs new typography | Skeleton treatment |
| Destructive-action behaviour unclear | Semantic element choice |
| Mobile support unknown and it changes the architecture | Non-colour status indicators |
| Expensive-to-reverse information-architecture decision | Responsive implementation details |

For a large task, present **one** approval gate with everything in it:

```text
Primary task:
Proposed user flow:
Rough layout:
Main usability decisions:
Expensive-to-reverse assumptions:
```

After approval, build the TODO list and continue. If the user has already said "apply it" or "continue", do not stop for micro-approvals.

---

## Worked example — 400-record usage screen

Request: *"Make the usage screen with 400 records more minimal and easier to use."*

### 1 · Task

```text
Primary user: Operations specialist
Primary task: Find anomalous usage records and start investigating them
Behaviour:    Scanning and row comparison, several times a day
Data volume:  400+ records, worst case ~2,000
Device:       Desktop primary, occasional tablet
Costly error: Treating a missing reading as zero and approving it
```

### 2 · Information priority

```text
P0  Account, period, usage, deviation, data status
P1  Source, rate, last reading
P2  Technical identifiers, metadata
```

Deviation was promoted to P0 during Stage 2: it is the value the user actually scans for, and it was previously buried among detail columns.

### 3 · Flow and friction

```md
| Step | Friction | Impact | Resolution |
|------|----------|--------|------------|
| Apply filter | Full-page reload empties the table | high | Keep previous result, announce staleness |
| Scan for anomalies | Deviation column reads like every other column | high | Promote to decision column; mark anomalous cells |
| Open a record | Modal loses filter context | medium | Side panel, filters stay applied |
```

### 4 · Layout

```text
Title · last updated · export
Search · frequent filters · advanced filters [3]
Applied filters · result count
Anomaly summary (one line, not a tile row)
Dense data table
Selection summary · bulk actions
```

### 5 · Usability decisions

```text
- Frequent filters stay visible; advanced ones move into a panel
- Deviation becomes the decision column, visually distinct
- Technical identifiers leave the default view, reachable in detail
- Identity column sticky under horizontal scroll
- Rows fold into cards below 560px
- Previous results stay on screen while new ones load
```

### 6 · TODO (abbreviated)

```text
[x] 1.1 Page regions and semantics
[x] 2.1 Filter controls separated from result summary
[x] 3.1 Loading / empty / no-results / error states
[ ] 4.1 320px fold strategy
[ ] 5.1 Dense tokens connected
[ ] 7.1 Keyboard and contrast validation
```

### 7 · What "more minimal" turned out to mean

Not smaller type. The screen lost: three repeated counts, two decorative tile rows, per-category chip colours, and a second separator system. Row height went **down** one density level only after all of that — and the table gained a column (deviation) rather than losing one.

---

## Output template

```text
User
  Role: ...
  Primary task: ...
  Success criterion: ...

UX decision
  Main flow: ...
  Removed friction:
    - ...

Layout
  Main regions: 1. ... 2. ... 3. ...
  Narrow-screen strategy: ...

Visual system
  Density: ... · Direction: ... · Typography: ...
  Numbers: tabular + right-aligned

TODO summary
  ✅ N completed · ⚠️ N validations pending · ❌ N blocking gaps

Changed files
  ~ ... / + ...

Validation
  ✅ ... / ⚠️ ...

Remaining risks
  - ...
```

## Verification

- [ ] Primary task written in one sentence
- [ ] Information priority documented, every visible item justified
- [ ] Flow and friction evaluated
- [ ] Wireframe produced and approved before styling
- [ ] Usability pass completed against the ten heuristics
- [ ] Density justified by data volume and behaviour
- [ ] TODO list created, dependency-ordered, every item with an acceptance criterion
- [ ] Items executed and validated one at a time
- [ ] Decisions and deviations recorded
