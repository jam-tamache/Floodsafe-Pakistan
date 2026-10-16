# FloodSafe Pakistan

FloodSafe Pakistan is a flood risk checker for cities in Sindh. It takes the 72-hour rainfall forecast for a city, looks at how high the city sits compared to others nearby, and gives a risk level.

Live site: https://floodsafepakistan.pythonanywhere.com

This is a student project. It is not a warning system and it is not a proven way to predict floods. For real warnings, use PMD, NDMA and PDMA Sindh.

## Why I made it

I live in Nawabshah. During the 2022 floods it rained for about two days, and our power was out for around a week.

After that I kept wondering if a simple tool could tell people, before the rain arrives, how bad it might get where they live. FloodSafe is my attempt to find out.

## What it does

- Gets the rainfall forecast for the next 72 hours from OpenWeatherMap.
- Compares the city's elevation with other cities in the same terrain group.
- Shows one of four levels: Low, Moderate, High or Very High.
- Has a scenario mode where you type in a rainfall amount (a 72-hour total) and see how the level changes.
- Has a map of the cities.
- Works in English, Urdu and Sindhi.

28 cities in Sindh are scored. Other places on the map are only there for reference.

## How the score works

Two things go in: expected rain over 72 hours, and the city's elevation compared to other cities in its group. The lower the city, the more the same rain counts. If little rain is expected, low elevation alone does not push the score up.

The rain thresholds are my own estimates, and nobody has checked them against local flood records. How I set them is explained in [METHODOLOGY.md](METHODOLOGY.md).

## Back-test

I tested the score on past rain events in Sindh. I wrote down the test rules and committed them before looking at any results ([BACKTEST_PROTOCOL.md](BACKTEST_PROTOCOL.md)).

There were nine cases. One was skipped because I could not find a reliable rainfall figure for it. That leaves eight:

- 5 floods: all 5 were flagged.
- 3 rainy periods with no flood: all 3 were flagged too, so 3 false alarms.
- 0 cases where it correctly stayed quiet.

I also compared it with a plain rule that raises an alarm whenever 50 mm or more of rain is expected. FloodSafe did not beat that rule, and it failed a goal I had set before the test. So this test does not show that adding elevation helps.

Eight cases is very small, and none of the eight was a dry spell. The test also used past rainfall figures, not live forecasts, so it says nothing about how accurate the live forecast is.

Every case, including the false alarms, is on the [back-test page](https://floodsafepakistan.pythonanywhere.com/back-test?lang=en).

## Limits

- Only tested on cities in Sindh. It has not been checked for the rest of Pakistan.
- It only uses rain and relative elevation. It does not know about drains, land use, canals or rivers.
- It does not cover river floods from broken embankments or glacier lake floods.
- Do not use it for emergency decisions.

## Built with

- Python and Flask
- HTML and CSS
- OpenWeatherMap for rainfall forecasts
- Public elevation data
- PythonAnywhere for hosting

## Feedback

If you find a wrong figure, a bad translation, or a source that would improve this, please open an issue on GitHub.