"""
get_elevation.py

Reads city_coordinates.csv (columns: city, region, lat, lon, status)
and looks up ground elevation (meters) for each city.

Primary source : Open-Elevation (https://api.open-elevation.com)
Fallback source: OpenTopoData  (https://api.opentopodata.org)

Writes city_elevation.csv with the original columns plus a new
`elevation_m` column. If a city fails on both APIs after retries,
elevation_m is left blank and the row is flagged in the console
output so it can be manually checked later.

Usage:
    python get_elevation.py
"""

import csv
import time
import sys
import urllib.request
import json

INPUT_FILE = "city_coordinates.csv"
OUTPUT_FILE = "city_elevation.csv"

OPEN_ELEVATION_URL = "https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
OPEN_TOPO_DATA_URL = "https://api.opentopodata.org/v1/srtm90m?locations={lat},{lon}"

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2
REQUEST_TIMEOUT_SECONDS = 10
PAUSE_BETWEEN_CITIES_SECONDS = 1  # be polite to free API tiers


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "FloodSafePakistan/1.0"})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_elevation_open_elevation(lat, lon):
    url = OPEN_ELEVATION_URL.format(lat=lat, lon=lon)
    data = fetch_json(url)
    return data["results"][0]["elevation"]


def get_elevation_opentopodata(lat, lon):
    url = OPEN_TOPO_DATA_URL.format(lat=lat, lon=lon)
    data = fetch_json(url)
    return data["results"][0]["elevation"]


def get_elevation_with_retries(lat, lon, city_name):
    # Try Open-Elevation first, with retries
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return get_elevation_open_elevation(lat, lon), "open-elevation"
        except Exception as e:
            print(f"  [{city_name}] Open-Elevation attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY_SECONDS)

    # Fall back to OpenTopoData, with retries
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return get_elevation_opentopodata(lat, lon), "opentopodata"
        except Exception as e:
            print(f"  [{city_name}] OpenTopoData attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY_SECONDS)

    return None, None


def main():
    try:
        with open(INPUT_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            rows = list(reader)
    except FileNotFoundError:
        print(f"ERROR: could not find {INPUT_FILE} in the current folder.")
        print("Make sure get_elevation.py and city_coordinates.csv are in the same directory.")
        sys.exit(1)

    if not rows:
        print(f"ERROR: {INPUT_FILE} has no data rows.")
        sys.exit(1)

    lat_key = "lat" if "lat" in fieldnames else "latitude"
    lon_key = "lon" if "lon" in fieldnames else "longitude"
    city_key = "city" if "city" in fieldnames else fieldnames[0]

    if lat_key not in fieldnames or lon_key not in fieldnames:
        print(f"ERROR: expected lat/lon columns, found columns: {fieldnames}")
        sys.exit(1)

    output_fieldnames = list(fieldnames) + ["elevation_m", "elevation_source"]
    results = []
    failed_cities = []

    print(f"Looking up elevation for {len(rows)} cities...\n")

    for i, row in enumerate(rows, start=1):
        city = row.get(city_key, f"row {i}")
        lat = row.get(lat_key)
        lon = row.get(lon_key)

        print(f"[{i}/{len(rows)}] {city} ({lat}, {lon})")

        if not lat or not lon:
            print("  SKIPPED: missing lat/lon")
            row["elevation_m"] = ""
            row["elevation_source"] = ""
            failed_cities.append(city)
            results.append(row)
            continue

        elevation, source = get_elevation_with_retries(lat, lon, city)

        if elevation is None:
            print(f"  FAILED after both APIs and {MAX_RETRIES} retries each.")
            row["elevation_m"] = ""
            row["elevation_source"] = ""
            failed_cities.append(city)
        else:
            print(f"  -> {elevation} m (source: {source})")
            row["elevation_m"] = elevation
            row["elevation_source"] = source

        results.append(row)
        time.sleep(PAUSE_BETWEEN_CITIES_SECONDS)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=output_fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nDone. Wrote {len(results)} rows to {OUTPUT_FILE}")
    if failed_cities:
        print(f"\n{len(failed_cities)} cities FAILED (elevation_m left blank):")
        for c in failed_cities:
            print(f"  - {c}")
        print("\nThese need a manual lookup or a re-run before the formula design can use this file safely.")
    else:
        print("All cities succeeded.")


if __name__ == "__main__":
    main()