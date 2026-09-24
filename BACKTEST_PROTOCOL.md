# FloodSafe Pakistan: Back-test Protocol

**Status:** Written and committed BEFORE any model run on any case. After the case list is frozen (section 5), this file is not edited. Results go in a separate file, `BACKTEST_RESULTS.md`.

## 1. Question

Does model-v1 raise an alert (Moderate Risk or higher) when urban/pluvial flooding was documented, and stay quiet when it was not?

## 2. Model under test

- Git tag `model-v1` (commit `dc0a7ae`).
- The back-test script imports `_compute_risk_core()` from `risk_check.py` at that tag. No reimplementation of the scoring logic.
- Any model change after this point means the results no longer apply to v1.

## 3. Alert definition

Alert = `risk_level_key` is Moderate Risk, High Risk or Very High Risk (score above 25/100).

## 4. Input

- Input is the **72-hour rainfall total (mm)** for the city, over the window [T, T+72h].
- Observed rainfall source: ERA5 via Open-Meteo Historical API (`models=era5`), hourly precipitation at each city's coordinates from `city_coordinates.csv`, summed over 72h (72 hourly values from 00:00 UTC on the window start date). Fixed now; not to be changed after results are seen.
- Production feeds the model an OpenWeatherMap *forecast* for the same window. The back-test feeds it *observed* rainfall. So this test measures the scoring rule given correct rainfall. It does NOT measure forecast quality. Forecast error would make real-world performance worse.
- Known limitation: reanalysis products tend to underestimate extreme convective rainfall. ERA5 has a resolution of about 25 km, so each value is an area average over a grid cell, not a point measurement in the city.

## 5. Case selection (frozen before any model run)

- Cases are chosen by **documented outcome only**, never by model output.
- Rainfall data is pulled only AFTER the case list is frozen.

**Flood case:** waterlogging or urban flooding in the named city, documented in an NDMA/PDMA/PMD report or a named news outlet (e.g. Dawn, The News, Express Tribune, Reuters). Minimum: one source giving the city and date.

**Non-flood case:** a 72-hour window in the same city with no flooding found in the sources searched. The search performed is recorded per case. At least 2 non-flood windows must be ones where a rain event was reported (PMD advisory or news) but no flooding was reported for that city. Otherwise the test is too easy to pass.

**Size and coverage:**
- 10 to 12 cases total.
- At least 5 non-flood windows.
- All 3 terrain groups covered (mega_urban_coastal, central_plains, arid_plains_desert), at least 2 cases each.
- If a group has no documented flood event, that group is reported as "untested", not filled with weak cases.

**Excluded from scoring (listed separately in results, with model output shown but not counted):** riverine flooding, embankment or canal breaches, GLOF, hill torrents, and any event where the documented cause is not local rainfall.

### Case table (fill before any model run)

| # | City | Terrain group | Window start (T) | Outcome (flood / non-flood) | Source(s) and search performed |
|---|------|---------------|------------------|-----------------------------|--------------------------------|
|   |      |               |                  |                             |                                |

## 6. Metrics

- Per terrain group and pooled: counts of hits, misses, false alarms, correct negatives.
- Raw counts only. No percentages while n is under 20 per group.
- No tuning of thresholds or weights after seeing results.

## 7. Baseline

Baseline rule: alert if 72h rainfall is 50 mm or more, for every city, with no terrain component. Report every case where the model and the baseline disagree. If the model does not beat this baseline, the elevation and regional-threshold design adds nothing demonstrated.

## 8. Pre-registered prediction

False alarms will outnumber misses.

## 9. Pass/fail (declared before running)

The model **fails** if either holds:
- (a) it misses more than one third of in-scope flood cases (pooled), or
- (b) it alerts on more than half of the non-flood cases.

Otherwise the outcome is reported as "did not fail on this sample", NOT "validated".

## 10. Reporting rules

- Publish everything, including failures.
- No case is dropped after the model run. If rainfall data is unavailable for a case, it is reported as dropped with the reason.
- Allowed wording: "Back-tested on N documented cases; results: ...".
- Limitations to state: small n, reanalysis rainfall bias, documentation bias (news coverage favors Karachi), no forecast error included.
