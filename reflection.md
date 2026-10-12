# Tinker 3B — Reflection (Rank & Explain)

## Part 4: Filter Bubble Analysis

### 1. Evidence of a filter bubble in the scoring

Running `python ranking.py` with the default profile
(`max_noise="moderate"`, `max_distance=1.0`, `min_seats=4`) returns:

```
1. Innovation Commons -- Score: 4.5
2. Grand Reading Room -- Score: 4.5
3. Engineering Lounge -- Score: 4.5
```

**All three top spots tie at exactly 4.5.** This is not a coincidence — it is
the direct result of **binary all-or-nothing scoring**. Each factor awards
its full weight or zero:

| Factor | Rule | Weight |
|---|---|---|
| Noise | `≤ max_noise` → award, else zero | 2.0 |
| Distance | `≤ max_distance` → award, else zero | 1.5 |
| Seats | `≥ min_seats` → award, else zero | 1.0 |

**Consequence:** any spot that passes all three thresholds scores exactly
4.5, no matter how much better or worse it is on each axis. A tiny café
2 blocks away and a huge library 0.8 miles away produce identical scores
if both pass the same three binary checks. **The ranking cannot distinguish
them.**

### 2. The filter bubble

> **"My scoring weights favor 'passes-the-threshold' spots over 'excels on one
> dimension' spots. Any spot that just barely clears the bar (e.g., 'moderate'
> noise, 1.0 mile distance, 4 seats) looks identical to one that exceeds it
> dramatically — because the model only asks 'is it good enough?' rather than
> 'how good is it?'. Students whose preference is 'perfect on one axis, mediocre
> on the rest' are systematically under-served: their ideal spot never surfaces,
> not because it scored badly, but because the aggregate formula cannot express
> 'excellence on one dimension'."**

### 3. Who is under-served by this weighting?

**Students who prioritize one dimension heavily.**

Concrete examples:
- A student who works in silence and would walk 2 miles for a perfectly
  quiet spot — never sees a "quiet but far" location in the top-3, because
  distance gets vetoed.
- A student who needs 30 seats for a group session — never sees a "quiet,
  close, but only 15 seats" spot, because seats gets vetoed.

**The model assumes a single archetype of 'good spot'** (medium on everything)
and rewards it consistently. It doesn't allow users to trade off one factor
for another, which is exactly what filter bubbles look like in real
recommendation systems.

### 4. What would fix it (not implemented, just noted)

- **Partial credit** instead of binary: score noise as `2.0 * (1 - distance_from_threshold)`
- **Weighted profile** so users can express "distance matters 3× more than seats"
- **Pareto front** ranking instead of a single score

Documenting is the deliverable here; the fix is out of scope for this Tinker.