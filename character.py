import random
import os


class Character:
    """Character Object."""

    def __init__(self, seed=None):
        self.seed = seed
        if self.seed is None:
            # self.seed = random.randrange(sys.maxsize)
            self.seed = random.randrange(999999)
        #
        # self.seed=567
        self.rnd = random.Random(int(self.seed))
        self.parts = {
            'backgrounds': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'bodies': {'path': None, 'color': None, 'pattern': True, 'pattern-color': None},
            'headshapes': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'eyes': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'glasses': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'mouths': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'moustaches': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'hats': {'path': None, 'color': None, 'pattern': True, 'pattern-color': None},
            'wrists': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'boards': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None},
            'fingers': {'path': None, 'color': None, 'pattern': False, 'pattern-color': None}
        }
        self.generate_traits()
        #

    def __eq__(self, character):
        """equality test."""
        for part in self.parts:
            if self.parts[part]['path'] != character.parts[part]['path']:
                return False
        return True

    def generate_traits(self):
        """Randomly Sets traits of the Character."""
        random_scale = 5
        for item in self.parts.items():
            files = os.listdir('./resources/' + item[0])
            img_path = 'resources/' + item[0] + '/' + self.rnd.choice(files)
            item[1]['path'] = img_path
            item[1]['color'] = (
                int(self.rnd.random() * random_scale) * int(256 / random_scale),
                int(self.rnd.random() * random_scale) * int(256 / random_scale),
                int(self.rnd.random() * random_scale) * int(256 / random_scale))
            item[1]['pattern-color'] = (
                int(self.rnd.random() * random_scale) * int(256 / random_scale),
                int(self.rnd.random() * random_scale) * int(256 / random_scale),
                int(self.rnd.random() * random_scale) * int(256 / random_scale))
            files = os.listdir('./resources/patterns')
            if item[1]['pattern']:
                item[1]['pattern'] = 'resources/patterns/' + self.rnd.choice(files)
            else:
                item[1]['pattern'] = 'resources/patterns/0.png'
        # print()
        self.parts['wrists']['color'] = self.parts['bodies']['color']
        self.parts['wrists']['pattern'] = self.parts['bodies']['pattern']
        self.parts['wrists']['pattern-color'] = self.parts['bodies']['pattern-color']
        self.parts['fingers']['color'] = self.parts['headshapes']['color']
        self.parts['boards']['color'] = (0, 0, 0)
        # print(self.to_string())

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
