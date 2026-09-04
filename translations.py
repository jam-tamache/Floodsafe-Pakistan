# translations.py
#
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
        # ---- Top-bar nav labels (NEW - replaces the sidebar nav labels
        # that were hardcoded directly in base.html before). About and
        # Data & Methodology are now real routes/pages, not same-page
        # anchors - see app.py for the new /about and /methodology routes.
        # Contact is deliberately NOT in this list yet - no destination
        # has been decided, so it isn't in nav until it does something.
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
        # NEW (this session) - the <details> toggle on index.html actually
        # wraps the FORECAST form (city only, no rainfall field), not a
        # scenario form. It was previously using scenario_toggle_label /
        # scenario_form_intro, which described a rainfall field that isn't
        # there - real copy/content mismatch, not just a naming nitpick.
        # scenario_toggle_label / scenario_form_intro above are unchanged
        # and still correctly describe the PRIMARY form on the page.
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
            # STUB - reuses High Risk's tips verbatim. Very High is meant to
            # be more severe than High (0.75-1.00 vs 0.50-0.75 on the
            # gauge) but the wording doesn't reflect that yet - e.g.
            # nothing here conveys heightened urgency vs the High tier.
            # Write real, distinct Very High guidance before this ships -
            # do not leave two tiers reading identically. STILL NOT DONE -
            # flagged again, this is the #2 outstanding liability.
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
    },

    # DRAFT - NOT VERIFIED. Needs native Urdu speaker review before use.
    # error_city_outside_coverage and elevation_note_* were added in an
    # earlier session and still need review. forecast_form_submit,
    # scenario_toggle_label, scenario_form_intro, forecast_toggle_label,
    # forecast_toggle_intro, forecast_error_unavailable, source_forecast,
    # source_scenario, score_breakdown, how_calculated_toggle,
    # explanation_with_elevation, explanation_without_elevation,
    # elevation_position_low/high, and nav_home/nav_about/
    # nav_how_it_works/nav_data_methodology are all NEW or still-unreviewed -
    # translated directly by Claude without a native-speaker pass. Flag ALL
    # of these when you do the Urdu review. This list has only grown across
    # sessions - do this review before adding anything else.
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
        # NEW (this session) - see the "en" block's comment above the same
        # two keys for why these exist. NOT yet native-speaker reviewed.
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
        "elevation_position_low": "نچلی زمین",
        "elevation_position_high": "اونچی زمین",
        # FIX (this session): this dict was still on the OLD 3-tier key set
        # ("Medium Risk" instead of "Moderate Risk", no "Very High Risk"
        # entry at all) - the actual cause of the KeyError: 'Moderate Risk'
        # crash when switching to Urdu on a result page. "en" and "sd" both
        # already had all four correct tier keys; only "ur" was stale.
        # "Very High Risk" translation below is a first-pass placeholder,
        # NOT yet native-speaker reviewed - flag with everything else.
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
            # STUB - same caveat as "en"'s "Very High Risk": verbatim copy
            # of High Risk. Still needs real, distinct wording.
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
    },

    # Sindhi translations. NOTE: previously marked fully reviewed by a
    # native speaker - but error_city_outside_coverage and elevation_note_*
    # were added in an earlier session and were never reviewed either.
    # forecast_form_submit, scenario_toggle_label, scenario_form_intro,
    # forecast_toggle_label, forecast_toggle_intro, forecast_error_unavailable,
    # source_forecast, source_scenario, score_breakdown, how_calculated_toggle,
    # explanation_with_elevation, explanation_without_elevation,
    # elevation_position_low/high, and nav_home/nav_about/nav_how_it_works/
    # nav_data_methodology are all NEW or still-unreviewed. Flag ALL of these
    # (not just the newest batch) for native-speaker review.
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
        # NEW (this session) - see the "en" block's comment above the same
        # two keys for why these exist. NOT yet native-speaker reviewed.
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
    },
}

SUPPORTED_LANGUAGES = ["en", "ur", "sd"]
DEFAULT_LANGUAGE = "en"


def get_translation(lang_code):
    """Return the translation dict for a language code, falling back to English."""
    return TRANSLATIONS.get(lang_code, TRANSLATIONS[DEFAULT_LANGUAGE])