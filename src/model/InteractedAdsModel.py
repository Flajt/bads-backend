import datetime
from typing import List

from src.model.Interaction import InteractionModel
class InteractedAdsModel:
    def __init__(self ,user_id:str,interactions:List[InteractionModel],creation_date:datetime.datetime=None):
        self.interactions = interactions
        self.user_id = user_id
        if (creation_date is not None):
            self.creation_date = creation_date
        else:
            self.creation_date = datetime.datetime.now()

    def toJson(self):
        interactions_as_json:List[dict] = []
        for interaction in self.interactions:
            interactions_as_json.append(interaction.toJson())
        return {
            "interactions": interactions_as_json,
            "user_id": self.user_id,
            "creation_date": self.creation_date.isoformat()
        }
    @staticmethod
    def fromJson(json):
        interactions = []
        for data in json["interactions"]:
            interactions.append(InteractionModel.fromJson(data))
        user_id = json["user_id"]
        return InteractedAdsModel(user_id,interactions,creation_date=json["creation_date"])

