# The Token Layer

A token layer means no component holds a colour, measurement or duration of its own. Density (`density-and-direction.md`) and the column grid (`grid.md`) are part of this layer too — not component decisions.

## Look for an existing layer first

**Standing up a parallel system is worse than using no tokens at all.** With two systems, both rot. Search before writing:

```bash
rg -l "^\s*--[a-z-]+:" --type css --type scss -g '!node_modules'   # CSS custom property definitions
rg -l "tailwind.config|theme\s*:|createTheme|defineTheme"           # JS/TS theme object
fd -g "*variables*.{css,scss,sass}" -g "*tokens*" -E node_modules   # named token files
fd -g "_variables.scss" -g "*.theme.*" -E node_modules              # framework theme files
```

If you find one:
- **Read it and extract the naming scheme** (`--color-*`, `$brand-*`, `theme.palette.*` — which is it?)
- Add missing tokens **into that scheme**; do not start a new name family
- Map by **role, not value**: if `--bg-elevated` exists, do not write `--surface-card`, use theirs
- If the layer is genuinely insufficient (e.g. no semantic status colours), add what is missing and say so in the report

If you find none, write the layer below.

## Name by role, not by value

```css
--surface-card: …      /* ✅ says where it is used */
--gray-100: …          /* ❌ says what it is; becomes a lie when the theme changes */
--ink-muted: …         /* ✅ */
--text-gray-500: …     /* ❌ not gray-500 in dark theme */
```

A value-named token loses its meaning in dark theme: `--gray-100` is a surface in light and text in dark. A role name stays true in both.

## The layer: nine groups

The set below was verified by screenshot in both themes. Values are `oklch` because the first number is lightness read directly, which makes contrast reasoning possible by eye.

```css
:root {
  color-scheme: light dark;

  /* 1 · Surfaces — three levels is enough: page, card, sunken */
  --surface-page:   oklch(97.5% 0.003 250);
  --surface-card:   oklch(100% 0 0);
  --surface-sunken: oklch(95.5% 0.004 250);
  --surface-field:  oklch(100% 0 0);

  /* 2 · Ink — three levels: strong, body, muted. Note the ratio beside each. */
  --ink-strong:   oklch(21% 0.012 260);   /* 14.6:1 on card */
  --ink-body:     oklch(34% 0.010 260);   /* 9.4:1 */
  --ink-muted:    oklch(46% 0.010 260);   /* 5.6:1 — above the 4.5 floor, not at it */
  --ink-onaccent: oklch(99% 0 0);

  /* 3 · Lines — two levels: divider and border */
  --line:        oklch(88% 0.005 260);
  --line-strong: oklch(72% 0.008 260);

  /* 4 · Accent — ONE functional accent. A second one splits the hierarchy. */
  --accent:       oklch(46% 0.14 252);
  --accent-hover: oklch(39% 0.14 252);
  --accent-quiet: oklch(95% 0.03 252);
  --focus-ring:   oklch(52% 0.17 252);

  /* 5 · Semantic status — each paired with an icon or text; colour is never the only cue */
  --danger:  oklch(45% 0.17 27);   --danger-quiet:  oklch(96% 0.03 27);
  --success: oklch(43% 0.11 155);  --success-quiet: oklch(96% 0.03 155);
  --warn:    oklch(48% 0.11 75);   --warn-quiet:    oklch(96% 0.04 75);

  /* 6 · Typography — one family, ROLE-named steps, closed weight set (`typography.md`).
     Names say what the step is FOR: `--text-caption` survives a redesign,
     `--text-small` becomes a lie the first time the scale shifts. */
  --font-ui: "Inter Variable", "Inter var", Inter,
             ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-mono: ui-monospace, "SFMono-Regular", "Cascadia Mono", Consolas, monospace;  /* technical identifiers only */

  --text-caption:   0.75rem;    /* 12px — hints, metadata, column headers */
  --text-data:      0.8125rem;  /* 13px — table cells, compact values */
  --text-body:      0.875rem;   /* 14px — descriptions, help text */
  --text-section:   1rem;       /* 16px — section headings */
  --text-title:     1.25rem;    /* 20px — page title */
  --text-metric-sm: 1.5rem;     /* 24px — KPI, small tile */
  --text-metric-lg: 2rem;       /* 32px — KPI, primary tile */

  --leading-tight:   1.2;
  --leading-label:   1.3;
  --leading-data:    1.35;
  --leading-body:    1.45;
  --leading-reading: 1.6;

  --weight-body:   400;  /* floor: never below 400 in a dense surface */
  --weight-label:  500;
  --weight-strong: 600;  /* the only emphasis step — a closed set, see typography.md */

  /* 7 · Density — vertical rhythm (`density-and-direction.md`) */
  --field-height: 36px;
  --field-pad-x:  10px;
  --space-field:  16px;
  --space-group:  40px;   /* ~2.5x field spacing */
  --space-card:   clamp(20px, 2vw, 32px);

  /* 8 · Grid — horizontal rhythm (`grid.md`) */
  --grid-cols:   12;
  --grid-gutter: 20px;
  --content-max: 76ch;

  /* 9 · Shape and motion */
  --radius: 5px;  --radius-sm: 3px;
  --duration: 120ms;
  --ease: cubic-bezier(0.2, 0, 0.2, 1);
}
```

Count discipline: three surfaces, three inks, two lines, one accent, one radius pair. Before adding a fifth grey, say which of the existing four is failing to do its job.

Note what is **absent** on purpose: there is no shadow token. Static surfaces are separated by borders; elevation is added only where something genuinely floats, and then one level suffices (`design-quality.md`).

## Density and theme are inherited in the same layer

Density moves the **surface** type step, not the whole scale: the role tokens above stay fixed, and a surface-level pair selects which of them a table cell or field label uses.

```css
:root {                        /* compact — the default */
  --surface-text-size:   var(--text-body);      /* 14px */
  --surface-label-size:  var(--text-caption);   /* 12px */
  --surface-line-height: 1.4;
}
[data-density="comfortable"] { --field-height: 44px; --field-pad-x: 14px;
                               --surface-text-size: 0.9375rem;          /* 15px */
                               --surface-label-size: var(--text-data);  /* 13px */
                               --surface-line-height: var(--leading-body);
                               --space-field: 20px; --space-group: 48px; --grid-gutter: 24px; }
[data-density="dense"]       { --field-height: 28px; --field-pad-x: 8px;
                               --surface-text-size: var(--text-data);      /* 13px */
                               --surface-label-size: var(--text-caption);  /* 12px */
                               --surface-line-height: var(--leading-data);
                               --space-field: 12px; --space-group: 32px; --grid-gutter: 12px; }
```

A component reads `--field-height`; it does not know which density it is in. Adding a density level should require no component changes — if it does, the token layer has leaked.

## Dark theme is not an inversion

```css
@media (prefers-color-scheme: dark) {
  :root {
    --surface-page:   oklch(19% 0.012 260);
    --surface-card:   oklch(24% 0.013 260);   /* card is HIGHER than page */
    --surface-sunken: oklch(21% 0.012 260);
    --surface-field:  oklch(27.5% 0.014 260); /* input is the highest surface */

    --ink-strong: oklch(97% 0.004 260);
    --ink-body:   oklch(88% 0.005 260);
    --ink-muted:  oklch(72% 0.008 260);

    --accent:       oklch(72% 0.13 252);      /* chroma down, lightness up */
    --ink-onaccent: oklch(18% 0.02 260);      /* ink on accent flips too */
  }
}
```

Three rules:

1. **Invert lightness, lower chroma.** The same chroma vibrates on a dark ground and fringes at the edges.
2. **Elevation order is preserved but values are re-picked** — in light theme the card is *whiter* than the page; in dark theme it is *lighter* than the page.
3. **Ink on the accent is theme-dependent too.** If `--ink-onaccent` stays white, it becomes unreadable on a light accent in dark theme.

In dark theme, surface lightness compresses into the 19-27.5% range: **carrying meaning by brightness alone stops working there.** Distinctions such as `readonly` vs `disabled` must be supported by a colour-independent cue (dashed border, lock icon) — see `forms.md`.

If a user preference exists, do not make the media query the only source:

```css
:root[data-theme="dark"]  { /* dark values */ }
:root[data-theme="light"] { /* light values */ }
```

## What is not a token

- A measurement used once in one component — leave it there
- Colour that comes from content (chart series palette → `design-quality.md`, derived from the semantic colours)
- A composition measurement specific to one surface (one tile's span)

Making every number a token turns the layer into an unreadable dictionary. The test: **if the same decision has to be made in two different places, it is a token.**

## One rule that belongs in the base layer

Not a token, but it lives in the same file and nowhere else works as well:

```css
[hidden] { display: none !important; }
```

`hidden` applies `display: none` from the UA stylesheet, so any component with its own `display` rule stays visible while marked hidden — a state component then renders as an empty strip in its success state. One line here closes the whole class of bug. The full account is in `interaction-and-states.md` §20.

## Verification

```bash
# hardcoded values left in components
rg -n "#[0-9a-fA-F]{3,8}|rgba?\(|oklch\(" src/components -g '!*tokens*'
rg -n ":\s*\d+px" src/components -g '!*tokens*'
rg -n "font-weight: [0-9]" src/components          # weight drift (450/550/650)
rg -n "tabular-nums(?!\s+lining)" src -P           # figure set applied by half
rg -n "^\s*\[hidden\]" src/styles                  # the base-layer rule above — present?
```

- [ ] No palette, spacing or type constants in component files; everything via `var(--…)`
- [ ] Token names are role-based (`--surface-card`), not value-based (`--gray-100`)
- [ ] Contrast ratios noted beside ink tokens, all ≥ 4.5:1
- [ ] One functional accent; semantic status colours separate from it
- [ ] Density and grid tokens at the root, not in components
- [ ] Dark theme values chosen individually — not an inversion — including `--ink-onaccent`
- [ ] If a token layer already existed, **it** was used and no second system was created
