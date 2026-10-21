"""
Back-test case data for FloodSafe Pakistan (model tag: model-v1).

Each case is a dated, sourced event. `city` is the same lowercase key
that risk_check.py uses, so a case can go straight into
_compute_risk_core().

Rainfall comes from official NDMA, PDMA and PMD documents. The protocol
planned ERA5, but it could not be reached. Each case names its document
in `source`. Every scored figure is a 24-hour reading, not a confirmed
72h total.

Each case has an `i18n` dict with "ur" and "sd" text. A missing key
means the English text is used. Sources stay in English so they can be
traced. The ur/sd text is unreviewed. Sindhi is the weakest.
"""

FLOOD_CASES = [
    {
        "id": "karachi_aug2020",
        "city": "karachi",
        "profile_key": "mega_urban_coastal",
        "lat": 24.8546842,
        "lon": 67.0207055,
        "date_window": "2020-08-24 to 2020-08-27",
        "rainfall_mm": 231.0,
        "rainfall_caveat": (
            "231.0mm is PMD's 24-hour record at Karachi-Faisal. "
            "PMD dates it 28 Aug 2020, one day after this window. "
            "It is not a 72-hour total. "
            "The real 72-hour total is likely higher, so treat 231.0mm as a floor. "
            "The August total at Karachi-Faisal was 588.0mm."
        ),
        "actual_outcome": "flood",
        "impact": "40 deaths over the three-day spell (Dawn, 28 Aug 2020)",
        "source": (
            "PMD, 'State of Pakistan's Climate in 2020' "
            "(https://cdpc.pmd.gov.pk/Pakistan_Climate_2020.pdf); "
            "Dawn, 28 Aug 2020 (https://www.dawn.com/news/1576798)"
        ),
        "i18n": {
            "ur": {
                "rainfall_caveat": (
                    "231.0 ملی میٹر کراچی-فیصل پر PMD کا 24 گھنٹے کا ریکارڈ ہے۔ "
                    "PMD نے اسے 28 اگست 2020 کی تاریخ دی ہے، جو اس مدت سے ایک دن بعد ہے۔ "
                    "یہ 72 گھنٹے کا کل نہیں۔ "
                    "72 گھنٹے کا اصل کل غالباً زیادہ ہے، اس لیے 231.0 ملی میٹر کو کم از کم حد سمجھیں۔ "
                    "کراچی-فیصل پر اگست کا کل 588.0 ملی میٹر تھا۔"
                ),
                "impact": "تین روزہ سلسلے میں 40 اموات (Dawn، 28 اگست 2020)",
                "source": (
                    "PMD، 'State of Pakistan's Climate in 2020' "
                    "(https://cdpc.pmd.gov.pk/Pakistan_Climate_2020.pdf)؛ "
                    "Dawn، 28 اگست 2020 (https://www.dawn.com/news/1576798)"
                ),
            },
            "sd": {
                "rainfall_caveat": (
                    "231.0 ملي ميٽر ڪراچي-فيصل تي PMD جو 24 ڪلاڪن جو رڪارڊ آهي. "
                    "PMD ان کي 28 آگسٽ 2020 جي تاريخ ڏني آهي، جيڪا هن مدي کان هڪ ڏينهن پوءِ آهي. "
                    "هي 72 ڪلاڪن جو ڪل ناهي. "
                    "72 ڪلاڪن جو اصل ڪل غالباً وڌيڪ آهي، تنهنڪري 231.0 ملي ميٽر کي گهٽ ۾ گهٽ حد سمجهو. "
                    "ڪراچي-فيصل تي آگسٽ جو ڪل 588.0 ملي ميٽر هو."
                ),
                "impact": "ٽن ڏينهن جي سلسلي ۾ 40 موت (Dawn، 28 آگسٽ 2020)",
                "source": (
                    "PMD، 'State of Pakistan's Climate in 2020' "
                    "(https://cdpc.pmd.gov.pk/Pakistan_Climate_2020.pdf)؛ "
                    "Dawn، 28 آگسٽ 2020 (https://www.dawn.com/news/1576798)"
                ),
            },
        },
    },
    {
        "id": "nawabshah_sba_aug2022",
        "city": "nawabshah",
        "profile_key": "central_plains",
        "lat": 26.2452915,
        "lon": 68.4040229,
        "date_window": "2022-08-23 to 2022-08-25",
        "rainfall_mm": 137.0,
        "rainfall_caveat": (
            "137.0mm is the SBA station reading for 24 to 25 Aug (NDMA SITREP-073). "
            "The damage figures are from 23 to 24 Aug, one day earlier in the same flood spell, which began on 17 Aug."
        ),
        "actual_outcome": "flood",
        "impact": "54,962 houses partially destroyed, 23,000 fully destroyed, 696 cattle lost (as of 23-24 Aug)",
        "source": (
            "NDMA Monsoon 2022 Daily SITREP No. 073, dated 25 Aug 2022 "
            "(https://www.ndma.gov.pk/storage/sitreps/August2022/0K4OF8fblju6B0XAjBr1.pdf); "
            "Tribune, 24 Aug 2022, quoting Sindh Information Minister Sharjeel Memon "
            "(https://tribune.com.pk/story/2372885/pmd-forecasts-heavy-rains-in-parts-of-three-provinces)"
        ),
        "i18n": {
            "ur": {
                "rainfall_caveat": (
                    "137.0 ملی میٹر 24 سے 25 اگست کے لیے SBA اسٹیشن کی ریڈنگ ہے (NDMA SITREP-073)۔ "
                    "نقصان کے اعداد 23 سے 24 اگست کے ہیں، یعنی ایک دن پہلے کے، اسی سیلابی سلسلے کے جو 17 اگست کو شروع ہوا۔"
                ),
                "impact": "54,962 گھر جزوی طور پر تباہ، 23,000 مکمل تباہ، 696 مویشی ہلاک (23-24 اگست تک)",
                "source": (
                    "NDMA Monsoon 2022 Daily SITREP نمبر 073، مورخہ 25 اگست 2022 "
                    "(https://www.ndma.gov.pk/storage/sitreps/August2022/0K4OF8fblju6B0XAjBr1.pdf)؛ "
                    "Tribune، 24 اگست 2022، سندھ کے وزیر اطلاعات شرجیل میمن کے حوالے سے "
                    "(https://tribune.com.pk/story/2372885/pmd-forecasts-heavy-rains-in-parts-of-three-provinces)"
                ),
            },
            "sd": {
                "rainfall_caveat": (
                    "137.0 ملي ميٽر 24 کان 25 آگسٽ لاءِ SBA اسٽيشن جي ريڊنگ آهي (NDMA SITREP-073). "
                    "نقصان جا انگ 23 کان 24 آگسٽ جا آهن، يعني هڪ ڏينهن اڳ جا، ساڳئي سيلابي سلسلي جا جيڪو 17 آگسٽ تي شروع ٿيو."
                ),
                "impact": "54,962 گهر جزوي طور تباهه، 23,000 مڪمل تباهه، 696 ڍور ضايع (23-24 آگسٽ تائين)",
                "source": (
                    "NDMA Monsoon 2022 Daily SITREP نمبر 073، تاريخ 25 آگسٽ 2022 "
                    "(https://www.ndma.gov.pk/storage/sitreps/August2022/0K4OF8fblju6B0XAjBr1.pdf)؛ "
                    "Tribune، 24 آگسٽ 2022، سنڌ جي اطلاعات واري وزير شرجيل ميمڻ جي حوالي سان "
                    "(https://tribune.com.pk/story/2372885/pmd-forecasts-heavy-rains-in-parts-of-three-provinces)"
                ),
            },
        },
    },
    {
        "id": "jacobabad_aug2022",
        "city": "jacobabad",
        "profile_key": "arid_plains_desert",
        "lat": 28.2813094,
        "lon": 68.4364361,
        "date_window": "2022-08-28",
        "rainfall_mm": None,
        "rainfall_caveat": (
            "No rainfall figure was found for this case. "
            "The flood is confirmed by satellite (Sentinel-1 SAR), not by a rain gauge. "
            "So it cannot be scored and is skipped."
        ),
        "actual_outcome": "flood",
        "impact": "Flood confirmed by Sentinel-1 SAR satellite images, about 28 Aug 2022",
        "source": (
            "Roth, F. et al., 'Sentinel-1-based analysis of the severe flood over "
            "Pakistan 2022', Nat. Hazards Earth Syst. Sci. 23, 3305-3325, 2023 "
            "(https://nhess.copernicus.org/articles/23/3305/2023/); "
            "'A framework for multi-sensor satellite data to evaluate crop "
            "production losses...', Nature Sci. Reports, 2023 "
            "(https://www.nature.com/articles/s41598-023-30347-y)"
        ),
        "i18n": {
            # No "source" key. The English citation is shown in every language.
            "ur": {
                "rainfall_caveat": (
                    "اس کیس کے لیے بارش کا کوئی عدد نہیں ملا۔ "
                    "سیلاب کی تصدیق سیٹلائٹ (Sentinel-1 SAR) سے ہوئی ہے، بارش ناپنے والے آلے سے نہیں۔ "
                    "اس لیے اسے اسکور نہیں کیا جا سکتا اور چھوڑ دیا گیا ہے۔"
                ),
                "impact": "Sentinel-1 SAR سیٹلائٹ تصاویر سے سیلاب کی تصدیق، تقریباً 28 اگست 2022",
            },
            "sd": {
                "rainfall_caveat": (
                    "هن ڪيس لاءِ برسات جو ڪو انگ نه مليو. "
                    "سيلاب جي تصديق سيٽلائيٽ (Sentinel-1 SAR) مان ٿي آهي، برسات ماپڻ واري اوزار مان نه. "
                    "تنهنڪري ان کي اسڪور نٿو ڪري سگهجي ۽ ڇڏيو ويو آهي."
                ),
                "impact": "Sentinel-1 SAR سيٽلائيٽ تصويرن مان سيلاب جي تصديق، لڳ ڀڳ 28 آگسٽ 2022",
            },
        },
    },
    {
        "id": "hyderabad_aug2026",
        "city": "hyderabad",
        "profile_key": "mega_urban_coastal",
        "lat": 25.4075358,
        "lon": 68.3613456,
        "date_window": "2026-08-02 to 2026-08-03",
        "rainfall_mm": 89.0,
        "rainfall_caveat": (
            "89mm is a PDMA 24-hour figure for Hyderabad City (Dawn, 3 Aug "
            "2026), not a 72-hour total."
            " The flood label rests on one Dawn photo of water at the railway station. PDMA's 3 Aug report lists no incident for Hyderabad."
        ),
        "actual_outcome": "flood",
        "impact": "Part of a multi-district rain event across Sindh; 8 deaths province-wide (Dawn, 3 Aug 2026)",
        "source": "Dawn, 3 Aug 2026, 'Sindh CM Murad orders emergency steps as downpour wreaks havoc in several districts' (https://www.dawn.com/news/2020214)",
        "i18n": {
            "ur": {
                "rainfall_caveat": (
                    "89 ملی میٹر حیدرآباد شہر کے لیے PDMA کا 24 گھنٹے کا عدد ہے "
                    "(Dawn، 3 اگست 2026)، 72 گھنٹے کا کل نہیں۔"
                    " سیلاب کا لیبل Dawn کی ایک تصویر پر مبنی ہے جس میں ریلوے اسٹیشن پر پانی ہے۔ PDMA کی 3 اگست کی رپورٹ میں حیدرآباد کا کوئی واقعہ درج نہیں۔"
                ),
                "impact": "سندھ بھر میں کئی اضلاع میں پھیلے بارشی واقعے کا حصہ؛ پورے صوبے میں 8 اموات (Dawn، 3 اگست 2026)",
                "source": "Dawn، 3 اگست 2026، 'Sindh CM Murad orders emergency steps as downpour wreaks havoc in several districts' (https://www.dawn.com/news/2020214)",
            },
            "sd": {
                "rainfall_caveat": (
                    "89 ملي ميٽر حيدرآباد شهر لاءِ PDMA جو 24 ڪلاڪن جو انگ آهي "
                    "(Dawn، 3 آگسٽ 2026)، 72 ڪلاڪن جو ڪل ناهي."
                    " سيلاب جو ليبل Dawn جي هڪ تصوير تي ٻڌل آهي جنهن ۾ ريلوي اسٽيشن تي پاڻي آهي. PDMA جي 3 آگسٽ جي رپورٽ ۾ حيدرآباد جو ڪو واقعو درج ناهي."
                ),
                "impact": "سڄي سنڌ ۾ ڪيترن ضلعن ۾ پکڙيل برسات واري واقعي جو حصو؛ سڄي صوبي ۾ 8 موت (Dawn، 3 آگسٽ 2026)",
                "source": "Dawn، 3 آگسٽ 2026، 'Sindh CM Murad orders emergency steps as downpour wreaks havoc in several districts' (https://www.dawn.com/news/2020214)",
            },
        },
    },
    {
        "id": "mirpurkhas_aug2026",
        "city": "mirpurkhas",
        "profile_key": "central_plains",
        "lat": 25.5263882,
        "lon": 69.0112387,
        "date_window": "2026-08-02 to 2026-08-03",
        "rainfall_mm": 111.0,
        "rainfall_caveat": (
            "111mm is a PDMA 24-hour figure for Mirpurkhas City (Dawn, 3 Aug "
            "2026), not a 72-hour total."
            " No source names flooding in the city. PDMA's 3 Aug report lists canal breaches in the district only."
        ),
        "actual_outcome": "flood",
        "impact": "Part of the same Sindh rain event as the Hyderabad and Umerkot cases",
        "source": "Dawn, 3 Aug 2026 (https://www.dawn.com/news/2020214)",
        "i18n": {
            "ur": {
                "rainfall_caveat": (
                    "111 ملی میٹر میرپورخاص شہر کے لیے PDMA کا 24 گھنٹے کا عدد ہے "
                    "(Dawn، 3 اگست 2026)، 72 گھنٹے کا کل نہیں۔"
                    " کسی ذریعے نے شہر میں سیلاب کا نام نہیں لیا۔ PDMA کی 3 اگست کی رپورٹ میں صرف ضلع کی نہروں میں شگاف درج ہیں۔"
                ),
                "impact": "سندھ کے اسی بارشی واقعے کا حصہ جس میں حیدرآباد اور عمرکوٹ کے کیسز شامل ہیں",
                "source": "Dawn، 3 اگست 2026 (https://www.dawn.com/news/2020214)",
            },
            "sd": {
                "rainfall_caveat": (
                    "111 ملي ميٽر ميرپورخاص شهر لاءِ PDMA جو 24 ڪلاڪن جو انگ آهي "
                    "(Dawn، 3 آگسٽ 2026)، 72 ڪلاڪن جو ڪل ناهي."
                    " ڪنهن ذريعي شهر ۾ سيلاب جو نالو ناهي ورتو. PDMA جي 3 آگسٽ جي رپورٽ ۾ رڳو ضلعي جي واهن ۾ ڏار درج آهن."
                ),
                "impact": "سنڌ جي ساڳئي برسات واري واقعي جو حصو جنهن ۾ حيدرآباد ۽ عمرڪوٽ جا ڪيس شامل آهن",
                "source": "Dawn، 3 آگسٽ 2026 (https://www.dawn.com/news/2020214)",
            },
        },
    },
    {
        "id": "umerkot_aug2026",
        "city": "umerkot",
        "profile_key": "arid_plains_desert",
        "lat": 25.3655302,
        "lon": 69.7401257,
        "date_window": "2026-08-02 to 2026-08-03",
        "rainfall_mm": 169.0,
        "rainfall_caveat": (
            "169mm is a PDMA 24-hour figure for Umerkot taluka (Dawn, 3 Aug "
            "2026), not a 72-hour total."
        ),
        "actual_outcome": "flood",
        "impact": (
            "Highest 24-hour rainfall reported in Sindh (PDMA, 169 mm). "
            "1 death by drowning. "
            "Same event as the other 2026 cases."
        ),
        "source": "Dawn, 3 Aug 2026 (https://www.dawn.com/news/2020214)",
        "i18n": {
            "ur": {
                "rainfall_caveat": (
                    "169 ملی میٹر عمرکوٹ تعلقہ کے لیے PDMA کا 24 گھنٹے کا عدد ہے "
                    "(Dawn، 3 اگست 2026)، 72 گھنٹے کا کل نہیں۔"
                ),
                "impact": (
                    "سندھ میں 24 گھنٹوں کی سب سے زیادہ بارش (PDMA، 169 ملی میٹر)۔ "
                    "ڈوبنے سے 1 موت۔ "
                    "باقی 2026 کے کیسز والا ہی واقعہ۔"
                ),
                "source": "Dawn، 3 اگست 2026 (https://www.dawn.com/news/2020214)",
            },
            "sd": {
                "rainfall_caveat": (
                    "169 ملي ميٽر عمرڪوٽ تعلقي لاءِ PDMA جو 24 ڪلاڪن جو انگ آهي "
                    "(Dawn، 3 آگسٽ 2026)، 72 ڪلاڪن جو ڪل ناهي."
                ),
                "impact": (
                    "سنڌ ۾ 24 ڪلاڪن جي سڀ کان وڌيڪ برسات (PDMA، 169 ملي ميٽر). "
                    "ٻڏڻ سبب 1 موت. "
                    "باقي 2026 جي ڪيسن وارو ساڳيو واقعو."
                ),
                "source": "Dawn، 3 آگسٽ 2026 (https://www.dawn.com/news/2020214)",
            },
        },
    },
]

NON_FLOOD_CASES = [
    {
        "id": "karachi_aug2020_nonflood",
        "city": "karachi",
        "profile_key": "mega_urban_coastal",
        "lat": 24.8546842,
        "lon": 67.0207055,
        "date_window": "2020-08-08 to 2020-08-09",
        "rainfall_mm": 47.0,
        "rainfall_caveat": (
            "47mm is a 24-hour PMD reading from the SITREP rainfall annex, "
            "not a 72-hour total."
        ),
        "actual_outcome": "no_flood",
        "impact": (
            "No flood damage reported in this window. "
            "The SITREP notes a few deaths and damages across Sindh, not tied to this reading."
        ),
        "source": (
            "NDMA Monsoon 2020 Daily SITREP No. 045, dated 9 Aug 2020, "
            "PMD rainfall Annex B (https://www.ndma.gov.pk/storage/sitreps/September2020/9y0Bmj0Ri5QMx5zX05bM.pdf)"
        ),
        "i18n": {
            "ur": {
                "rainfall_caveat": "47 ملی میٹر SITREP کے بارش کے ضمیمے سے PMD کی 24 گھنٹے کی ریڈنگ ہے، 72 گھنٹے کا کل نہیں۔",
                "impact": (
                    "اس مدت میں سیلابی نقصان کی کوئی اطلاع نہیں۔ "
                    "SITREP میں پورے سندھ میں کچھ اموات اور نقصانات کا ذکر ہے، جو اس ریڈنگ سے منسلک نہیں۔"
                ),
                "source": (
                    "NDMA Monsoon 2020 Daily SITREP نمبر 045، مورخہ 9 اگست 2020، "
                    "PMD بارش کا ضمیمہ B (https://www.ndma.gov.pk/storage/sitreps/September2020/9y0Bmj0Ri5QMx5zX05bM.pdf)"
                ),
            },
            "sd": {
                "rainfall_caveat": "47 ملي ميٽر SITREP جي برسات واري ضميمي مان PMD جي 24 ڪلاڪن جي ريڊنگ آهي، 72 ڪلاڪن جو ڪل ناهي.",
                "impact": (
                    "هن عرصي ۾ سيلابي نقصان جي ڪا اطلاع ناهي. "
                    "SITREP ۾ سڄي سنڌ ۾ ڪجهه موت ۽ نقصان جو ذڪر آهي، جيڪي هن ريڊنگ سان ڳنڍيل ناهن."
                ),
                "source": (
                    "NDMA Monsoon 2020 Daily SITREP نمبر 045، تاريخ 9 آگسٽ 2020، "
                    "PMD برسات جو ضميمو B (https://www.ndma.gov.pk/storage/sitreps/September2020/9y0Bmj0Ri5QMx5zX05bM.pdf)"
                ),
            },
        },
    },
    {
        "id": "mithi_aug2020_nonflood",
        "city": "mithi",
        "profile_key": "arid_plains_desert",
        "lat": 24.736412,
        "lon": 69.7973419,
        "date_window": "2020-08-08 to 2020-08-09",
        "rainfall_mm": 56.0,
        "rainfall_caveat": (
            "56mm is a 24-hour PMD reading from the SITREP rainfall annex, "
            "not a 72-hour total."
        ),
        "actual_outcome": "no_flood",
        "impact": "No flood damage reported in this window",
        "source": (
            "NDMA Monsoon 2020 Daily SITREP No. 045, dated 9 Aug 2020, "
            "PMD rainfall Annex B (https://www.ndma.gov.pk/storage/sitreps/September2020/9y0Bmj0Ri5QMx5zX05bM.pdf)"
        ),
        "i18n": {
            "ur": {
                "rainfall_caveat": "56 ملی میٹر SITREP کے بارش کے ضمیمے سے PMD کی 24 گھنٹے کی ریڈنگ ہے، 72 گھنٹے کا کل نہیں۔",
                "impact": "اس مدت میں سیلابی نقصان کی کوئی اطلاع نہیں",
                "source": (
                    "NDMA Monsoon 2020 Daily SITREP نمبر 045، مورخہ 9 اگست 2020، "
                    "PMD بارش کا ضمیمہ B (https://www.ndma.gov.pk/storage/sitreps/September2020/9y0Bmj0Ri5QMx5zX05bM.pdf)"
                ),
            },
            "sd": {
                "rainfall_caveat": "56 ملي ميٽر SITREP جي برسات واري ضميمي مان PMD جي 24 ڪلاڪن جي ريڊنگ آهي، 72 ڪلاڪن جو ڪل ناهي.",
                "impact": "هن عرصي ۾ سيلابي نقصان جي ڪا اطلاع ناهي",
                "source": (
                    "NDMA Monsoon 2020 Daily SITREP نمبر 045، تاريخ 9 آگسٽ 2020، "
                    "PMD برسات جو ضميمو B (https://www.ndma.gov.pk/storage/sitreps/September2020/9y0Bmj0Ri5QMx5zX05bM.pdf)"
                ),
            },
        },
    },
    {
        "id": "nawabshah_sba_jul2022_nonflood",
        "city": "nawabshah",
        "profile_key": "central_plains",
        "lat": 26.2452915,
        "lon": 68.4040229,
        "date_window": "2022-07-14 to 2022-07-15",
        "rainfall_mm": 60.0,
        "rainfall_caveat": (
            "The SITREP reports no incidents for this district. "
            "The 60mm figure is not yet checked against a PMD rainfall table. "
            "It is a 24-hour reading, not a 72-hour total."
        ),
        "actual_outcome": "no_flood",
        "impact": "No damage or incidents reported for Shaheed Benazirabad in this SITREP",
        "source": (
            "NDMA Monsoon 2022 Daily SITREP No. 031, covering 14-15 Jul 2022 "
            "(https://reliefweb.int/report/pakistan/ndma-monsoon-2022-daily-situation-report-no-031-1300-hrs-14-july-2022-1300-hrs-15-july-2022)"
        ),
        "i18n": {
            "ur": {
                "rainfall_caveat": (
                    "SITREP میں اس ضلع کے لیے کسی واقعے کی اطلاع نہیں۔ "
                    "60 ملی میٹر کا عدد ابھی PMD کی بارش کی جدول سے نہیں ملایا گیا۔ "
                    "یہ 24 گھنٹے کی ریڈنگ ہے، 72 گھنٹے کا کل نہیں۔"
                ),
                "impact": "اس SITREP میں شہید بینظیرآباد کے لیے کسی نقصان یا واقعے کی اطلاع نہیں",
                "source": (
                    "NDMA Monsoon 2022 Daily SITREP نمبر 031، 14-15 جولائی 2022 کا احاطہ "
                    "(https://reliefweb.int/report/pakistan/ndma-monsoon-2022-daily-situation-report-no-031-1300-hrs-14-july-2022-1300-hrs-15-july-2022)"
                ),
            },
            "sd": {
                "rainfall_caveat": (
                    "SITREP ۾ هن ضلعي لاءِ ڪنهن واقعي جي اطلاع ناهي. "
                    "60 ملي ميٽر جو انگ اڃا PMD جي برسات واري جدول سان نه ملايو ويو آهي. "
                    "هي 24 ڪلاڪن جي ريڊنگ آهي، 72 ڪلاڪن جو ڪل ناهي."
                ),
                "impact": "هن SITREP ۾ شهيد بينظيرآباد لاءِ ڪنهن نقصان يا واقعي جي اطلاع ناهي",
                "source": (
                    "NDMA Monsoon 2022 Daily SITREP نمبر 031، 14-15 جولاءِ 2022 جو احاطو "
                    "(https://reliefweb.int/report/pakistan/ndma-monsoon-2022-daily-situation-report-no-031-1300-hrs-14-july-2022-1300-hrs-15-july-2022)"
                ),
            },
        },
    },
]

ALL_CASES = FLOOD_CASES + NON_FLOOD_CASES


def case_text(case, field, lang):
    """Return case[field] in `lang`, or the English original if there is none."""
    if lang != "en":
        translated = case.get("i18n", {}).get(lang, {}).get(field)
        if translated:
            return translated
    return case.get(field)