"""
در دو لیستی که با اعداد تصادفی ابجد مقداردهی شده اند، چه تعداد بلوک  وجود دارند که مضرب 19 باشند؟

به بیان دیگر، احتمال رخداد یک بلوک که مجموع آن مضربی از 19 باشد چقدر است؟

اندازه بلوک ها قابل تنظیم است
همچنین اندازه مقسوم علیه (نوزده) نیز قابل تنظیم است

"""

import random
import statistics
from collections import Counter
import matplotlib.pyplot as plt

# لیست مجموعه اعداد ابجد
abjad_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800,
                 900, 1000]


# تابع نمونه‌برداری تصادفی
def sample_two_lists(k, list_length):
    """
    نمونه‌برداری دو لیست تصادفی از مجموعه اعداد ابجد.
    """
    all_list1 = []
    all_list2 = []

    for _ in range(k):
        list1 = random.choices(abjad_numbers, k=list_length)
        list2 = random.choices(abjad_numbers, k=list_length)
        all_list1.append(list1)
        all_list2.append(list2)

    return all_list1, all_list2


# تابع استخراج بلوک‌های متقارن
def extract_symmetric_blocks(list1, list2, N):
    """
    استخراج بلوک‌های متقارن از دو لیست.
    """
    symmetric_blocks = []

    for i in range(len(list1) - N + 1):
        block1 = list1[i:i + N]
        block2 = list2[len(list2) - i - N:len(list2) - i]


        symmetric_blocks.append((block1, block2))

    return symmetric_blocks


# تابع برای محاسبه مجموع بلوک‌ها و بررسی بخش‌پذیری
def check_divisibility_by_k(symmetric_blocks, K=19):
    """
    بررسی اینکه مجموع اعداد در دو بلوک متقارن بر K بخش‌پذیر است یا خیر.
    """
    count_divisible = 0

    for block1, block2 in symmetric_blocks:
        sum1 = sum(block1)
        sum2 = sum(block2)
        if sum1 % K == 0 and sum2 % K == 0:
            count_divisible += 1

    return count_divisible


# تابع برای تحلیل توزیع احتمال
def probability_of_divisible_blocks(all_list1, all_list2, N, K=19):
    """
    محاسبه احتمال اینکه دو بلوک متقارن بر K بخش‌پذیر باشند.
    """
    divisible_counts = []

    for list1, list2 in zip(all_list1, all_list2):
        symmetric_blocks = extract_symmetric_blocks(list1, list2, N)
        divisible_count = check_divisibility_by_k(symmetric_blocks, K)
        divisible_counts.append(divisible_count)

    total = len(divisible_counts)
    probability = sum(divisible_counts) / total

    return probability


# تنظیمات آزمایش
k = 100000  # تعداد آزمایش‌ها
list_length = 23  # طول هر لیست
block_length = 7  # طول بلوک متقارن
K = 19  # مقسوم علیه

# نمونه‌برداری از لیست‌ها
all_list1, all_list2 = sample_two_lists(k, list_length)

# محاسبه احتمال اینکه دو بلوک متقارن بر K بخش‌پذیر باشند
prob = probability_of_divisible_blocks(all_list1, all_list2, block_length, K)
print(f"احتمال اینکه دو بلوک متقارن مجموعشان بر {K} بخش‌پذیر باشد: {prob:.6f}")
