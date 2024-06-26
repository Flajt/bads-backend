import requests
from src.BloomFilter import BloomFilter
import base64
import random
from src.tests.fixtures import cat_map

ad_url = "http://192.168.178.30:8000/publisher/ads"
values = list(cat_map.values())
with open("./src/tests/test_ad.png","rb") as f:
    data = f.read()
b64_data = base64.b64encode(data).decode("ascii")
for i in range(1000):
    if (i % 10) == 0:
        print(f"Progress: {i} / 1000 ads created")
    bloom_filter:BloomFilter = BloomFilter.bloom_filter_from_desired_accuracy(accuracy=0.60,amount_items=13)
    categories = random.choices(values,k=5)
    age_group = str(random.choice([0,1,2,3,4,5,6,7,8,9]))         
    prepped_categories = set()
    for category in categories:
        for item in category.split("/"):
            if item != "" and item != " ":
                prepped_categories.add(item)
    for prepped_category in prepped_categories:
        bloom_filter.add(prepped_category)
    bloom_filter.add(age_group)
    prepped_categories.add(age_group)
    response = requests.post(ad_url, json={"title":"abc","data_bytes":b64_data,"ad_type":1,"lang":random.choice(["en","de"]),"content_type":"image/png","keywords":list(prepped_categories),"bloom_filter":bloom_filter.export()["bit_array"],"description":"abc","target_url":"https://www.google.com"})
print("Done!")