
import sys
from typing import List
from src.model import AdModel
from src.model.Interaction import InteractionModel


class MergedInteractedAdModel:
    """
    Contains the ad and the interaction combined into one object
    """
    def __init__(self, ad_model: AdModel.AdModel, interactions: List[InteractionModel]):
        self.ad_model:AdModel.AdModel = ad_model
        self.interactions:List[InteractionModel] = interactions
    
    def toJson(self):
        json_interactions = []
        sys.stderr.write(str(type(self.interactions))+"\n")
        sys.stderr.write(str(self.interactions)+"\n")
        for interaction in self.interactions:
            json_interactions.append(interaction.toJson())
        return {
            "ad": self.ad_model.toJson(),
            "interactions": json_interactions
        }