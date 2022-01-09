import os

import numpy as np

from PIL import Image, ImageTk


class ImageCharacter:

    def __init__(self, character, trait="", pattern=None):
        super().__init__()
        self.character = character
        self.trait = trait
        self.data = self.image_file2data(os.getcwd() + "/" + character.parts[trait]['path'])
        self.pattern_path = pattern
        self.color = character.parts[trait]['color']
        if self.data is not None:
            self.red, self.green, self.blue, self.alpha = self.data.T
            # self.white = (self.red + self.green + self.blue + self.alpha > 200 * 4)
            self.white = (self.red > 200) & (self.green > 200) & (self.blue > 200) & (self.alpha > 200)
            self.black = (self.red < 10) & (self.green < 10) & (self.blue < 10) & (self.alpha > 200)
            self.grey = (self.red <= 200) & (self.green <= 200) & (self.blue <= 200) & (self.alpha > 200) & \
                        (self.red >= 10) & (self.green >= 10) & (self.blue >= 10) & (self.alpha >= 10)
            self.shadow = (self.red < 10) & (self.green < 10) & (self.blue < 10) & (self.alpha < 200) & (
                    self.alpha > 100)
            self.transparent = (self.alpha < 10)
            if self.pattern_path is not None and '/0.png' not in self.pattern_path:
                print(self.pattern_path)
                self.pattern_data = self.image_file2data(self.pattern_path)
                self.pattern_red, self.pattern_green, self.pattern_blue, self.pattern_alpha = self.pattern_data.T
                self.pattern_areas = (self.pattern_red == 0) & (self.pattern_green == 0) & (self.pattern_blue == 255)

    @staticmethod
    def replace_color(image_data, trait, image_data1, image_data2, color):
        """"""
        blank = (image_data1 == -1)
        np.logical_and(image_data1, image_data2, out=blank)
        if len(color) == 3:
            image_data[trait].data[..., :-1][blank.T] = color
        else:
            image_data[trait].data[...][blank.T] = color

    @staticmethod
    def image_file2data(filepath):
        """get Data Arrays from filepath."""
        img = Image.open(filepath)
        img = img.convert('RGBA')
        return np.array(img)
        #
