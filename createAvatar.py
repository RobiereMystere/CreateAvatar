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
        #self.seed=567
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
        self.iconbitmap('icons/icon.ico')
        self.title("AVATAR CREATOR")
        self.canvasZone=tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.optZone=tk.Frame(self, relief=tk.RAISED, borderwidth=1)
    
        self.canvas=tk.Canvas(self.canvasZone,width=500,height=500)
        self.canvas.pack()
        self.sz=1
        self.pictures=list()
        self.currentCharacter=None
        self.canvasZone.pack(fill=tk.BOTH, expand=True)
        self.optZone.pack( expand=True)

        self.newCharacterButton=tk.Button(self.optZone,text="REROLL",command=self.newCharacter)
        self.newCharacterButton.grid(row=0,column=1)

        self.newCharacterButton=tk.Button(self.optZone,text="REFRESH",command=self.drawChar)
        self.newCharacterButton.grid(row=0,column=2)

        self.seedLabel = tk.Label(self.optZone, text="Seed" )
        self.seedLabel.grid(row=1,column=0)

        self.seedField=tk.Entry(self.optZone,width=20)
        self.seedField.grid(row=1,column=1)
        self.seedField.bind('<Return>', self.newCharacterSeed)

        self.seedButton=tk.Button(self.optZone,text="seed",command=self.newCharacterSeed)
        self.seedButton.grid(row=1,column=2)

        self.filenameLabel = tk.Label(self.optZone, text="File Name" )
        self.filenameLabel.grid(row=2,column=0)

        self.filenameField=tk.Entry(self.optZone,width=20)
        self.filenameField.grid(row=2,column=1)
        self.filenameField.bind('<Return>', self.savePicture)

        self.saveButton=tk.Button(self.optZone,text="SAVE",command=self.savePicture)
        self.saveButton.grid(row=2,column=2)

    def setTextInput(ctx,field,text):
        field.delete(0,"end")
        field.insert(0,text)

    def savePicture(ctx,event=None):
        x = tk.Canvas.winfo_rootx(ctx.canvas)
        y = tk.Canvas.winfo_rooty(ctx.canvas)
        w = tk.Canvas.winfo_width(ctx.canvas)
        h = tk.Canvas.winfo_height(ctx.canvas)
        filename=ctx.filenameField.get()
        if(len(filename)==0):
            filename=str(ctx.currentCharacter.seed)+".png"
        img= ImageGrab.grab(bbox=(x, y, x+w, y+h)).save(filename)

    def clear(self,ctx):
        for widgets in ctx.winfo_children():
            widgets.destroy()
    
    def newCharacterSeed(ctx,event=None):
        try:
            seed=int(ctx.seedField.get())
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
            light=131
            dark=110

            filepath=os.getcwd()+"/"+character.parts[trait]['path']
            im = Image.open(filepath)
            im = im.convert('RGBA')
            data = np.array(im)
            red, green, blue, alpha = data.T
            
            filepatheye=os.getcwd()+"/"+character.parts['eyes']['path']
            imeye = Image.open(filepatheye)
            imeye = imeye.convert('RGBA')
            dataeye = np.array(imeye)
            redeye, greeneye, blueeye, alphaeye = dataeye.T
            white_areaseye = (redeye > light) & (blueeye > light) & (greeneye > light)
            black_areaseye = (redeye < dark) & (blueeye < dark) & (greeneye < dark) & (alphaeye > 200)
            filepathhead=os.getcwd()+"/"+character.parts['headshapes']['path']
            imhead = Image.open(filepathhead)
            imhead = imhead.convert('RGBA')
            datahead = np.array(imhead)
            redhead, greenhead, bluehead, alphahead = datahead.T
            white_areashead = (redhead > light) & (bluehead > light) & (greenhead > light)
            grey_areashead = (redhead>=dark)&(redhead<=light) &(bluehead>=dark)&(bluehead<=light) &(greenhead>=dark)&(greenhead<=light)
            black_areashead = (redhead < dark) & (bluehead < dark) & (greenhead < dark)
            transp_areashead = (alphahead<10) | ((redhead < dark) & (bluehead < dark) & (greenhead < dark))

            light=131
            dark=110
            
            white_areas = (red > light) & (blue > light) & (green > light)
            black_areas = (red < dark) & (blue < dark) & (green < dark)
            grey_areas = (red>=dark)&(red<=light) &(blue>=dark)&(blue<=light) &(green>=dark)&(green<=light)
            green_areas = (red == 0) & (blue == 0) & (green == 255)
            red_areas = (red == 255) & (blue == 0) & (green == 0)& (alpha > 200)

            grey_replacement=character.parts[trait]['color']
            grey_replacement=(grey_replacement[0]*0.75,grey_replacement[1]*0.75,grey_replacement[2]*0.75)
            
            green_replacement=character.parts['headshapes']['color']
            green_replacement=(green_replacement[0]*0.75,green_replacement[1]*0.75,green_replacement[2]*0.75)

            red_replacement=character.parts['eyes']['color']
            red_replacement=(red_replacement[0]*0.75,red_replacement[1]*0.75,red_replacement[2]*0.75,255)
            
            data[..., :-1][white_areas.T] = character.parts[trait]['color']
            data[..., :-1][black_areas.T] =(0,0,0)
            data[..., :-1][grey_areas.T] = grey_replacement
            data[..., :-1][green_areas.T] = green_replacement


            blank=(redeye==-1)
            
            np.logical_and(red_areas,white_areaseye,out=blank)
            data[...][blank.T]=red_replacement
            
            np.logical_and(white_areashead,red_areas,out=blank)
            data[...,:-1][blank.T]=green_replacement
            np.logical_and(red_areas,white_areaseye,out=blank)
            data[...][blank.T]=red_replacement
            
            green_replacement=(green_replacement[0]*0.75,green_replacement[1]*0.75,green_replacement[2]*0.75)

            np.logical_and(grey_areashead,red_areas,out=blank)
            data[...,:-1][blank.T]=green_replacement

            np.logical_and(black_areaseye,red_areas,out=blank)
            data[...][blank.T]=(0,0,0,255)

            np.logical_and(transp_areashead,red_areas,out=blank)
            data[...][blank.T]=(255,0,0,0)

            im2 = Image.fromarray(data)

            img= ImageTk.PhotoImage(im2)

            ctx.pictures.append(img)
            ctx.canvas.create_image(250,250,image=img)
        numberWidth=20
        centerX=267
        numberPosY=450
        strSeed=str(character.seed)
        numberPosX=centerX-(len(strSeed)*numberWidth)/2
        for digit in (strSeed):

            filepath=os.getcwd()+"/numbers/"+digit+".png"
            img= ImageTk.PhotoImage(file=filepath)

            ctx.pictures.append(img)
            ctx.canvas.create_image(numberPosX,numberPosY,image=img)
            numberPosX+=20
        ctx.canvas.update()
        ctx.currentCharacter=character
        ctx.setTextInput(ctx.seedField,str(character.seed))
        
if __name__ == "__main__":
    newChar=Character()
    print(newChar.seed)
    app = Application()
    app.drawChar(newChar)
    app.mainloop()
    

