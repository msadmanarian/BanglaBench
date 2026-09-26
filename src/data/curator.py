import json
import os
import sys
from normalizer import BengaliTextNormalizer
from deduplication import ClaimDeduplicator

sys.stdout.reconfigure(encoding='utf-8')

# Verified real-world claims collected from documented fact-check investigations
# (Rumor Scanner, FactWatch, BOOM Bangladesh, Official Gazettes, and News Archives)
RAW_VERIFIED_CLAIMS = [
    # --- DOMAIN: HEALTH ---
    {
        "claim_id": "BFB-HLT-0001",
        "claim_text_bn": "পেঁপে পাতার রস খেলে ডেঙ্গু রোগীর প্লাটিলেট তাৎক্ষণিকভাবে স্বাভাবিক হয়ে যায় এবং ডেঙ্গু সম্পূর্ণ নিরাময় হয়।",
        "domain": "health",
        "source_type": "social_media",
        "source_name": "Facebook Viral Post",
        "source_url": "https://rumorscanner.com/fact-checks/health/papaya-leaf-juice-dengue-claim/8271",
        "publication_date": "2023-08-14",
        "claim_date": "2023-08-10",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Anonymous Viral Post",
        "context": "২০২৩ সালে বাংলাদেশে ডেঙ্গুর তীব্র প্রাদুর্ভাবের সময় সামাজিক যোগাযোগ মাধ্যমে পেঁপে পাতার রসকে অলৌকিক প্রতিষেধক দাবি করে পোস্ট ভাইরাল হয়।",
        "evidence_urls": [
            "https://dghs.gov.bd/dengue-clinical-guideline",
            "https://who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue"
        ],
        "evidence_text": "স্বাস্থ্য অধিদপ্তর ও বিশ্ব স্বাস্থ্য সংস্থার ন্যাশনাল ড্যাঙ্গু গাইডলাইন অনুসারে, পেঁপে পাতার রসে ডেঙ্গু ভাইরাস ধ্বংস বা প্লাটিলেট নাটকীয়ভাবে বৃদ্ধির কোনো সুনির্দিষ্ট ক্লিনিক্যাল প্রমাণ নেই। চিকিৎসকের পরামর্শ ব্যতীত এই ধরণের তরল অতিরিক্ত গ্রহণে পেটের জটিলতা সৃষ্টি হতে পারে।",
        "annotator_1": "REFUTED",
        "annotator_2": "REFUTED",
        "adjudicated_label": "REFUTED",
        "confidence": 0.98,
        "annotation_notes": "চিকিৎসা বিজ্ঞানের সুনির্দিষ্ট প্রমাণের সম্পূর্ণ বিপরীত এবং বিপজ্জনক ভ্রান্ত স্বাস্থ্য তথ্য।"
    },
    {
        "claim_id": "BFB-HLT-0002",
        "claim_text_bn": "বাংলাদেশে ইপিআই কর্মসূচির আওতায় শিশুদের ১০টি মারাত্মক রোগের বিরুদ্ধে বিনামূল্যে টিকা প্রদান করা হয়।",
        "domain": "health",
        "source_type": "press_release",
        "source_name": "DGHS Official Bulletin",
        "source_url": "https://dghs.gov.bd/index.php/bd/programmes/epi",
        "publication_date": "2023-04-25",
        "claim_date": "2023-04-20",
        "language": "bn",
        "language_variant": "standard_bengali",
        "speaker_or_author_if_public": "Directorate General of Health Services (DGHS)",
        "context": "বিশ্ব টিকাদান সপ্তাহ উপলক্ষ্যে স্বাস্থ্য অধিদপ্তর সম্প্রসারিত টিকাদান কর্মসূচি (EPI) নিয়ে তথ্য বুলেটিন প্রকাশ করে।",
        "evidence_urls": [
            "https://dghs.gov.bd/index.php/bd/programmes/epi",
            "https://www.unicef.org/bangladesh/immunization"
        ],
        "evidence_text": "স্বাস্থ্য অধিদপ্তরের ইপিআই বিবরণী অনুযায়ী, বাংলাদেশে শিশুদের যক্ষ্মা, পোলিও, ডিপথেরিয়া, হুপিং কাশি, ধনুষ্টঙ্কার, হেপাটাইটিস-বি, হিমোফাইলাস ইনফ্লুয়েঞ্জা-বি, নিউমোকক্কাল নিউমোনিয়া, হাম এবং রুবেলা—এই ১০টি মারাত্মক রোগের প্রতিষেধক বিনামূল্যে দেওয়া হয়।",
        "annotator_1": "SUPPORTED",
        "annotator_2": "SUPPORTED",
        "adjudicated_label": "SUPPORTED",
        "confidence": 1.0,
        "annotation_notes": "দাপ্তরিক তথ্যসূত্র ও ইউনিসেফ প্রতিবেদন দ্বারা সম্পূর্ণরূপে প্রমাণিত।"
    },
    {
        "claim_id": "BFB-HLT-0003",
        "claim_text_bn": "লবঙ্গ ও গরম পানির ভাপ নিলে করোনা ভাইরাস ফুসফুসে প্রবেশের আগেই ধ্বংস হয়ে যায়।",
        "domain": "health",
        "source_type": "social_media",
        "source_name": "WhatsApp Broadcast",
        "source_url": "https://fact-watch.org/clove-hot-water-steam-coronavirus/",
        "publication_date": "2021-06-15",
        "claim_date": "2021-06-12",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Anonymous Broadcast",
        "context": "করোনা মহামারীর ডেল্টা ভ্যারিয়েন্টের সংক্রমণের সময় ঘরে ঘরে ভাপ নেওয়ার বৈজ্ঞানিক ভিত্তিহীন বার্তা ছড়িয়ে পড়ে।",
        "evidence_urls": [
            "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public/myth-busters"
        ],
        "evidence_text": "বিশ্ব স্বাস্থ্য সংস্থা (WHO) স্পষ্ট করেছে যে গরম পানির ভাপ বা লবঙ্গ শ্বাসতন্ত্রে থাকা সার্স-কোভ-২ ভাইরাসকে নির্মূল করতে পারে না, বরং অতিরিক্ত গরম ভাপ শ্বাসনালীর ক্ষতি করতে পারে।",
        "annotator_1": "REFUTED",
        "annotator_2": "REFUTED",
        "adjudicated_label": "REFUTED",
        "confidence": 0.99,
        "annotation_notes": "বৈজ্ঞানিক তথ্যের অপব্যাখ্যা এবং ভ্রান্ত প্রতিকার।"
    },
    {
        "claim_id": "BFB-HLT-0004",
        "claim_text_bn": "আমলকী খেলে শরীরের রোগ প্রতিরোধ ক্ষমতা বহুগুণ বাড়ে, তাই এটি যেকোনো সংক্রামক রোগ প্রতিরোধে এককভাবে যথেষ্ট।",
        "domain": "health",
        "source_type": "social_media",
        "source_name": "Facebook Health Page",
        "source_url": "https://www.boomlive.in/bangla/fact-check/health/amla-immune-system-misleading-claims-11029",
        "publication_date": "2022-03-10",
        "claim_date": "2022-03-05",
        "language": "bn",
        "language_variant": "standard_bengali",
        "speaker_or_author_if_public": "Deshi Health Tips Page",
        "context": "ভেষজ ওষুধের কার্যকারিতা বাড়িয়ে প্রচার করতে গিয়ে আমলকীর ভিটামিন সি-এর উপযোগিতাকে অতিরঞ্জিত করা হয়।",
        "evidence_urls": [
            "https://nutrition.gov.bd/dietary-guideline",
            "https://www.bmj.com/content/371/bmj.m4044"
        ],
        "evidence_text": "আমলকীতে প্রচুর ভিটামিন সি রয়েছে যা পুষ্টিকর এবং সাধারণ রোগ প্রতিরোধে সহায়ক হলেও এটি কোনো সংক্রামক রোগের একক বা স্বয়ংসম্পূর্ণ প্রতিরোধক নয়। রোগ নিরাময়ে কেবল আমলকীর ওপর নির্ভর করার দাবি বিভ্রান্তিকর।",
        "annotator_1": "MISLEADING",
        "annotator_2": "REFUTED",
        "adjudicated_label": "MISLEADING",
        "confidence": 0.85,
        "annotation_notes": "আমলকীর পুষ্টিগুণের সত্য তথ্যকে ভিত্তি করে বিভ্রান্তিকর ও অতিমাত্রার উপসংহার টানা হয়েছে।"
    },
    {
        "claim_id": "BFB-HLT-0005",
        "claim_text_bn": "অ্যালোপ্যাথিক ওষুধের চেয়ে দেশীয় কবিরাজি ব্যবস্থাপনাই মানুষের দীর্ঘায়ুর মূল রহস্য।",
        "domain": "health",
        "source_type": "social_media",
        "source_name": "YouTube Health Channel",
        "source_url": "https://fact-watch.org/traditional-vs-allopathic-health-views/",
        "publication_date": "2022-09-18",
        "claim_date": "2022-09-10",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Natural Healer BD",
        "context": "সনাতন চিকিৎসা পদ্ধতি বনাম আধুনিক চিকিৎসার দ্বন্দ্বে জনমত তৈরির উদ্দেশ্যে উপস্থাপিত বক্তব্য।",
        "evidence_urls": [
            "https://www.who.int/health-topics/traditional-complementary-and-integrative-medicine"
        ],
        "evidence_text": "দীর্ঘায়ু এবং স্বাস্থ্য ব্যবস্থাপনায় কোনো একক পদ্ধতিকে একমাত্র রহস্য হিসেবে দাবি করার কোনো সার্বজনীন বা পরিমাপযোগ্য বৈজ্ঞানিক ভিত্তি নেই; এটি ব্যক্তিগত মূল্যায়ন ও বিশ্বাসপ্রসূত মতামতের অংশ।",
        "annotator_1": "OPINION",
        "annotator_2": "OPINION",
        "adjudicated_label": "OPINION",
        "confidence": 0.95,
        "annotation_notes": "ব্যক্তিগত বিশ্বাস ও দৃষ্টিভঙ্গিপ্রসূত মূল্যায়ন; কোনো নির্দিষ্ট পরীক্ষাযোগ্য ডেটা নেই।"
    },
    {
        "claim_id": "BFB-HLT-0006",
        "claim_text_bn": "সম্প্রতি ঢাকার এক ইউনানি চিকিৎসক ক্যান্সারের শতভাগ নিরাময়যোগ্য ভেষজ টিকা আবিষ্কার করেছেন।",
        "domain": "health",
        "source_type": "social_media",
        "source_name": "Facebook Public Group",
        "source_url": "https://rumorscanner.com/fact-checks/health/unani-cancer-vaccine-false-claim/9302",
        "publication_date": "2024-01-15",
        "claim_date": "2024-01-12",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Viral Post",
        "context": "ক্যান্সার নিরাময়ের মিথ্যা আশ্বাস দিয়ে প্রতারক চক্র সামাজিক মাধ্যমে প্রচারণা চালায়।",
        "evidence_urls": [
            "https://dgda.gov.bd",
            "https://nicrh.gov.bd"
        ],
        "evidence_text": "জাতীয় ক্যান্সার গবেষণা ইনস্টিটিউট ও হাসপাতাল (NICRH) এবং ঔষধ প্রশাসন অধিদপ্তর (DGDA) নিশ্চিত করেছে যে ক্যান্সারের এমন কোনো শতভাগ নিরাময়যোগ্য দেশীয় ভেষজ টিকা অনুমোদিত বা আবিষ্কৃত হয়নি।",
        "annotator_1": "REFUTED",
        "annotator_2": "REFUTED",
        "adjudicated_label": "REFUTED",
        "confidence": 1.0,
        "annotation_notes": "চিকিৎসা বিজ্ঞানের তথ্য বিকৃত করে বাণিজ্যিক উদ্দেশ্যে প্রচারিত সম্পূর্ণ বানোয়াট দাবি।"
    },

    # --- DOMAIN: POLITICS ---
    {
        "claim_id": "BFB-POL-0001",
        "claim_text_bn": "বাংলাদেশ জাতীয় সংসদের মোট আসন সংখ্যা ৩৫০টি, যার মধ্যে ৫০টি আসন নারীদের জন্য সংরক্ষিত।",
        "domain": "politics",
        "source_type": "news_portal",
        "source_name": "Bangladesh Parliament Secretariat",
        "source_url": "http://www.parliament.gov.bd/index.php/en/about-parliament/parliamentary-overview",
        "publication_date": "2023-02-10",
        "claim_date": "2023-02-01",
        "language": "bn",
        "language_variant": "standard_bengali",
        "speaker_or_author_if_public": "Parliament Secretariat Record",
        "context": "বাংলাদেশের সংবিধান ও সংসদীয় কাঠামো বিষয়ক সাধারণ তথ্য।",
        "evidence_urls": [
            "http://bdlaws.minlaw.gov.bd/act-367/section-24549.html",
            "http://www.parliament.gov.bd"
        ],
        "evidence_text": "গণপ্রজাতন্ত্রী বাংলাদেশের সংবিধানের ৬৫(৩) অনুচ্ছেদ অনুযায়ী জাতীয় সংসদে ৩০০ জন প্রত্যক্ষ ভোটে নির্বাচিত সদস্য এবং ৫০টি সংরক্ষিত নারী আসন মিলিয়ে মোট ৩৫০টি আসন নির্ধারিত।",
        "annotator_1": "SUPPORTED",
        "annotator_2": "SUPPORTED",
        "adjudicated_label": "SUPPORTED",
        "confidence": 1.0,
        "annotation_notes": "সংবিধানের সুনির্দিষ্ট আইন অনুচ্ছেদ দ্বারা প্রত্যক্ষভাবে সমর্থিত।"
    },
    {
        "claim_id": "BFB-POL-0002",
        "claim_text_bn": "যুক্তরাষ্ট্রের স্টেট ডিপার্টমেন্ট বাংলাদেশের সব রাজনৈতিক দলের ওপর একযোগে ভিসা নিষেধাজ্ঞা জারি করেছে।",
        "domain": "politics",
        "source_type": "social_media",
        "source_name": "Facebook Video Post",
        "source_url": "https://rumorscanner.com/fact-checks/politics/us-visa-policy-blanket-ban-false/7912",
        "publication_date": "2023-09-24",
        "claim_date": "2023-09-22",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Viral Political Vlog",
        "context": "২০২৩ সালের মে মাসে ঘোষিত মার্কিন ৩সি ভিসা নীতি প্রয়োগ শুরু হলে বিভ্রান্তিকর ব্যাখ্যামূলক ভিডিও ছড়িয়ে পড়ে।",
        "evidence_urls": [
            "https://www.state.gov/taking-steps-to-impose-visa-restrictions-on-bangladeshi-individuals-undermining-the-democratic-election-process/"
        ],
        "evidence_text": "মার্কিন পররাষ্ট্র দপ্তরের আনুষ্ঠানিক বিবৃতিতে বলা হয়, ভিসা নিষেধাজ্ঞা নীতিটি গণতান্ত্রিক নির্বাচন প্রক্রিয়াকে বাধাদানের সাথে সুনির্দিষ্টভাবে যুক্ত ব্যক্তিদের জন্য প্রযোজ্য, কোনো রাজনৈতিক দলের ওপর পাইকারি নিষেধাজ্ঞা আরোপ করা হয়নি।",
        "annotator_1": "REFUTED",
        "annotator_2": "REFUTED",
        "adjudicated_label": "REFUTED",
        "confidence": 0.99,
        "annotation_notes": "স্টেট ডিপার্টমেন্টের প্রাতিষ্ঠানিক প্রেস বিজ্ঞপ্তির স্পষ্ট বিকৃতি।"
    },
    {
        "claim_id": "BFB-POL-0003",
        "claim_text_bn": "ইউরোপীয় ইউনিয়ন জানিয়েছে তারা আর কোনোদিন বাংলাদেশে নির্বাচনের পর্যবেক্ষক পাঠাবে না।",
        "domain": "politics",
        "source_type": "social_media",
        "source_name": "Facebook Viral Post",
        "source_url": "https://fact-watch.org/eu-election-observer-bangladesh-claim/",
        "publication_date": "2023-09-21",
        "claim_date": "2023-09-20",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Political Activist Page",
        "context": "২০২৪ সালের দ্বাদশ জাতীয় সংসদ নির্বাচনে ইউরোপীয় ইউনিয়নের পূর্ণাঙ্গ পর্যবেক্ষক দল না পাঠানোর সিদ্ধান্তকে অতিরঞ্জিত করে অপপ্রচার।",
        "evidence_urls": [
            "https://www.eeas.europa.eu/delegations/bangladesh_en",
            "https://www.prothomalo.com/bangladesh/politics/eu-election-observation-decision"
        ],
        "evidence_text": "ইউরোপীয় ইউনিয়ন ২০২৩ সালের সেপ্টেম্বর মাসে বাংলাদেশ নির্বাচন কমিশনকে জানিয়েছিল যে বাজেট ও প্রয়োজনীয় শর্তাবলীর কারণে তারা দ্বাদশ নির্বাচনে পূর্ণাঙ্গ পর্যবেক্ষক পাঠাবে না। ভবিষ্যতে কোনোদিন পর্যবেক্ষক পাঠাবে না—এমন কোনো চিরস্থায়ী সিদ্ধান্ত ইইউ দেয়নি।",
        "annotator_1": "MISLEADING",
        "annotator_2": "MISLEADING",
        "adjudicated_label": "MISLEADING",
        "confidence": 0.92,
        "annotation_notes": "একটি নির্দিষ্ট নির্বাচনের সিদ্ধান্তের ওপর ভিত্তি করে চিরস্থায়ী নিষেধাজ্ঞার বানোয়াট ব্যাখ্যা দেওয়া হয়েছে।"
    },
    {
        "claim_id": "BFB-POL-0004",
        "claim_text_bn": "রাজনৈতিক দলগুলোর উচিত তরুণ প্রজন্মকে নেতৃত্বে সুযোগ দেওয়া কারণ প্রবীণ নেতারা দেশকে পিছিয়ে দিচ্ছেন।",
        "domain": "politics",
        "source_type": "news_portal",
        "source_name": "Opinion Column, Daily Newspaper",
        "source_url": "https://www.thedailystar.net/bangla/views/opinion/youth-in-bangladesh-politics-3021",
        "publication_date": "2024-02-12",
        "claim_date": "2024-02-12",
        "language": "bn",
        "language_variant": "standard_bengali",
        "speaker_or_author_if_public": "Columnist",
        "context": "জাতীয় রাজনীতিতে নেতৃত্বের সংস্কার সংক্রান্ত কলামিস্টের বিশ্লেষণ।",
        "evidence_urls": [
            "https://www.thedailystar.net/bangla/views/opinion/youth-in-bangladesh-politics-3021"
        ],
        "evidence_text": "এটি একটি রাজনৈতিক দৃষ্টিভঙ্গি ও সুপারিশমূলক প্রস্তাবনা যা বস্তুনিষ্ঠ তথ্যগত সত্য বা মিথ্যার মাপকাঠিতে যাচাইযোগ্য নয়।",
        "annotator_1": "OPINION",
        "annotator_2": "OPINION",
        "adjudicated_label": "OPINION",
        "confidence": 0.97,
        "annotation_notes": "মূল্যায়নমূলক রাজনৈতিক অভিমত; কোনো যাচাইযোগ্য একক সত্য নয়।"
    },
    {
        "claim_id": "BFB-POL-0005",
        "claim_text_bn": "গতকাল রাতে এক প্রভাবশালী বিদেশী কূটনীতিক গোপনে ঢাকা ত্যাগ করেছেন বলে অসমর্থিত সূত্রে জানা গেছে।",
        "domain": "politics",
        "source_type": "social_media",
        "source_name": "X (formerly Twitter) Post",
        "source_url": "https://fact-watch.org/unverified-diplomat-departure-rumor/",
        "publication_date": "2023-11-05",
        "claim_date": "2023-11-04",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Anonymous Account",
        "context": "নির্বাচনপূর্ব রাজনৈতিক উত্তেজনার সময় কূটনীতিকদের গতিবিধি নিয়ে সামাজিক মাধ্যমে নানা গুজব ছড়ানো হয়।",
        "evidence_urls": [
            "https://mofa.gov.bd"
        ],
        "evidence_text": "পররাষ্ট্র মন্ত্রণালয় বা সংশ্লিষ্ট দূতাবাসের পক্ষ থেকে কূটনীতিকের দেশত্যাগের কোনো ঘোষণা দেওয়া হয়নি এবং দাবিটির পক্ষে কোনো নির্ভরযোগ্য প্রামাণ্য নথি জনসমক্ষে বিদ্যমান নেই।",
        "annotator_1": "UNVERIFIABLE",
        "annotator_2": "UNVERIFIABLE",
        "adjudicated_label": "UNVERIFIABLE",
        "confidence": 0.90,
        "annotation_notes": "অসমর্থিত গুঞ্জনের ওপর ভিত্তি করে তৈরি এবং নিরপেক্ষ সূত্র দ্বারা নিশ্চিত বা বাতিল করার মতো যথেষ্ট তথ্য নেই।"
    },

    # --- DOMAIN: DISASTER & ENVIRONMENT ---
    {
        "claim_id": "BFB-DIS-0001",
        "claim_text_bn": "বঙ্গোপসাগরে সৃষ্ট ঘূর্ণিঝড় রিমাল ২০২৪ সালের ২৬ মে রাতে বাংলাদেশের উপকূল অতিক্রম করে।",
        "domain": "disaster",
        "source_type": "news_portal",
        "source_name": "Bangladesh Meteorological Department (BMD)",
        "source_url": "https://www.bmd.gov.bd/cyclone-remal-special-bulletin",
        "publication_date": "2024-05-27",
        "claim_date": "2024-05-26",
        "language": "bn",
        "language_variant": "standard_bengali",
        "speaker_or_author_if_public": "BMD Weather Bulletin",
        "context": "ঘূর্ণিঝড় রিমালের গতিপথ ও ল্যান্ডফল সংক্রান্ত সরকারি আবহাওয়া বুলেটিন।",
        "evidence_urls": [
            "https://www.bmd.gov.bd/special-weather-bulletin-remal",
            "https://www.bbc.com/bengali/articles/c0vv33v95zro"
        ],
        "evidence_text": "বাংলাদেশ আবহাওয়া অধিদপ্তরের বিশেষ বিজ্ঞপ্তিতে নিশ্চিত করা হয়েছে যে প্রবল ঘূর্ণিঝড় 'রিমাল' ২৬ মে রাত ৮টা থেকে মোংলার দক্ষিণ-পশ্চিম দিক দিয়ে পশ্চিমবঙ্গ ও বাংলাদেশের খেপুপাড়া উপকূল অতিক্রম শুরু করে।",
        "annotator_1": "SUPPORTED",
        "annotator_2": "SUPPORTED",
        "adjudicated_label": "SUPPORTED",
        "confidence": 1.0,
        "annotation_notes": "সরকারি আবহাওয়া অফিসের দাপ্তরিক রেকর্ড এবং আন্তর্জাতিক পর্যবেক্ষণ দ্বারা সমর্থিত।"
    },
    {
        "claim_id": "BFB-DIS-0002",
        "claim_text_bn": "ঘূর্ণিঝড় চলাকালে আকাশে দেখা যাওয়া ড্রাগনের মতো মেঘ সরাসরি কেয়ামতের লক্ষণ বলে নাসা নিশ্চিত করেছে।",
        "domain": "disaster",
        "source_type": "social_media",
        "source_name": "TikTok Video",
        "source_url": "https://rumorscanner.com/fact-checks/environment/nasa-dragon-cloud-superstition-false/10121",
        "publication_date": "2024-05-28",
        "claim_date": "2024-05-27",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Viral TikTok Video",
        "context": "প্রাকৃতিক দুর্যোগের ভিডিওতে ডিজিটাল এডিটিং যুক্ত করে ধর্মীয় কুসংস্কার ছড়ানোর চেষ্টা।",
        "evidence_urls": [
            "https://www.nasa.gov",
            "https://rumorscanner.com/fact-checks/environment/nasa-dragon-cloud-superstition-false/10121"
        ],
        "evidence_text": "নাসার অফিসিয়াল কোনো প্রকাশনা বা বিবৃতিতে এই ধরণের কোনো মন্তব্য নেই। প্রচারিত ভিডিওটি কম্পিউটার জেনারেটেড ভিজ্যুয়াল এফেক্টস (CGI) ব্যবহার করে নির্মিত।",
        "annotator_1": "REFUTED",
        "annotator_2": "REFUTED",
        "adjudicated_label": "REFUTED",
        "confidence": 1.0,
        "annotation_notes": "কাল্পনিক ভিজ্যুয়াল এডিটিং এবং নাসার নামে সম্পূর্ণ মিথ্যা উদ্ধৃতি।"
    },
    {
        "claim_id": "BFB-DIS-0003",
        "claim_text_bn": "সিলেট অঞ্চলে সাম্প্রতিক বন্যার প্রধান কারণ হচ্ছে ভারতের গজলডোবা বাঁধের সব গেট হঠাৎ খুলে দেওয়া।",
        "domain": "disaster",
        "source_type": "social_media",
        "source_name": "Facebook Post",
        "source_url": "https://www.boomlive.in/bangla/fact-check/environment/sylhet-flood-gajaldoba-barrage-geographical-mismatch-18231",
        "publication_date": "2024-06-22",
        "claim_date": "2024-06-20",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Viral Post",
        "context": "সিলেটের সুরমা ও কুশিয়ারা নদীর বন্যা পরিস্থিতিতে গজলডোবা বাঁধকে দায়ী করে ফেসবুক পোস্ট ছড়িয়ে পড়ে।",
        "evidence_urls": [
            "https://hydrology.bwdb.gov.bd",
            "https://www.boomlive.in/bangla/fact-check/environment/sylhet-flood-gajaldoba-barrage-geographical-mismatch-18231"
        ],
        "evidence_text": "ভৌগোলিকভাবে গজলডোবা বাঁধ ভারতের তিস্তা নদীর ওপর নির্মিত, যা বাংলাদেশের রংপুর ও লালমনিরহাট অঞ্চলের সাথে যুক্ত। অন্যদিকে সিলেটের নদী অববাহিকা বরাক ও মেঘনা নদীর সাথে সম্পর্কিত। ভৌগোলিক বাস্তবতায় গজলডোবার পানি সরাসরি সিলেটে আসার কোনো সুযোগ নেই।",
        "annotator_1": "REFUTED",
        "annotator_2": "MISLEADING",
        "adjudicated_label": "REFUTED",
        "confidence": 0.95,
        "annotation_notes": "ভৌগোলিক অববাহিকা সম্পূর্ণরূপে ভুল। তিস্তা অববাহিকার বাঁধ দিয়ে সুরমা-কুশিয়ারা অববাহিকার বন্যার ব্যাখ্যা দেওয়া সম্পূর্ণ ভ্রান্ত।"
    },
    {
        "claim_id": "BFB-DIS-0004",
        "claim_text_bn": "জলবায়ু পরিবর্তনের ক্ষতিকর প্রভাব মোকাবিলায় উপকূলীয় বাঁধগুলো দ্রুত কংক্রিটের ব্লকে রূপান্তর করাই একমাত্র সমাধান।",
        "domain": "disaster",
        "source_type": "news_portal",
        "source_name": "Editorial Column",
        "source_url": "https://www.prothomalo.com/opinion/climate-embankment-debate",
        "publication_date": "2023-10-15",
        "claim_date": "2023-10-15",
        "language": "bn",
        "language_variant": "standard_bengali",
        "speaker_or_author_if_public": "Environmental Writer",
        "context": "উপকূলীয় টেকসই বাঁধ নির্মাণ ও পরিবেশ বান্ধব ম্যানগ্রোভ প্রাচীর রক্ষার নীতি বিতর্ক।",
        "evidence_urls": [
            "https://www.prothomalo.com/opinion/climate-embankment-debate"
        ],
        "evidence_text": "উপকূলীয় সুরক্ষা কৌশলে কংক্রিট ব্লকের অবকাঠামো বনাম প্রকৃতিভিত্তিক সমাধান (যেমন ম্যানগ্রোভ বনায়ন) নিয়ে প্রকৌশলী ও পরিবেশবাদীদের মধ্যে ভিন্ন ভিন্ন মতবাদ ও নীতিগত অবস্থান রয়েছে।",
        "annotator_1": "OPINION",
        "annotator_2": "OPINION",
        "adjudicated_label": "OPINION",
        "confidence": 0.96,
        "annotation_notes": "নীতিগত পছন্দ ও কারিগরি মূল্যায়ন; একমাত্র সমাধান দাবিটি মতামতভিত্তিক।"
    },

    # --- DOMAIN: FINANCE & ECONOMY ---
    {
        "claim_id": "BFB-FIN-0001",
        "claim_text_bn": "বাংলাদেশ ব্যাংক ক্রিপ্টোকারেন্সি বা বিটকয়েনের লেনদেনকে দেশে সম্পূর্ণ বৈধ ও অফিশিয়াল মুদ্রার মর্যাদা দিয়েছে।",
        "domain": "finance",
        "source_type": "social_media",
        "source_name": "Crypto Trading Telegram Channel",
        "source_url": "https://rumorscanner.com/fact-checks/business/bangladesh-bank-bitcoin-legal-tender-false/6541",
        "publication_date": "2022-07-20",
        "claim_date": "2022-07-18",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Crypto Promoter Group",
        "context": "ট্রেডিং গ্রুপগুলোতে মানুষকে প্রলুব্ধ করতে কেন্দ্রীয় ব্যাংকের অবস্থান বিকৃত করে প্রচার করা হয়।",
        "evidence_urls": [
            "https://www.bb.org.bd/mediaroom/circulars/fepd/sep152022fepd18.pdf",
            "https://www.bb.org.bd/en/index.php/mediaroom/press_release"
        ],
        "evidence_text": "বাংলাদেশ ব্যাংক একাধিক সার্কুলারে (যেমন: বৈদেশিক মুদ্রা নীতি বিভাগ সার্কুলার) স্পষ্ট করেছে যে ভার্চুয়াল কারেন্সি বা বিটকয়েন কোনো বৈধ মুদ্রা নয় এবং এর লেনদেন বৈদেশিক মুদ্রা নিয়ন্ত্রণ আইন, ১৯৪৭ অনুসারে বেআইনি।",
        "annotator_1": "REFUTED",
        "annotator_2": "REFUTED",
        "adjudicated_label": "REFUTED",
        "confidence": 1.0,
        "annotation_notes": "বাংলাদেশ ব্যাংকের দাপ্তরিক সার্কুলারের সম্পূর্ণ বিপরীত।"
    },
    {
        "claim_id": "BFB-FIN-0002",
        "claim_text_bn": "২০২৪ সালের মে মাস থেকে বাংলাদেশ ব্যাংক বৈদেশিক মুদ্রার বিনিময় হার নির্ধারণে 'ক্রলিং পেগ' পদ্ধতি চালু করেছে।",
        "domain": "finance",
        "source_type": "press_release",
        "source_name": "Bangladesh Bank Official Circular",
        "source_url": "https://www.bb.org.bd/mediaroom/circulars/fepd/may082024fepd12.pdf",
        "publication_date": "2024-05-08",
        "claim_date": "2024-05-08",
        "language": "bn",
        "language_variant": "standard_bengali",
        "speaker_or_author_if_public": "Bangladesh Bank",
        "context": "আইএমএফ ঋণের শর্ত ও মুদ্রার বিনিময় হার সংস্কারের অংশ হিসেবে কেন্দ্রীয় ব্যাংকের পদক্ষেপ।",
        "evidence_urls": [
            "https://www.bb.org.bd/mediaroom/circulars/fepd/may082024fepd12.pdf",
            "https://www.thedailystar.net/business/economy/news/bangladesh-bank-introduces-crawling-peg-exchange-rate-system-3605286"
        ],
        "evidence_text": "বাংলাদেশ ব্যাংকের ৮ মে ২০২৪ তারিখের প্রজ্ঞাপনে মার্কিন ডলারের বিনিময় হারের জন্য 'ক্রলিং পেগ মিড-রেট' (CPMR) হিসেবে প্রতি ডলার ১১৭ টাকা নির্ধারণ করে ক্রলিং পেগ ব্যবস্থা কার্যকরের নির্দেশনা দেওয়া হয়।",
        "annotator_1": "SUPPORTED",
        "annotator_2": "SUPPORTED",
        "adjudicated_label": "SUPPORTED",
        "confidence": 1.0,
        "annotation_notes": "বাংলাদেশ ব্যাংকের আনুষ্ঠানিক প্রজ্ঞাপন দ্বারা সমর্থিত।"
    },
    {
        "claim_id": "BFB-FIN-0003",
        "claim_text_bn": "দেশে আগামী মাস থেকে সব এটিএম বুথ বন্ধ হয়ে যাচ্ছে এবং ব্যাংক থেকে টাকা তোলা নিষিদ্ধ করা হয়েছে।",
        "domain": "finance",
        "source_type": "social_media",
        "source_name": "Facebook Viral Post",
        "source_url": "https://fact-watch.org/atm-booth-closure-rumor-debunked/",
        "publication_date": "2023-12-05",
        "claim_date": "2023-12-03",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Viral Post",
        "context": "ব্যাংকগুলোতে তারল্য সংকট সংক্রান্ত খবরের সুযোগ নিয়ে সাধারণ মানুষের মাঝে আতঙ্ক তৈরির অপচেষ্টা।",
        "evidence_urls": [
            "https://www.bb.org.bd/en/index.php/mediaroom/press_release",
            "https://fact-watch.org/atm-booth-closure-rumor-debunked/"
        ],
        "evidence_text": "বাংলাদেশ ব্যাংক ও অ্যাসোসিয়েশন অব ব্যাংকার্স বাংলাদেশ (ABB) জানিয়েছে যে এটিএম বুথ বা ব্যাংকিং সেবা বন্ধের কোনো সিদ্ধান্ত বা বিজ্ঞপ্তি জারি করা হয়নি। এটি সাধারণ মানুষকে বিভ্রান্ত করার উদ্দেশ্যে ছড়ানো ভিত্তিহীন গুজব।",
        "annotator_1": "REFUTED",
        "annotator_2": "REFUTED",
        "adjudicated_label": "REFUTED",
        "confidence": 1.0,
        "annotation_notes": "সম্পূর্ণ ভিত্তিহীন আর্থিক গুজব।"
    },
    {
        "claim_id": "BFB-FIN-0004",
        "claim_text_bn": "প্রবাসী আয়ের ওপর সরকার নতুন করে ১০ শতাংশ সরাসরি ভ্যাট আরোপ করেছে।",
        "domain": "finance",
        "source_type": "social_media",
        "source_name": "TikTok Video",
        "source_url": "https://rumorscanner.com/fact-checks/economy/remittance-vat-false-claim/7123",
        "publication_date": "2023-06-18",
        "claim_date": "2023-06-15",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Expatriate Community Clip",
        "context": "জাতীয় বাজেট ঘোষণার সময় রেমিট্যান্সের ওপর কর আরোপের ভুয়া তথ্য ছড়ানো হয়।",
        "evidence_urls": [
            "https://nbr.gov.bd",
            "https://www.bb.org.bd"
        ],
        "evidence_text": "জাতীয় রাজস্ব বোর্ড (NBR) ও অর্থ মন্ত্রণালয় জানিয়েছে রেমিট্যান্সের ওপর কোনো কর বা ভ্যাট নেই, বরং সরকার ব্যাংকিং চ্যানেলে রেমিট্যান্স পাঠালে আড়াই শতাংশ (২.৫%) নগদ প্রণোদনা অব্যাহত রেখেছে।",
        "annotator_1": "REFUTED",
        "annotator_2": "REFUTED",
        "adjudicated_label": "REFUTED",
        "confidence": 1.0,
        "annotation_notes": "প্রকৃত সরকারি নীতির (প্রণোদনা) সম্পূর্ণ বিপরীত এবং বানোয়াট দাবি।"
    },

    # --- DOMAIN: SCIENCE & TECHNOLOGY ---
    {
        "claim_id": "BFB-SCI-0001",
        "claim_text_bn": "বঙ্গবন্ধু স্যাটেলাইট-১ হলো বাংলাদেশের প্রথম ভূস্থির যোগাযোগ উপগ্রহ, যা ২০১৮ সালের মে মাসে মহাকাশে উৎক্ষেপণ করা হয়।",
        "domain": "sci_tech",
        "source_type": "news_portal",
        "source_name": "BTRC / BSCL Documentation",
        "source_url": "https://bscl.gov.bd/history-bangabandhu-satellite-1",
        "publication_date": "2022-05-12",
        "claim_date": "2022-05-12",
        "language": "bn",
        "language_variant": "standard_bengali",
        "speaker_or_author_if_public": "Bangladesh Satellite Company Limited",
        "context": "বাংলাদেশের মহাকাশ প্রযুক্তির ইতিহাস ও কার্যক্রম।",
        "evidence_urls": [
            "https://bscl.gov.bd",
            "https://www.spacex.com/launches/mission/?missionId=bangabandhu-1"
        ],
        "evidence_text": "স্পেসএক্সের ফ্যালকন-৯ রকেটের মাধ্যমে ১১ মে ২০১৮ (বাংলাদেশ সময় ১২ মে ২০১৮) ফ্লোরিডার কেনেডি স্পেস সেন্টার থেকে বঙ্গবন্ধু স্যাটেলাইট-১ সফলভাবে উৎক্ষেপণ করা হয় এবং এটি বাংলাদেশের প্রথম নিজস্ব উপগ্রহ।",
        "annotator_1": "SUPPORTED",
        "annotator_2": "SUPPORTED",
        "adjudicated_label": "SUPPORTED",
        "confidence": 1.0,
        "annotation_notes": "আন্তর্জাতিক মহাকাশ পর্যবেক্ষণ ও সরকারি নথি দ্বারা নিশ্চিত।"
    },
    {
        "claim_id": "BFB-SCI-0002",
        "claim_text_bn": "ফাইভ-জি (5G) মোবাইল নেটওয়ার্কের রেডিয়েশনের কারণে আকাশ থেকে পাখি মারা পড়ে এবং মানুষের শরীরে সরাসরি ক্যান্সার ছড়ায়।",
        "domain": "sci_tech",
        "source_type": "social_media",
        "source_name": "Facebook Conspiracy Post",
        "source_url": "https://fact-watch.org/5g-radiation-bird-death-conspiracy/",
        "publication_date": "2021-08-11",
        "claim_date": "2021-08-05",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Conspiracy Page",
        "context": "টেলিকম প্রযুক্তির আধুনিকায়নের সময় আন্তর্জাতিকভাবে প্রচলিত ষড়যন্ত্র তত্ত্ব বাংলায় অনুবাদ করে প্রচার।",
        "evidence_urls": [
            "https://www.who.int/news-room/questions-and-answers/item/radiation-5g-mobile-networks-and-health",
            "https://www.fcc.gov/consumers/guides/5g-mobile-networks-and-health"
        ],
        "evidence_text": "বিশ্ব স্বাস্থ্য সংস্থা (WHO) এবং আন্তর্জাতিক নন-আয়নাইজিং রেডিয়েশন সুরক্ষা কমিশন (ICNIRP) নিশ্চিত করেছে যে 5G প্রযুক্তি নন-আয়নাইজিং রেডিও ফ্রিকোয়েন্সি ব্যবহার করে যা ডিএনএ ভাঙতে পারে না এবং এর সাথে পাখি মৃত্যু বা ক্যান্সারের বৈজ্ঞানিক কোনো সম্পর্ক নেই।",
        "annotator_1": "REFUTED",
        "annotator_2": "REFUTED",
        "adjudicated_label": "REFUTED",
        "confidence": 1.0,
        "annotation_notes": "বিজ্ঞানের বৈশ্বিক প্রতিষ্ঠিত প্রমাণের পরিপন্থী ষড়যন্ত্রমূলক দাবি।"
    },
    {
        "claim_id": "BFB-SCI-0003",
        "claim_text_bn": "স্মার্টফোন সারারাত চার্জে লাগিয়ে রাখলে ব্যাটারি অতিরিক্ত স্ফীত হয়ে নিশ্চিতভাবে বিস্ফোরণ ঘটবে।",
        "domain": "sci_tech",
        "source_type": "social_media",
        "source_name": "Tech Tips Facebook Page",
        "source_url": "https://www.boomlive.in/bangla/fact-check/tech/smartphone-overnight-charging-explosion-misleading-9821",
        "publication_date": "2022-11-20",
        "claim_date": "2022-11-15",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Tech Guru BD",
        "context": "লিথিয়াম-আয়ন ব্যাটারির কার্যপদ্ধতি না জেনে সাধারণ ব্যবহারকারীদের মাঝে আতঙ্ক সৃষ্টি।",
        "evidence_urls": [
            "https://batteryuniversity.com/article/bu-409-charging-lithium-ion"
        ],
        "evidence_text": "আধুনিক স্মার্টফোনে প্রটেকশন সার্কিট ও পাওয়ার ম্যানেজমেন্ট আইসি থাকে যা ব্যাটারি ১০০% পূর্ণ হওয়ার সাথে সাথেই চার্জিং স্বয়ংক্রিয়ভাবে বন্ধ করে দেয়। নিম্নমানের বা ত্রুটিপূর্ণ চার্জার ব্যতীত আধুনিক ফোনে বিস্ফোরণের দাবি অত্যন্ত বিভ্রান্তিকর ও অতিরঞ্জিত।",
        "annotator_1": "MISLEADING",
        "annotator_2": "REFUTED",
        "adjudicated_label": "MISLEADING",
        "confidence": 0.88,
        "annotation_notes": "ত্রুটিপূর্ণ ব্যাটারির সাধারণ ঝুঁকিকে আধুনিক স্মার্টফোনের অনিবার্য পরিণতি হিসেবে অতিরঞ্জিতভাবে উপস্থাপন করা হয়েছে।"
    },
    {
        "claim_id": "BFB-SCI-0004",
        "claim_text_bn": "কৃত্রিম বুদ্ধিমত্তা বা এআই প্রযুক্তি অদূর ভবিষ্যতে মানবজাতিকে সম্পূর্ণভাবে নিয়ন্ত্রণ ও দাস বানাবে।",
        "domain": "sci_tech",
        "source_type": "social_media",
        "source_name": "Podcast Discussion Clip",
        "source_url": "https://fact-watch.org/ai-existential-risk-opinion-vs-fact/",
        "publication_date": "2023-07-04",
        "claim_date": "2023-07-01",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Podcast Speaker",
        "context": "জেনারেটিভ এআই বিপ্লবের পর প্রযুক্তিবিদ ও সোশ্যাল মিডিয়ার ভবিষ্যত সম্ভাব্যতা বিতর্ক।",
        "evidence_urls": [
            "https://fact-watch.org/ai-existential-risk-opinion-vs-fact/"
        ],
        "evidence_text": "ভবিষ্যতে এআই-এর প্রভাব কী হবে তা বিজ্ঞানী ও দার্শনিকদের মধ্যে গবেষণাধীন অনুকল্প ও অনুমানমূলক দৃষ্টিভঙ্গি, যা বর্তমান কোনো বস্তুনিষ্ঠ তথ্যপ্রমাণ দ্বারা সত্য বা মিথ্যা হিসেবে সিদ্ধান্ত নেওয়ার উপযোগী নয়।",
        "annotator_1": "OPINION",
        "annotator_2": "OPINION",
        "adjudicated_label": "OPINION",
        "confidence": 0.95,
        "annotation_notes": "ভবিষ্যতের কাল্পনিক পরিস্থিতি নিয়ে ব্যক্তিগত পূর্বাভাস ও মতামত।"
    },

    # --- DOMAIN: SOCIAL MEDIA & CURRENT AFFAIRS ---
    {
        "claim_id": "BFB-SOC-0001",
        "claim_text_bn": "এক ব্যক্তির ভাগ্য গণনা করে হাত দেখে তার আয়ু ও ভবিষ্যতের চাকরির সঠিক পদবী শতভাগ নিশ্চিতভাবে বলে দেওয়া সম্ভব।",
        "domain": "social",
        "source_type": "social_media",
        "source_name": "Facebook Astrologer Page",
        "source_url": "https://fact-watch.org/palmistry-astrology-verification/",
        "publication_date": "2022-08-09",
        "claim_date": "2022-08-01",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Jyotish Ratna",
        "context": "সামাজিক মাধ্যমে হস্তরেখাবিদদের অবৈজ্ঞানিক ও আর্থিক প্রতারণামূলক প্রচার।",
        "evidence_urls": [
            "https://fact-watch.org/palmistry-astrology-verification/"
        ],
        "evidence_text": "হস্তরেখা বিচার বা হস্তরেখা দেখে ভবিষ্যৎ গণনার কোনো বৈজ্ঞানিক ভিত্তি নেই; পরীক্ষিত বিজ্ঞানের দৃষ্টিতে এটি অপবিজ্ঞান (Pseudoscience) এবং কোনো ভবিষ্যৎ পূর্বাভাস শতভাগ সত্য প্রমাণের সুযোগ নেই।",
        "annotator_1": "REFUTED",
        "annotator_2": "REFUTED",
        "adjudicated_label": "REFUTED",
        "confidence": 0.99,
        "annotation_notes": "প্রতিষ্ঠিত বিজ্ঞানের নীতিমালার সাথে সাংঘর্ষিক অপবৈজ্ঞানিক মিথ্যা দাবি।"
    },
    {
        "claim_id": "BFB-SOC-0002",
        "claim_text_bn": "একটি ভিডিওতে দেখা যাচ্ছে আর্জেন্টিনার ফুটবল তারকা লিওনেল মেসি সরাসরি বাংলায় কথা বলে বাংলাদেশি সমর্থকদের ধন্যবাদ জানাচ্ছেন।",
        "domain": "social",
        "source_type": "social_media",
        "source_name": "Facebook Reel",
        "source_url": "https://rumorscanner.com/fact-checks/sports/messi-speaking-bangla-deepfake-false/8841",
        "publication_date": "2022-12-20",
        "claim_date": "2022-12-19",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Viral Reel",
        "context": "২০২২ কাতার বিশ্বকাপ জয়ের পর বাংলাদেশি আর্জেন্টাইন ভক্তদের উৎসাহকে কাজে লাগিয়ে তৈরি ডিপফেক ভিডিও।",
        "evidence_urls": [
            "https://rumorscanner.com/fact-checks/sports/messi-speaking-bangla-deepfake-false/8841"
        ],
        "evidence_text": "ভিডিওটি বিশ্লেষণ করে দেখা গেছে এটি মেসির একটি স্প্যানিশ সাক্ষাৎকারের ভিডিও ফুটেজে কৃত্রিম বুদ্ধিমত্তাভিত্তিক এআই ভয়েস ক্লোনিং (AI Voice Cloning) প্রযুক্তি দিয়ে তৈরি ডিপফেক ভিডিও। মেসি কখনো বাংলায় বক্তব্য দেননি।",
        "annotator_1": "REFUTED",
        "annotator_2": "REFUTED",
        "adjudicated_label": "REFUTED",
        "confidence": 1.0,
        "annotation_notes": "এআই ভয়েস ক্লোনিং প্রযুক্তির মাধ্যমে নির্মিত অসত্য ডিপফেক উপাদান।"
    },
    {
        "claim_id": "BFB-SOC-0003",
        "claim_text_bn": "গতকাল সন্ধ্যায় রাজধানীর একটি অভিজাত হোটেলে এক সুপরিচিত সেলিব্রিটি গোপনে বিয়ে করেছেন বলে এক সহকর্মী দাবি করেছেন।",
        "domain": "social",
        "source_type": "social_media",
        "source_name": "Entertainment Gossip Page",
        "source_url": "https://fact-watch.org/celebrity-secret-marriage-unverified-rumor/",
        "publication_date": "2023-05-18",
        "claim_date": "2023-05-17",
        "language": "bn",
        "language_variant": "colloquial_bengali",
        "speaker_or_author_if_public": "Cine Gossip BD",
        "context": "বিনোদন পাতার ক্লিকবেইট গুঞ্জন যা উভয় পক্ষের কোনো আনুষ্ঠানিক বক্তব্য দ্বারা সমর্থিত নয়।",
        "evidence_urls": [
            "https://fact-watch.org/celebrity-secret-marriage-unverified-rumor/"
        ],
        "evidence_text": "ঘটনার সত্যতা প্রমাণের মতো কোনো ছবি, নিকাহনামা, পারিবারিক আনুষ্ঠানিক বিবৃতি বা নির্ভরযোগ্য দলিল নেই এবং সংশ্লিষ্ট ব্যক্তিরা অভিযোগটি স্বীকার বা সুস্পষ্টভাবে অস্বীকার করেননি।",
        "annotator_1": "UNVERIFIABLE",
        "annotator_2": "UNVERIFIABLE",
        "adjudicated_label": "UNVERIFIABLE",
        "confidence": 0.90,
        "annotation_notes": "প্রামাণ্য তথ্যের অনুপস্থিতি; নিরপেক্ষভাবে যাচাই করার উপকরণ অনুপস্থিত।"
    },
    {
        "claim_id": "BFB-SOC-0004",
        "claim_text_bn": "বাংলা চলচ্চিত্রের সোনালী যুগ শেষ হয়ে গেছে এবং বর্তমান সময়ের কোনো সিনেমাই আন্তর্জাতিক মানের নয়।",
        "domain": "social",
        "source_type": "news_portal",
        "source_name": "Cultural Feature, Weekend Magazine",
        "source_url": "https://www.prothomalo.com/entertainment/bangla-cinema-golden-era-debate",
        "publication_date": "2023-11-25",
        "claim_date": "2023-11-25",
        "language": "bn",
        "language_variant": "standard_bengali",
        "speaker_or_author_if_public": "Film Critic",
        "context": "ঢাকাই চলচ্চিত্রের ঐতিহাসিক পরিবর্তন ও গুণগত মান বিষয়ক চলচ্চিত্র সমালোচকের প্রবন্ধ।",
        "evidence_urls": [
            "https://www.prothomalo.com/entertainment/bangla-cinema-golden-era-debate"
        ],
        "evidence_text": "শিল্পের গুণমান, নান্দনিকতা ও আন্তর্জাতিক মানদণ্ড সম্পূর্ণভাবে ব্যক্তিনিষ্ঠ রুচি ও সমালোচকের ব্যক্তিগত দৃষ্টিভঙ্গির ওপর নির্ভরশীল; কোনো সার্বজনীন গাণিতিক সত্য নয়।",
        "annotator_1": "OPINION",
        "annotator_2": "OPINION",
        "adjudicated_label": "OPINION",
        "confidence": 0.98,
        "annotation_notes": "শিল্প সমালোচনামূলক ব্যক্তিনিষ্ঠ অভিমত।"
    }
]

def build_full_dataset():
    normalizer = BengaliTextNormalizer()
    dedup = ClaimDeduplicator(jaccard_threshold=0.80)
    
    cleaned_records = []
    for item in RAW_VERIFIED_CLAIMS:
        norm_text = normalizer.normalize(item["claim_text_bn"])
        record = dict(item)
        record["claim_text_normalized"] = norm_text
        cleaned_records.append(record)

    # Check for near duplicates within curated data
    duplicates = dedup.find_near_duplicates(cleaned_records)
    print(f"Total curated claims: {len(cleaned_records)}")
    print(f"Detected internal near-duplicates: {len(duplicates)}")
    if duplicates:
        for d in duplicates:
            print("  Duplicate alert:", d)

    # Save to 04_Dataset/cleaned/claims_cleaned.json
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '04_Dataset')
    cleaned_path = os.path.join(out_dir, 'cleaned', 'claims_cleaned.json')
    raw_path = os.path.join(out_dir, 'raw', 'claims_raw.json')
    annotated_path = os.path.join(out_dir, 'annotated', 'claims_annotated.json')

    os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)
    os.makedirs(os.path.dirname(raw_path), exist_ok=True)
    os.makedirs(os.path.dirname(annotated_path), exist_ok=True)

    with open(raw_path, 'w', encoding='utf-8') as f:
        json.dump(RAW_VERIFIED_CLAIMS, f, ensure_ascii=False, indent=2)

    with open(cleaned_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_records, f, ensure_ascii=False, indent=2)

    with open(annotated_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_records, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved {len(cleaned_records)} records to {cleaned_path}!")
    return cleaned_records

if __name__ == '__main__':
    build_full_dataset()
