import random
import os

from PixelOperations import PixelOperations
from rarity import Rarity


class Character:
    """Character Object."""
    resources_path = 'resources-alpha/'

    def __init__(self, seed: int = None) -> None:
        self.seed = seed
        if self.seed is None:
            # self.seed = random.randrange(sys.maxsize)
            self.seed = random.randrange(99999999)
        #
        # self.seed=567
        self.rnd = random.Random(int(self.seed))
        self.parts = {
            'backgrounds': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'backhaircuts': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'bodies': {'path': None, 'color': None, 'pattern': True, 'pattern-color': None},
            'headshapes': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'eyes': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'mouths': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'moustaches': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'glasses': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'haircuts': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'hats': {'path': None, 'color': None, 'pattern': True, 'pattern-color': None},
            'wrists': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'boards': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'fingers': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None}
        }
        self.ranking = ''
        self.generate_traits()
        self.rarity = 0
        print(self.ranking)
        #

    def __eq__(self, character):
        """equality test.
        :param character:
        :return:
        """
        for part in self.parts:
            if self.parts[part]['path'] != character.parts[part]['path']:
                return False
        return True

    def generate_traits(self):
        """Randomly Sets traits of the Character."""
        random_scale = 255
        for item in self.parts.items():
            files = os.listdir(self.resources_path + item[0])
            print(item)
            probabilities = [int(file.split('_')[1]) for file in files]
            print(probabilities)
            print(self.rnd.choices(files, weights=probabilities))
            img_path = self.resources_path + item[0] + '/' + self.rnd.choices(files, weights=probabilities, k=1)[0]
            item[1]['path'] = img_path
            item[1]['color'] = PixelOperations.random_color(self.rnd, random_scale)
            item[1]['pattern-color'] = PixelOperations.random_color(self.rnd, random_scale)
            files = os.listdir(self.resources_path + 'patterns')
            if item[1]['pattern'] and 'hair' not in item[1]['path']:
                item[1]['pattern'] = self.resources_path + 'patterns/' + self.rnd.choice(files)
            else:
                item[1]['pattern'] = self.resources_path + 'patterns/0.png'
        # print()
        if 'hair' in self.parts['hats']['path']:
            self.parts['hats']['color'] = self.parts['backhaircuts']['color']
            self.parts['haircuts']['path'] = self.resources_path + 'haircuts/0_10_.png'
            self.parts['backhaircuts']['path'] = self.resources_path + 'backhaircuts/0_50_.png'
        self.parts['haircuts']['color'] = self.parts['backhaircuts']['color']
        self.parts['moustaches']['color'] = PixelOperations.darker(self.parts['backhaircuts']['color'])
        self.parts['wrists']['color'] = self.parts['bodies']['color']
        self.parts['wrists']['pattern'] = self.parts['bodies']['pattern']
        self.parts['wrists']['pattern-color'] = self.parts['bodies']['pattern-color']
        self.parts['fingers']['color'] = self.parts['headshapes']['color']
        self.ranking = Rarity().ranking(self)
        self.parts['boards']['color'] = Rarity().rankings[self.ranking]['color']

    def to_string(self):
        """Printable output for the character."""
        string = ""
        for item in self.parts.items():
            string += item[0] + "\n"
            for item2 in item[1]:
                string += '\t' + item2 + ':' + str(item[1][item2]) + '\n'
        string += "Seed \n\t" + str(self.seed)
        return string
        #
