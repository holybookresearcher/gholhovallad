"""
آیاتی که حروف متقارن دارد را استخراج می کند
مثلا می گوییم کدام آیات 15 حرف متقارن دارد-این کد آیه را از وسط نصف می کند و طرفین را می شمارد که اگر متقارن باشد اطلاع می دهد
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
    """
    ایجاد ساختار داده قرآنی
    :param file_path:
    :return:
    """
    quran_data = []

    # خواندن فایل
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # تقسیم هر خط به شماره سوره، شماره آیه و متن آیه
            parts = line.strip().split('|')
            if len(parts) != 3:
                continue

            surah_number, ayah_number, ayah_text = parts
            surah_number = int(surah_number)
            ayah_number = int(ayah_number)

            # محاسبه معادل ابجدی برای حروف
            words = ayah_text.split()  # جدا کردن کلمات
            abjad_values_of_words = [sum(abjad_dict.get(char, 0) for char in word) for word in words]

            # محاسبه معادل ابجدی برای حروف
            abjad_values_of_letters = [abjad_dict.get(char, 0) for char in ayah_text if char in abjad_dict]

            # افزودن داده‌ها به لیست
            quran_data.append({
                'surah_number': surah_number,
                'ayah_number': ayah_number,
                'ayah_text': ayah_text,
                'abjad_values_of_words': abjad_values_of_words,
                'abjad_values_of_letters': abjad_values_of_letters
            })

    return quran_data


# تابع برای بررسی تطابق‌های متقارن
def count_symmetric_matches(list1, list2):
    """
    تعداد تطابق‌های متقارن در دو لیست را می‌شمارد.
    """
    count = 0
    n = len(list1)

    for i in range(n):
        if list1[i] == list2[n - 1 - i]:
            count += 1

    return count


# تابع برای بررسی تقسیم آیه به دو قسمت و شمارش تطابق‌های متقارن
def check_symmetric_matches_in_ayah(ayah_text, k):
    """
    بررسی می‌کند که آیا آیه می‌تواند به دو قسمت مساوی تقسیم شود
    و در آن بیش از k عدد متقارن وجود دارد.
    """
    abjad_values_of_letters = [abjad_dict.get(char, 0) for char in ayah_text if char in abjad_dict]

    # تقسیم آیه به دو قسمت مساوی
    mid = len(abjad_values_of_letters) // 2
    if len(abjad_values_of_letters) % 2 != 0:
        return 0  # اگر طول آیه فرد باشد، تقسیم به دو قسمت مساوی ممکن نیست

    # دو قسمت را جدا می‌کنیم
    first_half = abjad_values_of_letters[:mid]
    second_half = abjad_values_of_letters[mid:]

    # شمارش تطابق‌های متقارن
    matches = count_symmetric_matches(first_half, second_half)

    if matches >= k:
        return matches
    else:
        return 0


# تابع برای پیدا کردن آیات با بیش از k تطابق متقارن
def find_ayahs_with_symmetric_matches(quran_data, k):
    """
    آیات با بیش از k تطابق متقارن را پیدا می‌کند.
    """
    results = []

    for item in quran_data:
        ayah_text = item['ayah_text']
        matches = check_symmetric_matches_in_ayah(ayah_text, k)

        if matches > 0:
            results.append({
                'surah_number': item['surah_number'],
                'ayah_number': item['ayah_number'],
                'ayah_text': item['ayah_text'],
                'symmetric_matches': matches
            })

    return results


# استفاده از تابع برای خواندن فایل قرآن و پردازش آن
file_path = 'Data/Quran/quran-simple.txt'  # مسیر فایل قرآن
quran_data = create_quran_data_structure(file_path)

# گرفتن آیات با بیش از k تطابق متقارن
k = int(input("تعداد تطابق‌های متقارن حداقل (k): "))
matching_ayahs = find_ayahs_with_symmetric_matches(quran_data, k)

# نمایش نتایج
for ayah in matching_ayahs:
    print(f"سوره {ayah['surah_number']} آیه {ayah['ayah_number']}: {ayah['ayah_text']}")
    print(f"تعداد تطابق‌های متقارن: {ayah['symmetric_matches']}")
    print("-" * 50)
