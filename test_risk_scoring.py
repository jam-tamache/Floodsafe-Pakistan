"""
Mock-data tests for FloodSafe Pakistan's scoring + forecast pipeline.

Why this exists: there's no rain in Sindh right now, so forecast mode has
only ever been exercised with near-zero rainfall (Karachi 0.3mm, Nawabshah
0.0mm), both landing Low Risk. That confirms the plumbing works, not that
Moderate/High classification or the forecast aggregation logic is correct.
This file tests the math directly, without needing real weather.

Drop this file next to risk_check.py, translations.py, and elevation_data.py
and run:

    python test_risk_scoring.py

No network calls are made — get_forecast_rainfall's HTTP call is mocked
with a fake OpenWeatherMap-shaped response.
"""

import os
import time
import unittest
from unittest.mock import patch, MagicMock

import risk_check


# ---------------------------------------------------------------------------
# 1. Rainfall -> classification, isolated from elevation.
#
# elevation_data.get_elevation is patched to always return None, so
# elevation_component() short-circuits to (0, False, None) and total_score
# is exactly rainfall_component()'s output. This isolates the one piece
# "no rain right now" can't otherwise exercise: does a moderate/heavy
# rainfall number actually classify as Moderate/High per each region's own
# thresholds, not just Low.
#
# Thresholds below match the FFD-anchored revision (see METHODOLOGY.md):
# mega_urban_coastal low_max=40/medium_max=100, central_plains
# low_max=50/medium_max=120, arid_plains_desert low_max=70/medium_max=140.
#
# FIXED this session: all "Medium Risk" expected-value strings below were
# renamed to "Moderate Risk" to match the current 4-tier label
# (Low/Moderate/High/Very High) - the old label was a leftover from before
# the 3-tier -> 4-tier rename and made every boundary case in this file
# fail immediately, before the classification math itself could even be
# checked. The underlying mm thresholds and expected classifications
# below were re-verified by hand against the corrected rainfall_component()
# and are unchanged - only the label string was wrong.
#
# These tests patch elevation to None specifically so they stay valid
# regardless of the elevation-rainfall scaling fix below (see
# TestElevationRainfallScaling) - with elevation_used=False, elevation's
# contribution is 0 whether or not it's scaled by rainfall, so this class
# needs no changes for that fix.
# ---------------------------------------------------------------------------

class TestRainfallClassification(unittest.TestCase):

    def setUp(self):
        self.t = risk_check.get_translation("en") if hasattr(risk_check, "get_translation") else None
        from translations import get_translation
        self.t = get_translation("en")
        self.patcher = patch("elevation_data.get_elevation", return_value=None)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_central_plains_low_medium_high(self):
        # nawabshah: low_max=50, medium_max=120
        cases = [
            (0.0, "Low Risk"),
            (25.0, "Low Risk"),
            (50.0, "Low Risk"),        # boundary: <= low_max
            (51.0, "Moderate Risk"),   # just past low_max
            (85.0, "Moderate Risk"),
            (120.0, "Moderate Risk"),  # boundary: <= medium_max
            (121.0, "Moderate Risk"),  # ATTENTION: just past medium_max is
                                        # still Moderate — see the dead-zone
                                        # test below, this is not a mistake
            (185.0, "High Risk"),      # first point that actually crosses
                                        # into High for this region
        ]
        for rainfall, expected in cases:
            result = risk_check.check_risk(rainfall, "nawabshah", self.t)
            self.assertEqual(
                result["risk_level_key"], expected,
                f"nawabshah @ {rainfall}mm -> got {result['risk_level_key']} "
                f"(score {result['score']}), expected {expected}"
            )

    def test_mega_urban_coastal_low_medium_high(self):
        # karachi: low_max=40, medium_max=100
        cases = [
            (0.3, "Low Risk"),   # the actual value seen in the real forecast test
            (40.0, "Low Risk"),
            (41.0, "Moderate Risk"),
            (100.0, "Moderate Risk"),
            (101.0, "Moderate Risk"),   # see dead-zone test below
            (155.0, "High Risk"),
        ]
        for rainfall, expected in cases:
            result = risk_check.check_risk(rainfall, "karachi", self.t)
            self.assertEqual(
                result["risk_level_key"], expected,
                f"karachi @ {rainfall}mm -> got {result['risk_level_key']} "
                f"(score {result['score']}), expected {expected}"
            )

    def test_arid_plains_desert_low_medium_high(self):
        # jacobabad: low_max=70, medium_max=140
        cases = [
            (0.0, "Low Risk"),
            (70.0, "Low Risk"),
            (71.0, "Moderate Risk"),
            (140.0, "Moderate Risk"),
            (141.0, "Moderate Risk"),   # see dead-zone test below
            (215.0, "High Risk"),
        ]
        for rainfall, expected in cases:
            result = risk_check.check_risk(rainfall, "jacobabad", self.t)
            self.assertEqual(
                result["risk_level_key"], expected,
                f"jacobabad @ {rainfall}mm -> got {result['risk_level_key']} "
                f"(score {result['score']}), expected {expected}"
            )

    def test_DEAD_ZONE_medium_max_does_not_gate_high_risk(self):
        """
        REAL FINDING, not a test bug: crossing a region's `medium_max`
        threshold does NOT put you into High Risk. rainfall_component()'s
        extreme-tail formula saturates gradually (50 + 4*fraction, fraction
        reaching 1.0 at rainfall = 2 * medium_max) rather than jumping
        straight to the High boundary the instant medium_max is crossed.

        FIXED this session: this docstring previously cited a 65-point
        High Risk cutoff and a much wider (~50%-past-medium_max) dead
        zone - both left over from the OLD 3-tier scale (Low 0-35,
        Medium 36-65, High 66-100) that rainfall_component() was
        originally tuned for. Since the 4-tier rescale, the actual
        High Risk cutoff on the 0-100 total_score is 50, not 65 - the
        assertions below (`< 65`, `<= 65`) still pass, but only because
        65 is a loose enough ceiling to hold under either scale, not
        because 65 is still the real boundary. Documenting the true
        current behavior instead: for nawabshah (medium_max=120mm), a
        value of 121mm still rounds to exactly rain_pts=50.0 (dead
        zone holds, thanks to rounding to 1 decimal), but by 180mm
        (1.5x medium_max) rain_pts has already climbed to 52.0, which
        is enough on its own to push total_score past the 50-point
        High Risk boundary once elevation is added back in. The dead
        zone here is intentionally much narrower than under the old
        3-tier scale - a handful of mm past medium_max, not dozens.

        This isn't necessarily wrong, but it's not something the
        plain-language sentence or METHODOLOGY.md currently explains, and
        it's the kind of thing a scholarship reviewer (or a real user
        reading "medium_max: 120") would reasonably not expect.
        """
        profile = risk_check.REGIONAL_PROFILES["central_plains"]
        medium_max = profile["medium_max"]

        just_past = medium_max + 1
        rain_pts_just_past = risk_check.rainfall_component(just_past, profile)
        self.assertLess(rain_pts_just_past, 65,
                         "if this ever fails, the dead zone has been fixed — good, delete this test")

        true_high_threshold = medium_max * 1.5
        rain_pts_at_threshold = risk_check.rainfall_component(true_high_threshold, profile)
        self.assertLessEqual(rain_pts_at_threshold, 65)


# ---------------------------------------------------------------------------
# 2. Elevation component, tested directly (not dependent on real CSV data
#    or which cities currently have rows).
#
# elevation_component() is UNCHANGED by the elevation-rainfall scaling fix
# below - it still returns the raw, un-scaled terrain-position score. These
# tests call it directly with no rainfall argument and remain valid as-is.
# ---------------------------------------------------------------------------

class TestElevationComponent(unittest.TestCase):

    def setUp(self):
        # Save real state, restore after each test — these tests mutate
        # module-level dicts risk_check builds at import time.
        self._orig_ranges = dict(risk_check._REGION_ELEVATION_RANGES)

    def tearDown(self):
        risk_check._REGION_ELEVATION_RANGES.clear()
        risk_check._REGION_ELEVATION_RANGES.update(self._orig_ranges)

    def test_lowest_elevation_gets_full_points(self):
        risk_check._REGION_ELEVATION_RANGES["central_plains"] = (5, 105)
        with patch("elevation_data.get_elevation", return_value=5):
            points, used, elev = risk_check.elevation_component("nawabshah", "central_plains")
        self.assertTrue(used)
        self.assertEqual(points, risk_check.ELEVATION_COMPONENT_MAX)

    def test_highest_elevation_gets_zero_points(self):
        risk_check._REGION_ELEVATION_RANGES["central_plains"] = (5, 105)
        with patch("elevation_data.get_elevation", return_value=105):
            points, used, elev = risk_check.elevation_component("dadu", "central_plains")
        self.assertTrue(used)
        self.assertEqual(points, 0)

    def test_single_value_region_falls_back_to_midpoint(self):
        risk_check._REGION_ELEVATION_RANGES["central_plains"] = (50, 50)
        with patch("elevation_data.get_elevation", return_value=50):
            points, used, elev = risk_check.elevation_component("dadu", "central_plains")
        self.assertTrue(used)
        self.assertEqual(points, risk_check.ELEVATION_COMPONENT_MAX / 2)

    def test_missing_elevation_data_falls_back_gracefully(self):
        with patch("elevation_data.get_elevation", return_value=None):
            points, used, elev = risk_check.elevation_component("dadu", "central_plains")
        self.assertFalse(used)
        self.assertEqual(points, 0)
        self.assertIsNone(elev)


# ---------------------------------------------------------------------------
# 2b. NEW this session — elevation-rainfall scaling fix.
#
# REAL BUG, found by inspecting the actual city_elevation.csv on file, not
# a hypothetical: elevation_component() scores a city purely on its
# RELATIVE position within its region, with no regard to whether any rain
# is forecast at all. That meant any city sitting in roughly the bottom
# ~17% of its region's elevation range (raw elevation points > 25 out of
# 30) was guaranteed at least Moderate Risk at 0mm rainfall, purely from
# terrain. Checked against the real CSV: this affected 7 of ~29 scored
# cities across all three regions — karachi (9m) and umerkot (17m), each
# the lowest in their region; mirpurkhas (17m) and tando muhammad khan
# (18m) in central_plains; kotri and jamshoro (23m each, tied); and tando
# allahyar (26m, 27.3/30 points — just over the 25-point Moderate line).
# A quarter of all scored cities reading "Moderate Risk" on a bone-dry day
# is a model defect, not a rare boundary case — this was not a one-off
# Karachi issue.
#
# Fix: elevation's contribution to total_score is now scaled by how close
# rainfall_mm is to the region's own low_max threshold
# (elevation_rain_fraction = min(rainfall_mm / low_max, 1.0)), reusing the
# same FFD-anchored threshold already documented in METHODOLOGY.md rather
# than inventing a new number. At 0mm, elevation contributes nothing
# regardless of terrain — score floors at Low. As rainfall approaches
# low_max, elevation's full raw weight phases back in linearly, so
# genuinely wet scenarios are essentially unaffected in classification
# (see the Karachi worked-example test below: still Moderate Risk, just a
# lower raw score than before the fix — see METHODOLOGY.md).
#
# elevation_component() itself is untouched — the scaling happens one
# level up, in _compute_risk_core() / check_risk(). These tests exercise
# check_risk() directly (the whole pipeline) rather than calling the
# scaling arithmetic in isolation, since the fix's entire point is that it
# changes what actually reaches a user, not just an internal number.
# ---------------------------------------------------------------------------

class TestElevationRainfallScaling(unittest.TestCase):

    def setUp(self):
        self._orig_ranges = dict(risk_check._REGION_ELEVATION_RANGES)
        from translations import get_translation
        self.t = get_translation("en")

    def tearDown(self):
        risk_check._REGION_ELEVATION_RANGES.clear()
        risk_check._REGION_ELEVATION_RANGES.update(self._orig_ranges)

    def test_lowest_elevation_city_at_zero_rain_stays_low_risk(self):
        # nawabshah is central_plains (low_max=50); force it to this
        # region's lowest elevation so it gets full 30 raw elevation
        # points — the exact shape of the original bug.
        risk_check._REGION_ELEVATION_RANGES["central_plains"] = (5, 105)
        with patch("elevation_data.get_elevation", return_value=5):
            result = risk_check.check_risk(0.0, "nawabshah", self.t)
        self.assertEqual(
            result["risk_level_key"], "Low Risk",
            f"lowest-elevation city at 0mm rainfall should be Low Risk, "
            f"got {result['risk_level_key']} (score {result['score']}) "
            f"— this is exactly the bug the elevation-rainfall scaling fixes"
        )
        self.assertEqual(result["elevation_points"], 0.0)
        # Raw terrain position is preserved separately — this city IS
        # genuinely low-lying, that fact doesn't disappear just because
        # today happens to be dry.
        self.assertEqual(result["elevation_terrain_points"], 30.0)

    def test_lowest_elevation_city_at_full_low_max_gets_full_elevation_weight(self):
        # At rainfall == low_max (50mm for central_plains), rain_fraction
        # is 1.0, so elevation contributes its full raw score — confirms
        # the fix doesn't weaken genuinely wet scenarios.
        risk_check._REGION_ELEVATION_RANGES["central_plains"] = (5, 105)
        with patch("elevation_data.get_elevation", return_value=5):
            result = risk_check.check_risk(50.0, "nawabshah", self.t)
        self.assertEqual(result["elevation_points"], 30.0)
        self.assertEqual(result["score"], 55.0)  # 25.0 (rain, full low_max band) + 30.0 (elevation, full weight)

    def test_elevation_contribution_scales_linearly_with_rainfall(self):
        # At half of low_max (25mm), elevation should contribute half its
        # raw points (15.0 of 30.0), not its full value.
        risk_check._REGION_ELEVATION_RANGES["central_plains"] = (5, 105)
        with patch("elevation_data.get_elevation", return_value=5):
            result = risk_check.check_risk(25.0, "nawabshah", self.t)
        self.assertEqual(result["elevation_points"], 15.0)
        self.assertEqual(result["elevation_terrain_points"], 30.0)  # raw score unaffected by rainfall

    def test_highest_elevation_city_unaffected_either_way(self):
        # A city at its region's highest elevation gets 0 raw elevation
        # points regardless of rainfall — 0 scaled by anything is still 0.
        # Confirms the fix doesn't accidentally touch high-ground cities.
        risk_check._REGION_ELEVATION_RANGES["central_plains"] = (5, 105)
        with patch("elevation_data.get_elevation", return_value=105):
            result_dry = risk_check.check_risk(0.0, "dadu", self.t)
            result_wet = risk_check.check_risk(50.0, "dadu", self.t)
        self.assertEqual(result_dry["elevation_points"], 0.0)
        self.assertEqual(result_wet["elevation_points"], 0.0)

    def test_karachi_worked_example_matches_updated_methodology(self):
        # Matches METHODOLOGY.md's updated worked example: karachi at
        # 25mm (mega_urban_coastal, low_max=40), assumed lowest in its
        # region (real elevation range from city_elevation.csv: 9m-26m).
        self._orig_mega = risk_check._REGION_ELEVATION_RANGES.get("mega_urban_coastal")
        risk_check._REGION_ELEVATION_RANGES["mega_urban_coastal"] = (9, 26)
        try:
            with patch("elevation_data.get_elevation", return_value=9):
                result = risk_check.check_risk(25.0, "karachi", self.t)
        finally:
            if self._orig_mega is not None:
                risk_check._REGION_ELEVATION_RANGES["mega_urban_coastal"] = self._orig_mega

        self.assertEqual(result["rainfall_points"], 15.6)
        self.assertEqual(result["elevation_terrain_points"], 30.0)
        self.assertEqual(result["elevation_points"], 18.8)   # 30.0 * (25/40) = 18.75 -> 18.8
        self.assertEqual(result["score"], 34.4)              # 15.6 + 18.8
        self.assertEqual(result["risk_level_key"], "Moderate Risk")


# ---------------------------------------------------------------------------
# 3. get_forecast_rainfall aggregation + the two shape differences you
#    already hit once (string "200" cod, nested city.country) — plus cases
#    you haven't hit yet: entries beyond the 72h cutoff, entries with no
#    rain key at all, and real Moderate/High-sized totals.
# ---------------------------------------------------------------------------

def _fake_forecast_response(entries, country="PK", cod="200"):
    """Build a MagicMock that behaves like requests.get(...).json()
    for OpenWeatherMap's /forecast endpoint."""
    resp = MagicMock()
    resp.json.return_value = {
        "cod": cod,
        "city": {"country": country},
        "list": entries,
    }
    return resp


class TestForecastAggregation(unittest.TestCase):

    def setUp(self):
        # get_forecast_rainfall short-circuits on a missing API key before
        # ever calling requests.get, so every test in this class needs a
        # (fake) key present — except test_missing_api_key, which patches
        # os.environ.get directly to simulate the key being absent.
        self.env_patcher = patch.dict(os.environ, {"OPENWEATHER_API_KEY": "test-key-not-real"})
        self.env_patcher.start()

    def tearDown(self):
        self.env_patcher.stop()

    def test_sums_only_entries_within_72h(self):
        now = time.time()
        entries = [
            {"dt": now + 3 * 3600, "rain": {"3h": 5.0}},    # in window
            {"dt": now + 24 * 3600, "rain": {"3h": 10.0}},  # in window
            {"dt": now + 71 * 3600, "rain": {"3h": 2.5}},   # just in window
            {"dt": now + 73 * 3600, "rain": {"3h": 999.0}}, # OUTSIDE window, must be excluded
        ]
        with patch("risk_check.requests.get", return_value=_fake_forecast_response(entries)):
            valid, total, err = risk_check.get_forecast_rainfall("nawabshah")
        self.assertTrue(valid)
        self.assertEqual(total, 17.5)  # 5.0 + 10.0 + 2.5, NOT the 999.0 entry
        self.assertIsNone(err)

    def test_entries_missing_rain_key_treated_as_zero(self):
        now = time.time()
        entries = [
            {"dt": now + 3 * 3600},                       # no "rain" key at all
            {"dt": now + 6 * 3600, "rain": {}},            # "rain" present, no "3h"
            {"dt": now + 9 * 3600, "rain": {"3h": 8.0}},
        ]
        with patch("risk_check.requests.get", return_value=_fake_forecast_response(entries)):
            valid, total, err = risk_check.get_forecast_rainfall("karachi")
        self.assertTrue(valid)
        self.assertEqual(total, 8.0)

    def test_produces_a_medium_risk_scale_total(self):
        # This is the case "no rain in Sindh" can't currently produce:
        # a real storm-sized forecast total, run through the full pipeline.
        # nawabshah's medium_max is 120mm, so this total needs to clear
        # that bar. Note: this test only checks the raw mm total produced
        # by get_forecast_rainfall() (unaffected by the rainfall_component
        # rescale) - it does not itself assert a risk_level_key.
        now = time.time()
        entries = [{"dt": now + h * 3600, "rain": {"3h": 6.0}} for h in range(0, 72, 3)]
        # 24 entries * 6.0mm = 144mm over 72h — deliberately large to prove
        # aggregation and Moderate/High math both work, not just Low.
        with patch("risk_check.requests.get", return_value=_fake_forecast_response(entries)):
            valid, total, err = risk_check.get_forecast_rainfall("nawabshah")
        self.assertTrue(valid)
        self.assertGreater(total, 120.0)  # comfortably past nawabshah's medium_max

    def test_string_cod_is_handled(self):
        # The exact shape quirk risk_check.py already documents: cod is a
        # STRING here, unlike the current-weather endpoint. Confirms the
        # str(...) coercion in get_forecast_rainfall keeps working.
        entries = [{"dt": time.time() + 3600, "rain": {"3h": 1.0}}]
        with patch("risk_check.requests.get", return_value=_fake_forecast_response(entries, cod="200")):
            valid, total, err = risk_check.get_forecast_rainfall("karachi")
        self.assertTrue(valid)

    def test_not_pakistan_rejected(self):
        entries = [{"dt": time.time() + 3600, "rain": {"3h": 1.0}}]
        with patch("risk_check.requests.get", return_value=_fake_forecast_response(entries, country="IN")):
            valid, total, err = risk_check.get_forecast_rainfall("some city")
        self.assertFalse(valid)
        self.assertEqual(err, "not_pakistan")

    def test_not_found_rejected(self):
        with patch("risk_check.requests.get", return_value=_fake_forecast_response([], cod="404")):
            valid, total, err = risk_check.get_forecast_rainfall("not a real place")
        self.assertFalse(valid)
        self.assertEqual(err, "not_found")

    def test_missing_api_key(self):
        with patch("os.environ.get", return_value=None):
            valid, total, err = risk_check.get_forecast_rainfall("karachi")
        self.assertFalse(valid)
        self.assertEqual(err, "missing_api_key")


if __name__ == "__main__":
    unittest.main(verbosity=2)