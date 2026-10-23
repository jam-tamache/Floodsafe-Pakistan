# FloodSafe Pakistan

FloodSafe Pakistan is a flood risk checker for cities in Sindh. It looks at the 72-hour rain forecast and how high the city sits, then gives a risk level.

Live site: https://floodsafepakistan.pythonanywhere.com

This is a student project. It is not a warning system and it is not proven. For real warnings, use PMD, NDMA and PDMA Sindh.

## Why I made it

I live in Nawabshah. In the 2022 floods it rained for about two days. Most of the city flooded, some parts much more than others. Even the grid station flooded, and our power was out for about a week.

After that I wondered if a simple tool could tell people, before the rain, how bad it might get where they live. This is my attempt.

## What it does

- Gets the 72-hour rain forecast from OpenWeatherMap.
- Compares the city's elevation with other cities in the same terrain group.
- Shows one of four levels: Low, Moderate, High or Very High.
- Has a scenario mode: type a 72-hour rainfall total and see the level.
- Has a map of the cities.
- Works in English, Urdu and Sindhi. The Urdu and Sindhi text has not been reviewed by a native speaker yet.

28 cities in Sindh are scored. Other places on the map are for reference only.

## How the score works

Two things go in: rain over 72 hours, and the city's elevation compared to its group. The lower the city, the more the same rain counts. With little rain, low elevation alone does not raise the score.

The rain thresholds are my own estimates. I have only checked them on the eight back-test cases below. See [METHODOLOGY.md](METHODOLOGY.md).

The top score is about 84 out of 100, so most cities can never reach Very High.

## Back-test

I tested the score on past rain events in Sindh. I wrote the test rules and committed them before looking at any results ([BACKTEST_PROTOCOL.md](BACKTEST_PROTOCOL.md)).

There were nine cases. One was skipped because I could not find a reliable rainfall figure. Eight were scored:

- 5 floods: all 5 flagged.
- 3 rainy periods with no flood: all 3 flagged too. These are false alarms.
- 0 cases where it correctly stayed quiet.

I also compared it with a plain rule: raise an alarm when 50 mm or more of rain is expected. FloodSafe did not beat it, and it failed a goal I set before the test. So the test does not show that elevation helps.

Limits of the test:

- Eight cases is very small. None was a dry spell.
- Three of the five floods are one storm (2 to 3 August 2026), so they are not independent.
- Two of the five flood labels are weak (Hyderabad City and Mirpurkhas City). I kept both in. The case pages say how weak the evidence is.
- All eight rainfall figures are 24-hour readings, not 72-hour totals.
- It used past rainfall, not live forecasts, so it says nothing about how accurate the live forecast is.

Every scored case, including the false alarms, is on the [back-test page](https://floodsafepakistan.pythonanywhere.com/back-test?lang=en).

## Limits

- Only tested on cities in Sindh. Not checked for the rest of Pakistan.
- It only uses rain and relative elevation. It does not know about drains, land use, canals or rivers.
- It does not cover river floods from broken embankments or glacier lake floods.
- Do not use it for emergency decisions.

## Run it yourself

You need Python 3.

1. Download the project from GitHub.
2. Open a terminal in the project folder.
3. Run `pip install -r requirements.txt`
4. Get a free key from OpenWeatherMap.
5. Make a file named `.env` and write `OPENWEATHER_API_KEY=your_key` in it.
6. Run `python risk_check.py`
7. Open `http://127.0.0.1:5000` in your browser.

## Built with

- Python and Flask
- HTML and CSS
- OpenWeatherMap for rainfall forecasts
- City elevation data
- PythonAnywhere for hosting

## Feedback

If you find a wrong figure, a bad translation, or a source that would help, please open an issue on GitHub.