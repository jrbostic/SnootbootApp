from Tkinter import *
import query_library
import tkFont

__author__ = 'jesse bostic'
__author__ = 'nick ames'



class SnootbootGUI:

    FINDER = (['name', ('shape', query_library.get_boot_shapes), 'material', 'color', 'manufacturer', 'min price', 'max price', 'find', 'boot'], #boot
              ['name', ('length', query_library.get_tie_lengths), 'material', 'color', 'manufacturer', 'min price', 'max price', 'find', 'tie'], #tie
              ['name', ('type', query_library.get_clasp_types), 'material', 'color', 'manufacturer', 'min price', 'max price', 'find', 'clasp']) #clasp

    def __init__(self):
        self.root = Tk()
        self.root.resizable(0, 0)
        #self.root.attributes("-zoomed", True)

        self.root.title("Custom Snootboot Marketplace")
        self.root['bg'] = '#656565'
        self.frame = Frame(self.root)

        self.results = None
        self.scroll_window = None
        self. select_list = None

        self._boot_selection = None
        self._tie_selection = None
        self._clasp_selection = None

        self.boot_selection = StringVar()
        self.boot_selection.set("Boot: None Selected")
        self.tie_selection = StringVar()
        self.tie_selection.set("Tie: None Selected")
        self.clasp_selection = StringVar()
        self.clasp_selection.set("Clasp: None Selected")
        self.price_total = StringVar()
        self.price_total.set("Total: $0.00")

        self._create_components()

        self.frame.pack()
        self.root.mainloop()

    def set_selection(self, cancel=False):

        def toString(item, cat):
            the_string = ''
            for i in [1, 2, 3, 4, 8, 6]:
                if i==6:
                    the_string += "$" + str(item[i]) + '   '
                elif i==2:
                    if cat == 'Ties':
                        the_string += str(item[i]) + '"' + '   '
                    else:
                        the_string += str(item[i]) + '   '
                elif i==8:
                    the_string += item[i] + " (" + item[10] + ", " + item[11] + ")   "
                else:
                    the_string += item[i] + '   '
            return the_string

        if not cancel and self.select_list.curselection() and self.select_list:
            index = int(self.select_list.curselection()[0])
            item = self.results[index]
            category = item[-3]
            if category == 'Boots':
                self._boot_selection = item
                self.boot_selection.set(toString(self._boot_selection, category)) #category + ": " + str(item))
            elif category == "Ties":
                self._tie_selection = item
                self.tie_selection.set(toString(self._tie_selection, category))
            elif category == "Clasps":
                self._clasp_selection = item
                self.clasp_selection.set(toString(self._clasp_selection, category))
            else:
                print "something weird is happening!"

            boot_price = 0.00 if self._boot_selection is None else self._boot_selection[6]
            tie_price = 0.00 if self._tie_selection is None else self._tie_selection[6]
            clasp_price = 0.00 if self._clasp_selection is None else self._clasp_selection[6]

            self.price_total.set("Total: $" + str(boot_price + tie_price + clasp_price))

        if self.select_list.curselection() or cancel:
            self.scroll_window.destroy()

    def create_res_window(self, results, table_name):

        self.results = results

        def toString(item):
            the_string = ''
            for i in [1, 2, 3, 4, 8, 6]:
                if i==6:
                    the_string += "$" + str(item[i]) + '   '
                elif i==2:
                    if table_name == 'Tie':
                        the_string += str(item[i]) + '"' + '   '
                    else:
                        the_string += str(item[i]) + '   '
                elif i==8:
                    the_string += item[i] + " (" + item[10] + ", " + item[11] + ")   "
                else:
                    the_string += item[i] + '   '
            return the_string

        self.scroll_window = Toplevel(self.frame)
        self.scroll_window.geometry("%dx%d%+d%+d" % (500, 200, self.frame.winfo_rootx()+10, self.frame.winfo_rooty()))

        inner_window = Frame(self.scroll_window)
        inner_window.pack(fill=BOTH)

        scrollbar = Scrollbar(inner_window, orient=VERTICAL)
        xscrollbar = Scrollbar(inner_window, orient=HORIZONTAL)
        self.select_list = Listbox(inner_window, yscrollcommand=scrollbar.set, xscrollcommand=xscrollbar.set,
                                   font=tkFont.nametofont('TkFixedFont'))
        scrollbar.config( command = self.select_list.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        xscrollbar.config( command = self.select_list.xview)
        xscrollbar.pack(side=BOTTOM, fill=X)
        for item in results:
            self.select_list.insert(END, toString(item))
        self.select_list.pack(side=LEFT, fill=BOTH, expand=1)

        #currently destroy window... need to return/set selection
        Button(self.scroll_window, text="Select", command=self.set_selection).pack(side=LEFT, expand=1)
        Button(self.scroll_window, text="Cancel", command=lambda: self.set_selection(True)).pack(side=RIGHT, expand=1)

    def _create_components(self):

        row = 0
        any = "ALL"
        arrow_image = PhotoImage(file='arrow1.gif')

        Label(self.frame, text="Snootboot Name:  ").grid(row=row, column=0, columnspan=2, sticky=N+S+E)
        self.snootboot_name = Entry(self.frame)
        self.snootboot_name.grid(row=row, column=2, columnspan=2, sticky=N+S+E+W)

        row += 1

        for comp_list in self.FINDER:

            Label(self.frame, text="Find A "+comp_list[-1].title()+": ").grid(row=row, column=0)

            # Input Label for Name
            text = comp_list[0]
            comp_list[0] = Entry(self.frame)
            comp_list[0].insert(0, text.title())
            comp_list[0].grid(row=row, column=1, sticky=N+S+E+W)

            # Dropdowns for Shape, Length, Type
            text = comp_list[1][0]
            options = [list(i)[0] for i in sorted(comp_list[1][1]())]
            options[:0] = [any]
            variable = StringVar(self.frame)
            variable.set(text.title())
            comp_list[1] = apply(OptionMenu, (self.frame, variable) + tuple(options))
            comp_list[1].grid(row=row, column=2, sticky=N+S+E+W)
            # comp_list[1].config(compound='right', image=arrow_image, width=140)
            # comp_list[1].image=arrow_image
            # print comp_list[1]

            # Dropdowns for Material
            text = comp_list[2]
            options = [list(i)[0] for i in sorted(query_library.get_materials(comp_list[-1]))]
            options[:0] = [any]
            variable = StringVar(self.frame)
            variable.set(text.title())
            comp_list[2] = apply(OptionMenu, (self.frame, variable) + tuple(options))
            comp_list[2].grid(row=row, column=3, sticky=N+S+E+W)

            # Dropdowns for Color
            text = comp_list[3]
            options = [list(i)[0] for i in sorted(query_library.get_colors(comp_list[-1]))]
            options[:0] = [any]
            variable = StringVar(self.frame)
            variable.set(text.title())
            comp_list[3] = apply(OptionMenu, (self.frame, variable) + tuple(options))
            comp_list[3].grid(row=row, column=4, sticky=N+S+E+W)

            row += 1

            # Dropdowns for MFG
            text = comp_list[4]
            options = [list(i)[0] for i in sorted(query_library.get_mfgs(comp_list[-1]))]
            options[:0] = [any]
            variable = StringVar(self.frame)
            variable.set(text.title())
            comp_list[4] = apply(OptionMenu, (self.frame, variable) + tuple(options))
            comp_list[4].grid(row=row, column=1, sticky=N+S+E+W)

            # Input Label for Min Price
            text = comp_list[5]
            comp_list[5] = Entry(self.frame)
            comp_list[5].insert(0, text.title())
            comp_list[5].grid(row=row, column=2, sticky=N+S+E+W)

            # Input Label for Max Price
            text = comp_list[6]
            comp_list[6] = Entry(self.frame)
            comp_list[6].insert(0, text.title())
            comp_list[6].grid(row=row, column=3, sticky=N+S+E+W)

            # Find Button
            text = comp_list[7]
            comp_list[7] = Button(self.frame, text=text.title(),
                                  command=lambda name=comp_list[-1].title(),
                                                 clist=comp_list: self.create_res_window(query_library.action(name, clist), name))
            comp_list[7].grid(row=row, column=4, sticky=N+S+E+W)
            row += 1

        Label(self.frame, textvariable=self.boot_selection).grid(row=row, columnspan=10)
        row += 1
        Label(self.frame, textvariable=self.tie_selection).grid(row=row, columnspan=10)
        row += 1
        Label(self.frame, textvariable=self.clasp_selection).grid(row=row, columnspan=10)
        row += 1
        Label(self.frame, textvariable=self.price_total).grid(row=row, columnspan=10)
        row += 1