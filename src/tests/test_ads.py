from typing import List, Tuple
import pytest
import requests
import base64
import random
from src.tests.fixtures import cat_map


from src.BloomFilter import BloomFilter

class TestAds:        
    ad_url = 'http://localhost:8000/publisher/ads'
    user_url = 'http://localhost:8000/ad-profile'
    match_url = 'http://localhost:8000/ad'
    def test_ad_creation(self):    
        with open("./src/tests/test_ad.png","rb") as f:
            data = f.read()
        
        b64_data = base64.b64encode(data).decode("ascii")   
        bloom_filter:BloomFilter = BloomFilter.bloom_filter_from_desired_accuracy(accuracy=0.60,amount_items=18) 
        bloom_filter.add("abc")
        response = requests.post(self.ad_url, json={"title":"abc","data_bytes":b64_data,"ad_type":1,"lang":"en","content_type":"image/png","keywords":["abc"],"bloom_filter":bloom_filter.export()["bit_array"],"description":"abc","target_url":"https://www.google.com"})
        assert response.status_code == 201
        assert response.json()["ad_id"] is not None
        response = requests.delete("http://localhost:8000/delete-all")
        assert response.status_code == 200

    def test_multiple_ad_creations(self):
        values = list(cat_map.values())
        categories = random.choices(values,k=5) # substitute age group with random category for this test
        prepped_categories = set()
        with open("./src/tests/test_ad.png","rb") as f:
            data = f.read()
        b64_data = base64.b64encode(data).decode("ascii")
        for category in categories:
            for item in category.split("/"):
                prepped_categories.add(item)
        for _ in range(1000):
            bloom_filter:BloomFilter = BloomFilter.bloom_filter_from_desired_accuracy(accuracy=0.60,amount_items=13) 
            age_group = str(random.choice([0,1,2,3,4,5,6,7,8,9]))
            for prepped_category in prepped_categories:
                bloom_filter.add(prepped_category)
            bloom_filter.add(age_group)
            response = requests.post(self.ad_url, json={"title":"abc","data_bytes":b64_data,"ad_type":1,"lang":"en","content_type":"image/png","keywords":list(prepped_categories)+[age_group],"bloom_filter":bloom_filter.export()["bit_array"],"description":"abc","target_url":"https://www.google.com"})
            assert response.status_code == 201
            assert response.json()["ad_id"] is not None
        response = requests.delete("http://localhost:8000/delete-all")
        assert response.status_code == 200
    
    def test_match_ad(self):
        filters:List[Tuple[BloomFilter,List[str]]] = []
        values = list(cat_map.values())
        with open("./src/tests/test_ad.png","rb") as f:
            data = f.read()
        b64_data = base64.b64encode(data).decode("ascii")
        for _ in range(1000):
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
            filters.append((bloom_filter,list(prepped_categories)))
            response = requests.post(self.ad_url, json={"title":"abc","data_bytes":b64_data,"ad_type":1,"lang":random.choice(["en","de"]),"content_type":"image/png","keywords":list(prepped_categories),"bloom_filter":bloom_filter.export()["bit_array"],"description":"abc","target_url":"https://www.google.com"})
            assert response.status_code == 201
        choosen_filter = random.choice(filters)
        print(choosen_filter)
        user_resp = requests.post(self.user_url,json={"user_ad_profiles":[{"bloom_filter":choosen_filter[0].export()["bit_array"],"identifier":"abc","num_hash_func":choosen_filter[0].export()["num_hash_func"]}]})
        assert user_resp.status_code == 201
        response = requests.get(self.match_url+"?user_id=abc&lang=en&ad_type=1")
        keywords = choosen_filter[1]
        keywords_per_ad = []
        print(response.status_code)
        for ad in response.json()["ads"]:
            included_keywords = []
            for keyword in ad["keywords"]:
                if keyword in keywords:
                    included_keywords.append(keyword)
            keywords_per_ad.append(len(included_keywords))
        print(keywords_per_ad)
        print(len(keywords) * .06)
        assert response.status_code == 200
        response = requests.delete("http://localhost:8000/delete-all")
        assert response.status_code == 200