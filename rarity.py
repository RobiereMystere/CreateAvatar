import math
import os

from PixelOperations import PixelOperations


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
        character.rarity = self.get_rarity_score(character)

        rarest_score = self.get_rarest_score(character)
        commonest_score = self.get_most_common_score(character)

        character.rarity = 1 - ((character.rarity - rarest_score) / (commonest_score - rarest_score))
        ranking = ''
        for item in self.rankings.items():
            ranking = item[0]
            if character.rarity <= item[1]['probability']:
                break
        return ranking

    @staticmethod
    def get_rarity_score(character):
        scores = []
        k = 0
        for item in character.parts.items():
            weights = []
            files = os.listdir(character.resources_path + item[0])
            for file in files:
                weights.append(int(file.split("_")[1]))
            scores.append(int(item[1]['path'].split('_')[1]) / sum(weights))

        return sum(scores) / len(scores)

    @staticmethod
    def get_rarest_score(character):
        min_weights = []
        k = 0
        for item in character.parts.items():
            weights = []
            files = os.listdir(character.resources_path + item[0])
            for file in files:
                weights.append(int(file.split("_")[1]))
            min_weights.append(min(weights) / sum(weights))
            k += 1
        return sum(min_weights) / k

    @staticmethod
    def get_most_common_score(character):
        max_weights = []
        k = 0
        for item in character.parts.items():
            weights = []
            files = os.listdir(character.resources_path + item[0])
            for file in files:
                weights.append(int(file.split("_")[1]))
            max_weights.append(max(weights) / sum(weights))
            k += 1
        return sum(max_weights) / k
