# translations.py
#
# IMPORTANT - READ BEFORE SHIPPING:
# Urdu (ur) translations are drafted with reasonable confidence but NOT
# verified by a native speaker.
# Sindhi (sd) translations are drafted with LOWER confidence - Sindhi script
# and dialect accuracy is a real risk area.
# Both MUST be reviewed by a native Sindhi/Urdu speaker (per Hammad's family
# member) before this app is used by real people or submitted for review.
# This is safety-critical text (evacuation instructions, emergency numbers) -
# do not treat the drafted text below as final.

TRANSLATIONS = {
    "en": {
        "app_title": "FloodSafe Pakistan",
        "disclaimer_banner": (
            "This tool estimates risk from local rainfall totals only. It does "
            "not account for major river bund failures (Indus, Jhelum, Chenab) "
            "or northern Glacial Lake Outburst Floods (GLOFs). For river and "
            "glacial flood warnings, check official NDMA/PDMA alerts directly."
        ),
        "sindhi_pending_note": "Sindhi language support is being reviewed for accuracy and will be enabled soon.",
        "form_city_label": "City:",
        "form_city_placeholder": "Enter city",
        "form_rainfall_label": "Rainfall (mm):",
        "form_rainfall_placeholder": "Enter rainfall",
        "form_submit": "Check Risk",
        "city_label": "City:",
        "rainfall_label": "Rainfall:",
        "terrain_profile_label": "Terrain Profile:",
        "weather_label": "Current Weather:",
        "risk_level_label": "Risk Level:",
        "shelter_heading": "Shelter Information:",
        "safety_tips_heading": "Safety Tips:",
        "back_link": "Back",
        "error_both": "Please enter a valid city and rainfall.",
        "error_rainfall": "Please enter a valid rainfall (a positive number).",
        "error_city": "Please enter a valid city.",
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
            "Mountainous & Rugged Terrain": "Steep terrain increases landslide and flash flood risk - avoid hillside roads and dry riverbeds (nullahs) during and after rainfall.",
            "Central Agricultural Plains": "Low-lying farmland can pool water for days - keep livestock and stored grain away from field edges.",
            "Arid Plains & Deserts": "Dry, hard-packed ground sheds water fast - watch for sudden dry riverbed (nullah) overflows even hours after rain stops.",
        },
        "terrain_profile_labels": {
            "Mega-Urban & Coastal": "Mega-Urban & Coastal",
            "Mountainous & Rugged Terrain": "Mountainous & Rugged Terrain",
            "Central Agricultural Plains": "Central Agricultural Plains",
            "Arid Plains & Deserts": "Arid Plains & Deserts",
        },
    },

    # DRAFT - NOT VERIFIED. Needs native Urdu speaker review before use.
    "ur": {
        "app_title": "فلڈ سیف پاکستان",
        "disclaimer_banner": (
            "یہ ٹول صرف مقامی بارش کے اعداد و شمار سے خطرے کا اندازہ لگاتا ہے۔ یہ دریاؤں کے بند "
            "ٹوٹنے (سندھ، جہلم، چناب) یا شمالی گلیشیئر جھیل کے سیلاب (GLOFs) کو شامل نہیں کرتا۔ "
            "دریائی اور گلیشیئر سیلاب کی وارننگ کے لیے براہ راست NDMA/PDMA الرٹس دیکھیں۔"
        ),
        "sindhi_pending_note": "سندھی زبان کی سہولت درستگی کی جانچ کے بعد جلد شامل کی جائے گی۔",
        "form_city_label": "شہر:",
        "form_city_placeholder": "شہر درج کریں",
        "form_rainfall_label": "بارش (ملی میٹر):",
        "form_rainfall_placeholder": "بارش درج کریں",
        "form_submit": "خطرہ چیک کریں",
        "city_label": "شہر:",
        "rainfall_label": "بارش:",
        "terrain_profile_label": "زمینی خصوصیات:",
        "weather_label": "موجودہ موسم:",
        "risk_level_label": "خطرے کی سطح:",
        "shelter_heading": "پناہ گاہ کی معلومات:",
        "safety_tips_heading": "حفاظتی ہدایات:",
        "back_link": "واپس",
        "error_both": "براہ کرم درست شہر اور بارش درج کریں۔",
        "error_rainfall": "براہ کرم درست بارش درج کریں (ایک مثبت نمبر)۔",
        "error_city": "براہ کرم درست شہر درج کریں۔",
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
            "Mountainous & Rugged Terrain": "کھڑی ڈھلوانیں لینڈ سلائیڈ اور اچانک سیلاب کا خطرہ بڑھاتی ہیں - بارش کے دوران اور بعد میں پہاڑی راستوں اور خشک نالوں سے بچیں۔",
            "Central Agricultural Plains": "نشیبی زرعی زمین میں پانی کئی دنوں تک جمع رہ سکتا ہے - مویشیوں اور ذخیرہ شدہ اناج کو کھیتوں کے کناروں سے دور رکھیں۔",
            "Arid Plains & Deserts": "خشک، سخت زمین پانی کو تیزی سے بہا دیتی ہے - بارش رکنے کے کئی گھنٹوں بعد بھی اچانک خشک نالوں کے بہاؤ کا خیال رکھیں۔",
        },
        "terrain_profile_labels": {
            "Mega-Urban & Coastal": "بڑے شہری اور ساحلی علاقے",
            "Mountainous & Rugged Terrain": "پہاڑی اور ناہموار علاقے",
            "Central Agricultural Plains": "وسطی زرعی میدانی علاقے",
            "Arid Plains & Deserts": "خشک میدانی اور صحرائی علاقے",
        },
    },

    # DRAFT - LOW CONFIDENCE. Sindhi script/dialect accuracy is NOT verified.
    # Do not ship until reviewed by a native Sindhi speaker.
    "sd": {
        "app_title": "فلڊ سيف پاڪستان",
        "disclaimer_banner": (
            "هي اوزار فقط مقامي برسات جي انگن اکرن مان خطري جو اندازو لڳائيندو آهي. هي درياهي "
            "بند ٽٽڻ (سنڌو، جهلم، چناب) يا اترين برفاني ڍنڍ جي سيلاب (GLOFs) کي شامل نٿو ڪري. "
            "درياهي ۽ برفاني سيلاب جي وارننگ لاءِ سڌو سنئون NDMA/PDMA اطلاعات ڏسو."
        ),
        "sindhi_pending_note": "سنڌي ٻولي جي درستگي جي جانچ جاري آهي.",
        "form_city_label": "شهر:",
        "form_city_placeholder": "شهر داخل ڪريو",
        "form_rainfall_label": "برسات (ملي ميٽر):",
        "form_rainfall_placeholder": "برسات داخل ڪريو",
        "form_submit": "خطرو چيڪ ڪريو",
        "city_label": "شهر:",
        "rainfall_label": "برسات:",
        "terrain_profile_label": "زميني خاصيتون:",
        "weather_label": "موجوده موسم:",
        "risk_level_label": "خطري جو درجو:",
        "shelter_heading": "پناهگاهه جي معلومات:",
        "safety_tips_heading": "حفاظتي هدايتون:",
        "back_link": "واپس",
        "error_both": "مهرباني ڪري صحيح شهر ۽ برسات داخل ڪريو.",
        "error_rainfall": "مهرباني ڪري صحيح برسات داخل ڪريو (هڪ مثبت انگ).",
        "error_city": "مهرباني ڪري صحيح شهر داخل ڪريو.",
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
            "Mountainous & Rugged Terrain": "بيهي ڍلاڻون لينڊ سلائيڊ ۽ اوچتو سيلاب جو خطرو وڌائينديون آهن - برسات دوران ۽ پوءِ جبلن جي رستن ۽ سڪل نالن کان بچو.",
            "Central Agricultural Plains": "هيٺاهين زرعي زمين ۾ پاڻي ڪيترن ڏينهن تائين بيهي سگهي ٿو - ڍورن ۽ ذخيرو ٿيل اناج کي فيلڊ جي ڪنارن کان پري رکو.",
            "Arid Plains & Deserts": "سڪل، سخت زمين پاڻي کي تيزيءَ سان وهائي ٿي - برسات بند ٿيڻ کان ڪلاڪن پوءِ به اوچتو سڪل نالن جي وهڪري جو خيال رکو.",
        },
        "terrain_profile_labels": {
            "Mega-Urban & Coastal": "وڏا شهري ۽ ساحلي علائقا",
            "Mountainous & Rugged Terrain": "جبلي ۽ اڻ برابر علائقا",
            "Central Agricultural Plains": "مرڪزي زرعي ميدان",
            "Arid Plains & Deserts": "سڪل ميدان ۽ ريگستان",
        },
    },
}

SUPPORTED_LANGUAGES = ["en", "ur", "sd"]
DEFAULT_LANGUAGE = "en"


def get_translation(lang_code):
    """Return the translation dict for a language code, falling back to English."""
    return TRANSLATIONS.get(lang_code, TRANSLATIONS[DEFAULT_LANGUAGE])