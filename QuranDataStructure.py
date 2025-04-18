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

            # محاسبه معادل ابجدی برای کلمات
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


def get_surah_data(surah_number):
    """
      به ازای شماره سوره، ساختار داده ای آن را از قرآن باز می‌گرداند.
      """
    # بررسی وجود شماره سوره در داده‌های قرآن
    if surah_number < 1 or surah_number > 114:
        raise ValueError("شماره سوره باید بین 1 و 114 باشد.")

    surah_data = [item for item in quran_data if item.get('surah_number') == surah_number]

    return surah_data


def get_surah_letter_abjad(surah_number, ):

    """
    به ازای شماره سوره، ساختار ابجد حرفی آن را از قرآن باز می‌گرداند.
    """
    surah_info = get_surah_data(surah_number=112)

    surah_letter_abjad = surah_info.abjad_values_of_letters
    return surah_letter_abjad

# استفاده از تابع برای خواندن فایل قرآن و پردازش آن
file_path = 'quran.txt'  # مسیر فایل قرآن
quran_data = create_quran_data_structure(file_path)

get_surah_letter_abjad(surah_number=112)

print()