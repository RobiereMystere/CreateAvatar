import tkinter as tk
import random
import sys
import os
import pyscreenshot as ImageGrab

from PIL import Image, ImageTk
import numpy as np

class Character():
    def __init__(self,seed=None):
        if(seed==None):
            #self.seed = random.randrange(sys.maxsize)
            self.seed = random.randrange(9999)
        else:
            self.seed=seed
        self.sz=10
        self.rnd=random.Random(int(self.seed))
        self.parts={
                'backgrounds':{'path':None,'color':None},
                'bodies':{'path':None,'color':None},
                'headshapes':{'path':None,'color':None},
                'eyes':{'path':None,'color':None},
                'mouths':{'path':None,'color':None},
                'hats':{'path':None,'color':None}

                }
        self.generateTraits()
    
    def generateTraits(ctx):
        for i in ctx.parts:
            files = os.listdir('./'+i)
            imgpath = i+'/'+ctx.rnd.choice(files)
            ctx.parts[i]['path']=imgpath
            ctx.parts[i]['color']=(int(ctx.rnd.random()*255),int(ctx.rnd.random()*255),int(ctx.rnd.random()*255))

        print(ctx.parts)
class Application(tk.Tk):

    
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("AVATAR CREATOR")
        self.canvasZone=tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.optZone=tk.Frame(self, relief=tk.RAISED, borderwidth=1)
    
        self.canvas=tk.Canvas(self.canvasZone,width=500,height=500)
        self.canvas.pack()
        self.sz=1
        self.pictures=list()
        self.currentCharacter=None
        self.canvasZone.pack(fill=tk.BOTH, expand=True)
        self.optZone.pack(fill=tk.BOTH, expand=True)

        self.newCharacterButton=tk.Button(self.optZone,text="REROLL",command=self.newCharacter)
        self.newCharacterButton.grid(row=0,column=1)

        self.newCharacterButton=tk.Button(self.optZone,text="REFRESH",command=self.drawChar)
        self.newCharacterButton.grid(row=0,column=2)

        self.seedLabel = tk.Label(self.optZone, text="Seed" )
        self.seedLabel.grid(row=1,column=0)

        self.seedField=tk.Text(self.optZone, height=1)
        self.seedField.grid(row=1,column=1)

        self.seedButton=tk.Button(self.optZone,text="seed",command=self.newCharacterSeed)
        self.seedButton.grid(row=1,column=2)

        self.filenameLabel = tk.Label(self.optZone, text="File Name" )
        self.filenameLabel.grid(row=2,column=0)

        self.filenameField=tk.Text(self.optZone, height=1)
        self.filenameField.grid(row=2,column=1)

        self.saveButton=tk.Button(self.optZone,text="SAVE",command=self.savePicture)
        self.saveButton.grid(row=2,column=2)

    def savePicture(ctx):
        x = tk.Canvas.winfo_rootx(ctx.canvas)
        y = tk.Canvas.winfo_rooty(ctx.canvas)
        w = tk.Canvas.winfo_width(ctx.canvas)
        h = tk.Canvas.winfo_height(ctx.canvas)
        filename=ctx.filenameField.get("1.0",tk.END+"-1c")
        if(len(filename)==0):
            #filename="default.png"
            filename=str(ctx.currentCharacter.seed)+".png"
        img= ImageGrab.grab(bbox=(x, y, x+w, y+h)).save(filename)

    def clear(self,ctx):
        for widgets in ctx.winfo_children():
            widgets.destroy()
    
    def newCharacterSeed(ctx):
        try:
            seed=int(ctx.seedField.get("1.0",tk.END+"-1c"))
        except ValueError:
            seed=0            
        newChar=Character(seed=seed)
        ctx.drawChar(newChar)

    def newCharacter(ctx):
        newChar=Character()
        ctx.drawChar(newChar)

    
    def drawChar(ctx,character=None):
        if(character==None):
            character=ctx.currentCharacter
        for trait in character.parts:
            filepath=os.getcwd()+"/"+character.parts[trait]['path']
            im = Image.open(filepath)
            im = im.convert('RGBA')
            data = np.array(im)
            red, green, blue, alpha = data.T 
            light=131
            dark=110
            white_areas = (red > light) & (blue > light) & (green > light)
            black_areas = (red < dark) & (blue < dark) & (green < dark)
            grey_areas = (red>=dark)&(red<=light) &(blue>=dark)&(blue<=light) &(green>=dark)&(green<=light)

            data[..., :-1][white_areas.T] = character.parts[trait]['color']
            grey_replacement=character.parts[trait]['color']
            grey_replacement=(grey_replacement[0]*0.75,grey_replacement[1]*0.75,grey_replacement[2]*0.75)
            print(grey_replacement,trait)
            data[..., :-1][grey_areas.T] =grey_replacement
            print(True in grey_areas.T)
            data[..., :-1][black_areas.T] =(0,0,0)
            im2 = Image.fromarray(data)

            img= ImageTk.PhotoImage(im2)

            ctx.pictures.append(img)
            ctx.canvas.create_image(250,250,image=img)
        numberWidth=20
        centerX=267
        numberPosX=225
        numberPosY=450
        strSeed=str(character.seed)
        numberPosX=centerX-(len(strSeed)*numberWidth)/2
        for digit in (strSeed):
            #220,450
            filepath=os.getcwd()+"/numbers/"+digit+".png"
            img= ImageTk.PhotoImage(file=filepath)

            ctx.pictures.append(img)
            ctx.canvas.create_image(numberPosX,numberPosY,image=img)
            numberPosX+=20
        ctx.canvas.update()
        ctx.currentCharacter=character

        '''
        for i in range(0,int(ctx.canvas.cget('width')),character.sz):
            for j in range(0,int(ctx.canvas.cget('height')),character.sz):
                n=int(character.rnd.random() * 4096)
                h='{0:03x}'.format(n)
                col="#"+h
                ctx.canvas.create_rectangle( i,j,i+character.sz,j+character.sz ,fill=col,outline="")
        '''

if __name__ == "__main__":
    newChar=Character()
    print(newChar.seed)
    app = Application()
    app.drawChar(newChar)
    app.mainloop()
    

