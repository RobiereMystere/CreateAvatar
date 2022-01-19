import math
import os

from PixelOperations import PixelOperations
from character import Character


class Rarity:

    def __init__(self) -> None:
        super().__init__()

        self.rankings = {'common': {'probability': 1 / 6, 'color': PixelOperations.grey},
                         'uncommon': {'probability': 2 / 6, 'color': PixelOperations.green},
                         'rare': {'probability': 3 / 6, 'color': PixelOperations.cyan},
                         'epic': {'probability': 4 / 6, 'color': PixelOperations.purple},
                         'legendary': {'probability': 5 / 6, 'color': PixelOperations.yellow},
                         'unique': {'probability': 6 / 6, 'color': PixelOperations.orange}}

    def ranking(self, character):
        ranking = 'common'
        rarities = []
        for trait in character.parts:
            weight = int(character.parts[trait]['path'].split('_')[1])
            rarities.append(Rarity.get_rarity(trait)[weight])
        # ranking = (sum(rarities))
        print(rarities)
        score = math.prod(rarities)
        for key, value in self.rankings.items():
            if score < value['probability']:
                ranking = key
                break
        return ranking

    @staticmethod
    def get_rarity(trait):
        files = os.listdir(Character.resources_path + trait)

        weights = []
        for i in files:
            weights.append(int(i.split('_')[1]))
        if len(weights) == 1:
            return {1: 1.0}
        sum_weights = sum(weights)
        proba_picks = []
        for weight in weights:
            proba_picks.append(weight / sum_weights)
        sum_proba_picks = sum(proba_picks)
        raw_rarities = []
        for proba_pick in proba_picks:
            raw_rarities.append(proba_pick / (sum_proba_picks - proba_pick))
        rarities = {}
        index = 0
        for raw_rarity in raw_rarities:
            rarities[weights[index]] = (raw_rarity / max(raw_rarities))
            index += 1
        return rarities

    @classmethod
    def get_rarity_score(cls, character):
        for trait in character.parts:
            return Rarity.get_rarity(trait)

    @classmethod
    def get_rarest_score(cls, character):
        min_weights = []
        k = 0
        for item in character.parts.items():
            weights = []
            files = os.listdir(character.resources_path + item[0])
            for file in files:
                weights.append(int(file.split("_")[1]))
            if len(weights) > 1:
                min_weights.append(min(weights) / sum(weights))
                k += 1
        return 1 - (sum(min_weights) / k)

    @staticmethod
    def get_most_common_score(character):
        max_weights = []
        k = 0
        for item in character.parts.items():
            weights = []
            files = os.listdir(character.resources_path + item[0])
            for file in files:
                weights.append(int(file.split("_")[1]))
            if len(weights) > 1:
                max_weights.append(max(weights) / sum(weights))
                k += 1
        return 1 - (sum(max_weights) / k)
