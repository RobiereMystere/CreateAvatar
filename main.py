# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from application import Application
from character import Character
import matplotlib.pyplot as plt

if __name__ == "__main__":
    """new_character = Character()
    app = Application()
    app.draw_char(new_character)
    app.mainloop()
    """
    rarities = []
    for i in range(10000):
        rarities.append(Character(i).rarity)
    rarities.sort()
    plt.plot(rarities)
    for n in range(1, 7):
        print(n)
        plt.axhline(y=n / 6., color='r')
    plt.ylabel('some numbers')
    plt.show()
