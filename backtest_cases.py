"""
Back-test case data for FloodSafe Pakistan (model tag: model-v1).

Each case is a real, dated, sourced event. `city` matches the exact lowercase
key used in risk_check.py's REGIONAL_PROFILES / normalize_city(), so a case
can be run straight through check_risk()/​_compute_risk_core() with no name
translation needed.

ERA5/Open-Meteo was the original plan (per BACKTEST_PROTOCOL.md) but is not
reachable from this environment (sandbox network blocks it; the web-fetch
tool refuses constructed API URLs). Rainfall figures below are the official
station readings already sourced from NDMA/PDMA/PMD documents instead —
less uniform than a single reanalysis product, but every number traces to
a named government document, which is arguably the stronger source for a
scholarship submission. See `source` on each case.

`rainfall_mm` is what should be fed into check_risk()/_compute_risk_core()
as the 72h input. Where the real 72h total isn't confirmed, `rainfall_mm`
is left as the best available official floor and `rainfall_caveat` explains
the gap — do not silently treat it as a true 72h total.
"""

FLOOD_CASES = [
    {
        "id": "karachi_aug2020",
        "city": "karachi",
        "profile_key": "mega_urban_coastal",
        "lat": 24.8546842,
        "lon": 67.0207055,
        "date_window": "2020-08-24 to 2020-08-27",
        "rainfall_mm": 231.0,
        "rainfall_caveat": (
            "231.0mm is PMD's official single-day record at Karachi-Faisal "
            "(24 Aug – 27 Aug spell), not a confirmed 72h total. True 72h "
            "total is unconfirmed and likely higher — Karachi-Faisal's full "
            "August total was 588.0mm. Treat 231.0mm as a floor, not a "
            "measured 72h figure."
        ),
        "actual_outcome": "flood",
        "impact": "41 deaths (final toll)",
        "source": (
            "PMD Pakistan Monthly Climate Summary, August 2020 "
            "(https://cdpc.pmd.gov.pk/Pakistan_Monthly_Climate_Summary_August_2020.pdf); "
            "Dawn, 28 Aug 2020 (https://www.dawn.com/news/1576798); "
            "cross-checked against Wikipedia 2020 Karachi floods summary"
        ),
    },
    {
        "id": "nawabshah_sba_aug2022",
        "city": "nawabshah",
        "profile_key": "central_plains",
        "lat": 26.2452915,
        "lon": 68.4040229,
        "date_window": "2022-08-23 to 2022-08-25",
        "rainfall_mm": 137.0,
        "rainfall_caveat": (
            "137.0mm is the SBA station reading for the 24-25 Aug 24h "
            "window (NDMA SITREP-073). Damage figures below are a snapshot "
            "as of 23-24 Aug — one day earlier, same ongoing flood spell "
            "(started 17 Aug), not the identical 24h window."
        ),
        "actual_outcome": "flood",
        "impact": "54,962 houses partially destroyed, 23,000 fully destroyed, 696 cattle lost (as of 23-24 Aug)",
        "source": (
            "NDMA Monsoon 2022 Daily SITREP No. 073, dated 25 Aug 2022 "
            "(https://www.ndma.gov.pk/storage/sitreps/August2022/0K4OF8fblju6B0XAjBr1.pdf); "
            "Tribune, 24 Aug 2022, quoting Sindh Information Minister Sharjeel Memon "
            "(https://tribune.com.pk/story/2372885/pmd-forecasts-heavy-rains-in-parts-of-three-provinces)"
        ),
    },
    {
        "id": "jacobabad_aug2022",
        "city": "jacobabad",
        "profile_key": "arid_plains_desert",
        "lat": 28.2813094,
        "lon": 68.4364361,
        "date_window": "2022-08-28",
        "rainfall_mm": None,
        "rainfall_caveat": (
            "No rain-gauge rainfall figure was found for this case — it is "
            "satellite-confirmed inundation (Sentinel-1 SAR), not a rainfall "
            "reading. Cannot be run through check_risk()'s rainfall-based "
            "scoring as-is; usable only if the back-test separately checks "
            "elevation/terrain logic, or if a rainfall figure is found later."
        ),
        "actual_outcome": "flood",
        "impact": "Flood extent confirmed via Sentinel-1 SAR imagery, ~28 Aug 2022",
        "source": (
            "Roth, F. et al., 'Sentinel-1-based analysis of the severe flood over "
            "Pakistan 2022', Nat. Hazards Earth Syst. Sci. 23, 3305-3325, 2023 "
            "(https://nhess.copernicus.org/articles/23/3305/2023/); "
            "'A framework for multi-sensor satellite data to evaluate crop "
            "production losses...', Nature Sci. Reports, 2023 "
            "(https://www.nature.com/articles/s41598-023-30347-y)"
        ),
    },
    {
        "id": "hyderabad_aug2026",
        "city": "hyderabad",
        "profile_key": "mega_urban_coastal",
        "lat": 25.4075358,
        "lon": 68.3613456,
        "date_window": "2026-08-02 to 2026-08-03",
        "rainfall_mm": 89.0,
        "rainfall_caveat": None,
        "actual_outcome": "flood",
        "impact": "Part of a multi-district event; 8 deaths province-wide (see nawabshah/umerkot entries for shared context)",
        "source": (
            "Dawn, 3 Aug 2026, 'Sindh CM Murad orders emergency steps as downpour "
            "wreaks havoc in several districts' (https://www.dawn.com/news/2020214) "
            "— verified against full article text, not a snippet"
        ),
    },
    {
        "id": "mirpurkhas_aug2026",
        "city": "mirpurkhas",
        "profile_key": "central_plains",
        "lat": 25.5263882,
        "lon": 69.0112387,
        "date_window": "2026-08-02 to 2026-08-03",
        "rainfall_mm": 111.0,
        "rainfall_caveat": None,
        "actual_outcome": "flood",
        "impact": "Part of the same multi-district event as hyderabad_aug2026/umerkot_aug2026",
        "source": "Dawn, 3 Aug 2026 (https://www.dawn.com/news/2020214)",
    },
    {
        "id": "umerkot_aug2026",
        "city": "umerkot",
        "profile_key": "arid_plains_desert",
        "lat": 25.3655302,
        "lon": 69.7401257,
        "date_window": "2026-08-02 to 2026-08-03",
        "rainfall_mm": 169.0,
        "rainfall_caveat": None,
        "actual_outcome": "flood",
        "impact": "Highest rainfall in Sindh this event; 1 death by drowning; part of the same multi-district event",
        "source": "Dawn, 3 Aug 2026 (https://www.dawn.com/news/2020214)",
    },
]

NON_FLOOD_CASES = [
    {
        "id": "karachi_aug2020_nonflood",
        "city": "karachi",
        "profile_key": "mega_urban_coastal",
        "lat": 24.8546842,
        "lon": 67.0207055,
        "date_window": "2020-08-08 to 2020-08-09",
        "rainfall_mm": 47.0,
        "rainfall_caveat": None,
        "actual_outcome": "no_flood",
        "impact": "No flood damage reported in this window (Sindh section notes 'few deaths and damages' province-wide, not tied to this specific reading)",
        "source": (
            "NDMA Monsoon 2020 Daily SITREP No. 045, dated 9 Aug 2020, "
            "PMD rainfall Annex B (https://www.ndma.gov.pk/storage/sitreps/September2020/9y0Bmj0Ri5QMx5zX05bM.pdf)"
        ),
    },
    {
        "id": "mithi_aug2020_nonflood",
        "city": "mithi",
        "profile_key": "arid_plains_desert",
        "lat": 24.736412,
        "lon": 69.7973419,
        "date_window": "2020-08-08 to 2020-08-09",
        "rainfall_mm": 56.0,
        "rainfall_caveat": None,
        "actual_outcome": "no_flood",
        "impact": "No flood damage reported in this window",
        "source": (
            "NDMA Monsoon 2020 Daily SITREP No. 045, dated 9 Aug 2020, "
            "PMD rainfall Annex B (https://www.ndma.gov.pk/storage/sitreps/September2020/9y0Bmj0Ri5QMx5zX05bM.pdf)"
        ),
    },
    {
        "id": "nawabshah_sba_jul2022_nonflood",
        "city": "nawabshah",
        "profile_key": "central_plains",
        "lat": 26.2452915,
        "lon": 68.4040229,
        "date_window": "2022-07-14 to 2022-07-15",
        "rainfall_mm": 60.0,
        "rainfall_caveat": (
            "Damage-side NTR is confirmed (SBA is not mentioned in this SITREP's "
            "incident list at all). The 60mm rainfall figure itself has NOT been "
            "independently verified against a PMD rainfall table — flagged, not "
            "resolved."
        ),
        "actual_outcome": "no_flood",
        "impact": "No damage/incidents reported for Shaheed Benazirabad in this SITREP",
        "source": (
            "NDMA Monsoon 2022 Daily SITREP No. 031, covering 14-15 Jul 2022 "
            "(https://reliefweb.int/report/pakistan/ndma-monsoon-2022-daily-situation-report-no-031-1300-hrs-14-july-2022-1300-hrs-15-july-2022)"
        ),
    },
]

ALL_CASES = FLOOD_CASES + NON_FLOOD_CASES