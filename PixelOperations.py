class PixelOperations:
    orange = (255, 120, 0)
    yellow = (255, 195, 0)
    purple = (200, 0, 200)
    cyan = (0, 255, 255)
    black = (0, 0, 0)
    white = (255, 255, 255)
    grey = (127, 127, 127)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    @staticmethod
    def random_color(rnd, random_scale):
        return int(rnd.random() * random_scale) * int(256 / random_scale), \
               int(rnd.random() * random_scale) * int(256 / random_scale), \
               int(rnd.random() * random_scale) * int(256 / random_scale)

    @staticmethod
    def darker(color):
        return color[0] * 0.75, color[1] * 0.75, color[2] * 0.75
