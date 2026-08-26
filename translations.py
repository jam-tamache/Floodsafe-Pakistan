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
        "form_city_label": "City:",
        "form_city_placeholder": "Enter city",
        "form_rainfall_label": "Rainfall (mm):",
        "form_rainfall_placeholder": "Enter rainfall",
        "form_submit": "Check Risk",
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
        "risk_levels": {
            "Low Risk": "Low Risk",
            "Medium Risk": "Medium Risk",
            "High Risk": "High Risk",
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
            "Medium Risk": [
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
    # error_city_outside_coverage and elevation_note_* are NEW as of this
    # session - not yet reviewed even at draft quality, translated directly
    # by Claude without a native-speaker pass. Flag these two keys
    # specifically when you do the Urdu review.
    "ur": {
        "app_title": "فلڈ سیف پاکستان",
        "disclaimer_banner": (
            "یہ ٹول صرف مقامی بارش کے اعداد و شمار سے خطرے کا اندازہ لگاتا ہے۔ یہ دریاؤں کے بند "
            "ٹوٹنے (سندھ، جہلم، چناب) یا شمالی گلیشیئر جھیل کے سیلاب (GLOFs) کو شامل نہیں کرتا۔ "
            "دریائی اور گلیشیئر سیلاب کی وارننگ کے لیے براہ راست NDMA/PDMA الرٹس دیکھیں۔"
        ),
        "form_city_label": "شہر:",
        "form_city_placeholder": "شہر درج کریں",
        "form_rainfall_label": "بارش (ملی میٹر):",
        "form_rainfall_placeholder": "بارش درج کریں",
        "form_submit": "خطرہ چیک کریں",
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
        "risk_levels": {
            "Low Risk": "کم خطرہ",
            "Medium Risk": "درمیانہ خطرہ",
            "High Risk": "شدید خطرہ",
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
            "Medium Risk": [
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
    # native speaker (Aug 25 session) - but error_city_outside_coverage and
    # elevation_note_* below are NEW as of this session and have NOT been
    # through that review. Only these new keys need a native-speaker pass;
    # everything else here is still the verified set.
    "sd": {
        "app_title": "فلڊ سيف پاڪستان",
        "disclaimer_banner": (
            "هي اوزار فقط مقامي برسات جي انگن اکرن مان خطري جو اندازو لڳائيندو آهي. هي درياهي "
            "بند ٽٽڻ (سنڌو، جهلم، چناب) يا اترين برفاني ڍنڍ جي سيلاب (GLOFs) کي شامل نٿو ڪري. "
            "درياهي ۽ برفاني سيلاب جي وارننگ لاءِ سڌو سنئون NDMA/PDMA اطلاعات ڏسو."
        ),
        "form_city_label": "شهر:",
        "form_city_placeholder": "شهر داخل ڪريو",
        "form_rainfall_label": "برسات (ملي ميٽر):",
        "form_rainfall_placeholder": "برسات داخل ڪريو",
        "form_submit": "خطرو چيڪ ڪريو",
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
        "risk_levels": {
            "Low Risk": "گھٽ خطرو",
            "Medium Risk": "وچولو خطرو",
            "High Risk": "وڏو خطرو",
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
            "Medium Risk": [
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