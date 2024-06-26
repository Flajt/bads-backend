from typing import List
from src.model.UserAdProfileModel import UserAdProfileModel
from src.services.StorageService import StorageService
from src.DB import DB
from src.model import AdModel
import uuid
import base64

class AdSerivce:
    def __init__(self,db:DB,storage_service:StorageService):
        self.db = db
        self.storage_service = storage_service
    
    def create_ad(self,title:str,data:str,ad_type:AdModel.AdType,lang:str,content_type:str,keywords:List[str],bloom_filter:List[int],description:str,target_url:str) -> str:
        ad_id = uuid.uuid4().hex
        decoded_data = base64.b64decode(data)
        url = self.storage_service.save(decoded_data,ad_type,lang,ad_id,content_type)
        ad_download_url = self.storage_service.get_ad_download_url(ad_id)
        model = AdModel.AdModel(title=title,ad_id=ad_id,ad_type=ad_type,lang=lang,preview_url=url,keywords=keywords,bloom_filter=bloom_filter,asset_url=ad_download_url,budget=1000,publisher_id="1234567890",ad_description=description,target_url=target_url)
        self.db.create_ad(model)
        return ad_id
    
    def match_ad(self,user_profile:UserAdProfileModel,lang:str,ad_type:int)-> List[AdModel.AdModel]:
        ads:List[AdModel.AdModel] = []
        cursor = self.db.match_ad(user_profile,lang,ad_type)
        if cursor is None:
            return ads
        for ad in cursor:
            ads.append(AdModel.AdModel.fromJson(json=ad))
        return ads

    def del_ad(self,ad_id:str):
        self.db.remove_ad(ad_id)
    
    
