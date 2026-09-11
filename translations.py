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
        "score_breakdown": "Score: {score}/100 (rainfall {rain}/70, elevation {elev}/30)",
        "how_calculated_toggle": "How is this calculated?",
        "explanation_with_elevation": "With {rainfall}mm of rain and {city} sitting on {elevation_position} compared to nearby areas, this adds up to {risk_level}.",
        "explanation_without_elevation": "With {rainfall}mm of rain expected for {city}, this adds up to {risk_level}.",
        # NEW this session - see build_plain_explanation()'s docstring in
        # risk_check.py for when this fires. NOT native-speaker reviewed
        # (English original either, since it's new copy this session).
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
        "elevation_note_available": "Elevation for {city} ({elevation}m) was factored into this score relative to other {profile} locations.",
        "elevation_note_unavailable": "Elevation data for {city} was not available - this score is based on rainfall alone.",

        # ---- Home page (index.html) - NEW this batch. Flagged live via
        # screenshot: this subtitle was hardcoded English in index.html
        # with NO {{ t.key }} usage at all, same missing-mechanism class
        # of bug the About/How It Works pages had before. Key added here;
        # index.html itself still needs editing to use it - not done yet,
        # pending that file. NOT native-speaker reviewed.
        "home_subtitle": "Get an estimate of flood risk for any supported Sindh city based on a live 72-hour rainfall forecast.",

        # ---- About page (about.html) - NEW this batch. Was previously
        # hardcoded English directly in the template with no ur/sd
        # equivalent at all - not a missing-key gap, a missing-mechanism
        # gap. NOT native-speaker reviewed (English original either, since
        # it's new copy this session).
        "about_title": "About This Project",
        "about_lede": "FloodSafe Pakistan is a scenario-based flood risk awareness tool, built to help people in Sindh understand how local rainfall could translate into flood risk.",
        "about_validated_heading": "Validated for Sindh",
        "about_validated_body": "The risk-scoring model is currently validated for Sindh only, using thresholds calibrated to Sindh's specific terrain and rainfall patterns. The app's architecture is built to extend to the rest of Pakistan, but that requires separately validating thresholds for each new region's terrain before scoring it — not yet done, and planned for a future version.",
        "about_warning_heading": "Not an Official Warning",
        "about_warning_body": "FloodSafe does not predict flooding with certainty and is not a substitute for official warnings from PDMA Sindh or your local authorities.",
        "about_callout": "Cities outside Sindh are shown on the map for geographic context only and are not risk-scored, for the same reason above — their terrain hasn't been validated against this model yet.",

        # ---- How It Works page (how_it_works.html) - NEW this batch,
        # same hardcoded-with-no-translation-mechanism gap as About.
        "how_it_works_title": "How It Works",
        "how_it_works_body_1": "FloodSafe estimates flood risk for Sindh cities from two factors: rainfall (either a live 72-hour forecast or a scenario you type in) and each city's elevation relative to nearby cities in the same terrain region. The two are combined into a single 0–1 score, which maps to Low, Moderate, High, or Very High risk.",
        "how_it_works_body_2": "Rainfall thresholds are project-defined, not sourced from an official government classification — they were derived by the developer and are documented, with reasoning, in the project's methodology notes. Elevation data comes from a public elevation API, looked up once per city.",

        # ---- Result page (check.html) - remaining hardcoded strings
        # found this batch: "Risk Map", "Map unavailable...", "Why is the
        # risk...", the Rainfall/Elevation impact-bar labels, "Key
        # Information", "Assessment Type:", and the two assessment-type
        # values. rainfall_label/city_label already existed but were
        # being reused for the impact bars - given their own keys instead
        # since "Rainfall:" (with colon, a field label) and "Rainfall"
        # (a bar chip label) are different enough contexts to diverge
        # later without fighting each other.
        "risk_map_heading": "Risk Map",
        "map_unavailable": "Map unavailable for this location.",
        "why_risk_heading": "Why is the risk {risk_level}?",
        "impact_rainfall_label": "Rainfall",
        "impact_elevation_label": "Elevation",
        "key_information_heading": "Key Information",
        "assessment_type_label": "Assessment Type:",
        "assessment_type_forecast": "Forecast (72h)",
        "assessment_type_scenario": "Scenario (not current rainfall)",
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
        "score_breakdown": "اسکور: {score}/100 (بارش {rain}/70، بلندی {elev}/30)",
        "how_calculated_toggle": "یہ کیسے شمار کیا جاتا ہے؟",
        "explanation_with_elevation": "{rainfall} ملی میٹر بارش اور {city} کا آس پاس کے علاقوں کے مقابلے میں {elevation_position} پر ہونا، یہ مل کر {risk_level} بنتا ہے۔",
        "explanation_without_elevation": "{city} کے لیے متوقع {rainfall} ملی میٹر بارش کے ساتھ، یہ {risk_level} بنتا ہے۔",
        # NEW - NOT native-speaker reviewed
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
        "elevation_note_available": "{city} کی بلندی ({elevation} میٹر) کو دیگر {profile} مقامات کے مقابلے میں اس اسکور میں شامل کیا گیا۔",
        "elevation_note_unavailable": "{city} کے لیے بلندی کا ڈیٹا دستیاب نہیں تھا - یہ اسکور صرف بارش پر مبنی ہے۔",

        # ---- Home page - NEW, NOT reviewed
        "home_subtitle": "کسی بھی معاون سندھ شہر کے لیے لائیو 72 گھنٹے کی بارش کی پیشگوئی کی بنیاد پر سیلاب کے خطرے کا اندازہ حاصل کریں۔",

        # ---- About page - NEW, NOT reviewed
        "about_title": "اس منصوبے کے بارے میں",
        "about_lede": "فلڈ سیف پاکستان ایک منظرنامے پر مبنی سیلاب کے خطرے سے آگاہی کا ٹول ہے، جو سندھ کے لوگوں کو یہ سمجھنے میں مدد دینے کے لیے بنایا گیا ہے کہ مقامی بارش کس طرح سیلاب کے خطرے میں تبدیل ہو سکتی ہے۔",
        "about_validated_heading": "سندھ کے لیے تصدیق شدہ",
        "about_validated_body": "رسک اسکورنگ ماڈل فی الحال صرف سندھ کے لیے تصدیق شدہ ہے، جو سندھ کی مخصوص زمینی خصوصیات اور بارش کے انداز کے مطابق ترتیب دیا گیا ہے۔ ایپ کا ڈھانچہ باقی پاکستان تک وسعت دینے کے لیے بنایا گیا ہے، لیکن اس کے لیے ہر نئے علاقے کی زمینی خصوصیات کی الگ سے تصدیق درکار ہے - جو ابھی نہیں کی گئی اور مستقبل کے ورژن کے لیے مجوزہ ہے۔",
        "about_warning_heading": "یہ کوئی سرکاری وارننگ نہیں ہے",
        "about_warning_body": "فلڈ سیف یقین کے ساتھ سیلاب کی پیشگوئی نہیں کرتا اور PDMA سندھ یا آپ کے مقامی حکام کی سرکاری وارننگز کا متبادل نہیں ہے۔",
        "about_callout": "سندھ سے باہر کے شہر صرف جغرافیائی حوالے کے لیے نقشے پر دکھائے گئے ہیں اور ان کا خطرہ اسکور نہیں کیا گیا - اسی وجہ سے جیسا کہ اوپر بتایا گیا، ان کی زمینی خصوصیات ابھی اس ماڈل کے خلاف تصدیق شدہ نہیں ہیں۔",

        # ---- How It Works page - NEW, NOT reviewed
        "how_it_works_title": "یہ کیسے کام کرتا ہے",
        "how_it_works_body_1": "فلڈ سیف سندھ کے شہروں کے لیے دو عوامل سے سیلاب کے خطرے کا اندازہ لگاتا ہے: بارش (یا تو 72 گھنٹے کی لائیو پیشگوئی یا آپ کا درج کردہ منظرنامہ) اور ہر شہر کی بلندی اسی زمینی خطے کے قریبی شہروں کے مقابلے میں۔ یہ دونوں مل کر ایک 0 سے 1 تک کا اسکور بناتے ہیں، جو کم، درمیانہ، شدید، یا انتہائی شدید خطرے میں تبدیل ہوتا ہے۔",
        "how_it_works_body_2": "بارش کی حدیں منصوبے کے اپنے طے کردہ ہیں، کسی سرکاری درجہ بندی سے حاصل شدہ نہیں - یہ ڈویلپر نے مرتب کی ہیں اور ان کی وجوہات منصوبے کے طریقہ کار کے نوٹس میں دستاویزی ہیں۔ بلندی کا ڈیٹا ایک عوامی بلندی API سے حاصل کیا جاتا ہے، جو ہر شہر کے لیے ایک بار حاصل کیا جاتا ہے۔",

        # ---- Result page remaining strings - NEW, NOT reviewed
        "risk_map_heading": "خطرے کا نقشہ",
        "map_unavailable": "اس مقام کے لیے نقشہ دستیاب نہیں۔",
        "why_risk_heading": "خطرہ {risk_level} کیوں ہے؟",
        "impact_rainfall_label": "بارش",
        "impact_elevation_label": "بلندی",
        "key_information_heading": "اہم معلومات",
        "assessment_type_label": "تشخیص کی قسم:",
        "assessment_type_forecast": "پیشگوئی (72 گھنٹے)",
        "assessment_type_scenario": "منظرنامہ (موجودہ بارش نہیں)",
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
        "score_breakdown": "اسڪور: {score}/100 (برسات {rain}/70، بلندي {elev}/30)",
        "how_calculated_toggle": "هي ڪيئن ڳڻيو ويندو آهي؟",
        "explanation_with_elevation": "{rainfall} ملي ميٽر برسات ۽ {city} جو ڀرپاسي وارن علائقن جي مقابلي ۾ {elevation_position} تي هجڻ، هي گڏجي {risk_level} ٿو ٺاهي.",
        "explanation_without_elevation": "{city} لاءِ متوقع {rainfall} ملي ميٽر برسات سان، هي {risk_level} ٿو ٺاهي.",
        # NEW - NOT native-speaker reviewed
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
        "elevation_note_available": "{city} جي بلندي ({elevation} ميٽر) کي ٻين {profile} هنڌن جي مقابلي ۾ هن اسڪور ۾ شامل ڪيو ويو.",
        "elevation_note_unavailable": "{city} لاءِ بلندي جو ڊيٽا موجود نه هو - هي اسڪور فقط برسات تي ٻڌل آهي.",

        # ---- Home page - NEW, NOT reviewed
        "home_subtitle": "ڪنهن به سپورٽ ٿيل سنڌ جي شهر لاءِ لائيو 72 ڪلاڪن جي برسات جي اڳڪٿي جي بنياد تي سيلاب جي خطري جو اندازو حاصل ڪريو.",

        # ---- About page - NEW, NOT reviewed
        "about_title": "هن منصوبي بابت",
        "about_lede": "فلڊ سيف پاڪستان هڪ منظرنامي تي ٻڌل سيلاب جي خطري بابت آگاهي جو اوزار آهي، جيڪو سنڌ جي ماڻهن کي اهو سمجهڻ ۾ مدد ڏيڻ لاءِ ٺاهيو ويو آهي ته مقامي برسات ڪيئن سيلاب جي خطري ۾ تبديل ٿي سگهي ٿي.",
        "about_validated_heading": "سنڌ لاءِ تصديق ٿيل",
        "about_validated_body": "رسڪ اسڪورنگ ماڊل في الحال فقط سنڌ لاءِ تصديق ٿيل آهي، جيڪو سنڌ جي مخصوص زميني خاصيتن ۽ برسات جي نمونن مطابق ترتيب ڏنو ويو آهي. ايپ جو ڍانچو باقي پاڪستان تائين وڌائڻ لاءِ ٺاهيو ويو آهي، پر ان لاءِ هر نئين علائقي جي زميني خاصيتن جي الڳ تصديق گهرجي - جيڪا اڃا نه ٿي آهي ۽ ايندڙ ورجن لاءِ رٿيل آهي.",
        "about_warning_heading": "هي ڪا سرڪاري وارننگ ناهي",
        "about_warning_body": "فلڊ سيف يقين سان سيلاب جي اڳڪٿي نٿو ڪري ۽ PDMA سنڌ يا توهان جي مقامي اختيارين جي سرڪاري وارننگن جو متبادل ناهي.",
        "about_callout": "سنڌ کان ٻاهر جا شهر رڳو جاگرافيائي حوالي لاءِ نقشي تي ڏيکاريا ويا آهن ۽ انهن جو خطرو اسڪور نه ڪيو ويو آهي - ساڳئي سبب مطابق جيئن مٿي ٻڌايو ويو، سندن زميني خاصيتون اڃا هن ماڊل خلاف تصديق ٿيل ناهن.",

        # ---- How It Works page - NEW, NOT reviewed
        "how_it_works_title": "هي ڪيئن ڪم ڪري ٿو",
        "how_it_works_body_1": "فلڊ سيف سنڌ جي شهرن لاءِ ٻن عنصرن مان سيلاب جي خطري جو اندازو لڳائي ٿو: برسات (يا ته 72 ڪلاڪن جي لائيو اڳڪٿي يا توهان جو داخل ڪيل منظرنامو) ۽ هر شهر جي بلندي ساڳئي زميني علائقي جي ويجهن شهرن جي مقابلي ۾. ٻئي گڏجي هڪ 0 کان 1 تائين اسڪور ٺاهين ٿا، جيڪو گھٽ، وچولو، وڏو، يا تمام وڏو خطري ۾ تبديل ٿئي ٿو.",
        "how_it_works_body_2": "برسات جون حدون منصوبي جون پنهنجون مقرر ڪيل آهن، ڪنهن به سرڪاري درجه بندي مان حاصل ٿيل نه آهن - اهي ڊولپر پاران مرتب ڪيون ويون آهن ۽ سندن دليل منصوبي جي طريقيڪار جي نوٽس ۾ دستاويز ٿيل آهن. بلندي جو ڊيٽا هڪ عوامي بلندي API مان حاصل ڪيو ويندو آهي، جيڪو هر شهر لاءِ هڪ ڀيرو حاصل ڪيو ويندو آهي.",

        # ---- Result page remaining strings - NEW, NOT reviewed
        "risk_map_heading": "خطري جو نقشو",
        "map_unavailable": "هن هنڌ لاءِ نقشو دستياب ناهي.",
        "why_risk_heading": "خطرو {risk_level} ڇو آهي؟",
        "impact_rainfall_label": "برسات",
        "impact_elevation_label": "بلندي",
        "key_information_heading": "اهم معلومات",
        "assessment_type_label": "جانچ جو قسم:",
        "assessment_type_forecast": "اڳڪٿي (72 ڪلاڪ)",
        "assessment_type_scenario": "منظرنامو (موجوده برسات ناهي)",
    },
}

SUPPORTED_LANGUAGES = ["en", "ur", "sd"]
DEFAULT_LANGUAGE = "en"


def get_translation(lang_code):
    """Return the translation dict for a language code, falling back to English."""
    return TRANSLATIONS.get(lang_code, TRANSLATIONS[DEFAULT_LANGUAGE])