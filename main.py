import sys
import threading
import time
import tkinter

from pygame import mixer

import plia.aiplayer as aip
import view
import wumpus_world

GUI_ENABLED = True
BOARDWIDTH = 12
BOARDHEIGHT = 12
TIMEBETWEENSTEPS = 0.05
NPITS = 12
BASEPATH = 'plia/base.pl'
PREDPATH = 'plia/predicados.pl'


class SimThread(threading.Thread):
    def __init__(self, world_view, worldmap):
        super(SimThread, self).__init__()
        self.running = threading.Event()
        self.view = world_view
        self.worldmap = worldmap
        self.ia = aip.AIPlayer()

    def button_action(self):
        if self.check_end():
            self.view.destroy()
        elif self.running.is_set():
            self.view.changebuttontext('Continuar')
            self.running.clear()
        else:
            self.view.changebuttontext('Pausar')
            self.running.set()

    def feed_model_and_act(self):
        self.ia.set_observations(self.worldmap)
        action = self.ia.get_action()
        if action.type == 'm':
            self.worldmap.move_hero(action.direction)
        elif action.type == 'a':
            self.worldmap.fire_arrow(action.direction)

    def setup_view(self):
        if self.view is None:
            return
        mixer.init()

    def update_view(self):
        if self.view is None:
            return

        for room in self.worldmap.rooms.values():
            if room.explored:
                self.view.drawroom(room.posy, room.posx, room.objects)
        is_running = self.running.is_set()
        if is_running and not mixer.music.get_busy():
            mixer.music.load('sounds/music.ogg')
            mixer.music.play(-1)
        if is_running:
            self.view.changeinfolabel('Explorando...')
        elif self.worldmap.is_hero_dead:
            mixer.music.load('sounds/haha.ogg')
            mixer.music.play()
            self.view.changeinfolabel('O heroi esta morto!')
            self.view.changebuttontext('Sair')
        elif self.worldmap.found_gold:
            mixer.music.load('sounds/victory.ogg')
            mixer.music.play()
            self.view.changeinfolabel('O heroi encontrou o ouro!')
            self.view.changebuttontext('Sair')

    def check_end(self):
        return self.worldmap.is_hero_dead or self.worldmap.found_gold

    def run(self):
        super(SimThread, self).run()
        self.setup_view()
        self.running.wait()
        self.worldmap.setup(NPITS)
        self.update_view()
        while not self.check_end():
            self.running.wait()
            if self.view is not None:
                time.sleep(TIMEBETWEENSTEPS)
            self.feed_model_and_act()
            self.update_view()
        self.worldmap.reveal_all()
        self.running.clear()
        self.update_view()


def run_episode(seed):
    root, main_view = setup_gui()
    worldmap = wumpus_world.World(BOARDWIDTH, BOARDHEIGHT, seed)
    simthread = SimThread(main_view, worldmap)
    if GUI_ENABLED:
        main_view.createcontrolbutton(root, simthread.button_action)
    else:
        simthread.running.set()
    simthread.start()
    if root is not None:
        root.mainloop()
        simthread.end = True
    simthread.join()


def setup_gui():
    if GUI_ENABLED:
        root = tkinter.Tk()
        main_view = view.View(root, BOARDWIDTH, BOARDHEIGHT)
    else:
        root = None
        main_view = None
    return root, main_view


def main(argv):
    for i in range(2):
        seed = 94324
        run_episode(seed)
    mixer.quit()


if __name__ == "__main__":
    main(sys.argv)
