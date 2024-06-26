from typing import List,Dict
from src.BloomFilter import BloomFilter
from src.tests.fixtures import cat_map
import random

def test_brute_force_protection():
    bfvm:Dict[BloomFilter,List] = {} # bloom filter value map
    age_groups = [0,1,2,3,4,5,6,7,8,9]
    brute_force_fp_rate = []
    categories:List[str] = cat_map.values()
    for _ in range(10000):
        bloom = BloomFilter.bloom_filter_from_desired_accuracy(accuracy=0.60, amount_items=13)# ceil((2.5 * 5) + 1) (5 is the amount of categories 1 is an age group)
        choosen_categories = random.choices(list(categories), k=5)
        age_group = str(random.choice(age_groups))
        item_set = set()
        for cat in choosen_categories:
            for item in cat.split("/"):
                item_set.add(item)
        
        for item in item_set:
            bloom.add(item)
        bloom.add(age_group)
        item_set.add(age_group)
        bfvm[bloom] = item_set
    

    prepped_categories = set()
    for category in categories:
        for item in category.split("/"):
            prepped_categories.add(item)

    for bloom_filter,items in bfvm.items():
        false_positives = 0
        total_checks = len(prepped_categories)
        for category in prepped_categories:
            is_included = bloom_filter.contains(category)
            if is_included:
                if category not in items:
                    false_positives += 1
        
        for age_group in age_groups:
            is_included = bloom_filter.contains(str(age_group))
            if is_included:
                if str(age_group) not in items:
                    false_positives += 1
        
        false_positive_rate = false_positives / total_checks if total_checks > 0 else 0
        brute_force_fp_rate.append(false_positive_rate)
    
    average_fp_rate = sum(brute_force_fp_rate) / len(brute_force_fp_rate)
    print(average_fp_rate)
    assert average_fp_rate >= 0.4 and average_fp_rate <= 0.44 # it's not 100% accurate but it's a good enough approximation

def test_amount_unique_categories():
    entries = list(cat_map.values())
    categories = set()
    for entry in entries:
        for item in entry.split("/"):
            if item != "" and item != " ":
                categories.add(item)
    
    assert len(categories) == 446

def test_average():
    entries = list(cat_map.values())
    counter = 0
    for entry in entries:
        parts = entry.split("/")
        if "" in parts:
            parts.remove("")
        counter += len(parts)


    average = counter / len(entries)
    print(average)
    
    assert average >= 2.4 and average <= 2.5

        


