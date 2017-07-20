import sys
import time
from pygame import mixer
import Tkinter
import threading

import view
import world

BOARDWIDTH = 6
BOARDHEIGHT = 4
TIMEBETWEENSTEPS = 1
NPITS = 2

class SimThread(threading.Thread):
    def __init__(self, view, worldmap):
        super(SimThread, self).__init__()
        self.running = threading.Event()
        self.end = False
        self.view = view
        self.worldmap = worldmap

    def controlsim(self):
        if self.end:
            exit(0)
        if self.running.is_set():
            self.view.changebuttontext('Continuar')
            self.running.clear()
        else:
            self.view.changebuttontext('Pausar')
            self.running.set()

    def makeiamove(self):
        self.worldmap.randommove()

    def updateview(self):
        for room in self.worldmap.rooms.values():
            if room.explored:
                self.view.drawroom(room.posy, room.posx, room.objects)

    def run(self):
        super(SimThread, self).run()
        mixer.init()
        self.running.wait()
        self.worldmap.setup(NPITS)
        self.updateview()
        mixer.music.load('sounds/music.mp3')
        mixer.music.play()
        while not self.end:
            self.running.wait()
            self.view.changeinfolabel('Explorando...')
            time.sleep(TIMEBETWEENSTEPS)
            self.makeiamove()
            self.updateview()
            if self.worldmap.herodead:
                mixer.music.load('sounds/haha.mp3')
                mixer.music.play()
                self.view.changeinfolabel('O heroi esta morto!')
                self.end = True
            if self.worldmap.foundgold:
                mixer.music.load('sounds/victory.mp3')
                mixer.music.play()
                self.view.changeinfolabel('O heroi encontrou o ouro!')
                self.end = True
        self.worldmap.revealall()
        self.updateview()
        self.view.changebuttontext('Sair')



def main(argv):
    root = Tkinter.Tk()
    worldmap = world.World(BOARDWIDTH, BOARDHEIGHT)
    mainview = view.View(root, BOARDWIDTH, BOARDHEIGHT)
    simthread = SimThread(mainview, worldmap)
    mainview.createcontrolbutton(root, simthread.controlsim)

    simthread.start()
    root.mainloop()
    simthread.end = True
    simthread.join()
    mixer.quit()


if __name__ == "__main__":
    main(sys.argv)