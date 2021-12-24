from tkinter import *
from objects import *
from generic_widgets import *
from db import create

def generic_refresh(fetched_results, tree):
    copy = []
    for result in fetched_results:
        copy_result = result[0].rstrip()
        carry_list = []
        carry_list.append(copy_result)
        copy.append(carry_list)
    values = tree.get_values()
    if not len(values):
        for result in copy:
            tree.insert_args(result[0])
    else:
        for result in copy:
            if not result in values:
                tree.insert_args(result[0])

class AddModule(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title('Add a Module')
        self.geometry('600x600')

        self.name = InputField(master=self, text="Please enter the name of the module you want to add")
        save = Button(self, text="Add", height=5, background='green',command=self.press)
        save.pack(fill=X, expand=True)
    
    def get_module(self):
        module_name = self.name.get_input()
        module_name = module_name.rstrip()
        module = Module(module_name)
        return module
    def press(self):
        module = self.get_module()
        module.save()
        main_page.refresh()
        self.destroy()

class ModulePage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        dict ={'name': 'Your Modules'}
        self.tree = GenericTree(master=master, dict=dict)
        self.tree.bind("<Double-1>", self.delete)
        buttons = MainButtons(master=master, press = self.press, edit = self.edit, delete=self.delete)
        buttons.pack(side=BOTTOM, fill=X)
    def press(self): 
        AddModule()
    def refresh(self):
        results = Module().refresh()
        generic_refresh(results, self.tree)
    def edit(self):
        item = self.tree.selected_item()
        item = self.tree.get_item(item)
        item = item[0]
        id = Module(name=item).get_id()
        print(id)
        #Give this to the TopLevelPage
    def delete(self):
        item = self.tree.selected_item()
        carry_item = self.tree.get_item(item)
        self.tree.delete(item)
        carry_item = carry_item[0]
        Module(name=carry_item).delete()


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz App")
        self.geometry("900x600")
        create()
        
root = App()
main_page = ModulePage(master=root)
main_page.refresh()
root.mainloop()

"""
#---------------------------------------------------------------------------------------------------------------------------------
class AddAnswer(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title('Add an answer')
        self.geometry('600x600')

        self.description = InputField(master=self, text="Description:")
        self.why_iscorrect = InputField(master=self, text="Why is correct:")
        self.true_or_false = TwoOptionField(master=self, text="Is correct?", side=LEFT)
        
        save = Button(self, text="Add", height=5, background='green',command=self.press)
        save.pack(fill=X, expand=True)

    def get_answer(self):
        description = self.description.get_input()
        why_iscorrect = self.why_iscorrect.get_input()
        is_correct = self.true_or_false.get_input()
        return Answer(description, is_correct, why_iscorrect)

    def press(self):
        answer = self.get_answer()
        question = Question()
        answer.save(question)


dict ={'description': 'Description', 'iscorrect': 'Is correct', 'why_iscorrect':'Why is correct or wrong'}
answers = GenericTree(master=root, dict=dict)
def press(): 
    AddAnswer()
add_button = Button(root, text="Add module", command=press, height=5)
add_button.pack(side=BOTTOM, fill=X)
"""
