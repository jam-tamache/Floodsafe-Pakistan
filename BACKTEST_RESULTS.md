# FloodSafe Pakistan: Back-test Results

## Verdict

**The model FAILS its own pre-registered pass/fail rule.**

- Criterion (a), miss rate: **PASS** (0 of 5 floods missed).
- Criterion (b), false-alarm rate: **FAIL** (3 of 3 non-flood cases triggered an alert; the rule requires no more than half).

The model also does not beat the simple rainfall baseline (see below). The terrain and elevation design has not demonstrated added value on this test set.

## Method

- Protocol: `BACKTEST_PROTOCOL.md`, committed as `36e305e2fe6a52f71b03f85091d8a7e5ca28c021` on 24 Sep 2026 (commit message: "Add back-test protocol (draft)"). `git log --follow` shows this is the only commit touching the file, so it was not edited after commit.
- Alert threshold: Moderate Risk or higher (score > 25/100), as fixed in the protocol.
- Scored cases: 8 of 9. Jacobabad (28 Aug 2022) was skipped because no rainfall figure exists, only Sentinel-1 satellite confirmation of inundation.
- Code: `run_backtest.py`, cases in `backtest_cases.py`, case table in `CASE_TABLE_DRAFT.md`. Results were reproduced in the real repository and matched the earlier table exactly.

## Results

| Case | Type | Rain (mm) | Score | Outcome |
|---|---|---|---|---|
| Karachi, 24-27 Aug 2020 | Flood | 231.0 (PMD 24h reading, dated 28 Aug) | 84.0 Very High | Hit |
| Nawabshah/SBA, 23-25 Aug 2022 | Flood | 137 | 74.2 High | Hit |
| Hyderabad, 2-3 Aug 2026 | Flood | 89 | 45.4 Moderate | Hit (weakest) |
| Mirpurkhas, 2-3 Aug 2026 | Flood | 111 | 76.8 Very High | Hit |
| Umerkot, 2-3 Aug 2026 | Flood | 169 | 80.8 Very High | Hit |
| Karachi, 8-9 Aug 2020 | Non-flood | 47 | 57.9 High | False alarm |
| Mithi, 8-9 Aug 2020 | Non-flood | 56 | 32.6 Moderate | False alarm |
| Nawabshah/SBA, 14-15 Jul 2022 | Non-flood | 60 (unverified) | 52.2 High | False alarm |
| Jacobabad, 28 Aug 2022 | Flood | none | n/a | Skipped |

Totals (8 scored): 5 hits, 0 misses, 3 false alarms, 0 correct negatives.

- Miss rate: 0/5 = 0%.
- False-alarm rate: 3/3 = 100%.
- The pre-registered prediction "false alarms will outnumber misses" held (3 vs 0).

## Baseline comparison

Baseline (protocol section 7): alert if 72h rainfall is at least 50 mm, no terrain logic. Applied to the same 8 cases:

- Floods: 5 hits, 0 misses (all had 89-231 mm).
- Non-floods: 1 correct negative (Karachi, 47 mm), 2 false alarms (Mithi 56 mm, SBA 60 mm).

The baseline is at least as good as the model on every count and better on false alarms (2 vs 3 false alarms; 1 vs 0 correct negatives). The baseline's own false-alarm rate is 2/3, so it would also fail criterion (b). With only 3 non-flood cases, neither result is strong evidence.

## Deviations from the written protocol

1. Rainfall comes from official NDMA/PDMA/PMD documents, except the three Aug 2026 cases (Hyderabad, Mirpurkhas, Umerkot), which come from Dawn reporting (3 Aug 2026). It does not come from ERA5/Open-Meteo. This was forced by network limits in the working environment and decided before any model run, but it is still a deviation.
2. 9 cases in total against the required 10-12.
3. 3 non-flood cases against the required 5.
4. The `arid_plains_desert` group is **untested**. Its only case (Jacobabad) was skipped, and it was not filled with weak cases.
5. Karachi's 231.0 mm is PMD's 24-hour reading at Karachi-Faisal. PMD dates it 28 Aug 2020, one day after the case window (24-27 Aug). It is not a 72h total, and the true 72h total is unconfirmed. The case window was not changed after the results were seen. The rain score is at its ceiling (84.0, still a Hit), so this does not change the result.

## Limitations

- Very small sample. No percentage here is statistically meaningful.
- Documentation bias: well-documented floods (especially Karachi 2020) are easier to source than quiet non-flood days, which favors flood cases.
- The test uses observed rainfall, not forecasts, so it excludes forecast error. Real-world performance would be worse.
- One non-flood rainfall figure (SBA, 60 mm) is unverified.
- Git history proves the protocol existed on 24 Sep 2026. It cannot prove that no exploratory model run happened earlier.

## Known model issues (not fixed, deferred until after this back-test)

- Elevation is min-max scaled within each terrain group, so the highest city in a group always gets 0 elevation points.
- The Moderate Risk rainfall threshold varies about 4x between cities in the same region.
- 17 of 28 cities can never reach Very High Risk (maximum score about 84/100).

## Conclusion

FloodSafe catches floods but over-warns, and on this test it did not outperform a plain rainfall threshold. It should be described as "designed and calibrated for Sindh", not "validated".