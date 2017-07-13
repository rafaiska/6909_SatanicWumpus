import Tkinter
import sys
import optparse


class MainScreen(Tkinter.Tk):
    def __init__(self):
        super(self, MainScreen).__init__()
        worldmap = Tkinter.Frame(self)
        worldmap.pack()


def main(argv):
    mainscreen = MainScreen()
    mainscreen.mainloop()


if __name__ == "__main__":
    main(sys.argv)
