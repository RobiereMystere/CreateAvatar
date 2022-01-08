import numpy as np


class ImageData:

    def __init__(self, data=None, trait=""):
        super().__init__()
        self.data = data
        self.trait = trait
        if data is not None:
            self.red, self.green, self.blue, self.alpha = self.data.T
            self.white = (self.red + self.green + self.blue + self.alpha > 200 * 4)
            self.black = (self.red + self.green + self.blue < 10 * 4) & (self.alpha > 200)
            self.shadow = (self.alpha > 100) & (self.alpha < 200)
            self.transparent = (self.alpha < 10)

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

        self.data = np.where(self.data == (0,0,0,0), self.data, image_data.data)
        return self

    def replace_color(self, image_data, color):
        """parameters:
            datas :  dic with all datas
            area1 :  (str trait,str area)
            area2 :  (str trait,str area)
            color :  (r,g,b,a)
        """
        blank = (self.red == -1)
        np.logical_and(self.white, image_data.white, out=blank)
        if len(color) == 3:
            self.data[..., :-1][blank.T] = color
        else:
            self.data[...][blank.T] = color
