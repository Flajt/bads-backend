import datetime


class InteractionModel:
    def __init__(self,ad_id:str,app_id:str, creation_date:datetime.datetime):
        self.ad_id = ad_id
        self.app_id = app_id
        self.creation_date = creation_date
    
    def toJson(self):
        return {
            "ad_id": self.ad_id,
            "app_id": self.app_id,
            "creation_date": self.creation_date.isoformat()
        }
    @staticmethod
    def fromJson(json):
        return InteractionModel(json["ad_id"],json["app_id"],datetime.datetime.fromisoformat(json["creation_date"]))