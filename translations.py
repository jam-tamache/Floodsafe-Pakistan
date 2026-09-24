# English, Urdu, and Sindhi translations for FloodSafe Pakistan.

TRANSLATIONS = {
    "en": {
        "app_title": "FloodSafe Pakistan",
        "disclaimer_banner": (
            "This tool estimates risk from local rainfall totals only. It does "
            "not account for major river bund failures (Indus, Jhelum, Chenab) "
            "or northern Glacial Lake Outburst Floods (GLOFs). For river and "
            "glacial flood warnings, check official NDMA/PDMA alerts directly."
        ),
        "nav_home": "Home",
        "nav_about": "About",
        "nav_how_it_works": "How It Works",
        "nav_data_methodology": "Data & Methodology",
        "nav_map": "Map",

        # NEW - map page title/intro were hardcoded English in map.html
        # from the start, never wired to translations at all (unlike
        # every other page). Unreviewed by a native speaker, same as the
        # rest of the backlog.
        "map_title": "FloodSafe Pakistan \u2014 Map",
        "map_intro": "Color-coded by current risk level \u2014 click a marker for details. Grey pins are shown for map context only (outside Sindh, not risk-scored).",

        # NEW - map legend labels (check.html + map.html). Reuses the same
        # wording as risk_levels below for the 4 tiers, for consistency
        # with badges elsewhere in the app. legend_not_scored mirrors
        # about_callout's existing "not risk-scored" phrasing. Unreviewed
        # by a native speaker in ur/sd, same as the rest of the backlog.
        "legend_low": "Low Risk",
        "legend_moderate": "Moderate Risk",
        "legend_high": "High Risk",
        "legend_very_high": "Very High Risk",
        "legend_not_scored": "Not risk-scored",

        "city_names": {
            "karachi": "Karachi",
            "hyderabad": "Hyderabad",
            "badin": "Badin",
            "thatta": "Thatta",
            "sukkur": "Sukkur",
            "larkana": "Larkana",
            "nawabshah": "Nawabshah",
            "khairpur": "Khairpur",
            "dadu": "Dadu",
            "ghotki": "Ghotki",
            "moro": "Moro",
            "sakrand": "Sakrand",
            "kotri": "Kotri",
            "mirpurkhas": "Mirpurkhas",
            "shikarpur": "Shikarpur",
            "jamshoro": "Jamshoro",
            "naushahro feroze": "Naushahro Feroze",
            "tando allahyar": "Tando Allahyar",
            "tando muhammad khan": "Tando Muhammad Khan",
            "kashmore": "Kashmore",
            "ranipur": "Ranipur",
            "rohri": "Rohri",
            "shahdadkot": "Shahdadkot",
            "matiari": "Matiari",
            "jacobabad": "Jacobabad",
            "mithi": "Mithi",
            "umerkot": "Umerkot",
            "sanghar": "Sanghar",
            # Non-Sindh MAP_ONLY_CITIES (added this session) - map popups/tooltips only.
            "lahore": "Lahore",
            "islamabad": "Islamabad",
            "peshawar": "Peshawar",
            "quetta": "Quetta",
            "gwadar": "Gwadar",
            "pasni": "Pasni",
            "turbat": "Turbat",
            "sibi": "Sibi",
            "chaman": "Chaman",
            "cholistan": "Cholistan",
        },

        "form_city_label": "City:",
        "form_city_placeholder": "Enter city",
        "form_rainfall_label": "Rainfall (mm):",
        "form_rainfall_placeholder": "Enter rainfall",
        "form_submit": "Assess Flood Risk",
        "form_rainfall_hint": "e.g., 20, 50, 100, 150 mm",
        "forecast_form_submit": "Check Forecast Risk",
        "scenario_toggle_label": "Explore a scenario instead",
        "scenario_form_intro": "Enter a hypothetical rainfall amount to see how risk would change.",
        "forecast_toggle_label": "Or check today's live forecast instead",
        "forecast_toggle_intro": "We'll automatically pull the rainfall forecast for the next 72 hours for this city.",
        "city_label": "City:",
        "rainfall_label": "Rainfall:",
        "terrain_profile_label": "Terrain Profile:",
        "risk_level_label": "Risk Level:",
        "shelter_heading": "Shelter Information:",
        "safety_tips_heading": "Safety Tips:",
        "back_link": "Back",
        "error_both": "Please enter a valid city and rainfall.",
        "error_rainfall": "Please enter a valid rainfall (a positive number).",
        "error_city": "We couldn't find this location in our supported database.",
        "error_city_outside_coverage": (
            "This location is recognized, but our current risk model has only "
            "been validated for selected locations in Sindh."
        ),
        "forecast_error_unavailable": "We couldn't fetch a rainfall forecast right now. Try exploring a scenario instead.",
        "source_forecast": "Based on forecasted rainfall for the next {hours}h: {mm}mm expected.",
        "source_scenario": "Based on your hypothetical scenario of {mm}mm rainfall — not a real forecast.",
        # FIXED this session: rainfall max was shown as /70, but the real
        # rainfall ceiling is 54 (see RAINFALL_COMPONENT_MAX in app.py and
        # the "4. Why is the risk..." card, which already showed /54).
        "score_breakdown": "Score: {score}/100 (rainfall {rain}/54, elevation {elev}/30)",
        "how_calculated_toggle": "How is this calculated?",
        "explanation_with_elevation": "With {rainfall}mm of rain and {city} sitting on {elevation_position} compared to nearby areas, this adds up to {risk_level}.",
        "explanation_without_elevation": "With {rainfall}mm of rain expected for {city}, this adds up to {risk_level}.",
        "explanation_terrain_baseline": "{city}'s {risk_level} here is driven mainly by its {elevation_position} relative to nearby areas — actual forecasted rainfall is minimal, at just {rainfall}mm.",
        "elevation_position_low": "lower ground",
        "elevation_position_high": "higher ground",
        "risk_levels": {
            "Low Risk": "Low Risk",
            "Moderate Risk": "Moderate Risk",
            "High Risk": "High Risk",
            "Very High Risk": "Very High Risk",
        },
        "shelter_message": (
            "Specific shelter locations are not publicly listed by PDMA Sindh "
            "at a building level. In an emergency, call 1122 (Rescue Service) "
            "or check PDMA Sindh (pdma.gos.pk) / your district administration "
            "for the nearest active shelter."
        ),
        "safety_tips": {
            "Low Risk": [
                "No immediate danger, but keep an eye on local weather updates",
                "Clear roof drains and gutters in case rainfall picks up",
                "Keep your phone charged and stay informed on local advisories",
            ],
            "Moderate Risk": [
                "Move important documents (CNIC, land papers) to a high, dry place",
                "Keep emergency cash and a charged phone/power bank ready",
                "Avoid parking vehicles in low-lying or riverside areas",
                "Check on elderly neighbors and family who may need help evacuating",
            ],
            "High Risk": [
                "Evacuate immediately if local authorities issue a warning",
                "Never walk or drive through moving floodwater, even if it looks shallow",
                "Turn off electricity and gas at the mains before leaving home",
                "Call 1122 (Pakistan's emergency rescue service) if you're trapped or need help",
                "Follow evacuation guidance from PDMA Sindh / district administration - do not rely on this app for shelter locations",
            ],
            "Very High Risk": [
                "Evacuate immediately if local authorities issue a warning",
                "Never walk or drive through moving floodwater, even if it looks shallow",
                "Turn off electricity and gas at the mains before leaving home",
                "Call 1122 (Pakistan's emergency rescue service) if you're trapped or need help",
                "Follow evacuation guidance from PDMA Sindh / district administration - do not rely on this app for shelter locations",
            ],
        },
        # NEW this session: shown INSTEAD of safety_tips[risk] when rainfall
        # is negligible (see is_dry_conditions() in app.py). Deliberately
        # generic - every item is sensible on any day and none implies a
        # storm is coming. Applies to every city and every risk level.
        "safety_tips_dry_note": "No significant rain is involved in this assessment, so this rating reflects the area's terrain rather than an active flood threat. General preparedness tips:",
        "safety_tips_dry": [
            "Save emergency numbers: Rescue 1122 and PDMA Sindh (pdma.gos.pk)",
            "Keep copies of important documents (CNIC, land papers) in a waterproof bag",
            "Know your nearest higher ground and your evacuation route",
            "Check the forecast again if rain is expected",
        ],
        "terrain_warnings": {
            "Mega-Urban & Coastal": "Urban drainage systems can back up quickly - avoid clogged storm drains and underpasses.",
            "Central Agricultural Plains": "Low-lying farmland can pool water for days - keep livestock and stored grain away from field edges.",
            "Arid Plains & Deserts": "Dry, hard-packed ground sheds water fast - watch for sudden dry riverbed (nullah) overflows even hours after rain stops.",
        },
        "terrain_profile_labels": {
            "Mega-Urban & Coastal": "Mega-Urban & Coastal",
            "Central Agricultural Plains": "Central Agricultural Plains",
            "Arid Plains & Deserts": "Arid Plains & Deserts",
        },
                # UPDATED this session - reflects the elevation-rainfall scaling
        # fix (see risk_check.py / METHODOLOGY.md): elevation points now
        # only count in full once real rainfall is actually expected, so
        # {points} can change day to day for the same city as the rainfall
        # forecast changes, not just by which city was picked. Previously
        # this note implied a fixed number tied only to terrain position.
        "elevation_note_available": "{city} sits at {elevation}m. That is compared with other {profile} locations: the lower a city sits within its group, the more elevation points it can contribute (up to {max_points}). This only counts toward the score once real rainfall is expected — with little or no rain, elevation's contribution is scaled down, since low-lying terrain alone isn't a flood risk on a dry day. Right now it contributes {points} points. The bar above shows these points, not meters.",
        "elevation_note_unavailable": "Elevation data for {city} was not available - this score is based on rainfall alone.",
        "home_subtitle": "Get an estimate of flood risk for any supported Sindh city based on a live 72-hour rainfall forecast.",
        "about_title": "About This Project",
        "about_lede": "FloodSafe Pakistan is a scenario-based flood risk awareness tool, built to help people in Sindh understand how local rainfall could translate into flood risk.",
        "about_validated_heading": "Validated for Sindh",
        "about_validated_body": "The risk-scoring model is currently validated for Sindh only, using thresholds calibrated to Sindh's specific terrain and rainfall patterns. The app's architecture is built to extend to the rest of Pakistan, but that requires separately validating thresholds for each new region's terrain before scoring it — not yet done, and planned for a future version.",
        "about_warning_heading": "Not an Official Warning",
        "about_warning_body": "FloodSafe does not predict flooding with certainty and is not a substitute for official warnings from PDMA Sindh or your local authorities.",
        "about_callout": "Cities outside Sindh are shown on the map for geographic context only and are not risk-scored, for the same reason above — their terrain hasn't been validated against this model yet.",
        # NEW - About-page "why" section + link to the /floods-2022 page.
        # The 70 percent figure is from the World Bank/UNDP PDNA (Oct 2022);
        # it is cited on the floods_2022 page, which about_floods_link opens.
        "about_why_heading": "Why I built FloodSafe",
        "about_why_body_1": "The 2022 floods hit Sindh harder than any other province, with close to 70 percent of Pakistan's total flood damages and economic losses. I experienced them firsthand: large parts of my city were flooded and our electricity was out for seven days. I kept asking one question: what if people had access to clearer flood-risk information early enough to prepare?",
        "about_why_body_2": "FloodSafe estimates a city's flood risk from a rainfall scenario or a live 72-hour forecast, using rainfall and the city's elevation relative to nearby areas. It explains the result and provides practical safety guidance in English, Urdu, and Sindhi. It is a planning aid and does not replace official warnings from NDMA or PDMA.",
        "about_floods_link": "Read what happened in the 2022 floods",
        # NEW - full text of the /floods-2022 page (floods_2022.html). Figures are
        # from the World Bank/UNDP PDNA, UN OCHA and Britannica (see the page's
        # source list). English is the reference text; ur/sd are UNREVIEWED drafts.
        "floods_title": "The 2022 Floods",
        "floods_lede": "Between June and October 2022, record monsoon rains and glacier melt flooded Pakistan. Sindh was the worst-affected province.",
        "floods_what_heading": "What happened",
        "floods_what_body": "Unusually heavy monsoon rain, worsened by seasonal glacier runoff, caused the Indus River and its tributaries to flood. Rainfall in Sindh and Balochistan was about 4.5 times higher than normal, and roughly one third of the country was submerged.",
        "floods_pakistan_heading": "Across Pakistan",
        "floods_pakistan_body": "About 33 million people were affected and more than 1,700 lost their lives. Damages and economic losses exceeded USD 30 billion, and reconstruction needs exceeded USD 16 billion.",
        "floods_sindh_heading": "In Sindh",
        "floods_sindh_body": "Sindh accounted for close to 70 percent of total damages and losses. Of the more than 2 million houses affected nationwide, 89 percent were in Sindh: over 683,000 destroyed and over 1.1 million damaged. Nearly half of all recorded deaths were also in Sindh.",
        "floods_matters_heading": "Why this matters for FloodSafe",
        "floods_matters_body": "These are early assessments from October 2022 and the final figures may differ. FloodSafe is a planning aid that estimates flood risk from rainfall and elevation. It is not a forecast of flooding and does not replace official warnings from NDMA and PDMA.",
        "floods_sources_heading": "Sources",
        "how_it_works_title": "How It Works",
        "how_it_works_body_1": "FloodSafe estimates flood risk for Sindh cities from two factors: rainfall (either a live 72-hour forecast or a scenario you type in) and each city's elevation relative to nearby cities in the same terrain region. The two are combined into a single 0–1 score, which maps to Low, Moderate, High, or Very High risk.",
        "how_it_works_body_2": "Rainfall thresholds are project-defined, not sourced from an official government classification — they were derived by the developer and are documented, with reasoning, in the project's methodology notes. Elevation data comes from a public elevation API, looked up once per city.",
        "risk_map_heading": "Risk Map",
        "map_unavailable": "Map unavailable for this location.",
        "why_risk_heading": "Why is this rated {risk_level}?",
        "unit_mm": "mm",
        "impact_rainfall_label": "Rainfall score",
        "impact_elevation_label": "Elevation score",
        "impact_points_unit": "pts",
        "key_information_heading": "Key Information",
        "assessment_type_label": "Assessment Type:",
        "assessment_type_forecast": "Forecast (72h)",
        "assessment_type_scenario": "Scenario (not current rainfall)",

        "methodology_title": "Data & Methodology",
        "methodology_lede": "How a flood risk score actually gets calculated — in plain language, including what the model leaves out and where its limits are.",
        "methodology_scope_heading": "What this app covers",
        "methodology_scope_body": "FloodSafe Pakistan's risk scoring is built and checked for Sindh only. Cities outside Sindh — including major ones like Lahore, Islamabad, Peshawar, and Quetta — show up on the map for context, but deliberately don't get a risk score, because their terrain hasn't been checked against this model yet.",
        "methodology_not_prediction_heading": "This is not a flood prediction",
        "methodology_not_prediction_body": "FloodSafe estimates relative risk from a rainfall amount you give it — either a live 72-hour forecast, or a hypothetical number you type in yourself. It does not account for river embankment failures on the Indus, Jhelum, or Chenab, and it does not model glacial lake floods from the north. For those, check official NDMA or PDMA alerts directly.",
        "methodology_how_heading": "How a score is built",
        "methodology_how_body": "Every score combines two things: how much rain is expected over the next 72 hours, and how low-lying a city is compared to nearby cities with similar terrain. Rainfall can contribute up to 54 points, elevation up to 30, for a score out of 100. That number is then translated into one of four risk levels:",
        "methodology_72h_heading": "What \"72 hours\" means",
        "methodology_72h_body": "Every rainfall number this app scores — whether it's a live forecast or a number you type in yourself — represents a total over 72 hours, not a single day. Both modes mean the same thing, so a 50mm forecast and a 50mm scenario you type in are directly comparable.",
        "methodology_rainfall_heading": "Where the rainfall numbers come from",
        "methodology_rainfall_body_1": "Pakistan's Flood Forecasting Division publishes an official 24-hour rainfall scale — Light, Moderate, Heavy, Very Heavy, Extremely Heavy. FloodSafe's own thresholds are anchored to that scale, then scaled up to a 72-hour window using a standard rule of thumb (roughly ×1.73), rather than a rainfall curve measured specifically for Sindh.",
        "methodology_rainfall_body_2": "Because different terrain floods at different rainfall amounts, each of Sindh's three terrain types uses its own thresholds, shown below.",
        "methodology_rainfall_note": "The exact gap between regions is the developer's own judgment, not an independently measured figure — flagged here rather than presented as more precise than it is.",
        "methodology_table_region_header": "Terrain type",
        "methodology_table_low_header": "Moderate risk starts around",
        "methodology_table_medium_header": "High risk starts around",
        "methodology_table_tier_note": "These two numbers mark where Moderate and High risk typically begin from rainfall alone. Very High Risk isn't a separate rainfall threshold — it only happens when the combined rainfall-plus-elevation score crosses 75 out of 100 (see below). All four levels — Low, Moderate, High, and Very High — are used the same way everywhere in the app: the home page results, the map, and this page.",
        "methodology_example_heading": "A worked example",
                # UPDATED this session - matches the elevation-rainfall scaling fix
        # (see risk_check.py / METHODOLOGY.md). Total changed from 45.6 to
        # 34.4; classification (Moderate Risk) is unchanged. Previously this
        # example gave elevation full weight regardless of how little rain
        # was forecast, which is exactly the bug that was fixed.
        "methodology_example_body": "Say Karachi is forecast 25mm of rain over 72 hours. Its terrain type has a 40mm lower threshold, so 25mm scores about 15.6 of the rainfall component's first 25 points. If Karachi also happens to be the lowest-lying city in its terrain group, its elevation score would count for the full 30 points once rainfall reaches that same 40mm threshold — but at just 25mm, elevation's contribution is scaled down to about 18.8 of those 30 points, since low-lying terrain alone isn't treated as risky on a day with only light rain. Together, that's roughly 34.4 out of 100 — enough to land in the Moderate Risk range.",
        "methodology_deadzone_heading": "Why very heavy rain doesn't always spike the score",
        "methodology_deadzone_body": "Once rainfall passes a region's higher threshold, the rainfall component doesn't jump straight to its ceiling — it climbs gradually, reaching its maximum only once rainfall roughly doubles that threshold. This is a deliberate choice to avoid over-reacting to one extreme number, not a bug — but it's also not independently validated, and the project may revisit it later.",
        "methodology_ceiling_heading": "Why a perfect score is rare",
        "methodology_ceiling_body": "Because the rainfall component tops out at 54 points, not 70, the highest score this model can actually produce is about 84 out of 100 — not 100. Very High Risk (75-100) is still reachable, but only near the low end of that range. This is a real trade-off in how the score is built, not a bug.",
        "methodology_elevation_heading": "How elevation is scored",
        "methodology_elevation_body": "A city's elevation is compared only to other cities with the same terrain type, not the whole country — 7 meters means something different on the coast than it does inland. The lowest city in a group gets the most elevation points; the highest gets none. If elevation data isn't available for a city, the app says so directly and scores that city on rainfall alone, instead of guessing.",
        "methodology_not_modeled_heading": "What this model does not include",
        "methodology_not_modeled": [
            "Land use and land cover",
            "Drainage infrastructure or proximity to waterways",
            "Historical flood exposure as a live input",
            "River embankment failure risk (Indus, Jhelum, Chenab)",
            "Glacial Lake Outburst Floods (GLOFs)",
            "Repeated storms in a row — each 72-hour window is scored on its own",
        ],
        "methodology_limitations_heading": "Known limitations",
        "methodology_limitations": [
            "The spacing between regional rainfall thresholds is still developer judgment, not independently sourced",
            "The model has not yet been checked against real, documented flood events in Sindh",
            "A small number of cities' elevation values came from a backup data source instead of the primary one, though both use comparable satellite-based measurements",
        ],
        "methodology_validation_heading": "What \"validated\" means here",
        "methodology_validation_body": "In this project, it means the rainfall thresholds are tied to an official government classification through a stated method, and the scoring code is covered by automated tests. It does not mean the model has been checked against real floods in Sindh yet — that comparison is planned for after this first version.",
    },

    "ur": {
        "app_title": "فلڈ سیف پاکستان",
        "disclaimer_banner": (
            "یہ ٹول صرف مقامی بارش کے اعداد و شمار سے خطرے کا اندازہ لگاتا ہے۔ یہ دریاؤں کے بند "
            "ٹوٹنے (سندھ، جہلم، چناب) یا شمالی گلیشیئر جھیل کے سیلاب (GLOFs) کو شامل نہیں کرتا۔ "
            "دریائی اور گلیشیئر سیلاب کی وارننگ کے لیے براہ راست NDMA/PDMA الرٹس دیکھیں۔"
        ),
        "nav_home": "ہوم",
        "nav_about": "تعارف",
        "nav_how_it_works": "یہ کیسے کام کرتا ہے",
        "nav_data_methodology": "ڈیٹا اور طریقہ کار",
        "nav_map": "نقشہ",

        # NEW - map page title/intro were hardcoded English in map.html
        # from the start, never wired to translations at all (unlike
        # every other page). Unreviewed by a native speaker, same as the
        # rest of the backlog.
        "map_title": "فلڈ سیف پاکستان — نقشہ",
        "map_intro": "موجودہ خطرے کی سطح کے مطابق رنگ دیا گیا — تفصیلات کے لیے کسی نشان پر کلک کریں۔ سرمئی پن صرف نقشے کے تناظر کے لیے دکھائے گئے ہیں (سندھ سے باہر، خطرہ اسکور نہیں کیا گیا)۔",

        # NEW - unreviewed by a native speaker, same as the rest of the
        # translation backlog. Tier labels reuse risk_levels below for
        # consistency; legend_not_scored mirrors about_callout's phrasing.
        "legend_low": "کم خطرہ",
        "legend_moderate": "درمیانہ خطرہ",
        "legend_high": "شدید خطرہ",
        "legend_very_high": "انتہائی شدید خطرہ",
        "legend_not_scored": "خطرہ اسکور نہیں کیا گیا",

        "city_names": {
            "karachi": "کراچی",
            "hyderabad": "حیدرآباد",
            "badin": "بدین",
            "thatta": "ٹھٹھہ",
            "sukkur": "سکھر",
            "larkana": "لاڑکانہ",
            "nawabshah": "نوابشاہ",
            "khairpur": "خیرپور",
            "dadu": "دادو",
            "ghotki": "گھوٹکی",
            "moro": "مورو",
            "sakrand": "سکرنڈ",
            "kotri": "کوٹری",
            "mirpurkhas": "میرپورخاص",
            "shikarpur": "شکارپور",
            "jamshoro": "جامشورو",
            "naushahro feroze": "نوشہرو فیروز",
            "tando allahyar": "ٹنڈو الہ یار",
            "tando muhammad khan": "ٹنڈو محمد خان",
            "kashmore": "کشمور",
            "ranipur": "رانی پور",
            "rohri": "روہڑی",
            "shahdadkot": "شہداد کوٹ",
            "matiari": "مٹیاری",
            "jacobabad": "جیکب آباد",
            "mithi": "مٹھی",
            "umerkot": "عمرکوٹ",
            "sanghar": "سانگھڑ",
            # Non-Sindh MAP_ONLY_CITIES (added this session) - map popups/tooltips only.
            # UNREVIEWED by a native speaker (draft), same as the rest of the backlog.
            "lahore": "لاہور",
            "islamabad": "اسلام آباد",
            "peshawar": "پشاور",
            "quetta": "کوئٹہ",
            "gwadar": "گوادر",
            "pasni": "پسنی",
            "turbat": "تربت",
            "sibi": "سبی",
            "chaman": "چمن",
            "cholistan": "چولستان",
        },

        "form_city_label": "شہر:",
        "form_city_placeholder": "شہر درج کریں",
        "form_rainfall_label": "بارش (ملی میٹر):",
        "form_rainfall_placeholder": "بارش درج کریں",
        "form_submit": "خطرہ چیک کریں",
        "form_rainfall_hint": "مثال کے طور پر: 20، 50، 100، 150 ملی میٹر",
        "forecast_form_submit": "پیشگوئی خطرہ چیک کریں",
        "scenario_toggle_label": "بجائے اس کے ایک منظرنامہ آزمائیں",
        "scenario_form_intro": "خطرے میں تبدیلی دیکھنے کے لیے ایک فرضی بارش کی مقدار درج کریں۔",
        "forecast_toggle_label": "یا اس کے بجائے آج کی لائیو پیشگوئی چیک کریں",
        "forecast_toggle_intro": "ہم اس شہر کے لیے اگلے 72 گھنٹوں کی بارش کی پیشگوئی خودکار طور پر حاصل کریں گے۔",
        "city_label": "شہر:",
        "rainfall_label": "بارش:",
        "terrain_profile_label": "زمینی خصوصیات:",
        "risk_level_label": "خطرے کی سطح:",
        "shelter_heading": "پناہ گاہ کی معلومات:",
        "safety_tips_heading": "حفاظتی ہدایات:",
        "back_link": "واپس",
        "error_both": "براہ کرم درست شہر اور بارش درج کریں۔",
        "error_rainfall": "براہ کرم درست بارش درج کریں (ایک مثبت نمبر)۔",
        "error_city": "یہ مقام ہمارے ڈیٹا بیس میں نہیں ملا۔",
        "error_city_outside_coverage": (
            "یہ مقام تسلیم شدہ ہے، لیکن ہمارا موجودہ رسک ماڈل فی الحال صرف "
            "سندھ کے منتخب مقامات کے لیے تصدیق شدہ ہے۔"
        ),
        "forecast_error_unavailable": "ہم اس وقت بارش کی پیشگوئی حاصل نہیں کر سکے۔ براہ کرم اس کے بجائے ایک منظرنامہ آزمائیں۔",
        "source_forecast": "اگلے {hours} گھنٹوں کی پیشگوئی شدہ بارش پر مبنی: متوقع {mm} ملی میٹر۔",
        "source_scenario": "آپ کے فرضی منظرنامے پر مبنی جس میں {mm} ملی میٹر بارش شامل ہے - یہ حقیقی پیشگوئی نہیں ہے۔",
        # FIXED this session: rainfall max was /70, real ceiling is 54.
        "score_breakdown": "اسکور: {score}/100 (بارش {rain}/54، بلندی {elev}/30)",
        "how_calculated_toggle": "یہ کیسے شمار کیا جاتا ہے؟",
        "explanation_with_elevation": "{rainfall} ملی میٹر بارش اور {city} کا آس پاس کے علاقوں کے مقابلے میں {elevation_position} پر ہونا، یہ مل کر {risk_level} بنتا ہے۔",
        "explanation_without_elevation": "{city} کے لیے متوقع {rainfall} ملی میٹر بارش کے ساتھ، یہ {risk_level} بنتا ہے۔",
        "explanation_terrain_baseline": "{city} میں {risk_level} بنیادی طور پر اس کی {elevation_position} کی وجہ سے ہے — متوقع بارش صرف {rainfall} ملی میٹر ہے، یعنی نہ ہونے کے برابر۔",
        "elevation_position_low": "نچلی زمین",
        "elevation_position_high": "اونچی زمین",
        "risk_levels": {
            "Low Risk": "کم خطرہ",
            "Moderate Risk": "درمیانہ خطرہ",
            "High Risk": "شدید خطرہ",
            "Very High Risk": "انتہائی شدید خطرہ",
        },
        "shelter_message": (
            "PDMA سندھ کی جانب سے مخصوص پناہ گاہوں کی عمارتوں کی فہرست عام نہیں کی گئی۔ "
            "ہنگامی صورتحال میں 1122 (ریسکیو سروس) پر کال کریں یا قریب ترین فعال پناہ گاہ کے "
            "لیے PDMA سندھ (pdma.gos.pk) یا اپنی ضلعی انتظامیہ سے رابطہ کریں۔"
        ),
        "safety_tips": {
            "Low Risk": [
                "فوری خطرہ نہیں، لیکن مقامی موسمی اپڈیٹس پر نظر رکھیں",
                "بارش بڑھنے کی صورت میں چھت کے نالوں اور گٹروں کو صاف رکھیں",
                "اپنا فون چارج رکھیں اور مقامی انتباہات سے باخبر رہیں",
            ],
            "Moderate Risk": [
                "اہم دستاویزات (شناختی کارڈ، زمین کے کاغذات) کو اونچی، خشک جگہ پر منتقل کریں",
                "ہنگامی نقدی اور چارج شدہ فون/پاور بینک تیار رکھیں",
                "نشیبی یا دریا کنارے علاقوں میں گاڑی پارک کرنے سے گریز کریں",
                "بزرگ ہمسایوں اور خاندان کی خبر گیری کریں جنہیں انخلا میں مدد کی ضرورت ہو سکتی ہے",
            ],
            "High Risk": [
                "اگر مقامی حکام وارننگ جاری کریں تو فوری طور پر نکل جائیں",
                "بہتے ہوئے سیلابی پانی میں کبھی پیدل یا گاڑی سے نہ جائیں، چاہے وہ اتھلا نظر آئے",
                "گھر چھوڑنے سے پہلے مین سوئچ سے بجلی اور گیس بند کر دیں",
                "اگر پھنس جائیں یا مدد درکار ہو تو 1122 (پاکستان کی ہنگامی ریسکیو سروس) پر کال کریں",
                "PDMA سندھ / ضلعی انتظامیہ کی انخلا ہدایات پر عمل کریں - پناہ گاہ کی جگہ کے لیے صرف اس ایپ پر انحصار نہ کریں",
            ],
            "Very High Risk": [
                "اگر مقامی حکام وارننگ جاری کریں تو فوری طور پر نکل جائیں",
                "بہتے ہوئے سیلابی پانی میں کبھی پیدل یا گاڑی سے نہ جائیں، چاہے وہ اتھلا نظر آئے",
                "گھر چھوڑنے سے پہلے مین سوئچ سے بجلی اور گیس بند کر دیں",
                "اگر پھنس جائیں یا مدد درکار ہو تو 1122 (پاکستان کی ہنگامی ریسکیو سروس) پر کال کریں",
                "PDMA سندھ / ضلعی انتظامیہ کی انخلا ہدایات پر عمل کریں - پناہ گاہ کی جگہ کے لیے صرف اس ایپ پر انحصار نہ کریں",
            ],
        },
        # NEW this session - UNREVIEWED by a native speaker (draft).
        "safety_tips_dry_note": "اس تشخیص میں بارش نہ ہونے کے برابر ہے، اس لیے یہ درجہ بندی علاقے کی زمینی ساخت کو ظاہر کرتی ہے، سیلاب کے کسی فوری خطرے کو نہیں۔ عمومی تیاری کی ہدایات:",
        "safety_tips_dry": [
            "ہنگامی نمبر محفوظ کر لیں: ریسکیو 1122 اور PDMA سندھ (pdma.gos.pk)",
            "اہم دستاویزات (شناختی کارڈ، زمین کے کاغذات) کی نقول واٹر پروف تھیلے میں رکھیں",
            "اپنے قریب ترین اونچے مقام اور انخلا کے راستے سے واقف رہیں",
            "اگر بارش متوقع ہو تو پیشگوئی دوبارہ چیک کریں",
        ],
        "terrain_warnings": {
            "Mega-Urban & Coastal": "شہری نکاسی آب کا نظام جلد بھر سکتا ہے - بند نالوں اور انڈرپاسز سے بچیں۔",
            "Central Agricultural Plains": "نشیبی زرعی زمین میں پانی کئی دنوں تک جمع رہ سکتا ہے - مویشیوں اور ذخیرہ شدہ اناج کو کھیتوں کے کناروں سے دور رکھیں۔",
            "Arid Plains & Deserts": "خشک، سخت زمین پانی کو تیزی سے بہا دیتی ہے - بارش رکنے کے کئی گھنٹوں بعد بھی اچانک خشک نالوں کے بہاؤ کا خیال رکھیں۔",
        },
        "terrain_profile_labels": {
            "Mega-Urban & Coastal": "بڑے شہری اور ساحلی علاقے",
            "Central Agricultural Plains": "وسطی زرعی میدانی علاقے",
            "Arid Plains & Deserts": "خشک میدانی اور صحرائی علاقے",
        },
                # UPDATED this session - UNREVIEWED by a native speaker (draft),
        # same as the rest of the backlog. Mirrors the EN fix: elevation
        # points now only count in full once real rainfall is expected.
        "elevation_note_available": "{city} کی بلندی {elevation} میٹر ہے۔ اس کا موازنہ دیگر {profile} مقامات سے کیا جاتا ہے: گروپ میں جتنی نچلی جگہ ہو، اتنے ہی زیادہ بلندی پوائنٹس (زیادہ سے زیادہ {max_points}) شامل ہو سکتے ہیں۔ لیکن یہ پوائنٹس اسکور میں تبھی پورے شامل ہوتے ہیں جب واقعی بارش متوقع ہو - کم یا نہ ہونے کے برابر بارش کی صورت میں بلندی کا حصہ کم کر دیا جاتا ہے، کیونکہ صرف نشیبی زمین خشک دن میں سیلابی خطرہ نہیں بنتی۔ اس وقت یہ {points} پوائنٹس شامل کر رہی ہے۔ اوپر کی پٹی میٹر نہیں بلکہ یہی پوائنٹس دکھاتی ہے۔",
        "elevation_note_unavailable": "{city} کے لیے بلندی کا ڈیٹا دستیاب نہیں تھا - یہ اسکور صرف بارش پر مبنی ہے۔",
        "home_subtitle": "کسی بھی معاون سندھ شہر کے لیے لائیو 72 گھنٹے کی بارش کی پیشگوئی کی بنیاد پر سیلاب کے خطرے کا اندازہ حاصل کریں۔",
        "about_title": "اس منصوبے کے بارے میں",
        "about_lede": "فلڈ سیف پاکستان ایک منظرنامے پر مبنی سیلاب کے خطرے سے آگاہی کا ٹول ہے، جو سندھ کے لوگوں کو یہ سمجھنے میں مدد دینے کے لیے بنایا گیا ہے کہ مقامی بارش کس طرح سیلاب کے خطرے میں تبدیل ہو سکتی ہے۔",
        "about_validated_heading": "سندھ کے لیے تصدیق شدہ",
        "about_validated_body": "رسک اسکورنگ ماڈل فی الحال صرف سندھ کے لیے تصدیق شدہ ہے، جو سندھ کی مخصوص زمینی خصوصیات اور بارش کے انداز کے مطابق ترتیب دیا گیا ہے۔ ایپ کا ڈھانچہ باقی پاکستان تک وسعت دینے کے لیے بنایا گیا ہے، لیکن اس کے لیے ہر نئے علاقے کی زمینی خصوصیات کی الگ سے تصدیق درکار ہے - جو ابھی نہیں کی گئی اور مستقبل کے ورژن کے لیے مجوزہ ہے۔",
        "about_warning_heading": "یہ کوئی سرکاری وارننگ نہیں ہے",
        "about_warning_body": "فلڈ سیف یقین کے ساتھ سیلاب کی پیشگوئی نہیں کرتا اور PDMA سندھ یا آپ کے مقامی حکام کی سرکاری وارننگز کا متبادل نہیں ہے۔",
        "about_callout": "سندھ سے باہر کے شہر صرف جغرافیائی حوالے کے لیے نقشے پر دکھائے گئے ہیں اور ان کا خطرہ اسکور نہیں کیا گیا - اسی وجہ سے جیسا کہ اوپر بتایا گیا، ان کی زمینی خصوصیات ابھی اس ماڈل کے خلاف تصدیق شدہ نہیں ہیں۔",
        # NEW - UNREVIEWED by a native speaker (my draft), same as the rest
        # of the backlog.
        "about_why_heading": "میں نے فلڈ سیف کیوں بنایا",
        "about_why_body_1": "2022 کے سیلاب نے سندھ کو کسی بھی دوسرے صوبے سے زیادہ متاثر کیا؛ پاکستان کے کل سیلابی نقصانات اور معاشی خسارے کا تقریباً 70 فیصد سندھ میں ہوا۔ میں نے یہ سیلاب خود جھیلا: میرے شہر کے بڑے حصے زیرِ آب آ گئے اور ہماری بجلی سات دن تک بند رہی۔ میں ایک ہی سوال پوچھتا رہا: اگر لوگوں کو سیلاب کے خطرے کی واضح معلومات تیاری کے لیے کافی پہلے مل جاتیں تو کیا ہوتا؟",
        "about_why_body_2": "فلڈ سیف بارش کے کسی منظرنامے یا لائیو 72 گھنٹے کی پیشگوئی کی بنیاد پر، بارش اور آس پاس کے علاقوں کے مقابلے میں شہر کی بلندی کو استعمال کرتے ہوئے، شہر کے سیلابی خطرے کا اندازہ لگاتا ہے۔ یہ نتیجے کی وضاحت کرتا ہے اور انگریزی، اردو اور سندھی میں عملی حفاظتی ہدایات فراہم کرتا ہے۔ یہ منصوبہ بندی میں مدد کا ذریعہ ہے اور NDMA یا PDMA کی سرکاری وارننگز کا متبادل نہیں۔",
        "about_floods_link": "2022 کے سیلاب میں کیا ہوا، پڑھیں",
        # NEW - full text of the /floods-2022 page (floods_2022.html). Figures are
        # from the World Bank/UNDP PDNA, UN OCHA and Britannica (see the page's
        # source list). ur/sd are UNREVIEWED drafts - check the numbers as well as
        # the wording before relying on them.
        "floods_title": "2022 کے سیلاب",
        "floods_lede": "جون سے اکتوبر 2022 کے دوران ریکارڈ مون سون بارشوں اور گلیشیئر پگھلنے سے پاکستان میں سیلاب آیا۔ سندھ سب سے زیادہ متاثر ہونے والا صوبہ تھا۔",
        "floods_what_heading": "کیا ہوا",
        "floods_what_body": "غیر معمولی طور پر شدید مون سون بارشوں اور موسمی گلیشیئر پگھلاؤ کے باعث دریائے سندھ اور اس کے معاون دریاؤں میں سیلاب آ گیا۔ سندھ اور بلوچستان میں بارش معمول سے تقریباً 4.5 گنا زیادہ ہوئی، اور ملک کا تقریباً ایک تہائی حصہ زیرِ آب آ گیا۔",
        "floods_pakistan_heading": "پورے پاکستان میں",
        "floods_pakistan_body": "تقریباً 3 کروڑ 30 لاکھ (33 ملین) افراد متاثر ہوئے اور 1,700 سے زائد افراد جاں بحق ہوئے۔ نقصانات اور معاشی خسارہ 30 ارب امریکی ڈالر سے زیادہ رہا، اور بحالی و تعمیرِ نو کی ضروریات 16 ارب ڈالر سے زیادہ تھیں۔",
        "floods_sindh_heading": "سندھ میں",
        "floods_sindh_body": "پاکستان کے کل نقصانات اور معاشی خسارے کا تقریباً 70 فیصد سندھ میں ہوا۔ ملک بھر میں متاثر ہونے والے 20 لاکھ سے زائد گھروں میں سے 89 فیصد سندھ میں تھے: 6 لاکھ 83 ہزار سے زائد گھر تباہ ہوئے اور 11 لاکھ سے زائد کو نقصان پہنچا۔ ریکارڈ شدہ اموات کا تقریباً نصف بھی سندھ میں ہوا۔",
        "floods_matters_heading": "فلڈ سیف کے لیے یہ کیوں اہم ہے",
        "floods_matters_body": "یہ اکتوبر 2022 کے ابتدائی تخمینے ہیں اور حتمی اعداد و شمار مختلف ہو سکتے ہیں۔ فلڈ سیف منصوبہ بندی میں مدد کا ایک ذریعہ ہے جو بارش اور بلندی کی بنیاد پر سیلاب کے خطرے کا اندازہ لگاتا ہے۔ یہ سیلاب کی پیشگوئی نہیں ہے اور NDMA اور PDMA کی سرکاری وارننگز کا متبادل نہیں۔",
        "floods_sources_heading": "ذرائع",
        "how_it_works_title": "یہ کیسے کام کرتا ہے",
        "how_it_works_body_1": "فلڈ سیف سندھ کے شہروں کے لیے دو عوامل سے سیلاب کے خطرے کا اندازہ لگاتا ہے: بارش (یا تو 72 گھنٹے کی لائیو پیشگوئی یا آپ کا درج کردہ منظرنامہ) اور ہر شہر کی بلندی اسی زمینی خطے کے قریبی شہروں کے مقابلے میں۔ یہ دونوں مل کر ایک 0 سے 1 تک کا اسکور بناتے ہیں، جو کم، درمیانہ، شدید، یا انتہائی شدید خطرے میں تبدیل ہوتا ہے۔",
        "how_it_works_body_2": "بارش کی حدیں منصوبے کے اپنے طے کردہ ہیں، کسی سرکاری درجہ بندی سے حاصل شدہ نہیں - یہ ڈویلپر نے مرتب کی ہیں اور ان کی وجوہات منصوبے کے طریقہ کار کے نوٹس میں دستاویزی ہیں۔ بلندی کا ڈیٹا ایک عوامی بلندی API سے حاصل کیا جاتا ہے، جو ہر شہر کے لیے ایک بار حاصل کیا جاتا ہے۔",
        "risk_map_heading": "خطرے کا نقشہ",
        "map_unavailable": "اس مقام کے لیے نقشہ دستیاب نہیں۔",
        "why_risk_heading": "یہ {risk_level} کیوں ہے؟",
        "unit_mm": "ملی میٹر",
        "impact_rainfall_label": "بارش کا اسکور",
        "impact_elevation_label": "بلندی کا اسکور",
        "impact_points_unit": "پوائنٹس",
        "key_information_heading": "اہم معلومات",
        "assessment_type_label": "تشخیص کی قسم:",
        "assessment_type_forecast": "پیشگوئی (72 گھنٹے)",
        "assessment_type_scenario": "منظرنامہ (موجودہ بارش نہیں)",

        "methodology_title": "ڈیٹا اور طریقہ کار",
        "methodology_lede": "سیلاب کے خطرے کا اسکور دراصل کیسے شمار کیا جاتا ہے — سادہ زبان میں، بشمول اس کے کہ ماڈل کیا شامل نہیں کرتا اور اس کی حدود کہاں ہیں۔",
        "methodology_scope_heading": "یہ ایپ کیا شامل کرتی ہے",
        "methodology_scope_body": "فلڈ سیف پاکستان کا رسک اسکورنگ صرف سندھ کے لیے بنایا اور جانچا گیا ہے۔ سندھ سے باہر کے شہر — بشمول لاہور، اسلام آباد، پشاور اور کوئٹہ جیسے بڑے شہر — نقشے پر صرف حوالے کے لیے دکھائے جاتے ہیں، لیکن جان بوجھ کر انہیں کوئی رسک اسکور نہیں دیا جاتا، کیونکہ ان کی زمینی خصوصیات ابھی اس ماڈل کے خلاف جانچی نہیں گئیں۔",
        "methodology_not_prediction_heading": "یہ سیلاب کی پیشگوئی نہیں ہے",
        "methodology_not_prediction_body": "فلڈ سیف آپ کی فراہم کردہ بارش کی مقدار سے متعلقہ خطرے کا اندازہ لگاتا ہے — یا تو ایک لائیو 72 گھنٹے کی پیشگوئی، یا آپ کا خود درج کردہ ایک فرضی نمبر۔ یہ دریائے سندھ، جہلم یا چناب کے بند ٹوٹنے کا حساب نہیں رکھتا، اور نہ ہی شمال کے گلیشیئر جھیل کے سیلاب (GLOFs) کا ماڈل بناتا ہے۔ ان کے لیے براہ راست سرکاری NDMA یا PDMA الرٹس دیکھیں۔",
        "methodology_how_heading": "اسکور کیسے بنایا جاتا ہے",
        "methodology_how_body": "ہر اسکور دو چیزوں کو ملاتا ہے: اگلے 72 گھنٹوں میں متوقع بارش، اور اسی طرح کی زمینی خصوصیات رکھنے والے قریبی شہروں کے مقابلے میں شہر کی پستی۔ بارش زیادہ سے زیادہ 54 پوائنٹس اور بلندی زیادہ سے زیادہ 30 پوائنٹس شامل کر سکتی ہے، جو مجموعی طور پر 100 میں سے ایک اسکور بنتا ہے۔ یہ نمبر پھر چار خطرے کی سطحوں میں سے ایک میں تبدیل کیا جاتا ہے:",
        "methodology_72h_heading": "\"72 گھنٹے\" کا کیا مطلب ہے",
        "methodology_72h_body": "یہ ایپ جو بھی بارش کا نمبر شمار کرتی ہے — چاہے وہ لائیو پیشگوئی ہو یا آپ کا خود درج کردہ نمبر — وہ 72 گھنٹوں کا مجموعہ ظاہر کرتا ہے، نہ کہ ایک دن کا۔ دونوں طریقے ایک ہی چیز کا مطلب رکھتے ہیں، اس لیے 50 ملی میٹر کی پیشگوئی اور آپ کا خود درج کردہ 50 ملی میٹر کا منظرنامہ براہ راست موازنہ کے قابل ہیں۔",
        "methodology_rainfall_heading": "بارش کے نمبر کہاں سے آتے ہیں",
        "methodology_rainfall_body_1": "پاکستان کا فلڈ فورکاسٹنگ ڈویژن ایک سرکاری 24 گھنٹے کی بارش کی درجہ بندی جاری کرتا ہے — کم، درمیانہ، شدید، بہت شدید، انتہائی شدید۔ فلڈ سیف کی اپنی حدیں اسی درجہ بندی سے منسلک ہیں، پھر انہیں ایک معیاری اصول (تقریباً ×1.73) کے ذریعے 72 گھنٹے کی مدت کے لیے بڑھایا جاتا ہے، نہ کہ خاص طور پر سندھ کے لیے ناپی گئی بارش کی کوئی وکر۔",
        "methodology_rainfall_body_2": "چونکہ مختلف زمینی خصوصیات مختلف مقدار میں بارش پر سیلاب کا شکار ہوتی ہیں، سندھ کی تینوں زمینی اقسام اپنی اپنی حدیں استعمال کرتی ہیں، جو نیچے دکھائی گئی ہیں۔",
        "methodology_rainfall_note": "علاقوں کے درمیان درست فرق ڈویلپر کا اپنا فیصلہ ہے، کوئی آزادانہ طور پر ناپا گیا نمبر نہیں — یہاں اسے واضح طور پر بتایا جا رہا ہے بجائے اس کے کہ اسے زیادہ درست ظاہر کیا جائے۔",
        "methodology_table_region_header": "زمینی قسم",
        "methodology_table_low_header": "درمیانہ خطرہ یہاں سے شروع ہوتا ہے",
        "methodology_table_medium_header": "شدید خطرہ یہاں سے شروع ہوتا ہے",
        "methodology_table_tier_note": "یہ دونوں نمبر ظاہر کرتے ہیں کہ صرف بارش کی بنیاد پر درمیانہ اور شدید خطرہ عام طور پر کہاں سے شروع ہوتا ہے۔ انتہائی شدید خطرہ کوئی الگ بارش کی حد نہیں ہے — یہ تب ہوتا ہے جب بارش اور بلندی کا مجموعی اسکور 100 میں سے 75 سے تجاوز کر جائے (نیچے دیکھیں)۔ چاروں سطحیں — کم، درمیانہ، شدید، اور انتہائی شدید — پوری ایپ میں ایک ہی طرح استعمال ہوتی ہیں: ہوم پیج کے نتائج، نقشہ، اور یہ صفحہ۔",
        "methodology_example_heading": "ایک مثال",
                # UPDATED this session - UNREVIEWED by a native speaker (draft),
        # same as the rest of the backlog. Matches the EN fix: total
        # changed from 45.6 to 34.4, classification unchanged.
        "methodology_example_body": "فرض کریں کراچی کے لیے اگلے 72 گھنٹوں میں 25 ملی میٹر بارش کی پیشگوئی ہے۔ اس کی زمینی قسم کی نچلی حد 40 ملی میٹر ہے، تو 25 ملی میٹر بارش کے پہلے 25 پوائنٹس میں سے تقریباً 15.6 پوائنٹس بنتے ہیں۔ اگر کراچی اپنے زمینی گروپ میں سب سے نچلے مقام پر بھی ہو، تو اس کی بلندی کا اسکور اسی 40 ملی میٹر کی حد تک بارش پہنچنے پر ہی پورے 30 پوائنٹس شمار ہو گا - لیکن صرف 25 ملی میٹر پر، بلندی کا حصہ گھٹ کر تقریباً 18.8 پوائنٹس رہ جاتا ہے، کیونکہ ہلکی بارش والے دن میں صرف نشیبی زمین کو خطرناک نہیں سمجھا جاتا۔ ملا کر یہ 100 میں سے تقریباً 34.4 بنتا ہے - جو درمیانہ خطرے کی حد میں آنے کے لیے کافی ہے۔",
        "methodology_deadzone_heading": "شدید بارش ہمیشہ اسکور کو کیوں نہیں بڑھاتی",
        "methodology_deadzone_body": "جب بارش کسی علاقے کی بالائی حد سے تجاوز کر جائے، تو بارش کا حصہ فوری طور پر اپنی زیادہ سے زیادہ حد تک نہیں پہنچتا - یہ آہستہ آہستہ بڑھتا ہے، اور اپنی زیادہ سے زیادہ حد تک تب پہنچتا ہے جب بارش اس حد سے تقریباً دگنی ہو جائے۔ یہ ایک جان بوجھ کر کیا گیا فیصلہ ہے تاکہ ایک انتہائی نمبر پر حد سے زیادہ ردعمل نہ ہو، کوئی خرابی نہیں - لیکن یہ بھی آزادانہ طور پر تصدیق شدہ نہیں ہے، اور منصوبہ مستقبل میں اس پر نظرثانی کر سکتا ہے۔",
        "methodology_ceiling_heading": "ایک مکمل اسکور کیوں نایاب ہے",
        "methodology_ceiling_body": "چونکہ بارش کا حصہ 70 نہیں بلکہ 54 پوائنٹس پر ختم ہوتا ہے، اس ماڈل کا سب سے زیادہ ممکنہ اسکور تقریباً 100 میں سے 84 ہے، 100 نہیں۔ انتہائی شدید خطرہ (75-100) اب بھی حاصل کیا جا سکتا ہے، لیکن صرف اس حد کے نچلے سرے کے قریب۔ یہ اسکور بننے کے طریقے میں ایک حقیقی سمجھوتہ ہے، کوئی خرابی نہیں۔",
        "methodology_elevation_heading": "بلندی کیسے شمار کی جاتی ہے",
        "methodology_elevation_body": "کسی شہر کی بلندی کا موازنہ صرف اسی طرح کی زمینی خصوصیات رکھنے والے دیگر شہروں سے کیا جاتا ہے، پورے ملک سے نہیں - ساحل پر 7 میٹر کا مطلب اندرون ملک سے مختلف ہوتا ہے۔ گروپ میں سب سے نچلے شہر کو سب سے زیادہ بلندی پوائنٹس ملتے ہیں؛ سب سے اونچے کو کوئی نہیں ملتا۔ اگر کسی شہر کے لیے بلندی کا ڈیٹا دستیاب نہ ہو، تو ایپ یہ واضح طور پر بتاتی ہے اور اس شہر کا اسکور صرف بارش پر بناتی ہے، اندازہ لگانے کے بجائے۔",
        "methodology_not_modeled_heading": "یہ ماڈل کیا شامل نہیں کرتا",
        "methodology_not_modeled": [
            "زمین کا استعمال اور زمینی احاطہ",
            "نکاسی آب کا بنیادی ڈھانچہ یا آبی گزرگاہوں سے قربت",
            "تاریخی سیلابی نمائش بطور لائیو ان پٹ",
            "دریائے سندھ، جہلم، چناب کے بند ٹوٹنے کا خطرہ",
            "گلیشیئر جھیل کے سیلاب (GLOFs)",
            "لگاتار طوفان — ہر 72 گھنٹے کی مدت کو الگ سے شمار کیا جاتا ہے",
        ],
        "methodology_limitations_heading": "معلوم حدود",
        "methodology_limitations": [
            "علاقائی بارش کی حدوں کے درمیان فرق اب بھی ڈویلپر کا فیصلہ ہے، کوئی آزادانہ ذریعہ نہیں",
            "ماڈل کو ابھی تک سندھ کے حقیقی، دستاویزی سیلابی واقعات کے خلاف نہیں جانچا گیا",
            "چند شہروں کی بلندی کی قدریں بنیادی ذریعے کے بجائے ایک متبادل ڈیٹا ذریعے سے حاصل کی گئیں، اگرچہ دونوں موازنہ کے قابل سیٹلائٹ پر مبنی پیمائش استعمال کرتے ہیں",
        ],
        "methodology_validation_heading": "یہاں \"تصدیق شدہ\" کا کیا مطلب ہے",
        "methodology_validation_body": "اس منصوبے میں، اس کا مطلب یہ ہے کہ بارش کی حدیں ایک بیان کردہ طریقے کے ذریعے ایک سرکاری درجہ بندی سے منسلک ہیں، اور اسکورنگ کوڈ خودکار ٹیسٹس سے ڈھکا ہوا ہے۔ اس کا یہ مطلب نہیں کہ ماڈل کو سندھ میں حقیقی سیلابوں کے خلاف جانچا گیا ہے - یہ موازنہ اس پہلے ورژن کے بعد کے لیے مجوزہ ہے۔",
    },

    "sd": {
        "app_title": "فلڊ سيف پاڪستان",
        "disclaimer_banner": (
            "هي اوزار فقط مقامي برسات جي انگن اکرن مان خطري جو اندازو لڳائيندو آهي. هي درياهي "
            "بند ٽٽڻ (سنڌو، جهلم، چناب) يا اترين برفاني ڍنڍ جي سيلاب (GLOFs) کي شامل نٿو ڪري. "
            "درياهي ۽ برفاني سيلاب جي وارننگ لاءِ سڌو سنئون NDMA/PDMA اطلاعات ڏسو."
        ),
        "nav_home": "گهر",
        "nav_about": "تعارف",
        "nav_how_it_works": "هي ڪيئن ڪم ڪري ٿو",
        "nav_data_methodology": "ڊيٽا ۽ طريقيڪار",
        "nav_map": "نقشو",

        # NEW - map page title/intro were hardcoded English in map.html
        # from the start, never wired to translations at all (unlike
        # every other page). Unreviewed by a native speaker, same as the
        # rest of the backlog.
        "map_title": "فلڊ سيف پاڪستان — نقشو",
        "map_intro": "موجوده خطري جي سطح مطابق رنگ ڏنل — تفصيل لاءِ ڪنهن نشان تي ڪلڪ ڪريو. سرمائي پن رڳو نقشي جي حوالي لاءِ ڏيکاريا ويا آهن (سنڌ کان ٻاهر، خطرو اسڪور نه ڪيل).",

        # NEW - unreviewed by a native speaker, same as the rest of the
        # translation backlog. Tier labels reuse risk_levels below for
        # consistency; legend_not_scored mirrors about_callout's phrasing.
        "legend_low": "گھٽ خطرو",
        "legend_moderate": "وچولو خطرو",
        "legend_high": "وڏو خطرو",
        "legend_very_high": "تمام وڏو خطرو",
        "legend_not_scored": "خطرو اسڪور نه ڪيل",

        "city_names": {
            "karachi": "ڪراچي",
            "hyderabad": "حيدرآباد",
            "badin": "بدين",
            "thatta": "ٺٽو",
            "sukkur": "سکر",
            "larkana": "لاڙڪاڻو",
            "nawabshah": "نوابشاهه",
            "khairpur": "خيرپور",
            "dadu": "دادو",
            "ghotki": "گھوٽڪي",
            "moro": "مورو",
            "sakrand": "سڪرنڊ",
            "kotri": "ڪوٽڙي",
            "mirpurkhas": "ميرپور خاص",
            "shikarpur": "شڪارپور",
            "jamshoro": "ڄامشورو",
            "naushahro feroze": "نوشھرو فيروز",
            "tando allahyar": "ٽنڊو الھيار",
            "tando muhammad khan": "ٽنڊو محمد خان",
            "kashmore": "ڪشمور",
            "ranipur": "راڻيپور",
            "rohri": "روهڙي",
            "shahdadkot": "شھدادڪوٽ",
            "matiari": "مٽياري",
            "jacobabad": "جيڪب آباد",
            "mithi": "مٺي",
            "umerkot": "عمرڪوٽ",
            "sanghar": "سانگھڙ",
            # Non-Sindh MAP_ONLY_CITIES (added this session) - map popups/tooltips only.
            # UNREVIEWED by a native speaker (draft), same as the rest of the backlog.
            "lahore": "لاهور",
            "islamabad": "اسلام آباد",
            "peshawar": "پشاور",
            "quetta": "ڪوئٽا",
            "gwadar": "گوادر",
            "pasni": "پسني",
            "turbat": "تربت",
            "sibi": "سبي",
            "chaman": "چمن",
            "cholistan": "چولستان",
        },

        "form_city_label": "شهر:",
        "form_city_placeholder": "شهر داخل ڪريو",
        "form_rainfall_label": "برسات (ملي ميٽر):",
        "form_rainfall_placeholder": "برسات داخل ڪريو",
        "form_submit": "خطرو چيڪ ڪريو",
        "form_rainfall_hint": "مثال طور: 20، 50، 100، 150 ملي ميٽر",
        "forecast_form_submit": "اڳڪٿي خطرو چيڪ ڪريو",
        "scenario_toggle_label": "ان جي بدران هڪ منظرنامو آزمايو",
        "scenario_form_intro": "خطري ۾ تبديلي ڏسڻ لاءِ هڪ فرضي برسات جي مقدار داخل ڪريو.",
        "forecast_toggle_label": "يا ان جي بدران اڄ جي لائيو اڳڪٿي چيڪ ڪريو",
        "forecast_toggle_intro": "اسان هن شهر لاءِ ايندڙ 72 ڪلاڪن جي برسات جي اڳڪٿي خودڪار طور تي حاصل ڪنداسين.",
        "city_label": "شهر:",
        "rainfall_label": "برسات:",
        "terrain_profile_label": "زميني خاصيتون:",
        "risk_level_label": "خطري جو درجو:",
        "shelter_heading": "پناهگاهه جي معلومات:",
        "safety_tips_heading": "حفاظتي هدايتون:",
        "back_link": "واپس",
        "error_both": "مهرباني ڪري صحيح شهر ۽ برسات داخل ڪريو.",
        "error_rainfall": "مهرباني ڪري صحيح برسات داخل ڪريو (هڪ مثبت انگ).",
        "error_city": "هي هنڌ اسان جي ڊيٽابيس ۾ نه ملي سگهيو.",
        "error_city_outside_coverage": (
            "هي هنڌ سڃاتل آهي، پر اسان جو موجوده رسڪ ماڊل فقط سنڌ جي "
            "چونڊيل هنڌن لاءِ تصديق ٿيل آهي."
        ),
        "forecast_error_unavailable": "اسان هن وقت برسات جي اڳڪٿي حاصل نه ڪري سگهياسين. مهرباني ڪري ان جي بدران هڪ منظرنامو آزمايو.",
        "source_forecast": "ايندڙ {hours} ڪلاڪن جي اڳڪٿي ٿيل برسات تي ٻڌل: متوقع {mm} ملي ميٽر.",
        "source_scenario": "توهان جي فرضي منظرنامي تي ٻڌل جنهن ۾ {mm} ملي ميٽر برسات شامل آهي - هي حقيقي اڳڪٿي ناهي.",
        # FIXED this session: rainfall max was /70, real ceiling is 54.
        "score_breakdown": "اسڪور: {score}/100 (برسات {rain}/54، بلندي {elev}/30)",
        "how_calculated_toggle": "هي ڪيئن ڳڻيو ويندو آهي؟",
        "explanation_with_elevation": "{rainfall} ملي ميٽر برسات ۽ {city} جو ڀرپاسي وارن علائقن جي مقابلي ۾ {elevation_position} تي هجڻ، هي گڏجي {risk_level} ٿو ٺاهي.",
        "explanation_without_elevation": "{city} لاءِ متوقع {rainfall} ملي ميٽر برسات سان، هي {risk_level} ٿو ٺاهي.",
        "explanation_terrain_baseline": "{city} ۾ {risk_level} خاص طور تي ان جي {elevation_position} سبب آهي — متوقع برسات فقط {rainfall} ملي ميٽر آهي، يعني نه هجڻ جي برابر.",
        "elevation_position_low": "هيٺاهين زمين",
        "elevation_position_high": "مٿاهين زمين",
        "risk_levels": {
            "Low Risk": "گھٽ خطرو",
            "Moderate Risk": "وچولو خطرو",
            "High Risk": "وڏو خطرو",
            "Very High Risk": "تمام وڏو خطرو",
        },
        "shelter_message": (
            "PDMA سنڌ پاران مخصوص پناهگاهن جي عمارتن جي فهرست عام نه ڪئي وئي آهي. هنگامي حالت "
            "۾ 1122 (ريسڪيو سروس) تي ڪال ڪريو يا ويجهي پناهگاهه لاءِ PDMA سنڌ (pdma.gos.pk) "
            "يا پنهنجي ضلعي انتظاميه سان رابطو ڪريو."
        ),
        "safety_tips": {
            "Low Risk": [
                "فوري خطرو ناهي، پر مقامي موسمي اپڊيٽس تي نظر رکو",
                "برسات وڌڻ جي صورت ۾ ڇت جا نالا ۽ گٽر صاف رکو",
                "پنهنجو فون چارج رکو ۽ مقامي اطلاعن کان باخبر رهو",
            ],
            "Moderate Risk": [
                "اهم دستاويز (شناختي ڪارڊ، زمين جا ڪاغذ) مٿاهين، سڪل جاءِ تي منتقل ڪريو",
                "هنگامي نقد ۽ چارج ٿيل فون/پاور بينڪ تيار رکو",
                "هيٺاهين يا درياءَ ڪناري وارن علائقن ۾ گاڏي پارڪ ڪرڻ کان بچو",
                "پوڙها پاڙيسري ۽ خاندان جن کي لڏپلاڻ ۾ مدد گهربل هجي، انهن جي خبر گيري ڪريو",
            ],
            "High Risk": [
                "جيڪڏهن مقامي اختيارين وارننگ جاري ڪئي ته فوري طور تي نڪري وڃو",
                "وهندڙ سيلابي پاڻي مان ڪڏهن به پيادل يا گاڏي ذريعي نه گذرو، توڻي اهو گھٽ نظر اچي",
                "گهر ڇڏڻ کان اڳ مين سوئچ مان بجلي ۽ گئس بند ڪريو",
                "جيڪڏهن ڦاسي پيا يا مدد گهرجي ته 1122 (پاڪستان جي هنگامي ريسڪيو سروس) تي ڪال ڪريو",
                "PDMA سنڌ / ضلعي انتظاميه جي لڏپلاڻ هدايتن تي عمل ڪريو - پناهگاهه جي جاءِ لاءِ رڳو هن ايپ تي ڀروسو نه ڪريو",
            ],
            "Very High Risk": [
                "جيڪڏهن مقامي اختيارين وارننگ جاري ڪئي ته فوري طور تي نڪري وڃو",
                "وهندڙ سيلابي پاڻي مان ڪڏهن به پيادل يا گاڏي ذريعي نه گذرو، توڻي اهو گھٽ نظر اچي",
                "گهر ڇڏڻ کان اڳ مين سوئچ مان بجلي ۽ گئس بند ڪريو",
                "جيڪڏهن ڦاسي پيا يا مدد گهرجي ته 1122 (پاڪستان جي هنگامي ريسڪيو سروس) تي ڪال ڪريو",
                "PDMA سنڌ / ضلعي انتظاميه جي لڏپلاڻ هدايتن تي عمل ڪريو - پناهگاهه جي جاءِ لاءِ رڳو هن ايپ تي ڀروسو نه ڪريو",
            ],
        },
        # NEW this session - UNREVIEWED by a native speaker (draft).
        "safety_tips_dry_note": "هن جانچ ۾ برسات نه هجڻ جي برابر آهي، تنهنڪري هي درجو علائقي جي زميني بناوت کي ظاهر ڪري ٿو، سيلاب جي ڪنهن فوري خطري کي نه. عام تياري جون هدايتون:",
        "safety_tips_dry": [
            "هنگامي نمبر محفوظ ڪريو: ريسڪيو 1122 ۽ PDMA سنڌ (pdma.gos.pk)",
            "اهم دستاويزن (شناختي ڪارڊ، زمين جا ڪاغذ) جون نقلون واٽر پروف ٿيلهي ۾ رکو",
            "پنهنجي ويجهي مٿاهين جاءِ ۽ لڏپلاڻ جي رستي کان واقف رهو",
            "جيڪڏهن برسات متوقع هجي ته اڳڪٿي ٻيهر چيڪ ڪريو",
        ],
        "terrain_warnings": {
            "Mega-Urban & Coastal": "شهري نيڪال جو نظام جلدي ڀرجي سگهي ٿو - بند نالن ۽ انڊرپاسز کان بچو.",
            "Central Agricultural Plains": "هيٺاهين زرعي زمين ۾ پاڻي ڪيترن ڏينهن تائين بيهي سگهي ٿو - ڍورن ۽ ذخيرو ٿيل اناج کي فيلڊ جي ڪنارن کان پري رکو.",
            "Arid Plains & Deserts": "سڪل، سخت زمين پاڻي کي تيزيءَ سان وهائي ٿي - برسات بند ٿيڻ کان ڪلاڪن پوءِ به اوچتو سڪل نالن جي وهڪري جو خيال رکو.",
        },
        "terrain_profile_labels": {
            "Mega-Urban & Coastal": "وڏا شهري ۽ ساحلي علائقا",
            "Central Agricultural Plains": "مرڪزي زرعي ميدان",
            "Arid Plains & Deserts": "سڪل ميدان ۽ ريگستان",
        },
                # UPDATED this session - UNREVIEWED by a native speaker (draft; my
        # Sindhi is weaker than my Urdu), same as the rest of the backlog.
        # Mirrors the EN fix: elevation points now only count in full once
        # real rainfall is expected.
        "elevation_note_available": "{city} جي بلندي {elevation} ميٽر آهي. ان جو مقابلو ٻين {profile} هنڌن سان ڪيو ويندو آهي: گروپ ۾ جيترو هيٺاهون هجي، اوترا وڌيڪ بلندي پوائنٽ (وڌ ۾ وڌ {max_points}) شامل ٿي سگهن ٿا. پر هي پوائنٽ اسڪور ۾ تڏهن پورا شامل ٿين ٿا جڏهن واقعي برسات جي اميد هجي - گھٽ يا نه هجڻ جي برابر برسات جي صورت ۾ بلندي جو حصو گھٽايو ويندو آهي، ڇاڪاڻ ته فقط هيٺاهين زمين سڪل ڏينهن ۾ سيلابي خطرو نٿي بڻجي. هن وقت هي {points} پوائنٽ شامل ڪري رهي آهي. مٿي واري پٽي ميٽر نه پر اهي ئي پوائنٽ ڏيکاري ٿي.",
        "elevation_note_unavailable": "{city} لاءِ بلندي جو ڊيٽا موجود نه هو - هي اسڪور فقط برسات تي ٻڌل آهي.",
        "home_subtitle": "ڪنهن به سپورٽ ٿيل سنڌ جي شهر لاءِ لائيو 72 ڪلاڪن جي برسات جي اڳڪٿي جي بنياد تي سيلاب جي خطري جو اندازو حاصل ڪريو.",
        "about_title": "هن منصوبي بابت",
        "about_lede": "فلڊ سيف پاڪستان هڪ منظرنامي تي ٻڌل سيلاب جي خطري بابت آگاهي جو اوزار آهي، جيڪو سنڌ جي ماڻهن کي اهو سمجهڻ ۾ مدد ڏيڻ لاءِ ٺاهيو ويو آهي ته مقامي برسات ڪيئن سيلاب جي خطري ۾ تبديل ٿي سگهي ٿي.",
        "about_validated_heading": "سنڌ لاءِ تصديق ٿيل",
        "about_validated_body": "رسڪ اسڪورنگ ماڊل في الحال فقط سنڌ لاءِ تصديق ٿيل آهي، جيڪو سنڌ جي مخصوص زميني خاصيتن ۽ برسات جي نمونن مطابق ترتيب ڏنو ويو آهي. ايپ جو ڍانچو باقي پاڪستان تائين وڌائڻ لاءِ ٺاهيو ويو آهي، پر ان لاءِ هر نئين علائقي جي زميني خاصيتن جي الڳ تصديق گهرجي - جيڪا اڃا نه ٿي آهي ۽ ايندڙ ورجن لاءِ رٿيل آهي.",
        "about_warning_heading": "هي ڪا سرڪاري وارننگ ناهي",
        "about_warning_body": "فلڊ سيف يقين سان سيلاب جي اڳڪٿي نٿو ڪري ۽ PDMA سنڌ يا توهان جي مقامي اختيارين جي سرڪاري وارننگن جو متبادل ناهي.",
        "about_callout": "سنڌ کان ٻاهر جا شهر رڳو جاگرافيائي حوالي لاءِ نقشي تي ڏيکاريا ويا آهن ۽ انهن جو خطرو اسڪور نه ڪيو ويو آهي - ساڳئي سبب مطابق جيئن مٿي ٻڌايو ويو، سندن زميني خاصيتون اڃا هن ماڊل خلاف تصديق ٿيل ناهن.",
        # NEW - UNREVIEWED by a native speaker (my draft; my Sindhi is weaker
        # than my Urdu). Uses "سيلاب" for flood to match the rest of this
        # file, although "ٻوڏ" is the more idiomatic Sindhi word - a native
        # reviewer should decide.
        "about_why_heading": "مون فلڊ سيف ڇو ٺاهيو",
        "about_why_body_1": "2022 جي سيلاب سنڌ کي ٻين سڀني صوبن کان وڌيڪ متاثر ڪيو؛ پاڪستان جي ڪل سيلابي نقصانن ۽ معاشي خساري جو تقريباً 70 سيڪڙو سنڌ ۾ ٿيو. مون اهو سيلاب پاڻ ڏٺو: منهنجي شهر جا وڏا حصا پاڻيءَ هيٺ اچي ويا ۽ اسان جي بجلي ست ڏينهن بند رهي. مان هڪ ئي سوال پڇندو رهيس: جيڪڏهن ماڻهن کي سيلاب جي خطري بابت صاف معلومات تياريءَ لاءِ ڪافي اڳ ملي وڃي ها ته ڇا ٿئي ها؟",
        "about_why_body_2": "فلڊ سيف برسات جي ڪنهن منظرنامي يا لائيو 72 ڪلاڪن جي اڳڪٿي جي بنياد تي، برسات ۽ ڀرپاسي جي علائقن جي مقابلي ۾ شهر جي بلندي استعمال ڪندي، شهر جي سيلاب جي خطري جو اندازو لڳائي ٿو. هي نتيجي جي وضاحت ڪري ٿو ۽ انگريزي، اردو ۽ سنڌي ۾ عملي حفاظتي هدايتون ڏئي ٿو. هي منصوبابندي ۾ مدد جو ذريعو آهي ۽ NDMA يا PDMA جي سرڪاري وارننگن جو متبادل ناهي.",
        "about_floods_link": "2022 جي سيلاب ۾ ڇا ٿيو، پڙهو",
        # NEW - full text of the /floods-2022 page (floods_2022.html). Figures are
        # from the World Bank/UNDP PDNA, UN OCHA and Britannica (see the page's
        # source list). ur/sd are UNREVIEWED drafts - check the numbers as well as
        # the wording before relying on them.
        "floods_title": "2022 جو سيلاب",
        "floods_lede": "جون کان آڪٽوبر 2022 دوران رڪارڊ مون سون برساتن ۽ گليشيئر جي ڳرڻ سبب پاڪستان ۾ سيلاب آيو. سنڌ سڀ کان وڌيڪ متاثر ٿيندڙ صوبو هو.",
        "floods_what_heading": "ڇا ٿيو",
        "floods_what_body": "غير معمولي طور تي تمام وڏين مون سون برساتن ۽ موسمي گليشيئر ڳرڻ سبب درياءُ سنڌو ۽ ان جي شاخن ۾ سيلاب اچي ويو. سنڌ ۽ بلوچستان ۾ برسات معمول کان تقريباً 4.5 ڀيرا وڌيڪ ٿي، ۽ ملڪ جو تقريباً ٽيون حصو پاڻيءَ هيٺ اچي ويو.",
        "floods_pakistan_heading": "سڄي پاڪستان ۾",
        "floods_pakistan_body": "تقريباً 3 ڪروڙ 30 لک (33 ملين) ماڻهو متاثر ٿيا ۽ 1,700 کان وڌيڪ ماڻهو مري ويا. نقصان ۽ معاشي خسارو 30 ارب آمريڪي ڊالرن کان وڌيڪ رهيو، ۽ بحالي ۽ ٻيهر تعمير جون ضرورتون 16 ارب ڊالرن کان وڌيڪ هيون.",
        "floods_sindh_heading": "سنڌ ۾",
        "floods_sindh_body": "پاڪستان جي ڪل نقصان ۽ معاشي خساري جو تقريباً 70 سيڪڙو سنڌ ۾ ٿيو. سڄي ملڪ ۾ متاثر ٿيل 20 لک کان وڌيڪ گهرن مان 89 سيڪڙو سنڌ ۾ هئا: 6 لک 83 هزار کان وڌيڪ گهر تباهه ٿيا ۽ 11 لک کان وڌيڪ کي نقصان پهتو. رڪارڊ ٿيل موتن جو تقريباً اڌ به سنڌ ۾ ٿيو.",
        "floods_matters_heading": "فلڊ سيف لاءِ هي ڇو اهم آهي",
        "floods_matters_body": "هي آڪٽوبر 2022 جا شروعاتي اندازا آهن ۽ حتمي انگ مختلف ٿي سگهن ٿا. فلڊ سيف منصوبابندي ۾ مدد جو هڪ ذريعو آهي جيڪو برسات ۽ بلندي جي بنياد تي سيلاب جي خطري جو اندازو لڳائي ٿو. هي سيلاب جي اڳڪٿي ناهي ۽ NDMA ۽ PDMA جي سرڪاري وارننگن جو متبادل ناهي.",
        "floods_sources_heading": "ماخذ",
        "how_it_works_title": "هي ڪيئن ڪم ڪري ٿو",
        "how_it_works_body_1": "فلڊ سيف سنڌ جي شهرن لاءِ ٻن عنصرن مان سيلاب جي خطري جو اندازو لڳائي ٿو: برسات (يا ته 72 ڪلاڪن جي لائيو اڳڪٿي يا توهان جو داخل ڪيل منظرنامو) ۽ هر شهر جي بلندي ساڳئي زميني علائقي جي ويجهن شهرن جي مقابلي ۾. ٻئي گڏجي هڪ 0 کان 1 تائين اسڪور ٺاهين ٿا، جيڪو گھٽ، وچولو، وڏو، يا تمام وڏو خطري ۾ تبديل ٿئي ٿو.",
        "how_it_works_body_2": "برسات جون حدون منصوبي جون پنهنجون مقرر ڪيل آهن، ڪنهن به سرڪاري درجه بندي مان حاصل ٿيل نه آهن - اهي ڊولپر پاران مرتب ڪيون ويون آهن ۽ سندن دليل منصوبي جي طريقيڪار جي نوٽس ۾ دستاويز ٿيل آهن. بلندي جو ڊيٽا هڪ عوامي بلندي API مان حاصل ڪيو ويندو آهي، جيڪو هر شهر لاءِ هڪ ڀيرو حاصل ڪيو ويندو آهي.",
        "risk_map_heading": "خطري جو نقشو",
        "map_unavailable": "هن هنڌ لاءِ نقشو دستياب ناهي.",
        "why_risk_heading": "هي {risk_level} ڇو آهي؟",
        "unit_mm": "ملي ميٽر",
        "impact_rainfall_label": "برسات جو اسڪور",
        "impact_elevation_label": "بلندي جو اسڪور",
        "impact_points_unit": "پوائنٽ",
        "key_information_heading": "اهم معلومات",
        "assessment_type_label": "جانچ جو قسم:",
        "assessment_type_forecast": "اڳڪٿي (72 ڪلاڪ)",
        "assessment_type_scenario": "منظرنامو (موجوده برسات ناهي)",

        "methodology_title": "ڊيٽا ۽ طريقيڪار",
        "methodology_lede": "سيلاب جي خطري جو اسڪور اصل ۾ ڪيئن ڳڻيو ويندو آهي — سادي ٻولي ۾، بشمول ان جي ته ماڊل ۾ ڇا شامل ناهي ۽ ان جون حدون ڪٿي آهن.",
        "methodology_scope_heading": "هي ايپ ڇا شامل ڪري ٿي",
        "methodology_scope_body": "فلڊ سيف پاڪستان جو رسڪ اسڪورنگ رڳو سنڌ لاءِ ٺاهيو ۽ جانچيو ويو آهي. سنڌ کان ٻاهر جا شهر — بشمول لاهور، اسلام آباد، پشاور ۽ ڪوئٽا جهڙا وڏا شهر — نقشي تي رڳو حوالي لاءِ ڏيکاريا وڃن ٿا، پر ڄاڻي واڻي انهن کي ڪو به رسڪ اسڪور نه ڏنو وڃي ٿو، ڇاڪاڻ ته سندن زميني خاصيتون اڃا هن ماڊل خلاف نه جانچيون ويون آهن.",
        "methodology_not_prediction_heading": "هي سيلاب جي اڳڪٿي ناهي",
        "methodology_not_prediction_body": "فلڊ سيف توهان جي ڏنل برسات جي مقدار مان لاڳاپيل خطري جو اندازو لڳائي ٿو — يا ته هڪ لائيو 72 ڪلاڪن جي اڳڪٿي، يا توهان جو پاڻ داخل ڪيل هڪ فرضي انگ. هي درياءُ سنڌو، جهلم يا چناب جي بند ٽٽڻ جو حساب نٿو رکي، ۽ نه ئي اتر جي برفاني ڍنڍ جي سيلاب (GLOFs) جو ماڊل ٺاهي ٿو. انهن لاءِ سڌو سنئون سرڪاري NDMA يا PDMA اطلاعات ڏسو.",
        "methodology_how_heading": "اسڪور ڪيئن ٺاهيو ويندو آهي",
        "methodology_how_body": "هر اسڪور ٻن شين کي گڏ ڪري ٿو: ايندڙ 72 ڪلاڪن ۾ متوقع برسات، ۽ ساڳئي زميني خاصيتن وارن ويجهن شهرن جي مقابلي ۾ شهر جي هيٺاهين. برسات وڌ ۾ وڌ 54 پوائنٽ ۽ بلندي وڌ ۾ وڌ 30 پوائنٽ شامل ڪري سگهي ٿي، جيڪو ڪل 100 مان هڪ اسڪور ٺاهي ٿو. هي انگ پوءِ چئن خطري جي سطحن مان هڪ ۾ تبديل ڪيو ويندو آهي:",
        "methodology_72h_heading": "\"72 ڪلاڪن\" جو مطلب ڇا آهي",
        "methodology_72h_body": "هي ايپ جيڪو به برسات جو انگ ڳڻي ٿي — ڀلي اهو لائيو اڳڪٿي هجي يا توهان جو پاڻ داخل ڪيل انگ — اهو 72 ڪلاڪن جو مجموعو ظاهر ڪري ٿو، هڪ ڏينهن جو نه. ٻئي طريقا ساڳي شيءِ جو مطلب رکن ٿا، تنهنڪري 50 ملي ميٽر جي اڳڪٿي ۽ توهان جو پاڻ داخل ڪيل 50 ملي ميٽر جو منظرنامو سِڌو سنئون مقابلي جوڳا آهن.",
        "methodology_rainfall_heading": "برسات جا انگ ڪٿان اچن ٿا",
        "methodology_rainfall_body_1": "پاڪستان جو فلڊ فورڪاسٽنگ ڊويزن هڪ سرڪاري 24 ڪلاڪن جي برسات جي درجه بندي جاري ڪري ٿو — گھٽ، وچولو، وڏو، تمام وڏو، انتهائي وڏو. فلڊ سيف جون پنهنجون حدون ان ساڳئي درجه بندي سان ڳنڍيل آهن، پوءِ انهن کي هڪ معياري اصول (تقريباً ×1.73) ذريعي 72 ڪلاڪن جي مدت لاءِ وڌايو ويندو آهي، نه ڪا خاص طور تي سنڌ لاءِ ماپيل برسات جي وکر.",
        "methodology_rainfall_body_2": "ڇاڪاڻ ته مختلف زميني خاصيتون مختلف مقدار ۾ برسات تي سيلاب جو شڪار ٿينديون آهن، سنڌ جون ٽئي زميني قسمون پنهنجون پنهنجون حدون استعمال ڪن ٿيون، جيڪي هيٺ ڏيکاريل آهن.",
        "methodology_rainfall_note": "علائقن جي وچ ۾ صحيح فرق ڊولپر جو پنهنجو فيصلو آهي، ڪو به آزاد طور تي ماپيل انگ ناهي — هتي ان کي واضح طور تي ٻڌايو پيو وڃي بجاءِ ان جي ته ان کي وڌيڪ صحيح ڪري ڏيکاريو وڃي.",
        "methodology_table_region_header": "زميني قسم",
        "methodology_table_low_header": "وچولو خطرو هتان کان شروع ٿئي ٿو",
        "methodology_table_medium_header": "وڏو خطرو هتان کان شروع ٿئي ٿو",
        "methodology_table_tier_note": "هي ٻئي انگ ڏيکارين ٿا ته رڳو برسات جي بنياد تي وچولو ۽ وڏو خطرو عام طور تي ڪٿان شروع ٿئي ٿو. تمام وڏو خطرو ڪا الڳ برسات جي حد ناهي — هي تڏهن ٿئي ٿو جڏهن برسات ۽ بلندي جو گڏيل اسڪور 100 مان 75 کان لنگهي وڃي (هيٺ ڏسو). چارئي سطحون — گھٽ، وچولو، وڏو، ۽ تمام وڏو — سڄي ايپ ۾ ساڳئي طرح استعمال ٿين ٿيون: هوم پيج جا نتيجا، نقشو، ۽ هي صفحو.",
        "methodology_example_heading": "هڪ مثال",
                # UPDATED this session - UNREVIEWED by a native speaker (draft; my
        # Sindhi is weaker than my Urdu), same as the rest of the backlog.
        # Matches the EN fix: total changed from 45.6 to 34.4,
        # classification unchanged.
        "methodology_example_body": "فرض ڪريو ڪراچي لاءِ ايندڙ 72 ڪلاڪن ۾ 25 ملي ميٽر برسات جي اڳڪٿي آهي. ان جي زميني قسم جي هيٺين حد 40 ملي ميٽر آهي، تنهنڪري 25 ملي ميٽر برسات جي پهرين 25 پوائنٽن مان تقريباً 15.6 پوائنٽ ٺهن ٿا. جيڪڏهن ڪراچي پنهنجي زميني گروپ ۾ سڀ کان هيٺاهين هنڌ تي به هجي، ته ان جي بلندي جو اسڪور ان ساڳئي 40 ملي ميٽر حد تائين برسات پهچڻ تي ئي پورا 30 پوائنٽ ٿيندو - پر فقط 25 ملي ميٽر تي، بلندي جو حصو گھٽجي تقريباً 18.8 پوائنٽ رهجي وڃي ٿو، ڇاڪاڻ ته هلڪي برسات وارن ڏينهن ۾ رڳو هيٺاهين زمين کي خطرناڪ نه سمجهيو ويندو آهي. گڏي هي 100 مان تقريباً 34.4 ٿئي ٿو - جيڪو وچولي خطري جي حد ۾ اچڻ لاءِ ڪافي آهي.",
        "methodology_deadzone_heading": "تمام وڏي برسات هميشه اسڪور کي ڇو نٿي وڌائي",
        "methodology_deadzone_body": "جڏهن برسات ڪنهن علائقي جي مٿينءَ حد کان لنگهي وڃي، ته برسات جو حصو سِڌو سنئون پنهنجي وڌ ۾ وڌ حد تائين نٿو پهچي - هي آهستي آهستي وڌي ٿو، ۽ پنهنجي وڌ ۾ وڌ حد تائين تڏهن پهچي ٿو جڏهن برسات ان حد کان تقريباً ٻيڻي ٿي وڃي. هي هڪ ڄاڻي واڻي ڪيل فيصلو آهي ته جيئن هڪ انتهائي انگ تي حد کان وڌيڪ ردعمل نه ٿئي، ڪا خرابي ناهي - پر هي پڻ آزاد طور تي تصديق ٿيل ناهي، ۽ منصوبو مستقبل ۾ ان تي نظرثاني ڪري سگهي ٿو.",
        "methodology_ceiling_heading": "هڪ مڪمل اسڪور ڇو ناياب آهي",
        "methodology_ceiling_body": "ڇاڪاڻ ته برسات جو حصو 70 نه پر 54 پوائنٽن تي ختم ٿئي ٿو، هن ماڊل جو وڌ ۾ وڌ ممڪن اسڪور تقريباً 100 مان 84 آهي، 100 ناهي. تمام وڏو خطرو (75-100) اڃا حاصل ٿي سگهي ٿو، پر رڳو ان حد جي هيٺين ڇيڙي جي ويجهو. هي اسڪور ٺهڻ جي طريقي ۾ هڪ حقيقي سمجهوتو آهي، ڪا خرابي ناهي.",
        "methodology_elevation_heading": "بلندي ڪيئن ڳڻي ويندي آهي",
        "methodology_elevation_body": "ڪنهن شهر جي بلندي جو مقابلو رڳو ساڳئي زميني خاصيتن وارن ٻين شهرن سان ڪيو ويندو آهي، سڄي ملڪ سان نه - ساحل تي 7 ميٽر جو مطلب اندرون ملڪ کان مختلف هوندو آهي. گروپ ۾ سڀ کان هيٺاهين شهر کي بلندي جا سڀ کان وڌيڪ پوائنٽ ملن ٿا؛ سڀ کان مٿاهين کي ڪو نه ملي. جيڪڏهن ڪنهن شهر لاءِ بلندي جو ڊيٽا موجود نه هجي، ته ايپ اهو واضح طور تي ٻڌائي ٿي ۽ ان شهر جو اسڪور رڳو برسات تي ٺاهي ٿي، اندازو لڳائڻ جي بدران.",
        "methodology_not_modeled_heading": "هي ماڊل ڇا شامل نٿو ڪري",
        "methodology_not_modeled": [
            "زمين جو استعمال ۽ زميني ڍڪ",
            "نيڪال جو بنيادي ڍانچو يا پاڻياٺ گذرگاهن سان ويجهڙائي",
            "تاريخي سيلابي نمائش بطور لائيو ان پٽ",
            "درياءُ سنڌو، جهلم، چناب جي بند ٽٽڻ جو خطرو",
            "برفاني ڍنڍ جو سيلاب (GLOFs)",
            "لڳاتار طوفان — هر 72 ڪلاڪن جي مدت کي الڳ ڳڻيو ويندو آهي",
        ],
        "methodology_limitations_heading": "ڄاڻايل حدون",
        "methodology_limitations": [
            "علائقائي برسات جي حدن جي وچ ۾ فرق اڃا به ڊولپر جو فيصلو آهي، ڪو آزاد ذريعو ناهي",
            "ماڊل کي اڃا تائين سنڌ جي حقيقي، دستاويزي سيلابي واقعن خلاف نه جاچيو ويو آهي",
            "ڪجهه شهرن جي بلندي جون قدرون بنيادي ذريعي بدران هڪ متبادل ڊيٽا ذريعي مان حاصل ڪيون ويون، جيتوڻيڪ ٻئي ذريعا مقابلي جوڳا سيٽلائيٽ تي ٻڌل ماپون استعمال ڪن ٿا",
        ],
        "methodology_validation_heading": "هتي \"تصديق ٿيل\" جو مطلب ڇا آهي",
        "methodology_validation_body": "هن منصوبي ۾، ان جو مطلب اهو آهي ته برسات جون حدون هڪ ٻڌايل طريقي ذريعي هڪ سرڪاري درجه بندي سان ڳنڍيل آهن، ۽ اسڪورنگ ڪوڊ خودڪار ٽيسٽن سان ڍڪيل آهي. ان جو اهو مطلب ناهي ته ماڊل کي سنڌ ۾ حقيقي سيلابن خلاف جاچيو ويو آهي - هي مقابلو هن پهرين ورجن کان پوءِ لاءِ رٿيل آهي.",
    },
}

SUPPORTED_LANGUAGES = ["en", "ur", "sd"]
DEFAULT_LANGUAGE = "en"


def get_translation(lang_code):
    """Return the translation dict for a language code, falling back to English."""
    return TRANSLATIONS.get(lang_code, TRANSLATIONS[DEFAULT_LANGUAGE])