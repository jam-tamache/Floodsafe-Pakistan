"""
elevation_data.py

Loads city_elevation.csv (produced by get_elevation.py) once at app
startup and exposes a normalized city -> elevation_m lookup.

Deliberately does NOT hardcode any elevation numbers in source - the CSV
is the single source of truth. If the file is missing or a city's row is
blank, that is surfaced explicitly (ELEVATION_LOAD_ERROR / a city simply
not being in ELEVATIONS) rather than guessed at, consistent with the
project's "refuse rather than invent" rule.
"""

import csv
import os

ELEVATION_FILE = "city_elevation.csv"

# Populated by _load(). Keys are normalized city names (lowercase,
# stripped) matching risk_check.py's normalize_city(). Values are floats.
ELEVATIONS = {}

# None if load succeeded. Otherwise a short string describing why - the
# app should still run without elevation data, just fall back to a
# rainfall-only score and say so (see risk_check.py's elevation_component).
ELEVATION_LOAD_ERROR = None


def _load():
    global ELEVATION_LOAD_ERROR

    if not os.path.exists(ELEVATION_FILE):
        ELEVATION_LOAD_ERROR = (
            f"{ELEVATION_FILE} not found - run get_elevation.py first. "
            "Elevation scoring is disabled until this file exists."
        )
        return

    try:
        with open(ELEVATION_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if "city" not in (reader.fieldnames or []) or "elevation_m" not in (reader.fieldnames or []):
                ELEVATION_LOAD_ERROR = (
                    f"{ELEVATION_FILE} is missing expected columns "
                    f"(found: {reader.fieldnames}). Elevation scoring is disabled."
                )
                return

            loaded = 0
            for row in reader:
                city = (row.get("city") or "").strip().lower()
                raw_elevation = (row.get("elevation_m") or "").strip()
                if not city or not raw_elevation:
                    continue  # blank row or a city that failed during get_elevation.py
                try:
                    ELEVATIONS[city] = float(raw_elevation)
                    loaded += 1
                except ValueError:
                    continue  # malformed value, skip rather than crash

            if loaded == 0:
                ELEVATION_LOAD_ERROR = (
                    f"{ELEVATION_FILE} exists but no valid elevation_m values "
                    "were found in it. Elevation scoring is disabled."
                )
    except (OSError, csv.Error) as e:
        ELEVATION_LOAD_ERROR = f"Could not read {ELEVATION_FILE}: {e}. Elevation scoring is disabled."


_load()


def get_elevation(city_normalized):
    """Returns float elevation in meters, or None if unavailable for this city."""
    return ELEVATIONS.get(city_normalized)