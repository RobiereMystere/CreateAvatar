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

    def set_trait_pattern2dic(self, character, trait, datas):
        """set pattern of a trait into dictionary datas."""
        datapattern = self.image_file2data(os.getcwd() + "/" + character.parts[trait]['pattern'])
        dic_pattern = {}
        dic_pattern['data'] = datapattern
        dic_pattern['red'], \
        dic_pattern['green'], \
        dic_pattern['blue'], \
        dic_pattern['alpha'] = dic_pattern['data'].T
        datas[trait]['pattern_areas'] = \
            (dic_pattern['red'] == 0) \
            & (dic_pattern['green'] == 0) \
            & (dic_pattern['blue'] == 255)

    def image_file2dic(self, filepath, dic, character, trait):
        """set Dic from image filepath."""
        light = 200
        dark = 10
        data = self.image_file2data(filepath)
        data_pattern = self.image_file2data(os.getcwd() + "/" + character.parts[trait]['pattern'])
        dic_pattern = {}
        dic_pattern['data'] = data_pattern
        dic_pattern['red'], \
        dic_pattern['green'], \
        dic_pattern['blue'], \
        dic_pattern['alpha'] = dic_pattern['data'].T
        #
        dic['data'] = data
        dic['red'], \
        dic['green'], \
        dic['blue'], \
        dic['alpha'] = dic['data'].T
        dic['black_areas'] = \
            (dic['red'] < dark) \
            & (dic['green'] < dark) \
            & (dic['blue'] < dark) \
            & (dic['alpha'] > 200)
        dic['white_areas'] = \
            (dic['red'] > light) \
            & (dic['green'] > light) \
            & (dic['blue'] > light) \
            & (dic['alpha'] > 200)
        dic['transp_areas'] = \
            (dic['alpha'] < 10) \
            | ((dic['red'] < dark) & (dic['green'] < dark) & (dic['blue'] < dark))
        dic['grey_areas'] = \
            (dic['red'] >= dark) \
            & (dic['red'] <= light) \
            & (dic['green'] >= dark) \
            & (dic['green'] <= light) \
            & (dic['blue'] >= dark) \
            & (dic['blue'] <= light)
        dic['pattern_areas'] = \
            (dic_pattern['red'] == 0) \
            & (dic_pattern['green'] == 0) \
            & (dic_pattern['blue'] == 255)

    @staticmethod
    def data2dic(data, dic):
        # update dictionary with data
        light = 200
        dark = 10
        dic['red'], \
        dic['green'], \
        dic['blue'], \
        dic['alpha'] = data.T
        dic['black_areas'] = \
            (dic['red'] < dark) \
            & (dic['green'] < dark) \
            & (dic['blue'] < dark) \
            & (dic['alpha'] > 200)
        dic['white_areas'] = \
            (dic['red'] > light) \
            & (dic['green'] > light) \
            & (dic['blue'] > light) \
            & (dic['alpha'] > 200)
        dic['transp_areas'] = \
            (dic['alpha'] < 10) \
            | ((dic['red'] < dark) & (dic['green'] < dark) & (dic['blue'] < dark))
        dic['grey_areas'] = \
            (dic['red'] >= dark) \
            & (dic['red'] <= light) \
            & (dic['green'] >= dark) \
            & (dic['green'] <= light) \
            & (dic['blue'] >= dark) \
            & (dic['blue'] <= light)
        dic['green_areas'] = \
            (dic['red'] == 0) \
            & (dic['green'] == 255) \
            & (dic['blue'] == 0)
        dic['red_areas'] = \
            (dic['red'] == 255) \
            & (dic['green'] == 0) \
            & (dic['blue'] == 0)

    def set_color(self, color):
        self.data[...][self.white.T] = color

    def superpose(self, image_data, color):
        """superpose self Matrix on image_data."""
        # self.data += image_data.data
        # blank = (self.red == -1)
        # np.logical_and(self.transparent, image_data.white, out=blank)
        # print(color)
        # self.data[...][self.black.T] = color
        print(self.data)
        if self.data is None:
            self.data = image_data.data
            return self
        '''for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j][3] == 0:
                    self.data[i][j] = image_data.data[i][j]'''

        self.data = np.where(self.data == (0, 0, 0, 0), self.data, image_data.data)
        return self

    @staticmethod
    def intersect(area1, area2):
        blank = (area1 == -1)
        np.logical_and(area1, area2, out=blank)
        return blank

    @staticmethod
    def replace_color(image_data, trait, image_data1, image_data2, color):
        """parameters:
            datas :  dic with all datas
            area1 :  (str trait,str area)
            area2 :  (str trait,str area)
            color :  (r,g,b,a)
            blank :  np.array
        """
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
