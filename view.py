import Tkinter
from PIL import Image, ImageTk


class View(object):
    def __init__(self, root, width, height):
        root.title('Wumpus World')
        self.worldmap = Tkinter.Frame(master=root)
        self.worldmap.pack()
        self.siminfo = Tkinter.StringVar()
        self.simpanel = Tkinter.Label(master=root, textvariable=self.siminfo)
        self.simpanel.pack()
        self.siminfo.set('Bem vindo ao mundo de Wumpus!')

        self.rooms = {}
        for i in xrange(height):
            for j in xrange(width):
                newimage = ImageTk.PhotoImage(file='sprites/room.png')
                newroom = Tkinter.Label(master=self.worldmap, image=newimage)
                newroom.photo = newimage
                newroom.grid(row=i, column=j)
                self.rooms[i, j] = newroom

    def changebuttontext(self, newtext):
        self.simcontrol.configure(text=newtext)

    def changeinfolabel(self, newtext):
        self.siminfo.set(newtext)

    def createcontrolbutton(self, root, callfunction):
        self.simcontrol = Tkinter.Button(master=root, text='Iniciar IA', command=callfunction)
        self.simcontrol.pack()

    def addwumpus(self, image):
        wumpusimage = Image.open('sprites/wumpus.png')
        image.paste(wumpusimage, (0, 0), wumpusimage)

    def addpit(self, image):
        pitimage = Image.open('sprites/pit.png')
        image.paste(pitimage, (0, 27), pitimage)

    def addhero(self, image):
        heroimage = Image.open('sprites/explorer.png')
        image.paste(heroimage, (23, 17), heroimage)

    def addbreeze(self, image):
        breezeimage = Image.open('sprites/breeze.png')
        image.paste(breezeimage, (45, 2), breezeimage)

    def addstench(self, image):
        stenchimage = Image.open('sprites/stench.png')
        image.paste(stenchimage, (2, 2), stenchimage)

    def addgold(self, image):
        goldimage = Image.open('sprites/gold.png')
        image.paste(goldimage, (47, 47), goldimage)

    def drawroom(self, i, j, elements):
        newimage = Image.open('sprites/empty.png', 'r')
        if 'w' in elements:
            self.addwumpus(newimage)
        if 'p' in elements:
            self.addpit(newimage)
        if 'h' in elements:
            self.addhero(newimage)
        if 'b' in elements:
            self.addbreeze(newimage)
        if 's' in elements:
            self.addstench(newimage)
        if 'g' in elements:
            self.addgold(newimage)
        newimagetk = ImageTk.PhotoImage(newimage)
        self.rooms[i, j].configure(image=newimagetk)
        self.rooms[i, j].photo = newimagetk


