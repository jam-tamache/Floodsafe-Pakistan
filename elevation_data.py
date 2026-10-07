"""
elevation_data.py

Loads city_elevation.csv (made by get_elevation.py) once at startup and
gives a city -> elevation in metres lookup.

No elevation numbers are written in the code. If the file or a city's
value is missing, the city is simply left out and the app does not guess.
"""

import csv
import os

ELEVATION_FILE = "city_elevation.csv"

# Filled by _load(). Keys are lowercase city names, values are floats.
ELEVATIONS = {}

# None if loading worked, otherwise a short reason. The app still runs
# without elevation and uses rainfall only.
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
                    continue  # blank row, or a city that failed in get_elevation.py
                try:
                    ELEVATIONS[city] = float(raw_elevation)
                    loaded += 1
                except ValueError:
                    continue  # bad value, skip it

            if loaded == 0:
                ELEVATION_LOAD_ERROR = (
                    f"{ELEVATION_FILE} exists but no valid elevation_m values "
                    "were found in it. Elevation scoring is disabled."
                )
    except (OSError, csv.Error) as e:
        ELEVATION_LOAD_ERROR = f"Could not read {ELEVATION_FILE}: {e}. Elevation scoring is disabled."


_load()


def get_elevation(city_normalized):
    """Return elevation in metres, or None if this city has no value."""
    return ELEVATIONS.get(city_normalized)