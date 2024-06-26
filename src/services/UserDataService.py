from typing import List
from src.DB import DB
from src.model.UserAdProfileModel import UserAdProfileModel


class UserDataService:
    def __init__(self, db:DB):
        self.db = db

    def get_user_data(self, user_id:str):
        return self.db.get_ad_profile(user_id)
    
    def create_user_data(self,bloom_filter:List[int],user_id:str,num_hash_functions:int):
        profile = UserAdProfileModel(bloom_filter=bloom_filter,identifier=user_id,hash_functions=num_hash_functions)
        self.db.create_ad_profile(profile)
