from tkinter import *
from tkinter.ttk import Combobox, Treeview

#This is InputField class. This class gives label and text together.
class InputField(Frame):
    def __init__(self, master, text, side=TOP):
        Frame.__init__(self, master)        
        self.master = master
        self.text = text
        self.side = side
        Label(self, text=self.text).pack(side=self.side)
        
        self.txt =Text(self, height=8)
        if side == TOP:
            txt_side = BOTTOM
        else :
            txt_side = TOP

        self.txt.pack(side=txt_side, fill=X, expand=TRUE, padx=20, pady=20)
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

#This class is made to give user two options. Options can be true and false or randomized and not randomized or etc
class TwoOptionField(Frame):
    def __init__(self, master, text, side=TOP, options=['True', 'False']):
        Frame.__init__(self, master)
        self.master = master
        Label(self, text=text).pack(side=side)
        self.option= Combobox(self, values=options)
        self.option.pack(side=RIGHT, fill=X, expand=TRUE, padx=20, pady=20)
        self.pack(fill=X, expand=TRUE)
    def get_input(self):
        return self.option.get()

#This is a generic treeview that shows our objects
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
    
    def insert_args(self, values): 
        self.tree.insert('', END, values=values)

    def delete(self, item):
        self.tree.delete(item)

    def delete_everything(self):
        ids = self.tree.get_children()
        for id in ids:
            self.delete(id)
            
#This widgets are four main buttons that is used in most pages
class MainButtons(Frame):
    def __init__(self, master, back ,press, delete, update):
        Frame.__init__(self, master)
        self.master = master

        self.back_button = Button(self, text="Back", command=back, height=5, width=30)
        self.back_button.grid(row=0, column=0)

        self.add_button = Button(self, text="Add", command=press, height=5, width=30)
        self.add_button.grid(row=0, column=1)
        
        self.delete_button = Button(self, text="Delete", command=delete, height=5, width=30)
        self.delete_button.grid(row=0, column=2)

        self.update_button = Button(self, text="Update", command=update, height=5, width=30)
        self.update_button.grid(row=0, column=3)

class EditMainButtons(Frame):
    def __init__(self, master, back ,press, delete, edit, update):
        Frame.__init__(self, master)
        self.master = master

        self.back_button = Button(self, text="Back", command=back, height=5, width=24)
        self.back_button.grid(row=0, column=0)

        self.add_button = Button(self, text="Add", command=press, height=5, width=24)
        self.add_button.grid(row=0, column=1)
        
        self.delete_button = Button(self, text="Delete", command=delete, height=5, width=24)
        self.delete_button.grid(row=0, column=2)

        self.update_button = Button(self, text="Update", command=update, height=5, width=24)
        self.update_button.grid(row=0, column=3)

        self.refresh_button = Button(self, text="Edit", command=edit, height=5, width=24)
        self.refresh_button.grid(row=0, column=4)
