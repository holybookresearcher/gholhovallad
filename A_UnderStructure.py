"""
    این فایل متن قرآن را در قالب یک جدول ارائه می دهد که ستونهای این جدول بردار ویژگی قرآنی هستند
    این جدول میتواند زیرساختی برای انواع پردازش های قرآنی باشد

"""

import pandas as pd
import re
from collections import Counter

# تابع حذف اعراب (حروف حرکتی عربی)
def remove_diacritics(text):
    arabic_diacritics = re.compile(r'[\u064B-\u0652\u0670]')
    return re.sub(arabic_diacritics, '', text)

# مسیر فایل متنی قرآن
file_path = "Data/Quran/quranV1.txt"

# جدول نام سوره‌ها
sura_names = {
    1: "الفاتحة", 2: "البقرة", 3: "آل عمران", 4: "النساء", 5: "المائدة", 6: "الأنعام", 7: "الأعراف",
    8: "الأنفال", 9: "التوبة", 10: "يونس", 11: "هود", 12: "يوسف", 13: "الرعد", 14: "إبراهيم",
    15: "الحجر", 16: "النحل", 17: "الإسراء", 18: "الكهف", 19: "مريم", 20: "طه", 21: "الأنبياء",
    22: "الحج", 23: "المؤمنون", 24: "النور", 25: "الفرقان", 26: "الشعراء", 27: "النمل", 28: "القصص",
    29: "العنكبوت", 30: "الروم", 31: "لقمان", 32: "السجدة", 33: "الأحزاب", 34: "سبإ", 35: "فاطر",
    36: "يس", 37: "الصافات", 38: "ص", 39: "الزمر", 40: "غافر", 41: "فصلت", 42: "الشورى",
    43: "الزخرف", 44: "الدخان", 45: "الجاثية", 46: "الأحقاف", 47: "محمد", 48: "الفتح",
    49: "الحجرات", 50: "ق", 51: "الذاريات", 52: "الطور", 53: "النجم", 54: "القمر", 55: "الرحمن",
    56: "الواقعة", 57: "الحديد", 58: "المجادلة", 59: "الحشر", 60: "الممتحنة", 61: "الصف",
    62: "الجمعة", 63: "المنافقون", 64: "التغابن", 65: "الطلاق", 66: "التحريم", 67: "الملك",
    68: "القلم", 69: "الحاقة", 70: "المعارج", 71: "نوح", 72: "الجن", 73: "المزمل", 74: "المدثر",
    75: "القيامة", 76: "الإنسان", 77: "المرسلات", 78: "النبأ", 79: "النازعات", 80: "عبس",
    81: "التكوير", 82: "الانفطار", 83: "المطففين", 84: "الانشقاق", 85: "البروج", 86: "الطارق",
    87: "الأعلى", 88: "الغاشية", 89: "الفجر", 90: "البلد", 91: "الشمس", 92: "الليل", 93: "الضحى",
    94: "الشرح", 95: "التين", 96: "العلق", 97: "القدر", 98: "البينة", 99: "الزلزلة", 100: "العاديات",
    101: "القارعة", 102: "التكاثر", 103: "العصر", 104: "الهمزة", 105: "الفيل", 106: "قريش",
    107: "الماعون", 108: "الكوثر", 109: "الكافرون", 110: "النصر", 111: "المسد", 112: "الإخلاص",
    113: "الفلق", 114: "الناس"
}

# جدول ابجد ساده
abjad_table = {
    'ا':1, 'ب':2, 'ج':3, 'د':4, 'ه':5, 'و':6, 'ز':7, 'ح':8, 'ط':9, 'ي':10,
    'ك':20, 'ل':30, 'م':40, 'ن':50, 'س':60, 'ع':70, 'ف':80, 'ص':90, 'ق':100,
    'ر':200, 'ش':300, 'ت':400, 'ث':500, 'خ':600, 'ذ':700, 'ض':800, 'ظ':900, 'غ':1000
}

# لیست حروف مقطعه معروف
disjoint_letters = {'الم', 'المر', 'طسم', 'حم', 'طس', 'يس', 'ص', 'ق', 'ن', 'كهيعص', 'عسق'}

quran_stop_signs = {
    "وقف لازم":           {"char": "ۘ", "unicode": ord("ۘ"), "desc": "توقف کامل و واجب"},
    "وقف مرخص":          {"char": "ۖ", "unicode": ord("ۖ"), "desc": "توقف اختیاری ولی بهتر است"},
    "وقف معانقه":         {"char": "ۗ", "unicode": ord("ۗ"), "desc": "توقف و ادامه همزمان"},
    "وقف ناپسند":         {"char": "ۙ", "unicode": ord("ۙ"), "desc": "توقف ناپسند است"},
    "وقف جائز":          {"char": "ۚ", "unicode": ord("ۚ"), "desc": "توقف جایز است"},
    "وقف مجوز / جذر":    {"char": "ۛ", "unicode": ord("ۛ"), "desc": "توقف مجاز است ولی بهتر است ادامه داد / علامت جذر"},
    "وقف ممنوع":         {"char": "ۜ", "unicode": ord("ۜ"), "desc": "توقف ممنوع است"},
    "سجده مستحب":        {"char": "۞", "unicode": ord("۞"), "desc": "سجده مستحب"},
    "سجده واجب":         {"char": "۩", "unicode": ord("۩"), "desc": "سجده واجب"},
    "وقف لازم بلند":      {"char": "ۚۚ", "unicode": None, "desc": "وقف لازم بلند (دو علامت پشت سر هم)"},
    "علامت نشانه ادامه": {"char": "۟", "unicode": ord("۟"), "desc": "علامت نشانه ادامه خواندن"},
    "علامت وقف ج":       {"char": "۠", "unicode": ord("۠"), "desc": "علامت وقف نوع ج"},
    "علامت وقف ط":       {"char": "ۡ", "unicode": ord("ۡ"), "desc": "علامت وقف نوع ط"},
    "علامت وقف ز":       {"char": "ۢ", "unicode": ord("ۢ"), "desc": "علامت وقف نوع ز"},
    "علامت وقف ص":       {"char": "ۣ", "unicode": ord("ۣ"), "desc": "علامت وقف نوع ص"},
    "علامت وقف ق":       {"char": "ۤ", "unicode": ord("ۤ"), "desc": "علامت وقف نوع ق"},
    "علامت وقف صاد":     {"char": "ۥ", "unicode": ord("ۥ"), "desc": "علامت وقف صاد"},
}


def remove_quran_stop_signs(text):
    """
    حذف تمام علائم وقف قرآن از متن ورودی
    """
    for name, info in quran_stop_signs.items():
        if info["char"] in text:
            text = text.replace(info["char"], "")
    return text



# تابع محاسبه ارزش ابجدی یک کلمه یا متن
def abjad_value(word):
    return sum(abjad_table.get(ch, 0) for ch in word if ch in abjad_table)

rows = []
with open(file_path, encoding="utf-8") as f:
    for line in f:
        sura, aya, text = line.strip().split("|")
        sura = int(sura)
        aya = int(aya)

        # نسخه اصلی با اعراب
        original_text = text

        # نسخه بدون علائم وقف
        text_no_stop_signs = remove_quran_stop_signs(text)

        # نسخه بدون اعراب و بدون علائم وقف
        text_no_diacritics = remove_diacritics(text_no_stop_signs)

        words = text_no_stop_signs.split()
        letters = [c for c in text_no_stop_signs if c.isalpha()]
        word_counts = Counter(words)
        letter_counts = Counter(letters)
        unique_words = set(words)

        abjad_word_vector = [str(abjad_value(w)) for w in words]
        abjad_letter_vector = [str(abjad_table.get(ch, 0)) for ch in letters if ch in abjad_table]

        disjoint_count = sum(1 for w in words if w in disjoint_letters)

        row = {
            "کتاب": "قرآن",
            "شماره سوره": sura,
            "نام سوره": sura_names.get(sura, ""),
            "شماره آیه": aya,
            "آیه با اعراب": original_text[:50],              # ۵۰ حرف اول آیه با اعراب
            "آیه بدون اعراب": text_no_diacritics[:50],     # ۵۰ حرف اول آیه بدون اعراب
            "تعداد کلمات": len(words),
            "تعداد حروف": len(letters),
            "میانگین طول کلمات": round(len(letters) / len(words), 2) if words else 0,
            "تعداد واژه‌های منحصر به‌فرد": len(unique_words),
            "نسبت تنوع واژگان": round(len(unique_words) / len(words), 2) if words else 0,
            "تعداد کلمات مشترک با حروف مقطعه": disjoint_count,
            "شماره ابجد کل آیه": abjad_value(text_no_stop_signs),
            "بردار ابجد کلمات": "-".join(abjad_word_vector),
            "بردار ابجد حروف": "-".join(abjad_letter_vector),
            "پرتکرارترین حرف": letter_counts.most_common(1)[0][0] if letter_counts else "",
            "پرتکرارترین کلمه": word_counts.most_common(1)[0][0] if word_counts else ""
        }
        rows.append(row)


df = pd.DataFrame(rows)
df.to_csv("quran_features.csv", index=False, encoding="utf-8-sig")