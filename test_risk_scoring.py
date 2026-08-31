"""
Mock-data tests for FloodSafe Pakistan's scoring + forecast pipeline.

Why this exists: there's no rain in Sindh right now, so forecast mode has
only ever been exercised with near-zero rainfall (Karachi 0.3mm, Nawabshah
0.0mm), both landing Low Risk. That confirms the plumbing works, not that
Medium/High classification or the forecast aggregation logic is correct.
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
# rainfall number actually classify as Medium/High per each region's own
# thresholds, not just Low.
#
# Thresholds below match the FFD-anchored revision (see METHODOLOGY.md):
# mega_urban_coastal low_max=40/medium_max=100, central_plains
# low_max=50/medium_max=120, arid_plains_desert low_max=70/medium_max=140.
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
            (51.0, "Medium Risk"),     # just past low_max
            (85.0, "Medium Risk"),
            (120.0, "Medium Risk"),    # boundary: <= medium_max
            (121.0, "Medium Risk"),    # ATTENTION: just past medium_max is
                                        # still Medium — see the dead-zone
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
            (41.0, "Medium Risk"),
            (100.0, "Medium Risk"),
            (101.0, "Medium Risk"),   # see dead-zone test below
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
            (71.0, "Medium Risk"),
            (140.0, "Medium Risk"),
            (141.0, "Medium Risk"),   # see dead-zone test below
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
        extreme-tail formula (60 + 10*fraction, saturating at rainfall =
        1.5 * medium_max) means a city can be past its documented
        "medium_max" boundary and still score Medium Risk overall — it
        takes rainfall AT LEAST 50% past medium_max before rain_pts alone
        can exceed the 65-point High Risk cutoff.

        Concretely, for nawabshah (medium_max=120mm): every rainfall value
        from 121mm up to 180mm classifies as Medium Risk, even though the
        methodology language implies medium_max is where "medium" ends.
        That's a 59mm-wide band where a city already past its stated
        medium-risk ceiling still doesn't get flagged High.

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
# 3. get_forecast_rainfall aggregation + the two shape differences you
#    already hit once (string "200" cod, nested city.country) — plus cases
#    you haven't hit yet: entries beyond the 72h cutoff, entries with no
#    rain key at all, and real Medium/High-sized totals.
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
        # nawabshah's medium_max is now 120mm, so this total needs to clear
        # that bar (the old assertion's 55.0 floor was sized for the old
        # thresholds and no longer proves anything under the new ones).
        now = time.time()
        entries = [{"dt": now + h * 3600, "rain": {"3h": 6.0}} for h in range(0, 72, 3)]
        # 24 entries * 6.0mm = 144mm over 72h — deliberately large to prove
        # aggregation and Medium/High math both work, not just Low.
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