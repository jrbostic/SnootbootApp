"""
Provides GUI functionality to navigate database, save completed snootboots,
and delete snootboots.  Also displays information about available choices (based
on db contents) and tracks components of current boot with its total price.
"""

from Tkinter import *
import query_library
import tkFont

__author__ = 'jesse bostic'
__author__ = 'nick ames'


class SnootbootGUI:
    """The GUI for exploring and otherwise interacting with snootboot database."""

    # initially holds values related to buttons text or function
    #  but later becomes the container for component references
    FINDER = (['name', ('shape', query_library.get_boot_shapes), 'material', 'color', 'manufacturer', 'min price',
               'max price', 'find', 'boot'],  # boot
              ['name', ('length', query_library.get_tie_lengths), 'material', 'color', 'manufacturer', 'min price',
               'max price', 'find', 'tie'],  # tie
              ['name', ('type', query_library.get_clasp_types), 'material', 'color', 'manufacturer', 'min price',
               'max price', 'find', 'clasp'])  # clasp

    VAR_LIST = []

    def __init__(self):
        """Initializes a new GUI instance."""

        self.root = Tk()
        self.root.resizable(0, 0)

        self.root.title("Custom Snootboot Marketplace")
        self.root['bg'] = '#656565'
        self.frame = Frame(self.root, padx=10, pady=15)

        # key objects for selection
        self.results = None
        self.scroll_window = None
        self. select_list = None

        # currently selected items
        self._boot_selection = None
        self._tie_selection = None
        self._clasp_selection = None

        # variables associated with display (auto repaint)
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
        """Sets user selection and main string reps in instance.
        As a side effect, closes toplevel selection window.

        :param cancel: whether the action was cancelled
        :return: None
        """

        def toString(item, cat):
            """Returns an appropriate string rep for display.

            :param item: item to represent
            :param cat: category of item
            :return: formatted string
            """

            the_string = ''
            for i in [1, 2, 3, 4, 8, 6]:
                if i == 6:
                    the_string += "$" + "%.2f" % item[i] + '   '
                elif i == 2:
                    if cat == 'Ties':
                        the_string += str(item[i]) + '"' + '   '
                    else:
                        the_string += str(item[i]) + '   '
                elif i == 8:
                    the_string += item[i] + " (" + item[10] + ", " + item[11] + ")   "
                else:
                    the_string += item[i] + '   '

            return the_string

        # only execute if there was a selection and action not cancelled
        if not cancel and self.select_list.curselection() and self.select_list:
            index = int(self.select_list.curselection()[0])
            item = self.results[index]
            category = item[-3]
            if category == 'Boots':
                self._boot_selection = item
                self.boot_selection.set(toString(self._boot_selection, category))
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

            self.price_total.set("Total: $" + "%.2f" % (boot_price + tie_price + clasp_price))

        # only close if valid selection or cancelled
        if self.select_list.curselection() or cancel:
            self.scroll_window.destroy()

    def create_res_window(self, results, table_name):
        """Creates a window to navigate and select item results of query.
        As side effect, uses set_selection function to resolve selection events.

        :param results: the results to display
        :param table_name: the name of the table being queried
        :return: None
        """

        self.results = results

        def to_string(item):
            """Returns an appropriate string reps for results display.

            :param item: item to represent
            :return: formatted string
            """
            the_string = ''
            for i in [1, 2, 3, 4, 8, 6]:
                if i == 6:
                    the_string += "$" + "%.2f" % item[i] + '   '
                elif i == 2:
                    if table_name == 'Tie':
                        the_string += str(item[i]) + '"' + '   '
                    else:
                        the_string += str(item[i]) + '   '
                elif i == 8:
                    the_string += item[i] + " (" + item[10] + ", " + item[11] + ")   "
                else:
                    the_string += item[i] + '   '
            return the_string

        # setup toplevel display
        self.scroll_window = Toplevel(self.frame)
        self.scroll_window.geometry("%dx%d%+d%+d" % (500, 200, self.frame.winfo_rootx()+10, self.frame.winfo_rooty()))

        inner_window = Frame(self.scroll_window)
        inner_window.pack(fill=BOTH)

        # setup horizontal and vertical scrollbars
        scrollbar = Scrollbar(inner_window, orient=VERTICAL)
        xscrollbar = Scrollbar(inner_window, orient=HORIZONTAL)
        self.select_list = Listbox(inner_window, yscrollcommand=scrollbar.set, xscrollcommand=xscrollbar.set,
                                   font=tkFont.nametofont('TkFixedFont'))
        scrollbar.config( command = self.select_list.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        xscrollbar.config( command = self.select_list.xview)
        xscrollbar.pack(side=BOTTOM, fill=X)

        # insert string reps of result items
        for item in results:
            self.select_list.insert(END, to_string(item))
        self.select_list.pack(side=LEFT, fill=BOTH, expand=1)

        #currently destroy window... need to return/set selection
        Button(self.scroll_window, text="Select", command=self.set_selection).pack(side=LEFT, expand=1)
        Button(self.scroll_window, text="Cancel", command=lambda: self.set_selection(True)).pack(side=RIGHT, expand=1)

    def create_snoot_window(self):
        """Creates display window for navigating/deleting saved snootboots.

        :return: None
        """

        def delete_selection(select_list):
            """Deletes selected item from list"""

            if select_list.curselection():
                query_library.del_snoot(select_list.get(select_list.curselection())[0])
                select_list.delete(select_list.curselection())

        # setup window and scrollbars
        snoot_win = Toplevel(self.frame)
        snoot_win.geometry("%dx%d%+d%+d" % (500, 200, self.frame.winfo_rootx()+10, self.frame.winfo_rooty()))

        inner_window = Frame(snoot_win)
        inner_window.pack(fill=BOTH)

        scrollbar = Scrollbar(inner_window, orient=VERTICAL)
        xscrollbar = Scrollbar(inner_window, orient=HORIZONTAL)
        select_list = Listbox(inner_window, yscrollcommand=scrollbar.set, xscrollcommand=xscrollbar.set,
                              font=tkFont.nametofont('TkFixedFont'))
        scrollbar.config( command=select_list.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        xscrollbar.config( command=select_list.xview)
        xscrollbar.pack(side=BOTTOM, fill=X)

        # insert string reps of saved snootboots
        results = query_library.get_snoots()
        for item in results:
            select_list.insert(END, item)
        select_list.pack(side=LEFT, fill=BOTH, expand=1)

        Button(snoot_win, text="Delete", command=lambda sel=select_list: delete_selection(sel)).pack(side=LEFT,
                                                                                                     expand=1)
        Button(snoot_win, text="Done", command=snoot_win.destroy).pack(side=RIGHT, expand=1)

    def reset_components(self):
        """Resets GUI components and selections stored in object state.

        :return: None
        """

        adjust = 0

        # reset components
        for category in self.FINDER:

            category[0].delete(0, END)
            category[0].insert(0, "Name")
            if category[-1] == 'boot':
                self.VAR_LIST[adjust].set("Shape")
            elif category[-1] == 'tie':
                self.VAR_LIST[adjust].set("Length")
            elif category[-1] == 'clasp':
                self.VAR_LIST[adjust].set("Type")
            self.VAR_LIST[adjust+1].set("Material")
            self.VAR_LIST[adjust+2].set("Color")
            self.VAR_LIST[adjust+3].set("Manufacturer")
            category[5].delete(0, END)
            category[5].insert(0, "Min Price")
            category[6].delete(0, END)
            category[6].insert(0, "Max Price")

            adjust += 4

        # reset other state members
        self.snootboot_name.delete(0, END)
        self._boot_selection = None
        self._tie_selection = None
        self._clasp_selection = None
        self.boot_selection.set("Boot: None Selected")
        self.tie_selection.set("Tie: None Selected")
        self.clasp_selection.set("Clasp: None Selected")
        self.price_total.set("Total: $0.00")

    def save_boot(self):
        """Saves snootboot entry into main table and resets components.
        Otherwise notifies user of incomplete snootboot selection.

        :return: None
        """

        if self._boot_selection is not None \
                and self._tie_selection is not None \
                and self._clasp_selection is not None:

            boot_price = 0.00 if self._boot_selection is None else self._boot_selection[6]
            tie_price = 0.00 if self._tie_selection is None else self._tie_selection[6]
            clasp_price = 0.00 if self._clasp_selection is None else self._clasp_selection[6]
            total = boot_price+tie_price+clasp_price
            query_library.insert_snoot((self.snootboot_name.get(), self._boot_selection[0],
                                       self._tie_selection[0], self._clasp_selection[0], total))
            self.reset_components()
        else:

            error_box = Toplevel(self.frame)
            error_box.title("Snoot Not Complete")
            error_box.geometry("%dx%d%+d%+d" % (200, 100, self.frame.winfo_rootx()+75, self.frame.winfo_rooty()+10))
            Message(error_box, text="Whooops! You haven't completed your Snootboot!").pack()
            Button(error_box, text="Ok", command=error_box.destroy).pack()

    def _create_components(self):
        """This is the beast that creates and populates components.

        :return: None
        """

        # maintains grid location of components
        row = 0

        # string representing no filter on attribute
        any_att = "ALL"

        # snootboot name entry widget and label
        Label(self.frame, text="Snootboot Name:  ").grid(row=row, column=0, columnspan=2, sticky=N+S+E)
        self.snootboot_name = Entry(self.frame)
        self.snootboot_name.grid(row=row, column=2, columnspan=2, sticky=N+S+E+W)

        row += 1

        # loops through each list of parameters to create components
        #  then stores components back in FINDER at index of parameters
        for comp_list in self.FINDER:

            Label(self.frame, text="Find A "+comp_list[-1].title()+": ").grid(row=row, column=0)

            # Input box for Name
            text = comp_list[0]
            comp_list[0] = Entry(self.frame)
            comp_list[0].insert(0, text.title())
            comp_list[0].grid(row=row, column=1, sticky=N+S+E+W)

            # Dropdowns for Shape, Length, Type
            text = comp_list[1][0]
            options = [i[0] for i in sorted(comp_list[1][1]())]
            options[:0] = [any_att]
            variable = StringVar(self.frame)
            variable.set(text.title())
            self.VAR_LIST.append(variable)
            comp_list[1] = apply(OptionMenu, (self.frame, variable) + tuple(options))
            comp_list[1].grid(row=row, column=2, sticky=N+S+E+W)

            # Dropdowns for Material
            text = comp_list[2]
            options = [i[0] for i in sorted(query_library.get_materials(comp_list[-1]))]
            options[:0] = [any_att]
            variable = StringVar(self.frame)
            variable.set(text.title())
            self.VAR_LIST.append(variable)
            comp_list[2] = apply(OptionMenu, (self.frame, variable) + tuple(options))
            comp_list[2].grid(row=row, column=3, sticky=N+S+E+W)

            # Dropdowns for Color
            text = comp_list[3]
            options = [i[0] for i in sorted(query_library.get_colors(comp_list[-1]))]
            options[:0] = [any_att]
            variable = StringVar(self.frame)
            variable.set(text.title())
            self.VAR_LIST.append(variable)
            comp_list[3] = apply(OptionMenu, (self.frame, variable) + tuple(options))
            comp_list[3].grid(row=row, column=4, sticky=N+S+E+W)

            row += 1

            # Dropdowns for MFG
            text = comp_list[4]
            options = [i[0] for i in sorted(query_library.get_mfgs(comp_list[-1]))]
            options[:0] = [any_att]
            variable = StringVar(self.frame)
            variable.set(text.title())
            self.VAR_LIST.append(variable)
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
            comp_list[7] = Button(self.frame, text=text.title(), command=lambda name=comp_list[-1].title(),
                                  clist=comp_list: self.create_res_window(query_library.action(name, clist), name))
            comp_list[7].grid(row=row, column=4, sticky=N+S+E+W)
            row += 1

        # labels for displaying snootboot selection data
        Label(self.frame, textvariable=self.boot_selection).grid(row=row, columnspan=10)
        row += 1
        Label(self.frame, textvariable=self.tie_selection).grid(row=row, columnspan=10)
        row += 1
        Label(self.frame, textvariable=self.clasp_selection).grid(row=row, columnspan=10)
        row += 1
        Label(self.frame, textvariable=self.price_total).grid(row=row, columnspan=10)
        row += 1

        Button(self.frame, text="New Boot", command=self.reset_components).grid(row=row, column=1, sticky=E)
        Button(self.frame, text="View My Boots", command=self.create_snoot_window).grid(row=row, column=2)
        Button(self.frame, text="Save Boot", command=self.save_boot).grid(row=row, column=3, sticky=W)
