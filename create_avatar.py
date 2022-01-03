"""Randomly Generate Avatars Module."""
import tkinter as tk
import random
import os
import pyscreenshot as ImageGrab
from PIL import Image, ImageTk
import numpy as np

class Character():
    """Character Object."""
    def __init__(self,seed=None):
        self.seed=seed
        if self.seed is None :
            #self.seed = random.randrange(sys.maxsize)
            self.seed = random.randrange(9999)
        #
        #self.seed=567
        self.rnd=random.Random(int(self.seed))
        self.parts={
                'backgrounds':{'path':None,'color':None},
                'bodies':{'path':None,'color':None},
                'headshapes':{'path':None,'color':None},
                'eyes':{'path':None,'color':None},
                'glasses':{'path':None,'color':None},
                'mouths':{'path':None,'color':None},
                'hats':{'path':None,'color':None}
                }
        self.generate_traits()
        #
    def generate_traits(self):
        """Randomly Sets traits of the Character."""
        for item in self.parts.items():
            files = os.listdir('./resources/'+item[0])
            imgpath = 'resources/'+item[0]+'/'+self.rnd.choice(files)
            item[1]['path']=imgpath
            item[1]['color']=(
                int(self.rnd.random()*255),
                int(self.rnd.random()*255),
                int(self.rnd.random()*255))
        print(self.to_string())
    def to_string(self):
        """Printable output for the character."""
        string=""
        for item in self.parts.items():
            string+=item[0]+"\n"
            for item2 in item[1]:
                string+='\t'+item2+':'+str(item[1][item2])+'\n'
        return string

        #
class Application(tk.Tk):
    """GUI Object."""
    def __init__(self):
        tk.Tk.__init__(self)
        self.pictures=[]
        self.current_character=None
        self.tk.call('wm', 'iconphoto', self._w, ImageTk.PhotoImage(file='icons/icon.ico'))
        self.title("AVATAR CREATOR")
        self.canvas_zone=tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.opt_zone=tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        #
        self.canvas=tk.Canvas(self.canvas_zone,width=500,height=500)
        self.canvas.pack()
        self.canvas_zone.pack(fill=tk.BOTH, expand=True)
        self.opt_zone.pack( expand=True)
        #
        tk.Button(self.opt_zone,text="REROLL",command=self.new_character).grid(row=0,column=1)
        tk.Button(self.opt_zone,text="REFRESH",command=self.draw_char).grid(row=0,column=2)
        #
        tk.Label(self.opt_zone, text="Seed" ).grid(row=1,column=0)
        #
        self.seed_field=tk.Entry(self.opt_zone,width=20)
        self.seed_field.grid(row=1,column=1)
        self.seed_field.bind('<Return>', self.new_character_seed)
        #
        tk.Button(self.opt_zone,text="seed",command=self.new_character_seed).grid(row=1,column=2)
        #
        tk.Label(self.opt_zone, text="File Name" ).grid(row=2,column=0)
        #
        self.filename_field=tk.Entry(self.opt_zone,width=20)
        self.filename_field.grid(row=2,column=1)
        self.filename_field.bind('<Return>', self.save_picture)
        #
        tk.Button(self.opt_zone,text="SAVE",command=self.save_picture).grid(row=2,column=2)
        #
    @staticmethod
    def set_text_input(field,text):
        """Could be in a tool module."""
        field.delete(0,"end")
        field.insert(0,text)
        #
    def save_picture(self,event=None):
        """Saves Picture."""
        if event is not None:
            print("<RETURN>",event)
        pos_x = tk.Canvas.winfo_rootx(self.canvas)
        pos_y = tk.Canvas.winfo_rooty(self.canvas)
        width = tk.Canvas.winfo_width(self.canvas)
        height = tk.Canvas.winfo_height(self.canvas)
        filename=self.filename_field.get()
        if len(filename)==0:
            filename=str(self.current_character.seed)+".png"
        img= ImageGrab.grab(bbox=(pos_x,
                                  pos_y,
                                  pos_x+width,
                                  pos_y+height))
        img.save("saves/"+filename)
        #
    @staticmethod
    def clear(ctx):
        """clears all elements."""
        for widgets in ctx.winfo_children():
            widgets.destroy()
        #
    def new_character_seed(self,event=None):
        """Create new character with seed set manually."""
        if event is not None:
            print("<RETURN>",event)
        try:
            seed=int(self.seed_field.get())
        except ValueError:
            seed=0
        self.draw_char(Character(seed=seed))
        #
    def new_character(self):
        """Create new character."""
        self.draw_char(Character())
        #
    @staticmethod
    def image_file2data(filepath):
        """get Data Arrays from filepath."""
        img = Image.open(filepath)
        img = img.convert('RGBA')
        return np.array(img)
        #
    def draw_char(self,character=None):
        """Draw a Character."""
        self.clear(self.canvas)
        if character is None :
            character=self.current_character
        for trait in character.parts:
            light=200
            dark=10
            #
            datas={
                    trait:{'data':None,
                        'red':None,
                        'green':None,
                        'blue':None,
                        'alpha':None,
                        'black_areas':None,
                        'white_areas':None,
                        'transp_areas':None,
                        'red_areas':None,
                        'green_areas':None,
                        'grey_areas':None
                        },
                    'eyes':{'data':None},
                    'headshapes':{'data':None},
                    'glasses':{'data':None}
                    }
            for item in datas.items():
                #print(item[1]['data']is datas[item[0]]['data'])
                data = self.image_file2data(os.getcwd()+"/"+character.parts[item[0]]['path'])
                item[1]['data']=data
                item[1]['red'],\
                        item[1]['green'],\
                        item[1]['blue'],\
                        item[1]['alpha']=item[1]['data'].T
                item[1]['black_areas'] = \
                        (item[1]['red'] < dark)\
                        &(item[1]['green'] < dark)\
                        &(item[1]['blue'] < dark) \
                        & (item[1]['alpha'] > 200)
                item[1]['white_areas'] = \
                        (item[1]['red'] > light)\
                        &(item[1]['green'] > light)\
                        &(item[1]['blue'] > light) \
                        & (item[1]['alpha'] > 200)
                item[1]['transp_areas'] = \
                        (item[1]['alpha'] < 10)\
                        |((item[1]['red'] < dark)\
                        &(item[1]['green'] < dark)\
                        &(item[1]['blue'] < dark))
                item[1]['grey_areas'] = \
                        (item[1]['red'] >=dark)\
                        &(item[1]['red'] <=light)\
                        &(item[1]['green'] >=dark)\
                        &(item[1]['green'] <=light)\
                        &(item[1]['blue'] >=dark)\
                        &(item[1]['blue'] <=light)
                item[1]['green_areas'] = \
                        (item[1]['red'] == 0)\
                        &(item[1]['green'] == 255)\
                        &(item[1]['blue'] == 0)
                item[1]['red_areas'] = \
                        (item[1]['red'] == 255)\
                        &(item[1]['green'] == 0)\
                        &(item[1]['blue'] == 0)
            #
            grey_replacement=character.parts[trait]['color']
            grey_replacement=(grey_replacement[0]*0.75,
                              grey_replacement[1]*0.75,
                              grey_replacement[2]*0.75,
                              255)
            #
            green_replacement=character.parts['headshapes']['color']
            green_replacement=(green_replacement[0]*0.75,
                               green_replacement[1]*0.75,
                               green_replacement[2]*0.75
                               ,255)
            #
            red_replacement=character.parts['eyes']['color']
            red_replacement=(red_replacement[0]*0.75,
                             red_replacement[1]*0.75,
                             red_replacement[2]*0.75)
            red_replacementg=red_replacement
            if 'glasses/0.png' not in character.parts['glasses']['path']:
                red_replacementg=character.parts['glasses']['color']
                red_replacementg=((red_replacement[0]*0.75+red_replacementg[0])/2,
                                 (red_replacement[1]*0.75+red_replacementg[1])/2,
                                 (red_replacement[2]*0.75+red_replacementg[2])/2)
                #
            datas[trait]['data'][...,:-1][datas[trait]['white_areas'].T] =\
                    character.parts[trait]['color']
            datas[trait]['data'][...,:-1][datas[trait]['black_areas'].T] = (0,0,0)
            datas[trait]['data'][...][datas[trait]['grey_areas'].T] = grey_replacement
            datas[trait]['data'][...][datas[trait]['green_areas'].T] = green_replacement
            #
            self.replace_color(
                    datas,
                    trait,
                    ('eyes','white_areas'),
                    (trait,'red_areas'),
                    red_replacement)
            self.replace_color(
                    datas,
                    trait,
                    ('headshapes','white_areas'),
                    (trait,'red_areas'),
                    green_replacement)
            self.replace_color(datas,
                    trait,
                    ('eyes','white_areas'),
                    (trait,'red_areas'),
                    red_replacement)
            green_replacement=(green_replacement[0]*0.75,
                               green_replacement[1]*0.75,
                               green_replacement[2]*0.75,
                               255)
            self.replace_color(datas,
                    trait,
                    ('headshapes','grey_areas'),
                    (trait,'red_areas'),
                    green_replacement)
            self.replace_color(datas,
                    trait,
                    ('eyes','black_areas'),
                    (trait,'red_areas'),
                    (0,0,0,255))
            self.replace_color(datas,
                    trait,
                    ('glasses','black_areas'),
                    (trait,'red_areas'),
                    (0,0,0,255))
            self.replace_color(datas,
                    trait,
                    ('glasses','white_areas'),
                    (trait,'red_areas'),
                    red_replacementg)
            self.replace_color(datas,
                    trait,
                    ('headshapes','transp_areas'),
                    (trait,'red_areas'),
                    (255,0,0,0))
            self.replace_color(datas,
                    trait,
                    ('headshapes','black_areas'),
                    (trait,'red_areas'),
                    (255,0,0,0))
            image2 = Image.fromarray(datas[trait]['data'])
            image= ImageTk.PhotoImage(image2)
            self.pictures.append(image)
            self.canvas.create_image(250,250,image=image)
        self.draw_seed(character)
        #
    def draw_seed(self,character):
        """Draw the SEED used to Generate Random."""
        number_width=20
        center_x=267
        number_pos_y=450
        str_seed=str(character.seed)
        number_pos_x=center_x-(len(str_seed)*number_width)/2
        for digit in (str_seed):
            filepath=os.getcwd()+"/resources/numbers/"+digit+".png"
            img= ImageTk.PhotoImage(file=filepath)
            self.pictures.append(img)
            self.canvas.create_image(number_pos_x,number_pos_y,image=img)
            number_pos_x+=20
        self.canvas.update()
        self.current_character=character
        self.set_text_input(self.seed_field,str(character.seed))
    @staticmethod
    def replace_color(datas,trait,area1,area2,color):
        """parameters:
            datas :  dic with all datas
            area1 :  (str trait,str area)
            area2 :  (str trait,str area)
            color :  (r,g,b,a)
            blank :  np.array
        """
        blank=(datas['eyes']['red']==-1)
        np.logical_and(datas[area1[0]][area1[1]],datas[area2[0]][area2[1]],out=blank)
        if len(color)==3 :
            datas[trait]['data'][...,:-1][blank.T]=color
        else:
            datas[trait]['data'][...][blank.T]=(color)

if __name__ == "__main__":
    new_character=Character()
    print(new_character.seed)
    app = Application()
    app.draw_char(new_character)
    app.mainloop()
#
#
#
