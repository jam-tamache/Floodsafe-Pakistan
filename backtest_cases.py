"""
Back-test case data for FloodSafe Pakistan (model tag: model-v1).

Each case is a dated, sourced event. `city` is the same lowercase key that
risk_check.py uses in REGIONAL_PROFILES and normalize_city(), so a case can
go straight into check_risk() or _compute_risk_core().

BACKTEST_PROTOCOL.md planned ERA5/Open-Meteo for rainfall, but it could not
be reached. The rainfall figures here are official station readings from
NDMA, PDMA and PMD documents instead. Each case names its document in
`source`.

`rainfall_mm` is the 72h input for check_risk(). Where the real 72h total is
not confirmed, it holds the best official figure and `rainfall_caveat`
explains the gap.

Translations: the English fields (`rainfall_caveat`, `impact`, `source`) are
the reference text. Each case also has an `i18n` dict with "ur" and "sd"
versions of them. A missing key means the English text is used. Publication
names, document numbers and URLs stay in English so every source can be
traced. The ur/sd text is unreviewed: a native speaker must read it (Sindhi
is weakest).
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
            "231.0mm is PMD's official 24-hour record at Karachi-Faisal, "
            "dated 28 Aug 2020 by PMD. That date is one day after this case "
            "window (24 Aug – 27 Aug). It is not a confirmed 72h total. "
            "True 72h total is unconfirmed and likely higher: Karachi-Faisal's "
            "full August total was 588.0mm. Treat 231.0mm as a floor, not a "
            "measured 72h figure."
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
                    "231.0 ملی میٹر کراچی-فیصل پر PMD کا سرکاری 24 گھنٹے کا ریکارڈ ہے، "
                    "جسے PMD نے 28 اگست 2020 کی تاریخ دی ہے۔ یہ تاریخ اس کیس کی مدت "
                    "(24 تا 27 اگست) سے ایک دن بعد ہے۔ یہ تصدیق شدہ 72 گھنٹے کا کل نہیں۔ "
                    "72 گھنٹے کا اصل کل غیر تصدیق شدہ اور غالباً زیادہ ہے: "
                    "کراچی-فیصل پر اگست کا پورا کل 588.0 ملی میٹر تھا۔ "
                    "231.0 ملی میٹر کو کم از کم حد سمجھیں، ناپا ہوا 72 گھنٹے کا عدد نہیں۔"
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
                    "231.0 ملي ميٽر ڪراچي-فيصل تي PMD جو سرڪاري 24 ڪلاڪن جو رڪارڊ آهي، "
                    "جنهن کي PMD 28 آگسٽ 2020 جي تاريخ ڏني آهي. هي تاريخ هن ڪيس جي مدي "
                    "(24 کان 27 آگسٽ) کان هڪ ڏينهن پوءِ آهي. هي تصديق ٿيل 72 ڪلاڪن جو ڪل ناهي. "
                    "72 ڪلاڪن جو اصل ڪل غير تصديق ٿيل ۽ غالباً وڌيڪ آهي: "
                    "ڪراچي-فيصل تي آگسٽ جو پورو ڪل 588.0 ملي ميٽر هو. "
                    "231.0 ملي ميٽر کي گهٽ ۾ گهٽ حد سمجهو، ماپيل 72 ڪلاڪن جو انگ نه."
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
            "137.0mm is the SBA station reading for the 24-25 Aug 24h "
            "window (NDMA SITREP-073). Damage figures below are a snapshot "
            "as of 23-24 Aug: one day earlier, same ongoing flood spell "
            "(started 17 Aug), not the identical 24h window."
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
                    "137.0 ملی میٹر 24-25 اگست کے 24 گھنٹوں کے لیے SBA اسٹیشن کی "
                    "ریڈنگ ہے (NDMA SITREP-073)۔ نقصان کے اعداد 23-24 اگست تک کا "
                    "اسنیپ شاٹ ہیں: ایک دن پہلے کے، اسی جاری سیلابی سلسلے "
                    "(17 اگست سے شروع) کے، بالکل وہی 24 گھنٹے نہیں۔"
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
                    "137.0 ملي ميٽر 24-25 آگسٽ جي 24 ڪلاڪن لاءِ SBA اسٽيشن جي "
                    "ريڊنگ آهي (NDMA SITREP-073). نقصان جا انگ 23-24 آگسٽ تائين جو "
                    "اسنيپ شاٽ آهن: هڪ ڏينهن اڳ جا، ساڳئي جاري سيلابي سلسلي "
                    "(17 آگسٽ کان شروع) جا، بلڪل اهي 24 ڪلاڪ نه."
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
            "No rain-gauge rainfall figure was found for this case: it is "
            "satellite-confirmed inundation (Sentinel-1 SAR), not a rainfall "
            "reading. Cannot be run through check_risk()'s rainfall-based "
            "scoring as-is; usable only if the back-test separately checks "
            "elevation/terrain logic, or if a rainfall figure is found later."
        ),
        "actual_outcome": "flood",
        "impact": "Flood extent confirmed via Sentinel-1 SAR imagery, ~28 Aug 2022",
        "source": (
            "Roth, F. et al., 'Sentinel-1-based analysis of the severe flood over "
            "Pakistan 2022', Nat. Hazards Earth Syst. Sci. 23, 3305-3325, 2023 "
            "(https://nhess.copernicus.org/articles/23/3305/2023/); "
            "'A framework for multi-sensor satellite data to evaluate crop "
            "production losses...', Nature Sci. Reports, 2023 "
            "(https://www.nature.com/articles/s41598-023-30347-y)"
        ),
        "i18n": {
            # No "source" key: it is a citation, so the English original is
            # shown in every language.
            "ur": {
                "rainfall_caveat": (
                    "اس کیس کے لیے بارش ناپنے والے آلے کا کوئی عدد نہیں ملا۔ یہ "
                    "سیٹلائٹ (Sentinel-1 SAR) سے تصدیق شدہ زیرِ آب علاقہ ہے، بارش کی "
                    "ریڈنگ نہیں۔ اسے بارش پر مبنی اسکورنگ میں جوں کا توں نہیں چلایا "
                    "جا سکتا؛ یہ تبھی کارآمد ہے جب بیک ٹیسٹ بلندی/زمین کے منطق کو "
                    "الگ سے جانچے، یا بعد میں بارش کا عدد مل جائے۔"
                ),
                "impact": "Sentinel-1 SAR تصاویر سے سیلاب کا پھیلاؤ تصدیق شدہ، تقریباً 28 اگست 2022",
            },
            "sd": {
                "rainfall_caveat": (
                    "هن ڪيس لاءِ برسات ماپڻ واري اوزار جو ڪو انگ نه مليو. هي "
                    "سيٽلائيٽ (Sentinel-1 SAR) مان تصديق ٿيل پاڻيءَ هيٺ آيل علائقو آهي، "
                    "برسات جي ريڊنگ نه. ان کي برسات تي ٻڌل اسڪورنگ ۾ جيئن آهي تيئن "
                    "نٿو هلائي سگهجي؛ هي تڏهن ڪم جو آهي جڏهن بيڪ ٽيسٽ بلندي/زمين جي "
                    "منطق کي الڳ جاچي، يا پوءِ برسات جو انگ ملي وڃي."
                ),
                "impact": "Sentinel-1 SAR تصويرن مان سيلاب جو ڦهلاءُ تصديق ٿيل، لڳ ڀڳ 28 آگسٽ 2022",
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
        "rainfall_caveat": None,
        "actual_outcome": "flood",
        "impact": "Part of a multi-district event; 8 deaths province-wide (see nawabshah/umerkot entries for shared context)",
        "source": (
            "Dawn, 3 Aug 2026, 'Sindh CM Murad orders emergency steps as downpour "
            "wreaks havoc in several districts' (https://www.dawn.com/news/2020214) "
            "(verified against full article text, not a snippet)"
        ),
        "i18n": {
            "ur": {
                "impact": "کئی اضلاع میں پھیلے واقعے کا حصہ؛ پورے صوبے میں 8 اموات (مشترکہ پس منظر کے لیے نوابشاہ/عمرکوٹ کے اندراجات دیکھیں)",
                "source": (
                    "Dawn، 3 اگست 2026، 'Sindh CM Murad orders emergency steps as downpour "
                    "wreaks havoc in several districts' (https://www.dawn.com/news/2020214) "
                    "(مکمل مضمون کے متن سے تصدیق کی گئی، صرف اقتباس سے نہیں)"
                ),
            },
            "sd": {
                "impact": "ڪيترن ضلعن ۾ پکڙيل واقعي جو حصو؛ سڄي صوبي ۾ 8 موت (گڏيل پس منظر لاءِ نوابشاهه/عمرڪوٽ جا اندراج ڏسو)",
                "source": (
                    "Dawn، 3 آگسٽ 2026، 'Sindh CM Murad orders emergency steps as downpour "
                    "wreaks havoc in several districts' (https://www.dawn.com/news/2020214) "
                    "(پورو مضمون پڙهي تصديق ڪئي وئي، رڳو اقتباس مان نه)"
                ),
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
        "rainfall_caveat": None,
        "actual_outcome": "flood",
        "impact": "Part of the same multi-district event as hyderabad_aug2026/umerkot_aug2026",
        "source": "Dawn, 3 Aug 2026 (https://www.dawn.com/news/2020214)",
        "i18n": {
            "ur": {
                "impact": "اسی کئی اضلاع والے واقعے کا حصہ جس میں hyderabad_aug2026 اور umerkot_aug2026 شامل ہیں",
                "source": "Dawn، 3 اگست 2026 (https://www.dawn.com/news/2020214)",
            },
            "sd": {
                "impact": "ساڳئي ڪيترن ضلعن وارو واقعو جنهن ۾ hyderabad_aug2026 ۽ umerkot_aug2026 شامل آهن",
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
        "rainfall_caveat": None,
        "actual_outcome": "flood",
        "impact": "Highest rainfall in Sindh this event; 1 death by drowning; part of the same multi-district event",
        "source": "Dawn, 3 Aug 2026 (https://www.dawn.com/news/2020214)",
        "i18n": {
            "ur": {
                "impact": "اس واقعے میں سندھ کی سب سے زیادہ بارش؛ ڈوبنے سے 1 موت؛ اسی کئی اضلاع والے واقعے کا حصہ",
                "source": "Dawn، 3 اگست 2026 (https://www.dawn.com/news/2020214)",
            },
            "sd": {
                "impact": "هن واقعي ۾ سنڌ جي سڀ کان وڌيڪ برسات؛ ٻڏڻ سبب 1 موت؛ ساڳئي ڪيترن ضلعن وارو واقعو",
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
        "rainfall_caveat": None,
        "actual_outcome": "no_flood",
        "impact": "No flood damage reported in this window (Sindh section notes 'few deaths and damages' province-wide, not tied to this specific reading)",
        "source": (
            "NDMA Monsoon 2020 Daily SITREP No. 045, dated 9 Aug 2020, "
            "PMD rainfall Annex B (https://www.ndma.gov.pk/storage/sitreps/September2020/9y0Bmj0Ri5QMx5zX05bM.pdf)"
        ),
        "i18n": {
            "ur": {
                "impact": "اس مدت میں سیلابی نقصان کی کوئی اطلاع نہیں (سندھ کے حصے میں پورے صوبے کے لیے 'کم اموات اور نقصانات' درج ہیں، جو اس مخصوص ریڈنگ سے منسلک نہیں)",
                "source": (
                    "NDMA Monsoon 2020 Daily SITREP نمبر 045، مورخہ 9 اگست 2020، "
                    "PMD بارش کا ضمیمہ B (https://www.ndma.gov.pk/storage/sitreps/September2020/9y0Bmj0Ri5QMx5zX05bM.pdf)"
                ),
            },
            "sd": {
                "impact": "هن عرصي ۾ سيلابي نقصان جي ڪا اطلاع ناهي (سنڌ واري حصي ۾ سڄي صوبي لاءِ 'ٿورا موت ۽ نقصان' درج آهن، جيڪي هن مخصوص ريڊنگ سان ڳنڍيل ناهن)",
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
        "rainfall_caveat": None,
        "actual_outcome": "no_flood",
        "impact": "No flood damage reported in this window",
        "source": (
            "NDMA Monsoon 2020 Daily SITREP No. 045, dated 9 Aug 2020, "
            "PMD rainfall Annex B (https://www.ndma.gov.pk/storage/sitreps/September2020/9y0Bmj0Ri5QMx5zX05bM.pdf)"
        ),
        "i18n": {
            "ur": {
                "impact": "اس مدت میں سیلابی نقصان کی کوئی اطلاع نہیں",
                "source": (
                    "NDMA Monsoon 2020 Daily SITREP نمبر 045، مورخہ 9 اگست 2020، "
                    "PMD بارش کا ضمیمہ B (https://www.ndma.gov.pk/storage/sitreps/September2020/9y0Bmj0Ri5QMx5zX05bM.pdf)"
                ),
            },
            "sd": {
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
            "Damage-side NTR is confirmed (SBA is not mentioned in this SITREP's "
            "incident list at all). The 60mm rainfall figure itself has NOT been "
            "independently verified against a PMD rainfall table: flagged, not "
            "resolved."
        ),
        "actual_outcome": "no_flood",
        "impact": "No damage/incidents reported for Shaheed Benazirabad in this SITREP",
        "source": (
            "NDMA Monsoon 2022 Daily SITREP No. 031, covering 14-15 Jul 2022 "
            "(https://reliefweb.int/report/pakistan/ndma-monsoon-2022-daily-situation-report-no-031-1300-hrs-14-july-2022-1300-hrs-15-july-2022)"
        ),
        "i18n": {
            "ur": {
                "rainfall_caveat": (
                    "نقصان کے حوالے سے 'کوئی اطلاع نہیں' (NTR) کی تصدیق ہو چکی ہے "
                    "(اس SITREP کی واقعات کی فہرست میں SBA کا ذکر ہی نہیں)۔ "
                    "60 ملی میٹر کا عدد خود PMD کی بارش کی جدول سے آزادانہ طور پر "
                    "تصدیق شدہ نہیں۔ اس پر نشان لگایا گیا ہے، مسئلہ حل نہیں ہوا۔"
                ),
                "impact": "اس SITREP میں شہید بینظیرآباد کے لیے کسی نقصان یا واقعے کی اطلاع نہیں",
                "source": (
                    "NDMA Monsoon 2022 Daily SITREP نمبر 031، 14-15 جولائی 2022 کا احاطہ "
                    "(https://reliefweb.int/report/pakistan/ndma-monsoon-2022-daily-situation-report-no-031-1300-hrs-14-july-2022-1300-hrs-15-july-2022)"
                ),
            },
            "sd": {
                "rainfall_caveat": (
                    "نقصان جي حوالي سان 'ڪا اطلاع ناهي' (NTR) جي تصديق ٿي چڪي آهي "
                    "(هن SITREP جي واقعن واري فهرست ۾ SBA جو ذڪر ئي ناهي). "
                    "60 ملي ميٽر جو انگ پاڻ PMD جي برسات واري جدول سان آزاد طور "
                    "تصديق ٿيل ناهي. ان تي نشان لڳايو ويو آهي، مسئلو حل نه ٿيو آهي."
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