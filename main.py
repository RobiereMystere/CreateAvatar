# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random


import rarity


def get_rarity_score(pick, elems, weights):
    allprobs = []
    for weight in weights:
        allprobs.append(weight / sum(weights))
    probpick = weights[elems.index(pick)] / sum(weights)
    rapportedpickprob = 1-(probpick / (sum(allprobs)-probpick))
    return rapportedpickprob


if __name__ == "__main__":
    rarity.Rarity.get_rarity("headshapes")

    """new_character = Character()
    app = Application()
    app.draw_char(new_character)
    app.mainloop()
    """
    '''
    rarities = []
    for i in range(1000):
        rarities.append(Character(i).rarity)
    rarities.sort()
    plt.plot(rarities)'''
    '''for n in range(1, 7):
        print(n)
        plt.axhline(y=n / 6., color='r')
    rnd = random.Random(99)
    elems = [0, 1, 2, 3, 4, 5]
    weights = [50, 30, 20, 1, 200, 50]
    picks = []
    rarities = []
    for pick in range(10000):
        picks.append(rnd.choices(elems, weights=weights)[0])
    probabilities = []
    for pick in elems:
        rarities.append(get_rarity_score(pick, elems, weights))
    print(rarities)
    all_rarities=[]
    for pick in picks:
        all_rarities.append(rarities[elems.index(pick)])
    all_rarities.sort()

    plt.plot(all_rarities)
    plt.ylabel('some numbers')
    plt.show()
'''