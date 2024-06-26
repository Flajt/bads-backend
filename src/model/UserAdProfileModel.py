import datetime


class UserAdProfileModel:
    def __init__(self,bloom_filter,identifier,hash_functions):
        self.bloom_filter:list[int] = bloom_filter
        self.identifier:str = identifier
        self.creationDate = datetime.datetime.now()
        self.num_hash_functions:int = hash_functions
    def toJson(self):
        return {
            "bloom_filter":self.bloom_filter,
            "identifier":self.identifier,
            "creation_date":self.creationDate.isoformat(),
            "num_hash_functions":self.num_hash_functions
        }
    @staticmethod
    def fromJson(json):
        ad_profile_model = UserAdProfileModel([], "", 0)
        ad_profile_model.bloom_filter = json["bloom_filter"]
        ad_profile_model.identifier = json["identifier"]
        ad_profile_model.creationDate = datetime.datetime.fromisoformat(json["creation_date"])
        ad_profile_model.num_hash_functions = json["num_hash_functions"]
        return ad_profile_model