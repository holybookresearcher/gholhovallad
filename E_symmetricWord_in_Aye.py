"""
    آیاتی با کلمات متقارن را پیدا می کند
مثال وقتی عدد چهار را به عنوان ورودی بدهیم آنگاه آیه ای می آورد که در آن چهار کلمه متقارن وجود داشته باشد:
سوره 22 آیه 61
آیه: ذَٰلِكَ بِأَنَّ اللَّهَ يُولِجُ اللَّيْلَ فِي النَّهَارِ وَيُولِجُ النَّهَارَ فِي اللَّيْلِ وَأَنَّ اللَّهَ سَمِيعٌ بَصِيرٌ
کلمه وسط: وَيُولِجُ
کلمات متقارن:
- اللَّهَ ↔ اللَّهَ
- اللَّيْلَ ↔ اللَّيْلِ
- فِي ↔ فِي
- النَّهَارِ ↔ النَّهَارَ
--------------------------------------------------

"""

import re

# دیکشنری ابجد کبیر برای حروف
abjad_dict = {
    'ا': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9,
    'ی': 10, 'ک': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80,
    'ص': 90, 'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600,
    'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000
}


# تابع برای پردازش هر آیه و ایجاد ساختار داده
def create_quran_data_structure(file_path):
    quran_data = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) != 3:
                continue

            surah_number, ayah_number, ayah_text = parts
            surah_number = int(surah_number)
            ayah_number = int(ayah_number)

            words = ayah_text.split()  # جدا کردن کلمات
            abjad_values_of_words = [sum(abjad_dict.get(char, 0) for char in word) for word in words]

            quran_data.append({
                'surah_number': surah_number,
                'ayah_number': ayah_number,
                'ayah_text': ayah_text,
                'abjad_values_of_words': abjad_values_of_words
            })

    return quran_data


# تابع برای محاسبه مجموع ابجدی یک کلمه
def calculate_abjad(word):
    return sum(abjad_dict.get(char, 0) for char in word)


# تابع برای پیدا کردن آیات با کلمات متقارن
def find_symmetric_words_in_ayah(ayah_text):
    words = ayah_text.split()
    abjad_values_of_words = [calculate_abjad(word) for word in words]

    # حذف آیاتی که تعداد کلمات آنها فرد نیست
    if len(words) % 2 == 0:
        return None

    mid_index = len(words) // 2
    left_side = abjad_values_of_words[:mid_index]
    right_side = abjad_values_of_words[mid_index + 1:]

    middle_word = words[mid_index]

    # بررسی کلمات متقارن
    matched_words = []
    for i in range(min(len(left_side), len(right_side))):
        if left_side[i] == right_side[len(right_side) - 1 - i]:
            matched_words.append((words[i], words[len(words) - 1 - i]))

    return {
        "middle_word": middle_word,
        "left_side": left_side,
        "right_side": right_side,
        "matched_words": matched_words
    }


# تابع برای نمایش نتایج به صورت متنی
def print_symmetric_words_report(quran_data, k):
    for item in quran_data:
        ayah_text = item['ayah_text']
        result = find_symmetric_words_in_ayah(ayah_text)

        if result and len(result["matched_words"]) >= k:
            print(f"سوره {item['surah_number']} آیه {item['ayah_number']}")
            print(f"آیه: {ayah_text}")
            print(f"کلمه وسط: {result['middle_word']}")

            print("کلمات متقارن:")
            for word_pair in result["matched_words"]:
                print(f"- {word_pair[0]} ↔ {word_pair[1]}")

            print("-" * 50)


# استفاده از تابع برای خواندن فایل قرآن و پردازش آن
file_path = 'Data/Quran/quran-simple.txt'  # مسیر فایل قرآن
quran_data = create_quran_data_structure(file_path)

# تعداد حداقل کلمات متقارن
k = 4

# نمایش گزارش
print_symmetric_words_report(quran_data, k)
