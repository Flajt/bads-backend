from typing import List
import pymongo
import os
from src.model import AdModel, InteractedAdsModel, UserAdProfileModel, PublisherModel
from src.model.Interaction import InteractionModel

class DB:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGO_URI")
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client.bads
        self.ads = self.db.ads
        self.user_data = self.db.users
        self.interacted_ads = self.db.interactedAds
        self.user_data.create_index("user_id")
        self.ads.create_index("ad_id")
        self.interacted_ads.create_index("creation_date",expireAfterSeconds=60*60*48) # expire after 48 hours
        self.user_data.create_index("creation_date",expireAfterSeconds=60*60*48) # expire after 2 days
        # In Prod you would also have a blacklist collection to store blacklisted ads etc

    def create_ad(self,ad:AdModel.AdModel):
        self.ads.insert_one(ad.toJson()) # Time: O(1) Space: O(k)
    
    def remove_ad(self,ad_id:str):
        self.ads.delete_one({"ad_id":ad_id}) # Time: O(1)
    
    def get_ad(self,ad_id:str)->(AdModel.AdModel | None):
        ad = self.ads.find_one({"ad_id":ad_id}) # Time: O(1), Space O(1)
        if ad is None: # Time: O(1)
            return None # Time: O(1)
        return AdModel.AdModel.fromJson(ad) # Time: O(k), Space O(1)
    
    def update_ad(self,ad_id:str,ad:AdModel.AdModel):
        self.ads.update_one({"ad_id":ad_id},ad.toJson()) # Time: O(1) Space: O(1)
    
    def create_ad_profile(self,profile:UserAdProfileModel.UserAdProfileModel):
        self.user_data.insert_one(profile.toJson()) # Time: O(1) Space: O(1)
    
    def record_interaction(self,user_id:str, interaction:InteractionModel):
        self.interacted_ads.update_one({"user_id":user_id},{"$push":{"interactions":interaction.toJson()}}) # Time: O(1) Space: O(1)

    def delete_ad_profile(self,profile:UserAdProfileModel.UserAdProfileModel):
        self.user_data.delete_one({"identifier":profile.user_id}) # Time: O(1)

    def get_ad_profile(self,user_id:str)->(UserAdProfileModel.UserAdProfileModel | None):
        profile = self.user_data.find_one({"identifier":user_id}) # Time: O(1) Space: O(1)
        if profile is None: # Time: O(1)
            return None # Time: O(1)
        return UserAdProfileModel.UserAdProfileModel.fromJson(profile) # Time: O(1) Space: O(1)
    
    def match_ad(self,profile:UserAdProfileModel.UserAdProfileModel,lang:str,ad_type:int):
      cursor = self.ads.aggregate([ # Time complexity total: O(n*m), space complexity total: O(n*m), output space complexity: O(1)
          {'$match': {'lang': lang, 'ad_type': ad_type}}, # Time: O(n) Space: O(m)
          {'$addFields': {'matchingBits': {'$map': {'input': {'$zip': {'inputs': ['$bloom_filter', profile.bloom_filter]}}, 'as': 'pair', 'in': {'$bitAnd': [{'$arrayElemAt': ['$$pair', 0]}, {'$arrayElemAt': ['$$pair', 1]}]}}}}}, # Time: O(n*m). Space: O(n)
          {'$addFields': {'matchCount': {'$reduce': {'input': '$matchingBits','initialValue': 0,'in': {'$add': ['$$value', '$$this']}}}}}, # Time: O(n*m), Space O(n*m) (m = array size)
          {'$sort': {'matchCount': -1}}, # Time O(n log n)? Space O(k) where k = 10, see: https://www.mongodb.com/docs/manual/reference/operator/aggregation/sort/#-sort-operator-and-memory
          {"$limit": 10} # Time: O(1) best & worst case, space O(1) best and worst case, Space: O(1)
          ])
      return cursor
    
    def save_interaction_profile(self,interaction:InteractionModel):
        self.interacted_ads.insert_one(interaction.toJson()) # Time: O(1) Space: O(k)

    def retrive_ad_interactions(self,user_id:str) -> (InteractedAdsModel.InteractedAdsModel | None):
        interaction = self.interacted_ads.find_one({"user_id":user_id}) # Time: O(1) Space: O(1)
        if interaction is None: # Time: O(1)
            return None # Time: O(1)
        return InteractedAdsModel.InteractedAdsModel.fromJson(interaction) # Time: O(1) Space: O(1)
    
    def delete_ad_interactions(self,user_id:str):
        self.interacted_ads.delete_many({"user_id":user_id}) # Time: O(1)
    
    def TEST_WIPE_ALL(self):
        """
        DON'T USE IN PROD!, JUST DON'T! 
        """
        self.ads.drop()
        self.user_data.drop()
        self.interacted_ads.drop()