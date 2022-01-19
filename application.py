"""Randomly Generate Avatars Module."""
import tkinter as tk
import os
import pyscreenshot as ImageGrab
from PIL import Image, ImageTk
import numpy as np

from ImageCharacter import ImageCharacter
from character import Character


class Application(tk.Tk):
    """GUI Object."""

    def __init__(self):
        tk.Tk.__init__(self)
        self.picture = None
        self.list_box_files = None
        self.list_box = None
        self.pictures = []
        self.current_character = None
        self.tk.call('wm', 'iconphoto', self._w, ImageTk.PhotoImage(file='icons/icon.ico'))
        self.title("AVATAR CREATOR")
        self.canvas_zone = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.opt_zone = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.select_zone = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        #
        self.list_boxes(self.select_zone, Character())
        self.selected_trait = None
        self.canvas = tk.Canvas(self.canvas_zone, width=500, height=500)
        self.canvas.pack()
        self.select_zone.pack(side=tk.RIGHT, expand=True)

        self.canvas_zone.pack(fill=tk.BOTH, expand=True)
        self.opt_zone.pack(expand=True)
        #
        tk.Button(self.opt_zone, text="RE-ROLL", command=self.new_character).grid(row=0, column=1)
        tk.Button(self.opt_zone, text="REFRESH", command=self.draw_char).grid(row=0, column=2)
        #
        tk.Label(self.opt_zone, text="Seed").grid(row=1, column=0)
        #
        self.seed_field = tk.Entry(self.opt_zone, width=20)
        self.seed_field.grid(row=1, column=1)
        self.seed_field.bind('<Return>', self.new_character_seed)
        #
        tk.Button(self.opt_zone, text="seed", command=self.new_character_seed).grid(row=1, column=2)
        #
        tk.Label(self.opt_zone, text="File Name").grid(row=2, column=0)
        #
        self.filename_field = tk.Entry(self.opt_zone, width=20)
        self.filename_field.bind('<Return>', self.save_picture)
        self.resolution_scales = {
            'width': tk.Scale(self.opt_zone,
                              from_=100,
                              to=10000,
                              resolution=100,
                              length=200,
                              orient=tk.HORIZONTAL),
            'height': tk.Scale(self.opt_zone,
                               from_=100,
                               to=10000,
                               resolution=100,
                               length=200,
                               orient=tk.HORIZONTAL)
        }
        self.resolution_scales['width'].set(500)
        self.resolution_scales['height'].set(500)
        tk.Label(self.opt_zone, text="width").grid(row=4, column=0)
        self.resolution_scales['width'].grid(row=4, column=1)
        tk.Label(self.opt_zone, text="height").grid(row=5, column=0)
        self.resolution_scales['height'].grid(row=5, column=1)
        #
        tk.Button(self.opt_zone, text="SAVE", command=self.save_picture).grid(row=2, column=2)
        tk.Button(self.opt_zone, text="search SEED", command=self.search_seed).grid(row=3, column=2)
        self.start_seed_field = tk.Entry(self.opt_zone, width=20)
        self.start_seed_field.grid(row=4, column=2)
        self.end_seed_field = tk.Entry(self.opt_zone, width=20)
        self.end_seed_field.grid(row=5, column=2)
        tk.Button(self.opt_zone, text="generate multiple", command=self.generate_multiple).grid(row=6, column=2)

    def generate_multiple(self):
        for seed in range(int(self.start_seed_field.get()), int(self.end_seed_field.get())):
            self.new_character_seed(seed=seed)
            self.save_picture()

    def search_seed(self):
        seed = 0
        character = Character(seed)
        while character != self.current_character:
            character = Character(seed)
            seed += 1
        print(seed - 1)

    def list_boxes(self, zone, character):
        self.list_box_files = tk.Listbox(zone, selectmode=tk.SINGLE)
        self.list_box = tk.Listbox(zone, selectmode=tk.SINGLE)
        self.list_box.insert(tk.END, *character.parts)
        self.list_box.bind('<<ListboxSelect>>', self.on_select)
        self.list_box_files.bind('<<ListboxSelect>>', self.change_trait)
        self.list_box.pack()
        self.list_box_files.pack()

    def change_trait(self, evt):
        w = evt.widget
        print(w.curselection())
        if len(w.curselection()) > 0:
            index = int(w.curselection()[0])
            value = w.get(index)
            print(value, self.current_character.parts[self.selected_trait])
            self.current_character.parts[self.selected_trait]['path'] = self.current_character.resources_path + \
                                                                        self.selected_trait + '/' + value
        self.draw_char()

    def on_select(self, evt):
        w = evt.widget
        if len(w.curselection()) > 0:
            index = int(w.curselection()[0])
            value = w.get(index)
            files = os.listdir(self.current_character.resources_path + value)
            self.list_box_files.delete(0, tk.END)
            self.list_box_files.insert(tk.END, *files)
            print('You selected item %d: "%s"' % (index, value))
            self.selected_trait = value

    @staticmethod
    def set_text_input(field, text):
        """Could be in a tool module."""
        field.delete(0, "end")
        field.insert(0, text)
        #

    def save_picture(self, event=None):
        """Saves Picture."""
        if event is not None:
            print("<RETURN>", event)
        filename = self.filename_field.get()
        if len(filename) == 0:
            filename = str(self.current_character.seed) + ".png"
        self.picture.save("saves/" + self.current_character.ranking + "_" + filename)
        print("saved as ", filename)

    def clear(self):
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.canvas_zone, width=500, height=500)
        self.canvas.pack()

    def new_character_seed(self, event=None, seed=None):
        """Create new character with seed set manually."""
        if event is not None:
            print("<RETURN>", event)
        try:
            if seed is None:
                seed = int(self.seed_field.get())
        except ValueError:
            seed = 0
        self.draw_char(Character(seed=seed))
        #

    def new_character(self):
        """Create new character."""
        self.current_character = Character()
        self.draw_char(self.current_character)
        #

    def draw_char(self, character=None):
        """Draw a Character."""
        image2 = None
        self.clear()
        self.pictures = []
        self.picture = None
        if character is None:
            character = self.current_character
        images = {}
        for trait in character.parts:
            image_data = ImageCharacter(character, trait, character.parts[trait]['pattern'])
            images[trait] = image_data

            grey_replacement = images[trait].color
            grey_replacement = (grey_replacement[0] * 0.75,
                                grey_replacement[1] * 0.75,
                                grey_replacement[2] * 0.75,
                                255)

            images[trait].data[..., :-1][images[trait].white.T] = images[trait].color
            images[trait].data[..., :-1][images[trait].black.T] = (0, 0, 0)
            images[trait].data[...][images[trait].grey.T] = grey_replacement
            images[trait].data[...][images[trait].shadow.T] = (0, 0, 0, 0)
            pattern_color = character.parts[trait]['pattern-color']
            pattern_shadow = (pattern_color[0] * 0.75,
                              pattern_color[1] * 0.75,
                              pattern_color[2] * 0.75,
                              255)
            if '/0.png' not in character.parts[trait]['pattern']:
                ImageCharacter.replace_color(images, trait, images[trait].pattern_areas, images[trait].white,
                                             pattern_color)
                ImageCharacter.replace_color(images, trait, images[trait].pattern_areas, images[trait].grey,
                                             pattern_shadow)
            try:
                ImageCharacter.replace_color(images, trait, images[trait].shadow, images['headshapes'].white,
                                             (0, 0, 0, 127))
                ImageCharacter.replace_color(images, trait, images[trait].shadow, images['headshapes'].grey,
                                             (0, 0, 0, 127))
                ImageCharacter.replace_color(images, trait, images[trait].shadow, images['bodies'].white,
                                             (0, 0, 0, 127))
                ImageCharacter.replace_color(images, trait, images[trait].shadow, images['bodies'].grey,
                                             (0, 0, 0, 127))
            except KeyError:
                pass
            image3 = Image.fromarray(images[trait].data)

            if image2 is None:
                image2 = Image.fromarray(images[trait].data)
            else:
                image2.alpha_composite(image3)

            image = ImageTk.PhotoImage(image2)

            self.pictures.append(image)
            self.canvas.create_image(250, 250, image=image)
        self.picture = image2
        self.draw_seed(character)

    def draw_seed(self, character):
        """Draw the SEED used to Generate Random."""
        number_width = 18
        center_x = 267
        number_pos_y = 450
        str_seed = str(character.seed)
        number_pos_x = center_x - (len(str_seed) * number_width) / 2
        for digit in str_seed:
            filepath = os.getcwd() + "/" + character.resources_path + "numbers/" + digit + ".png"
            img = ImageTk.PhotoImage(file=filepath)
            img2 = Image.open(filepath)
            self.pictures.append(img)
            self.canvas.create_image(number_pos_x, number_pos_y, image=img)
            self.picture.alpha_composite(img2, (int(number_pos_x)-10, int(number_pos_y)-10))
            number_pos_x += number_width
        self.canvas.update()
        self.current_character = character
        self.set_text_input(self.seed_field, str(character.seed))
