from risk_check import _compute_risk_core
from backtest_cases import ALL_CASES

ALERT_TIERS = {"Moderate Risk", "High Risk", "Very High Risk"}

print(f"{'case':32} {'rain_mm':>8} {'score':>7} {'tier':16} {'predicted':10} {'actual':10} {'result'}")
print("-" * 100)

results = []
for case in ALL_CASES:
    if case["rainfall_mm"] is None:
        print(f"{case['id']:32} {'N/A':>8} {'--':>7} {'--':16} {'SKIPPED':10} {case['actual_outcome']:10} no rainfall figure available")
        continue

    core = _compute_risk_core(case["city"], case["rainfall_mm"])
    predicted_alert = core["risk_level_key"] in ALERT_TIERS
    predicted = "alert" if predicted_alert else "no_alert"
    actual = "flood" if case["actual_outcome"] == "flood" else "no_flood"

    if actual == "flood" and predicted == "alert":
        outcome = "HIT"
    elif actual == "flood" and predicted == "no_alert":
        outcome = "MISS (false negative)"
    elif actual == "no_flood" and predicted == "alert":
        outcome = "FALSE ALARM"
    else:
        outcome = "CORRECT (quiet)"

    results.append(outcome)
    print(f"{case['id']:32} {case['rainfall_mm']:8.1f} {core['score']:7.1f} {core['risk_level_key']:16} {predicted:10} {actual:10} {outcome}")

print("-" * 100)
print(f"Total scored cases: {len(results)} (of {len(ALL_CASES)} total, {len(ALL_CASES)-len(results)} skipped for missing rainfall)")
for tag in ["HIT", "MISS (false negative)", "FALSE ALARM", "CORRECT (quiet)"]:
    print(f"  {tag}: {results.count(tag)}")