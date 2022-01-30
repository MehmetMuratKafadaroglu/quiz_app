from re import T
from tkinter import *
from tkinter.ttk import Combobox, Treeview
"""
Made by 001143514
Generic widgets gives generic widgets and functions to main file.
This file exist to decrease the duplication in main file.
This file should not communicate with database/objects this file should only communicate with the main file
"""

def generic_refresh(values, tree):
    """
    Delete everything and do a query and insert them over again
    """
    tree.delete_everything()
    for value in values:
        arg = list(value)
        tree.insert_args(arg)

def delete_element(_list, index):
    copy = _list
    element = _list[index]
    copy.remove(element)
    return copy

def replace_elements(_list, current_element, desired_element):
    copy = []
    for element in _list:
        if element == current_element:
            copy.append(desired_element)
        else:
            copy.append(element)
    return copy

def del_first_and_last(_list):
    _list = _list[:-1]
    _list = _list[1:]
    return _list

# This is InputField class. This class gives label and text together.
class InputField(Frame):
    def __init__(self, master, text, side=TOP):
        Frame.__init__(self, master)
        self.master = master
        self.text = text
        self.side = side
        Label(self, text=self.text).pack(side=self.side)

        self.txt = Text(self, height=8)
        if side == TOP:
            txt_side = BOTTOM
        else:
            txt_side = TOP

        self.txt.pack(side=txt_side, fill=X, expand=TRUE, padx=20, pady=20)
        self.pack(fill=X, expand=TRUE)

    def get_input(self):
        return self.txt.get("1.0", 'end')

    def get_text(self):
        return self.text

    def get_side(self):
        return self.side

    def set_text(self, text):
        self.text = text

    def set_side(self, side):
        self.side = side


# This class is made to give user two options. Options can be true and false or randomized and not randomized or etc
class OptionField(Frame):
    def __init__(self, master, text, side=TOP, options=['True', 'False']):
        Frame.__init__(self, master)
        self.master = master
        Label(self, text=text).pack(side=side)
        self.option = Combobox(self, values=options)
        self.option.pack(side=RIGHT, fill=X, expand=TRUE, padx=20, pady=20)
        self.pack(fill=X, expand=TRUE)

    def get_input(self):
        return self.option.get()


# This is a generic treeview that shows our objects
class GenericTree(Frame):
    def __init__(self, master, dict):
        Frame.__init__(self, master)
        self.master = master
        keys = dict.keys()
        self.columns = list(keys)
        self.tree = Treeview(master, columns=self.columns, show="headings", height=25)
        for key in keys:
            self.tree.heading(key, text=dict[key], anchor=CENTER)
        self.tree.pack(fill=X)

    def get_values(self):
        values = []
        ids = self.tree.get_children()
        for pk in ids:
            values.append(self.get_item(pk))
        return values

    def selected_item(self):
        try:
            selected_item = self.tree.selection()[0]
            return selected_item
        except:
            print("User did not choose anything this is not an error")
            return None

    def get_item(self, pk):
        return self.tree.item(pk)['values']

    def insert_args(self, values):
        self.tree.insert('', END, values=values)

    def delete(self, item):
        self.tree.delete(item)

    def delete_everything(self):
        ids = self.tree.get_children()
        for pk in ids:
            self.delete(pk)

class EditMainButtons(Frame):
    def __init__(self, master, back, press, delete, edit, update, txt="Edit"):
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

        self.edit_button = Button(self, text=txt, command=edit, height=5, width=24)
        self.edit_button.grid(row=0, column=4)
        

class TakeQuizButtons(Frame):
    def __init__(self, master, back, take, txt=None):
        Frame.__init__(self, master)
        self.master = master
        self.back_button = Button(self, text="Back", command=back, height=5, width=60)
        self.back_button.grid(row=0, column=0)
        if txt is None:
            txt = 'Take'
        self.take_button = Button(self, text=txt, command=take, height=5, width=60)
        self.take_button.grid(row=0, column=1)

class ResultsPageButtons(Frame):
    def __init__(self, master, back, delete, get_report):
        Frame.__init__(self, master)
        self.master = master
        self.back_button = Button(self, text="Back", command=back, height=5, width=40)
        self.back_button.grid(row=0, column=0)

        self.delete_button= Button(self, text="Clear Results", command=delete, height=5, width=40)
        self.delete_button.grid(row=0, column=1)

        self.get_rep_button = Button(self, text="Get Report", command=get_report, height=5, width=40)
        self.get_rep_button.grid(row=0, column=2)

class RaiseMessage(Toplevel):
    def __init__(self, message):
        Toplevel.__init__(self)
        self.message = message
        self.display = Label(self, text=message)
        self.display.pack(fill=BOTH, expand=1)
        self.geometry('400x50')


class AnswersAndLabel(Frame):
    def __init__(self, master, question):
        Frame.__init__(self, master)
        self.master = master
        self.answers = question.answers
        length = len(self.answers)
        button_width = 120 / length
        button_width = int(button_width)

        Label(self, text=question.question, height=8, relief='solid', width=100).grid(row=0, column=0, pady=10)
        for i in range(length):
            answer = self.answers[i]
            AnswerButton(self, answer, button_width).grid(row=i + 1, column=0, pady=10)
        self.master.adjust_height(i + 1)

    def next(self, status, why_iscorrect):
        self.master.next_question(status, why_iscorrect)


class AnswerButton(Frame):
    def __init__(self, master, answer, btn_width):
        Frame.__init__(self, master)
        self.master = master
        self.status = answer.iscorrect
        self.description = answer.description
        self.why_iscorrect = answer.why_iscorrect
        self.btn = Button(self, text=self.description, width=btn_width, command=self.press, height=5)
        self.btn.pack(fill=BOTH, expand=1)

    def press(self):
        self.master.next(self.status, self.why_iscorrect)


class Results(Frame):
    def __init__(self, master, results, why_iscorrect):
        Frame.__init__(self, master)
        self.results = results
        self.why_iscorrect = why_iscorrect
        self.final_result = 0
        self.labels = []
        number_of_question = len(self.results)
        for i in range(number_of_question):
            result = self.results[i]
            self.final_result += result
            if result:
                result = 'Correct '
            else:
                result = 'Not Correct'
            result += '\nExplanation: ' + self.why_iscorrect[i]
            txt = "%s. Question is: %s" % (i + 1, result)
            carry_label = Label(self, text=txt, height=3)
            self.labels.append(carry_label)
        txt = "Your final result is %s / %s" % (self.final_result, number_of_question)

        Label(self, text=txt, height=8, relief='solid').pack(fill=X, expand=True)
        Button(self, text="Exit", command=self.exit, height=5).pack(fill=X, expand=True)
        for label in self.labels:
            label.pack(fill=X, expand=1)

    def exit(self):
        self.master.exit()


