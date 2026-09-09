# FloodSafe Pakistan — Methodology

This document explains how a risk score is calculated and what the model
does and does not claim. It exists because "why does 120mm become a
boundary" needs to be an answerable question, not an assumption.

## Scope

FloodSafe Pakistan's *architecture* is designed to generalize to any
Pakistani location given coordinates, elevation, and a regional rainfall
threshold. For V1, only Sindh locations are validated and scored. Cities
outside Sindh (Lahore, Islamabad, Peshawar, Quetta, and others - see
`MAP_ONLY_CITIES` in `risk_check.py`) are shown on the map for national
context only and explicitly refuse a risk score.

This tool does not predict floods. It estimates relative risk for a
rainfall total the user provides — either typed in manually (scenario
mode) or pulled from an OpenWeatherMap forecast (forecast mode). It does
not use live/current weather as an input to the score, does not model
river bund failures (Indus/Jhelum/Chenab) or Glacial Lake Outburst Floods,
and should not be presented as an authoritative forecast.

## Rainfall time window: 72 hours

Every rainfall figure this app scores — scenario or forecast — represents
a **72-hour total**, not a single day. This matters and used to be
undefined: forecast mode always summed a 72-hour window, but scenario
mode's input field never stated a duration, meaning identical-looking
numbers from the two modes weren't necessarily comparable. Both modes now
mean the same thing. (Action item for the UI: scenario mode's rainfall
label should read "Rainfall over the next 72 hours (mm)" to make this
explicit to the user, not just to the code.)

## The risk score

```
total_score (0-100) = rainfall_component (0-54, saturating)
                     + elevation_component (0-30)

score_0_1 = total_score / 100

Low Risk:       0.00 - 0.25
Moderate Risk:  0.25 - 0.50
High Risk:      0.50 - 0.75
Very High Risk: 0.75 - 1.00
```

Because the rainfall component saturates at ~54 rather than 70, the true
achievable ceiling on `total_score` is **~84/100, not 100**. Very High
Risk (0.75-1.00) is reachable but only near the low end of that range.
This is a real trade-off of the current design, not a bug — a
non-linear-tail alternative that reclaims the full 0-100 range is a
documented option if the compressed ceiling turns out to matter.

Classification always happens on the **unrounded** `score_0_1` value,
before any display rounding. An earlier bug rounded `score_0_1` to 2
decimals before classifying it, which could erase a real, small excess
past a tier boundary (e.g. 0.254 rounding to 0.25, incorrectly satisfying
the "≤ 0.25 Low Risk" branch). Display rounding now happens strictly
after classification — see `_compute_risk_core()` in `risk_check.py`.

### Rainfall component (0 to ~54 points)

Each of Sindh's regional profiles (Mega-Urban & Coastal, Central
Agricultural Plains, Arid Plains & Deserts) has a `low_max` and
`medium_max` rainfall threshold in millimeters. Rainfall is scaled into
points in three bands, aligned to the classification boundaries above:

- **`rainfall_mm ≤ low_max`** — scales linearly from 0 to 25 points.
- **`low_max < rainfall_mm ≤ medium_max`** — scales linearly from 25 to
  50 points.
- **`rainfall_mm > medium_max`** — scales from 50 toward a ceiling of 54,
  saturating as rainfall approaches **2× `medium_max`**. This is the
  deliberate "dead zone": crossing `medium_max` does not, by itself, push
  the rainfall component's contribution much past 50 — see below.

(See `rainfall_component()` in `risk_check.py` for the exact piecewise
scaling.)

**Sourcing.** Pakistan's Flood Forecasting Division (FFD, under PMD
Lahore) publishes an official 24-hour rainfall intensity classification:
Light ≤10mm, Moderate 10.1–30mm, Heavy 30.1–70mm, Very Heavy 70.1–150mm,
Extremely Heavy >150mm (ffd.pmd.gov.pk/bulletin). This app's tier
categories are anchored to that scale as follows:

- **Low/Moderate boundary** ≈ FFD's Light + Moderate rain (up to 30mm/24h)
- **Moderate/High territory** ≈ FFD's Heavy rain (30.1–70mm/24h)
- **High/Very High territory** begins near where FFD's Very Heavy category
  begins (>70mm/24h)

Because this app scores 72-hour totals, not 24-hour totals, those FFD
boundaries are scaled up using a depth-duration relationship: the
rainfall depth needed to represent a given intensity grows sub-linearly
with duration, approximated here as `scale = sqrt(72/24) ≈ 1.73`. This is
a standard simplification of depth-duration-frequency (DDF) behavior, not
a DDF curve fitted to actual Sindh gauge data — that would require a
historical rainfall dataset this project doesn't have access to for V1.
Treat the scaling as a defensible starting point, not a validated curve.

Applying that scale to FFD's 30mm / 70mm boundaries gives a baseline of
**low_max ≈ 52mm, medium_max ≈ 121mm** for a 72-hour window, which this
project rounds to **50mm / 120mm** for `central_plains` (treated as the
baseline "typical" terrain).

**Terrain adjustment.** The other two regions' thresholds are lower
(Mega-Urban & Coastal) or higher (Arid Plains & Deserts) than that
baseline, on the reasoning that dense urban drainage systems back up at
lower rainfall totals than open agricultural land, while dry, hard-packed
desert soil can absorb more rainfall before flooding becomes likely.
**This part is still developer judgment, not independently sourced** —
the adjustment preserves the same proportional spread the project used
before this revision (Mega-Urban & Coastal roughly 20% below baseline,
Arid Plains & Deserts roughly 40-17% above it depending on the
threshold), rebased onto the FFD-anchored baseline instead of floating
free of any reference point. A genuine terrain-specific justification
(e.g., documented urban drainage capacity for Karachi) would be a
stronger source than this and is a reasonable post-V1 improvement.

| Region | low_max (72h) | medium_max (72h) |
|---|---|---|
| Mega-Urban & Coastal | 40mm | 100mm |
| Central Agricultural Plains (baseline) | 50mm | 120mm |
| Arid Plains & Deserts | 70mm | 140mm |

### Worked example: Karachi, 25mm forecast over 72 hours

- `low_max` for Mega-Urban & Coastal = 40mm. 25mm ≤ 40mm, so:
  `rainfall_points = 25 × (25 / 40) = 15.6`
- Assuming Karachi is the lowest-elevation city in its region, it gets
  the full 30 elevation points: `elevation_points = 30.0`
- `total_score = 15.6 + 30.0 = 45.6` → `score_0_1 = 0.456` →
  **Moderate Risk** (0.25 - 0.50 range)

### The "dead zone" past `medium_max`

Once rainfall exceeds a region's `medium_max`, the rainfall component
does not jump straight to its 54-point ceiling — it ramps up gradually,
reaching full saturation only once rainfall reaches **2× `medium_max`**.
For `central_plains` (`medium_max = 120mm`), that means rainfall between
120mm and 240mm all maps to rainfall points somewhere between 50 and 54 —
a genuine, deliberate flattening near the top of the scale, not a bug.

This is a real design trade-off, not a validated finding: the saturation
distance (100% of `medium_max`) is a somewhat arbitrary choice, not
independently sourced, and directly caps how much the rainfall component
alone can push a city toward Very High Risk. `test_risk_scoring.py`'s
dead-zone test locks in the current 100%-of-`medium_max` saturation
distance; if that distance is ever narrowed (e.g. to make the tail more
responsive to extreme rainfall), this section and that test both need to
be updated together — the two must never drift apart again.

### Elevation component (0-30 points)

Elevation data comes from Open-Elevation, with OpenTopoData as a
fallback, fetched per-city by `get_elevation.py` and stored in
`city_elevation.csv`. A city's elevation is scored **relative to other
cities in its own regional profile** - not on one national scale -
because low elevation means something different in coastal terrain
than it does inland. The lowest-elevation city in a region scores the
full 30 points; the highest scores 0.

- **Limitation:** this rewards relative position within a small set of
  cities (4-20 per region), not an absolute flood-risk elevation
  threshold from a hydrological study. It is a reasonable first-pass
  signal, not a validated flood model.
- If elevation data is unavailable for a city, elevation_component
  returns 0 and the result explicitly tells the user the score is
  rainfall-only for that city - never silently substituted.

## What's explicitly NOT modeled in V1

- Land-use / land-cover
- Drainage infrastructure or proximity to water bodies
- Historical flood exposure as a live model input
- River bund failure risk (Indus, Jhelum, Chenab)
- Glacial Lake Outburst Floods (GLOFs)
- Soil saturation / antecedent conditions (multiple back-to-back storms
  are not distinguished from one 72-hour event with the same total)

## Known data-quality caveats

- Some cities' elevation values were fetched from a fallback source
  (OpenTopoData) rather than the primary source (Open-Elevation) due to
  transient network errors during data collection - both sources use
  broadly comparable satellite-derived elevation models (SRTM-based),
  but this is worth disclosing, not hiding.
- The "Mountainous & Rugged Terrain" profile was removed after review -
  its only three members (Gwadar, Pasni, Turbat) are in Balochistan, not
  Sindh, and were the wrong scope for a Sindh-focused V1.
- Terrain-adjustment ratios between regions (see above) are carried
  forward from an earlier, unsourced version of this project and have
  not themselves been independently validated — only the baseline they're
  now applied to has a citable source.

## Validation status

"Validated" in this document means the thresholds are anchored to an
official Pakistani rainfall classification (FFD) via a stated, simplified
scaling method, and the scoring code has automated tests covering
Low/Moderate/High/Very High classification, elevation edge cases, and
forecast aggregation (`test_risk_scoring.py`, 15/15 passing). It does
**not** mean this model has been tested against historical flood outcomes
in Sindh — that is explicitly a post-V1 item (comparing model output
against 2-3 documented real flood events, including cases where the
model would be wrong).

## Open items

- Terrain-adjustment ratios between regions are still developer judgment,
  not independently sourced — a real improvement target post-V1.
- Update the scenario-mode rainfall input label to say "72 hours"
  explicitly, matching forecast mode.
- Whether to narrow the dead-zone saturation distance (currently 100% of
  `medium_max`) is an open design decision, not yet made — see "The dead
  zone" section above. If changed, it must be changed in code and this
  doc together, with `test_risk_scoring.py` updated to match.
- Historical validation against real flood events (post-V1, per roadmap).