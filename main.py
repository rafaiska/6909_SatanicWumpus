import sys
import threading
import time

import tkinter
from pygame import mixer

import plia.aiplayer as aip
import view
import world

BOARDWIDTH = 12
BOARDHEIGHT = 12
TIMEBETWEENSTEPS = 1
NPITS = 2
BASEPATH = 'plia/base.pl'
PREDPATH = 'plia/predicados.pl'


class SimThread(threading.Thread):
    def __init__(self, view, worldmap):
        super(SimThread, self).__init__()
        self.running = threading.Event()
        self.end = False
        self.view = view
        self.worldmap = worldmap
        self.ia = aip.AIPlayer((BOARDWIDTH, BOARDHEIGHT))
        self.ia.hero_pos = self.worldmap.find_hero()

    def controlsim(self):
        if self.end:
            sys.exit(1)
        if self.running.is_set():
            self.view.changebuttontext('Continuar')
            self.running.clear()
        else:
            self.view.changebuttontext('Pausar')
            self.running.set()

    def makeiamove(self):
        self.ia.update(self.worldmap.get_current_room())
        self.worldmap.move_hero(self.ia.nextstep())
        # self.worldmap.randommove()

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
        mixer.music.load('sounds/music.ogg')
        mixer.music.play(-1)
        while not self.end:
            self.running.wait()
            self.view.changeinfolabel('Explorando...')
            time.sleep(TIMEBETWEENSTEPS)
            self.makeiamove()
            self.updateview()
            if self.worldmap.is_hero_dead:
                mixer.music.load('sounds/haha.ogg')
                mixer.music.play()
                self.view.changeinfolabel('O heroi esta morto!')
                self.end = True
            if self.worldmap.found_gold:
                mixer.music.load('sounds/victory.ogg')
                mixer.music.play()
                self.view.changeinfolabel('O heroi encontrou o ouro!')
                self.end = True
        self.worldmap.reveal_all()
        self.updateview()
        self.view.changebuttontext('Sair')


def main(argv):
    root = tkinter.Tk()
    worldmap = world.World(BOARDWIDTH, BOARDHEIGHT, 94324)
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
