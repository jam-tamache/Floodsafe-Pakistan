"""
Mock-data tests for FloodSafe Pakistan's scoring and forecast code.

There is no rain in Sindh right now, so these tests check the math
directly with fake data. No network calls are made: the OpenWeatherMap
response is mocked.

Put this file next to risk_check.py, translations.py and elevation_data.py,
then run:

    python test_risk_scoring.py
"""

import os
import time
import unittest
from unittest.mock import patch, MagicMock

import risk_check
from translations import get_translation


# ---------------------------------------------------------------------------
# 1. Rainfall to risk level, with elevation switched off.
#
# get_elevation is patched to return None, so the total score is only the
# rainfall part. Thresholds follow METHODOLOGY.md:
# mega_urban_coastal 40/100, central_plains 50/120, arid_plains_desert 70/140.
# ---------------------------------------------------------------------------

class TestRainfallClassification(unittest.TestCase):

    def setUp(self):
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
            (121.0, "Moderate Risk"),  # still Moderate, see the dead-zone test
            (185.0, "High Risk"),      # a value that reaches High here
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
            (0.3, "Low Risk"),   # the value seen in the real forecast test
            (40.0, "Low Risk"),
            (41.0, "Moderate Risk"),
            (100.0, "Moderate Risk"),
            (101.0, "Moderate Risk"),   # see the dead-zone test
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
            (141.0, "Moderate Risk"),   # see the dead-zone test
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
        Going past a region's medium_max does not jump straight to High Risk.
        One mm past medium_max the rainfall points are 50.0, which is still
        Moderate: High Risk starts only above 50 points.
        """
        profile = risk_check.REGIONAL_PROFILES["central_plains"]
        just_past = profile["medium_max"] + 1

        rain_pts = risk_check.rainfall_component(just_past, profile)
        self.assertLessEqual(
            rain_pts, 50,
            "if this ever fails, the dead zone has been fixed. Good, delete this test"
        )

        result = risk_check.check_risk(just_past, "nawabshah", self.t)
        self.assertEqual(result["risk_level_key"], "Moderate Risk")


# ---------------------------------------------------------------------------
# 2. Elevation component, tested directly.
#
# elevation_component() returns the raw terrain score with no rainfall
# scaling, so these tests call it without a rainfall argument.
# ---------------------------------------------------------------------------

class TestElevationComponent(unittest.TestCase):

    def setUp(self):
        # Save the module-level ranges and restore them after each test.
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
# 2b. Elevation scaled by rainfall.
#
# Without scaling, a low-lying city scored Moderate Risk even at 0 mm of rain.
# Elevation points are now multiplied by min(rainfall_mm / low_max, 1.0), so
# a dry day stays Low. These tests run the whole check_risk() pipeline.
# ---------------------------------------------------------------------------

class TestElevationRainfallScaling(unittest.TestCase):

    def setUp(self):
        self._orig_ranges = dict(risk_check._REGION_ELEVATION_RANGES)
        self.t = get_translation("en")

    def tearDown(self):
        risk_check._REGION_ELEVATION_RANGES.clear()
        risk_check._REGION_ELEVATION_RANGES.update(self._orig_ranges)

    def test_lowest_elevation_city_at_zero_rain_stays_low_risk(self):
        # nawabshah is central_plains (low_max=50). Forced to the lowest
        # elevation so it gets the full 30 raw elevation points.
        risk_check._REGION_ELEVATION_RANGES["central_plains"] = (5, 105)
        with patch("elevation_data.get_elevation", return_value=5):
            result = risk_check.check_risk(0.0, "nawabshah", self.t)
        self.assertEqual(
            result["risk_level_key"], "Low Risk",
            f"lowest-elevation city at 0mm rainfall should be Low Risk, "
            f"got {result['risk_level_key']} (score {result['score']})"
        )
        self.assertEqual(result["elevation_points"], 0.0)
        # The raw terrain score is kept separately.
        self.assertEqual(result["elevation_terrain_points"], 30.0)

    def test_lowest_elevation_city_at_full_low_max_gets_full_elevation_weight(self):
        # At rainfall == low_max (50mm here) elevation counts in full.
        risk_check._REGION_ELEVATION_RANGES["central_plains"] = (5, 105)
        with patch("elevation_data.get_elevation", return_value=5):
            result = risk_check.check_risk(50.0, "nawabshah", self.t)
        self.assertEqual(result["elevation_points"], 30.0)
        self.assertEqual(result["score"], 55.0)  # 25.0 rain + 30.0 elevation

    def test_elevation_contribution_scales_linearly_with_rainfall(self):
        # At half of low_max (25mm), elevation counts for half (15 of 30).
        risk_check._REGION_ELEVATION_RANGES["central_plains"] = (5, 105)
        with patch("elevation_data.get_elevation", return_value=5):
            result = risk_check.check_risk(25.0, "nawabshah", self.t)
        self.assertEqual(result["elevation_points"], 15.0)
        self.assertEqual(result["elevation_terrain_points"], 30.0)  # raw score unchanged

    def test_highest_elevation_city_unaffected_either_way(self):
        # Highest ground gets 0 raw points, and 0 scaled by anything is 0.
        risk_check._REGION_ELEVATION_RANGES["central_plains"] = (5, 105)
        with patch("elevation_data.get_elevation", return_value=105):
            result_dry = risk_check.check_risk(0.0, "dadu", self.t)
            result_wet = risk_check.check_risk(50.0, "dadu", self.t)
        self.assertEqual(result_dry["elevation_points"], 0.0)
        self.assertEqual(result_wet["elevation_points"], 0.0)

    def test_karachi_worked_example_matches_updated_methodology(self):
        # Matches the worked example in METHODOLOGY.md: karachi at 25mm
        # (low_max=40), lowest in its region (9m to 26m in city_elevation.csv).
        # tearDown restores the original ranges.
        risk_check._REGION_ELEVATION_RANGES["mega_urban_coastal"] = (9, 26)
        with patch("elevation_data.get_elevation", return_value=9):
            result = risk_check.check_risk(25.0, "karachi", self.t)

        self.assertEqual(result["rainfall_points"], 15.6)
        self.assertEqual(result["elevation_terrain_points"], 30.0)
        self.assertEqual(result["elevation_points"], 18.8)   # 30.0 * (25/40) = 18.75, rounded
        self.assertEqual(result["score"], 34.4)              # 15.6 + 18.8
        self.assertEqual(result["risk_level_key"], "Moderate Risk")


# ---------------------------------------------------------------------------
# 3. get_forecast_rainfall: summing, the 72h cutoff, and response shapes.
# ---------------------------------------------------------------------------

def _fake_forecast_response(entries, country="PK", cod="200"):
    """Build a MagicMock that acts like requests.get(...).json()
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
        # get_forecast_rainfall stops early if there is no API key, so these
        # tests set a fake one. test_missing_api_key patches os.environ.get
        # itself to remove it.
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
            {"dt": now + 73 * 3600, "rain": {"3h": 999.0}}, # outside window, must be left out
        ]
        with patch("risk_check.requests.get", return_value=_fake_forecast_response(entries)):
            valid, total, err = risk_check.get_forecast_rainfall("nawabshah")
        self.assertTrue(valid)
        self.assertEqual(total, 17.5)  # 5.0 + 10.0 + 2.5, not the 999.0 entry
        self.assertIsNone(err)

    def test_entries_missing_rain_key_treated_as_zero(self):
        now = time.time()
        entries = [
            {"dt": now + 3 * 3600},                       # no "rain" key
            {"dt": now + 6 * 3600, "rain": {}},            # "rain" but no "3h"
            {"dt": now + 9 * 3600, "rain": {"3h": 8.0}},
        ]
        with patch("risk_check.requests.get", return_value=_fake_forecast_response(entries)):
            valid, total, err = risk_check.get_forecast_rainfall("karachi")
        self.assertTrue(valid)
        self.assertEqual(total, 8.0)

    def test_storm_sized_forecast_adds_up_to_exact_total(self):
        # Checks the mm total from get_forecast_rainfall() only, not a risk
        # level (levels are tested in section 1).
        # 24 entries at 1h, 4h, ... 70h, all inside the 72h window.
        now = time.time()
        entries = [{"dt": now + h * 3600, "rain": {"3h": 6.0}} for h in range(1, 72, 3)]
        with patch("risk_check.requests.get", return_value=_fake_forecast_response(entries)):
            valid, total, err = risk_check.get_forecast_rainfall("nawabshah")
        self.assertTrue(valid)
        self.assertEqual(len(entries), 24)
        self.assertEqual(total, 144.0)  # 24 * 6.0mm

    def test_string_cod_is_handled(self):
        # In the forecast endpoint "cod" is a string, unlike the current-weather
        # endpoint. This checks the str(...) conversion still works.
        entries = [{"dt": time.time() + 3600, "rain": {"3h": 1.0}}]
        with patch("risk_check.requests.get", return_value=_fake_forecast_response(entries, cod="200")):
            valid, total, err = risk_check.get_forecast_rainfall("karachi")
        self.assertTrue(valid)
        self.assertEqual(total, 1.0)

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