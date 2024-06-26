from enum import Enum
from typing import Any, List

class AdType(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    
class AdModel:
    def __init__(self,title:str,ad_id:str, asset_url:str, preview_url:str, ad_description:str, budget:float,ad_type:int,keywords:List[str],bloom_filter,lang:str,publisher_id:str,target_url:str):
        self.title = title
        self.ad_id = ad_id
        self.asset_url = asset_url
        self.preview_url = preview_url
        self.ad_description = ad_description
        self.budget = budget
        self.ad_type = ad_type
        self.keywords = keywords
        self.bloom_filter = bloom_filter
        self.lang = lang
        self.publisher_id = publisher_id
        self.target_url = target_url
    def toJson(self):
        return {
            "title":self.title,
            "ad_id":self.ad_id,
            "asset_url":self.asset_url,
            "preview_url":self.preview_url,
            "ad_description":self.ad_description,
            "budget":self.budget,
            "ad_type":self.ad_type,
            "keywords":self.keywords,
            "bloom_filter":self.bloom_filter,
            "lang":self.lang,
            "publisher_id":self.publisher_id,
            "target_url":self.target_url
        }
    @staticmethod
    def fromJson(json:dict[str,Any]):
        ad_model = AdModel("","","","","",0,AdType.SMALL.value,[],[],"", "","")
        ad_model.title = json["title"]
        ad_model.ad_id = json["ad_id"]
        ad_model.asset_url = json["asset_url"]
        ad_model.preview_url = json["preview_url"]
        ad_model.ad_description = json["ad_description"]
        ad_model.budget = json["budget"]
        ad_model.ad_type = json["ad_type"]
        ad_model.keywords = json["keywords"]
        ad_model.bloom_filter = json["bloom_filter"]
        ad_model.lang = json["lang"],
        ad_model.publisher_id = json["publisher_id"]
        ad_model.target_url = json["target_url"]
        return ad_model