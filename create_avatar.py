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
                'backgrounds':{'path':None,'color':None,'pattern':False,'pattern-color':None},
                'bodies':{'path':None,'color':None,'pattern':True,'pattern-color':None},
                'headshapes':{'path':None,'color':None,'pattern':False,'pattern-color':None},
                'eyes':{'path':None,'color':None,'pattern':False,'pattern-color':None},
                'glasses':{'path':None,'color':None,'pattern':False,'pattern-color':None},
                'moustaches':{'path':None,'color':None,'pattern':False,'pattern-color':None},
                'mouths':{'path':None,'color':None,'pattern':False,'pattern-color':None},
                'hats':{'path':None,'color':None,'pattern':True,'pattern-color':None}
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
            item[1]['pattern-color']=(
                int(self.rnd.random()*255),
                int(self.rnd.random()*255),
                int(self.rnd.random()*255))
            files = os.listdir('./resources/patterns')
            if(item[1]['pattern']):
                item[1]['pattern']='resources/patterns/'+self.rnd.choice(files)
            else:
                item[1]['pattern']='resources/patterns/0.png'

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
        self.resolution_scales={
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
        tk.Label(self.opt_zone, text="width" ).grid(row=4,column=0)
        self.resolution_scales['width'].grid(row=4,column=1)
        tk.Label(self.opt_zone, text="height" ).grid(row=5,column=0)
        self.resolution_scales['height'].grid(row=5,column=1)
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

        img=img.resize(
                (self.resolution_scales['width'].get(),self.resolution_scales['height'].get())
            ,resample=0)
        img.save("saves/"+filename)
        print("saved as ",filename)
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
    def image_file2dic(self,filepath,dic,character,trait):
        """set Dic from image filepath."""
        light=200
        dark=10
        data = self.image_file2data(filepath)
        datapattern = self.image_file2data(os.getcwd()+"/"+character.parts[trait]['pattern'])
        dicpattern={}
        dicpattern['data']=datapattern
        dicpattern['red'],\
                dicpattern['green'],\
                dicpattern['blue'],\
                dicpattern['alpha']=dicpattern['data'].T
        #
        dic['data']=data
        dic['red'],\
                dic['green'],\
                dic['blue'],\
                dic['alpha']=dic['data'].T
        dic['black_areas'] = \
                (dic['red'] < dark)\
                &(dic['green'] < dark)\
                &(dic['blue'] < dark) \
                & (dic['alpha'] > 200)
        dic['white_areas'] = \
                (dic['red'] > light)\
                &(dic['green'] > light)\
                &(dic['blue'] > light) \
                & (dic['alpha'] > 200)
        dic['transp_areas'] = \
                (dic['alpha'] < 10)\
                |((dic['red'] < dark)\
                &(dic['green'] < dark)\
                &(dic['blue'] < dark))
        dic['grey_areas'] = \
                (dic['red'] >=dark)\
                &(dic['red'] <=light)\
                &(dic['green'] >=dark)\
                &(dic['green'] <=light)\
                &(dic['blue'] >=dark)\
                &(dic['blue'] <=light)
        dic['green_areas'] = \
                (dic['red'] == 0)\
                &(dic['green'] == 255)\
                &(dic['blue'] == 0)
        dic['pattern_areas'] = \
                (dicpattern['red'] == 0)\
                &(dicpattern['green'] == 0)\
                &(dicpattern['blue'] == 255)
        dic['red_areas'] = \
                (dic['red'] == 255)\
                &(dic['green'] == 0)\
                &(dic['blue'] == 0)
    @staticmethod
    def data2dic(data,dic):
        #update dictionary with data
        light=200
        dark=10
        dic['red'],\
                dic['green'],\
                dic['blue'],\
                dic['alpha']=data.T
        dic['black_areas'] = \
                (dic['red'] < dark)\
                &(dic['green'] < dark)\
                &(dic['blue'] < dark) \
                & (dic['alpha'] > 200)
        dic['white_areas'] = \
                (dic['red'] > light)\
                &(dic['green'] > light)\
                &(dic['blue'] > light) \
                & (dic['alpha'] > 200)
        dic['transp_areas'] = \
                (dic['alpha'] < 10)\
                |((dic['red'] < dark)\
                &(dic['green'] < dark)\
                &(dic['blue'] < dark))
        dic['grey_areas'] = \
                (dic['red'] >=dark)\
                &(dic['red'] <=light)\
                &(dic['green'] >=dark)\
                &(dic['green'] <=light)\
                &(dic['blue'] >=dark)\
                &(dic['blue'] <=light)
        dic['green_areas'] = \
                (dic['red'] == 0)\
                &(dic['green'] == 255)\
                &(dic['blue'] == 0)
        dic['red_areas'] = \
                (dic['red'] == 255)\
                &(dic['green'] == 0)\
                &(dic['blue'] == 0)

    def set_trait_pattern2dic(self,character,trait,datas):
        """set pattern of a trait into dictionary datas."""
        datapattern = self.image_file2data(os.getcwd()+"/"+character.parts[trait]['pattern'])
        dicpattern={}
        dicpattern['data']=datapattern
        dicpattern['red'],\
                dicpattern['green'],\
                dicpattern['blue'],\
                dicpattern['alpha']=dicpattern['data'].T
        datas[trait]['pattern_areas'] = \
                (dicpattern['red'] == 0)\
                &(dicpattern['green'] == 0)\
                &(dicpattern['blue'] == 255)

    def draw_char(self,character=None):
        """Draw a Character."""
        self.clear(self.canvas)
        if character is None :
            character=self.current_character
        for trait in character.parts:
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
                        'grey_areas':None,
                        'pattern_areas':None,
                        'pattern_color':None
                        },
                    'eyes':{'data':None},
                    'headshapes':{'data':None},
                    'glasses':{'data':None}
                    }
            for item in datas.items():
                #print(item[1]['data']is datas[item[0]]['data'])
                self.image_file2dic(os.getcwd()+"/"+character.parts[item[0]]['path'],item[1],character,trait)
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
            pattern_color=character.parts[trait]['pattern-color']
            pattern_color_eyes=character.parts['eyes']['pattern-color']
            pattern_color_glasses=character.parts['glasses']['pattern-color']
            pattern_color_headshapes=character.parts['headshapes']['pattern-color']
            pattern_shadow=(pattern_color[0]*0.75,
                               pattern_color[1]*0.75,
                               pattern_color[2]*0.75,
                               255)
            pattern_shadow_eyes=(pattern_color_eyes[0]*0.75,
                               pattern_color_eyes[1]*0.75,
                               pattern_color_eyes[2]*0.75,
                               255)
            pattern_shadow_glasses=(pattern_color_glasses[0]*0.75,
                               pattern_color_glasses[1]*0.75,
                               pattern_color_glasses[2]*0.75,
                               255)
            pattern_shadow_headshapes=(pattern_color_headshapes[0]*0.75,
                               pattern_color_headshapes[1]*0.75,
                               pattern_color_headshapes[2]*0.75,
                               255)
            green_replacement=(green_replacement[0]*0.75,
                               green_replacement[1]*0.75,
                               green_replacement[2]*0.75,
                               255)
            pattern_shadow_headshapes=(pattern_color_headshapes[0]*0.75,
                               pattern_color_headshapes[1]*0.75,
                               pattern_color_headshapes[2]*0.75,
                               255)
            self.replace_color(datas,
                    trait,
                    (trait,'pattern_areas'),
                    (trait,'grey_areas'),
                    pattern_shadow)
            self.replace_color(datas,
                    trait,
                    (trait,'pattern_areas'),
                    (trait,'white_areas'),
                    pattern_color)
            self.set_trait_pattern2dic(character,'headshapes',datas)
            self.set_trait_pattern2dic(character,'eyes',datas)
            self.set_trait_pattern2dic(character,'glasses',datas)
            
            self.replace_color(datas,
                    trait,
                    ('eyes','pattern_areas'),
                    (trait,'red_areas'),
                    pattern_shadow_eyes)
 
            self.replace_color(datas,
                    trait,
                    ('glasses','pattern_areas'),
                    (trait,'red_areas'),
                    pattern_shadow_glasses)
 
            self.replace_color(datas,
                    trait,
                    ('headshapes','pattern_areas'),
                    (trait,'red_areas'),
                    pattern_shadow_headshapes)
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
            datas[trait]['data'][...,:-1][blank.T]=(color)
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
