from Tkinter import *
import query_library

__author__ = 'jesse bostic'
__author__ = 'nick ames'



class SnootbootGUI:

    FINDER = (['name', 'shape', 'material', 'color', 'manufacturer', 'min price', 'max price', 'find'], #boot
              ['name', 'length', 'material', 'color', 'manufacturer', 'min price', 'max price', 'find'], #tie
              ['name', 'type', 'material', 'color', 'manufacturer', 'min price', 'max price', 'find']) #clasp

    def __init__(self):
        self.root = Tk()
        self.root.attributes("-zoomed", True)

        self.root.title("Custom Snootboot Marketplace")
        self.root['bg'] = '#656565'
        self.frame = Frame(self.root)

        self._create_components()

        self.frame.pack()
        self.root.mainloop()

    def _create_components(self):

        row = 0

        for comp_list in self.FINDER:
            text = comp_list[0]
            comp_list[0] = Entry(self.frame)
            comp_list[0].insert(0, text)
            comp_list[0].grid(row=row, column=0)

            text = comp_list[1]
            comp_list[1] = Entry(self.frame)
            comp_list[1].insert(END, text)
            comp_list[1].grid(row=row, column=1)

            row += 1

        OPTIONS = [
            "pig",
            "bunny",
            "chicken"
        ]

        variable = StringVar(self.frame)
        variable.set(OPTIONS[0]) # default value

        w = apply(OptionMenu, (self.frame, variable) + tuple(OPTIONS))
        w.grid()