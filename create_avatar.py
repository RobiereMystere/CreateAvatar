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
        for i in self.parts:
            files = os.listdir('./'+i)
            imgpath = i+'/'+self.rnd.choice(files)
            self.parts[i]['path']=imgpath
            self.parts[i]['color']=(
                int(self.rnd.random()*255),
                int(self.rnd.random()*255),
                int(self.rnd.random()*255))
        print(self.parts)
        #
class Application(tk.Tk):
    """GUI Object."""
    def __init__(self):
        tk.Tk.__init__(self)
        self.iconbitmap('icons/icon.ico')
        self.title("AVATAR CREATOR")
        self.canvas_zone=tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.opt_zone=tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        #
        self.canvas=tk.Canvas(self.canvas_zone,width=500,height=500)
        self.canvas.pack()
        self.pictures=[]
        self.current_character=None
        self.canvas_zone.pack(fill=tk.BOTH, expand=True)
        self.opt_zone.pack( expand=True)
        #
        self.new_character_button=tk.Button(self.opt_zone,text="REROLL",command=self.new_character)
        self.new_character_button.grid(row=0,column=1)
        #
        self.new_character_button=tk.Button(self.opt_zone,text="REFRESH",command=self.draw_char)
        self.new_character_button.grid(row=0,column=2)
        #
        self.seed_label = tk.Label(self.opt_zone, text="Seed" )
        self.seed_label.grid(row=1,column=0)
        #
        self.seed_field=tk.Entry(self.opt_zone,width=20)
        self.seed_field.grid(row=1,column=1)
        self.seed_field.bind('<Return>', self.new_character_seed)
        #
        self.seed_button=tk.Button(self.opt_zone,text="seed",command=self.new_character_seed)
        self.seed_button.grid(row=1,column=2)
        #
        self.filename_label = tk.Label(self.opt_zone, text="File Name" )
        self.filename_label.grid(row=2,column=0)
        #
        self.filename_field=tk.Entry(self.opt_zone,width=20)
        self.filename_field.grid(row=2,column=1)
        self.filename_field.bind('<Return>', self.save_picture)
        #
        self.save_button=tk.Button(self.opt_zone,text="SAVE",command=self.save_picture)
        self.save_button.grid(row=2,column=2)
        #
    @staticmethod
    def set_text_input(field,text):
        """Could be in a tool module."""
        field.delete(0,"end")
        field.insert(0,text)
        #
    def save_picture(self,event=None):
        """Saves Picture."""
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
        img.save(filename)
        #
    def clear(self):
        """clears all elements."""
        for widgets in self.winfo_children():
            widgets.destroy()
        #
    def new_character_seed(self,event=None):
        """Create new character with seed set manually."""
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
        if character is None :
            character=self.current_character
        for trait in character.parts:
            light=200
            dark=10
            #
            data = self.image_file2data(os.getcwd()+"/"+character.parts[trait]['path'])
            dataeye = self.image_file2data(os.getcwd()+"/"+character.parts['eyes']['path'])
            datahead = self.image_file2data(os.getcwd()+"/"+character.parts['headshapes']['path'])
            dataglasses = self.image_file2data(os.getcwd()+"/"+character.parts['glasses']['path'])
            #
            red, green, blue, alpha = data.T
            redeye, greeneye, blueeye, alphaeye = dataeye.T
            redhead, greenhead, bluehead, alphahead = datahead.T
            redglasses, greenglasses, blueglasses, alphaglasses = dataglasses.T
            #
            black_areasglasses = (redglasses < dark)\
                             & (blueglasses < dark)\
                             & (greenglasses < dark)\
                             & (alphaglasses > 200)
            transp_areashead = (alphahead<10)
            whiteb_areasglasses = (redglasses > light)\
                             & (blueglasses > light)\
                             & (greenglasses > light)\
                             & (alphaglasses > 200)
            #
            white_areaseye = (redeye > light) \
                             & (blueeye > light)\
                             & (greeneye > light)
            black_areaseye = (redeye < dark)\
                             & (blueeye < dark)\
                             & (greeneye < dark)\
                             & (alphaeye > 200)
            #
            white_areashead = (redhead > light)\
                              & (bluehead > light)\
                              & (greenhead > light)
            grey_areashead = (redhead>=dark)\
                             &(redhead<=light)\
                             &(bluehead>=dark)\
                             &(bluehead<=light)\
                             &(greenhead>=dark)\
                             &(greenhead<=light)
            transp_areashead = (alphahead<10)\
                               | ((redhead < dark)\
                                  & (bluehead < dark)\
                                  & (greenhead < dark))
            #
            white_areas = (red > light)\
                          & (blue > light)\
                          & (green > light)
            black_areas = (red < dark)\
                          & (blue < dark)\
                          & (green < dark)
            grey_areas = (red>=dark)&(red<=light)\
                         &(blue>=dark)&(blue<=light)\
                         &(green>=dark)&(green<=light)
            green_areas = (red == 0)\
                          & (blue == 0)\
                          & (green == 255)
            red_areas = (red == 255)\
                        & (blue == 0)\
                        & (green == 0)\
                        & (alpha > 200)
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
            data[...,:-1][white_areas.T] = character.parts[trait]['color']
            data[...,:-1][black_areas.T] =(0,0,0)
            data[...][grey_areas.T] = grey_replacement
            data[...][green_areas.T] = green_replacement
            #
            blank=(redeye==-1)
            #
            np.logical_and(red_areas,white_areaseye,out=blank)
            data[...,:-1][blank.T]=red_replacement
            #
            np.logical_and(white_areashead,red_areas,out=blank)
            data[...][blank.T]=green_replacement
            np.logical_and(red_areas,white_areaseye,out=blank)
            data[...,:-1][blank.T]=red_replacement
            #
            green_replacement=(green_replacement[0]*0.75,
                               green_replacement[1]*0.75,
                               green_replacement[2]*0.75,
                               255)
            #
            np.logical_and(grey_areashead,red_areas,out=blank)
            data[...][blank.T]=green_replacement
            #
            np.logical_and(black_areaseye,red_areas,out=blank)
            data[...][blank.T]=(0,0,0,255)
            #
            np.logical_and(black_areasglasses,red_areas,out=blank)
            data[...][blank.T]=(0,0,0,255)
            #
            np.logical_and(whiteb_areasglasses,red_areas,out=blank)
            data[...,:-1][blank.T]=red_replacementg
            #
            np.logical_and(transp_areashead,red_areas,out=blank)
            data[...][blank.T]=(255,0,0,0)
            #
            image2 = Image.fromarray(data)
            image= ImageTk.PhotoImage(image2)
            #
            self.pictures.append(image)
            self.canvas.create_image(250,250,image=image)
        number_width=20
        center_x=267
        number_pos_y=450
        str_seed=str(character.seed)
        number_pos_x=center_x-(len(str_seed)*number_width)/2
        for digit in (str_seed):
            filepath=os.getcwd()+"/numbers/"+digit+".png"
            img= ImageTk.PhotoImage(file=filepath)
            self.pictures.append(img)
            self.canvas.create_image(number_pos_x,number_pos_y,image=img)
            number_pos_x+=20
        self.canvas.update()
        self.current_character=character
        self.set_text_input(self.seed_field,str(character.seed))
        #
        #
if __name__ == "__main__":
    new_character=Character()
    print(new_character.seed)
    app = Application()
    app.draw_char(new_character)
    app.mainloop()
#
#
#
