import datetime
from typing import List
from src.DB import DB
from src.model.InteractedAdsModel import InteractedAdsModel
from src.model.Interaction import InteractionModel
from src.model.MergedInteractedAdModel import MergedInteractedAdModel
from src.model.AdModel import AdModel


class InteractedAdService:
    def __init__(self,db:DB):
        self.db = db
    
    def retrive_interactions(self,user_id:str) -> (List[MergedInteractedAdModel] | None):
        interactions = self.db.retrive_ad_interactions(user_id)
        if interactions is None:
            return None
        models = []
        ad_interaction_map:dict[AdModel,InteractionModel] = {}
        for interaction in interactions.interactions:
            ad = self.db.get_ad(interaction.ad_id)
            if ad is not None:
                if ad.ad_id in ad_interaction_map:
                    ad_interaction_map[ad].append(interaction)
                else:
                    ad_interaction_map[ad] = [interaction]
        for ad,interactions in ad_interaction_map.items():
            models.append(MergedInteractedAdModel(ad,interactions))
        return models
    
    def create_interaction_profiles(self,user_ids:List[str]):
        for user_id in user_ids:
            self.db.save_interaction_profile(InteractedAdsModel(user_id=user_id,interactions=[]))
    
    def record_interaction(self,ad_id:str,user_id:int,app_id:str):
        self.db.record_interaction(user_id,InteractionModel(ad_id=ad_id,app_id=app_id,creation_date=datetime.datetime.now()))