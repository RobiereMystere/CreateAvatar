class PixelOperations:
    black = (0, 0, 0)

    @staticmethod
    def random_color(rnd, random_scale):
        return int(rnd.random() * random_scale) * int(256 / random_scale), \
               int(rnd.random() * random_scale) * int(256 / random_scale), \
               int(rnd.random() * random_scale) * int(256 / random_scale)

    @staticmethod
    def darker(color):
        return color[0] * 0.75, color[1] * 0.75, color[2] * 0.75
