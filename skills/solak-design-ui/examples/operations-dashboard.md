# Operations dashboard

A worked example of a `screen-redesign` starting from "make us a dashboard", which carries no task and has to be converted into one before anything is drawn.

## Surface contract

- **Surface:** service operations overview, this week
- **Primary user:** duty operations lead, checked at shift start and after every alert
- **Primary task:** decide what needs attention right now, and hand over cleanly at shift end
- **Success condition:** the lead can name the one thing that needs action, or confirm there is none
- **Main decision:** is anything degrading, and is it degrading fast enough to act on
- **Data volume:** 9 tiles, 5-minute aggregation, 7-day window
- **Data freshness:** delayed 5 minutes; one source is hourly and lags further
- **Costly mistake:** believing a flat line that is actually a stalled feed
- **Primary device and input:** desktop wallboard and laptop; not a phone surface, but must not break on one
- **Supported minimum width:** 320px
- **Loading behaviour:** tile-shaped skeletons, no shift
- **Empty behaviour:** per tile, with the reason
- **Error behaviour:** inside the tile; one failed source does not blank the page
- **Responsive strategy:** bento collapses by priority, reading order preserved
- **Accessibility risks:** status colour, chart text below the size floor
- **Out of scope:** the alerting configuration, per-service drill-downs

## Converting "modern" into a decision

The request named a style and no task. Four questions, asked once: who looks at this, what they do next, what a wrong read costs, and how fresh the numbers are. The answers turned a wallboard into a **handover surface** — and that changed the layout more than any style choice would have.

The decision line sits at the top, above the tiles, in words:

```text
Two services degrading · error rate up 3.2× on checkout since 09:40
```

A dashboard that makes the viewer assemble the conclusion from nine tiles has moved the work rather than done it.

## Each tile answers one question

| Tile | Question | Size |
|------|----------|------|
| Error rate | Is anything failing more than usual? | 2×2 |
| Latency p95 | Is it slow enough for users to notice? | 2×1 |
| Throughput | Is traffic itself abnormal? | 1×1 |
| Queue depth | Is work piling up faster than it drains? | 2×1 |
| Failed jobs | What needs a human? | 1×2 |
| Feed freshness | Can I trust the tiles above? | 1×1 |
| Deploys today | Did we cause this? | 1×1 |
| On-call | Who acts? | 1×1 |
| Budget burn | Anything to escalate at handover? | 1×1 |

A tenth tile — "requests per region" — was cut. It was interesting and answered no question anyone acts on.

**Importance drives size.** Error rate is 2×2 because it is the primary decision; nine equal cards would have made it one of nine.

## Freshness is a tile, not a footnote

The "can I trust this" tile exists because the costly mistake is a flat line that is really a stalled feed:

```text
Feed freshness
  Metrics    Delayed 5 min   ✓
  Billing    Updated 11:02   ⚠ 58 min behind
  Deploys    Live            ✓
```

No tile is labelled "live" unless it is. Every other tile carries its own last-updated time in the corner.

## Missing is not zero

A tile with no data keeps its structure and states the reason — "No data · billing feed stalled since 11:02" — rather than rendering `0`. Zero throughput and absent throughput lead to opposite actions, and a dashboard that cannot tell them apart is worse than no dashboard.

## Status without relying on colour

Every threshold state carries a glyph and a word alongside the colour. Verified with a greyscale screenshot: with colour removed, the hierarchy still reads and the good/bad judgement survives. Direction arrows sit beside deltas, because "up" is good on throughput and bad on error rate — the colour alone was ambiguous even in colour.

## Responsive

Bento composition, driven by a **container** query on the main region because the bento's width depends on whether the navigation is beside it: a 1024px viewport gives 756px with the rail open and 988px without.

| Container width | Composition | Why |
|-----------------|-------------|-----|
| ≥ 52rem | 4 columns | Measured comfortable width for the 2×2 tile |
| < 52rem | 2 columns, wide tiles span both | 4 columns gave each tile ~170px and context lines wrapped to three lines |
| < 30rem | 1 column | Two columns put the metric and its unit on separate lines |

Reading order is preserved when it stacks: decision first, trust second, detail last. A grid that reflows into a different priority order is a different dashboard.

Chart SVGs get `min-inline-size: 420px` inside a scroll container — below that the axis ticks fall under 12px, and SVG text does not obey the page's minimum size.

## Rejected alternative

**A single combined health score, 0-100.** It fits the wallboard beautifully and was rejected: the lead's next action depends on *which* thing is degrading, and a composite number deletes exactly that. It also degrades gracefully in the wrong direction — a stalled feed and a healthy system both produce a stable score.

## Validation

- ✅ Primary decision stated in one sentence, in words, above the tiles
- ✅ Every tile has a question; one tile removed for not having one
- ✅ Freshness visible per tile; nothing cached is labelled live
- ✅ Missing data shown as missing with a reason; never zero
- ✅ Greyscale pass: hierarchy and judgement survive without colour
- ✅ Container-query thresholds measured, not guessed · ✅ 320px verified
- ✅ Tile-level errors do not blank the dashboard
- ⚠️ Not tested on the actual wallboard hardware, which is 4K at a distance — type sizes are reasoned for a laptop

## Remaining risks

- No handover has actually been performed against this layout; the "what needs attention" framing is inferred from the interview, not observed
- The 5-minute delay is stated but the aggregation window is not visualised; a spike shorter than the window is invisible and nothing on screen says so
- Budget burn is the least-used tile and is present mostly because it was asked for — a candidate for removal after a month of use
