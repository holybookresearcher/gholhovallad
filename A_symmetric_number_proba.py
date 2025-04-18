"""
این فایل لیستی تصادفی از اعداد ابجد تولید می کند
در یک شبیه سازی بررسی می کند که چقدر احتمال دارد که در دو لیست متقارن تعداد مشخصی عدد یکسان وجود داشته باشد
مثلا چقدر احتمال دارد که در دو لیست متقارن که هر کدام دارای طول 23 هستند، چهار عدد یکسان متقارن وجود داشته باشد

طول لیست و تعداد اعداد قابل تنظیم هستند
در پایان برنامه نموداری رسم می شود و احتمال تطابق متقارن را به ازای تعداد مشخصی از اعداد بیان می کند.
"""

import random
import statistics
from collections import Counter
import matplotlib.pyplot as plt

# لیست مجموعه اعداد ابجد
abjad_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

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


# تابع شمارش تعداد تطابق‌های متقارن
def count_symmetric_matches(list1, list2):
    """
    تعداد تطابق‌های متقارن در دو لیست را می‌شمارد.
    """
    if len(list1) != len(list2):
        raise ValueError("طول دو لیست باید برابر باشد.")

    count = 0
    n = len(list1)

    for i in range(n):
        if list1[i] == list2[n - 1 - i]:
            count += 1

    return count


# تابع برای تحلیل توزیع احتمال تعداد تطابق‌های متقارن
def symmetric_match_distribution(all_list1, all_list2):
    """
    محاسبه توزیع احتمال تعداد تطابق‌های متقارن (۰ تا n)
    """
    match_counts = []

    for l1, l2 in zip(all_list1, all_list2):
        n = len(l1)
        count = sum(1 for i in range(n) if l1[i] == l2[n - 1 - i])
        match_counts.append(count)

    # شمارش تعداد دفعات هر مقدار تطابق
    counter = Counter(match_counts)

    total = len(match_counts)
    probability_distribution = {k: v / total for k, v in sorted(counter.items())}

    print("توزیع احتمال تعداد تطابق‌های متقارن:")
    for matches, prob in probability_distribution.items():
        print(f"{matches} تطابق → احتمال: {prob:.4f}")

    return probability_distribution


# تابع برای محاسبه احتمال دقیقاً t تطابق متقارن
def get_probability_of_matches(probability_distribution, t):
    """
    احتمال داشتن دقیقاً t تطابق متقارن از توزیع احتمال ورودی.
    """
    return probability_distribution.get(t, 0)


# تابع برای رسم نمودار توزیع احتمال تطابق‌های متقارن
def plot_match_distribution(probability_distribution):
    """
    رسم نمودار هیستوگرام توزیع احتمال تطابق‌های متقارن.
    """
    match_counts = list(probability_distribution.keys())
    probabilities = list(probability_distribution.values())

    plt.bar(match_counts, probabilities, width=0.8, color='skyblue', edgecolor='black')

    plt.xlabel('#Symmetric match', fontsize=12)
    plt.ylabel('Probability', fontsize=12)
    plt.title('Statistical Distribution of Symmetric Match', fontsize=14)
    plt.xticks(match_counts, fontsize=10)
    plt.yticks(fontsize=10)

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


# تنظیمات آزمایش
k = 1000000  # تعداد آزمایش‌ها
list_length = 23  # طول هر لیست

# نمونه‌برداری از لیست‌ها
all_list1, all_list2 = sample_two_lists(k, list_length)

# محاسبه توزیع احتمال تطابق‌های متقارن
dist = symmetric_match_distribution(all_list1, all_list2)

# محاسبه احتمال دقیقاً 2 تطابق متقارن
prob_t_2 = get_probability_of_matches(dist, t=4)
print(f"احتمال داشتن دقیقاً 4 تطابق متقارن: {prob_t_2:.6f}")


# رسم نمودار توزیع احتمال
plot_match_distribution(dist)
