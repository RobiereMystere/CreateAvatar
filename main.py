# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random

from matplotlib import pyplot as plt

import rarity
from application import Application
from character import Character

if __name__ == "__main__":
    new_character = Character()
    app = Application()
    app.draw_char(new_character)
    app.mainloop()
