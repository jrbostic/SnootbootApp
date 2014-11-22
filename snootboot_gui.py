from Tkinter import *
import query_library

__author__ = 'jesse bostic'
__author__ = 'nick ames'



class SnootbootGUI:

    FINDER = (['name', ('shape', query_library.get_boot_shapes), 'material', 'color', 'manufacturer', 'min price', 'max price', 'find', 'boot'], #boot
              ['name', ('length', query_library.get_tie_lengths), 'material', 'color', 'manufacturer', 'min price', 'max price', 'find', 'tie'], #tie
              ['name', ('type', query_library.get_clasp_types), 'material', 'color', 'manufacturer', 'min price', 'max price', 'find', 'clasp']) #clasp

    def __init__(self):
        self.root = Tk()
        #self.root.attributes("-zoomed", True)

        self.root.title("Custom Snootboot Marketplace")
        self.root['bg'] = '#656565'
        self.frame = Frame(self.root)

        self._create_components()

        self.frame.pack()
        self.root.mainloop()

    def _create_components(self):

        row = 0

        for comp_list in self.FINDER:

            Label(self.frame, text="Find A "+comp_list[-1].title()+": ").grid(row=row, column=0)

            text = comp_list[0]
            comp_list[0] = Entry(self.frame)
            comp_list[0].insert(0, text.title())
            comp_list[0].grid(row=row, column=1)

            text = comp_list[1][0]
            options = [list(i)[0] for i in sorted(comp_list[1][1]())]
            variable = StringVar(self.frame)
            variable.set(text.title())
            comp_list[1] = apply(OptionMenu, (self.frame, variable) + tuple(options))
            comp_list[1].grid(row=row, column=2)

            row += 1

