from tkinter import *
from tkinter.ttk import Combobox, Treeview

class InputField(Frame):
    def __init__(self, master, text, side=TOP):
        Frame.__init__(self, master)        
        self.master = master
        self.text = text
        self.side = side
        Label(self, text=self.text).pack(side=self.side)
        
        self.txt =Text(self, height=8)
        self.txt.pack(side=BOTTOM, fill=X, expand=TRUE, padx=20, pady=20)
        self.pack(fill=X, expand=TRUE)
    def get_input(self):
        return self.txt.get("1.0",'end')

    def get_text(self):
        return self.text
    
    def get_side(self):
        return self.side

    def set_text(self, text):
        self.text = text

    def set_side(self, side):
        self.side=side

class TwoOptionField(Frame):
    def __init__(self, master, text, side=TOP):
        Frame.__init__(self, master)
        self.master = master
        Label(self, text=text).pack(side=side)
        self.option= Combobox(self, values=['True', 'False']).pack(side=RIGHT, fill=X, expand=TRUE, padx=20, pady=20)
        self.pack(fill=X, expand=TRUE)
    def get_input(self):
        return self.option.get()

class GenericTree(Frame):
    def __init__(self, master, dict):
        Frame.__init__(self, master)
        self.master = master
        keys = dict.keys()
        self.columns = list(keys)
        self.tree = Treeview(master, columns=self.columns,  show="headings", height=25)
        for key in keys:   
            self.tree.heading(key, text=dict[key], anchor=CENTER)
        self.tree.pack(fill=X)

    def get_values(self):
        values = []
        ids = self.tree.get_children()
        for id in ids:
            values.append(self.get_item(id))
        return values

    def selected_item(self):
        selected_item = self.tree.selection()[0]
        return selected_item

    def get_item(self, id):
        return self.tree.item(id)['values']
    
    def insert_args(self, *args):        
        args = tuple(args)
        self.tree.insert('', END, values=args)

    def delete(self, item):
        self.tree.delete(item)

class MainButtons(Frame):
    def __init__(self, master, press, edit, delete):
        Frame.__init__(self, master)
        self.master = master

        add_button = Button(self, text="Add module", command=press, height=5, width=41)
        add_button.grid(row=0, column=0)

        refresh_button = Button(self, text="Edit", command=edit, height=5, width=41)
        refresh_button.grid(row=0, column=1)
        
        delete_button = Button(self, text="Delete", command=delete, height=5, width=41)
        delete_button.grid(row=0, column=2)
