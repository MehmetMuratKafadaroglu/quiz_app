from tkinter import *
from objects import *
from generic_widgets import *
from db import create

def generic_refresh(result, tree):
    values = tree.get_values()
    values = change_to_tuple(values)
    if not len(values):
        tree.insert_args(result)
    else:
        if not result in values:
            tree.insert_args(result)

def delete_element(_list, index):
    copy = _list
    first_element = _list[index]
    copy.remove(first_element)       
    return copy 

def replace_element(_list, current_element, desired_element):
    copy = []
    for element in _list:
        if element == current_element:
            copy.append(desired_element)
        else:
            copy.append(element)
    return copy

def change_to_tuple(_list):
    copy = []
    for element in _list:
        copy.append(tuple(element))
    return copy
#******************************************************************************************************************
register_module = None
register_quiz = None
register_question = None
register_answer= None

class AddModule(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title('Add a Module')
        self.geometry('600x600')

        self.name = InputField(master=self, text="Please enter the name of the module you want to add")
        save = Button(self, text="Add", height=5, background='green', command=self.press)
        save.pack(fill=X, expand=True)

    def press(self):
        module_name = self.name.get_input()
        module_name = module_name.rstrip()
        module = Module(name=module_name)
        module.save()
        start_page.refresh()
        self.destroy()


class ModulePage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        heads = {'name': 'Your Modules'}
        self.tree = GenericTree(master=self, dict=heads)
        self.tree.bind("<Double-1>", self.delete)
        self.buttons = MainButtons(self, back=self.back, press=self.add, edit=self.edit, delete=self.delete)
        self.buttons.pack(fill=X, expand=True)
        self.refresh()
    def back(self):
        self.destroy()

    def add(self):
        AddModule()

    def refresh(self):
        results = Module().refresh()
        for result in results:
            generic_refresh(result, self.tree)

    def edit(self):
        item = self.tree.selected_item()
        item = self.tree.get_item(item)
        item = item[0]
        module = Module(name=item)
        global register_module
        register_module = module
        self.pack_forget()
        quiz_page.pack(fill=BOTH, expand=True)
        quiz_page.refresh()

    def delete(self):
        item = self.tree.selected_item()
        carry_item = self.tree.get_item(item)
        self.tree.delete(item)
        carry_item = carry_item[0]
        Module(name=carry_item).delete()

#******************************************************************************************************************
class AddQuiz(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title('Add a Quiz')
        self.geometry('600x600')

        self.name = InputField(master=self, text="Please enter the name of the quiz you want to add")
        self.is_randomized = TwoOptionField(self, "Is the quiz randomized", options=['Randomized', 'Not Randomized'])
        save = Button(self, text="Add", height=5, background='green', command=self.press)
        save.pack(fill=X, expand=True)

    def press(self):
        quiz_name = self.name.get_input()
        quiz_name = quiz_name.rstrip()
        is_randomized = self.is_randomized.get_input()
        
        if is_randomized=="Randomized":
            is_randomized = 1
        else: 
            is_randomized= 0

        quiz = Quiz(name=quiz_name, israndomized=is_randomized)
        quiz.save(register_module)
        quiz_page.refresh()
        self.destroy()

class QuizPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        heads =  {'name':'Quiz name', 'is_randomized': 'Is randomized'}
        self.tree = GenericTree(master=self, dict=heads)
        self.tree.pack()
        self.tree.bind("<Double-1>", self.delete)
        self.buttons = MainButtons(self, back=self.back, press=self.add, edit=self.edit, delete=self.delete)
        self.buttons.pack(fill=X, expand=True)
        self.buttons.pack(side=BOTTOM, fill=X)

    def back(self):
        start_page.pack(fill=BOTH, expand=True)
        self.pack_forget()

    def add(self):
        AddQuiz()

    def refresh(self):
        if register_module is not None:
            module_id = register_module.get_id()
            results = Quiz().refresh(module_id)
            
            for result in results:
                result_in_list = list(result)
                copy = delete_element(result_in_list, 0)
                copy = delete_element(copy, len(copy)-1)

                if copy[1]:
                    desired_element = 'Randomized'
                else:
                    desired_element = 'Not Randomized'

                copy = replace_element(copy, copy[1],desired_element) 
                copy = tuple(copy) 
                generic_refresh(copy, self.tree)                  
        else:  
            print("Do nothing")

    def edit(self):
        item = self.tree.selected_item()
        item = self.tree.get_item(item)
        
        name = item[0]
        if item[1] == 'Randomized':
            status = 1
        else:
            status = 0
        quiz = Quiz(name=name, israndomized=status)

        global register_quiz
        register_quiz = quiz
        self.pack_forget()
        question_page.pack(fill=BOTH, expand=True)
        question_page.refresh()

    def delete(self):
        item = self.tree.selected_item()
        carry_item = self.tree.get_item(item)
        self.tree.delete(item)
        
        if carry_item[1] == "Randomized":
            carry_item = replace_element(carry_item, "Randomized", 1)
        else:
            carry_item = replace_element(carry_item, "Not Randomized", 0)
        Quiz(name=carry_item[0], israndomized=carry_item[1]).delete(register_module)

#******************************************************************************************************************
class AddQuestions(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title('Add a Question')
        self.geometry('600x600')

        self.name = InputField(master=self, text="Please enter the question you want to add")
        save = Button(self, text="Add", height=5, background='green', command=self.press)
        save.pack(fill=X, expand=True)

    def press(self):
        question = self.name.get_input()
        question = question.rstrip()
        
        question = Question(question=question)
        question.save(register_quiz, module_class=register_module)
        question_page.refresh()
        self.destroy()

class QuestionPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        heads =  {'name':'Questions of the Quiz'}
        self.tree = GenericTree(master=self, dict=heads)
        self.tree.pack()
        self.tree.bind("<Double-1>", self.delete)
        self.buttons = MainButtons(self, back=self.back, press=self.add, edit=self.edit, delete=self.delete)
        self.buttons.pack(fill=X, expand=True)
        self.buttons.pack(side=BOTTOM, fill=X)

    def back(self):
        quiz_page.pack(fill=BOTH, expand=True)
        self.pack_forget()

    def add(self):
        AddQuestions()

    def refresh(self):
        if register_quiz is not None:
            quiz_id = register_quiz.get_id(register_module)
            results = Question().refresh(foreign_key=quiz_id)            
            for result in results:
                result_in_list = list(result)
                copy = delete_element(result_in_list, 0)
                copy = delete_element(copy, len(copy)-1)
                copy = tuple(copy) 
                generic_refresh(copy, self.tree)                  
        else:  
            print("Do something")

    def edit(self):
        item = self.tree.selected_item()
        item = self.tree.get_item(item)
        
        question = item[0]
        question = Question(question=question)
        
        global register_question
        register_question = question
        self.pack_forget()
        answer_page.pack(fill=BOTH, expand=True)
        answer_page.refresh()


    def delete(self):
        item = self.tree.selected_item()
        carry_item = self.tree.get_item(item)
        self.tree.delete(item)
        Question(question=carry_item[0]).delete(register_quiz, register_module)

#******************************************************************************************************************
class AddAnswers(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title('Add a Answers')
        self.geometry('600x600')

        self.answer = InputField(master=self, text="Please enter the answer you want to add")
        self.iscorrect = TwoOptionField(master=self, text="Is this answer is true or false")
        self.why_iscorrect = InputField(master=self, text="Why this answer is correct or wrong")
        save = Button(self, text="Add", height=5, background='green', command=self.press)
        save.pack(fill=X, expand=True)

    def press(self):
        answer = self.answer.get_input()
        answer = answer.rstrip()
        
        why_iscorrect = self.why_iscorrect.get_input()
        why_iscorrect = why_iscorrect.rstrip()
        
        is_correct = self.iscorrect.get_input()
        if bool(is_correct):
            is_correct = 1
        else:
            is_correct = 0

        answer = Answer(description=answer, iscorrect=is_correct, why_iscorrect=why_iscorrect)
        answer.save(register_question, register_quiz, register_module)

        answer_page.refresh()
        self.destroy()

class AnswerPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        heads =  {'name':'Answers of the question', 'iscorrect': "Is this question correct", 'why_iscorrect': "If it is correct why it is" }
        self.tree = GenericTree(master=self, dict=heads)
        self.tree.pack()
        self.tree.bind("<Double-1>", self.delete)
        self.buttons = MainButtons(self, back=self.back, press=self.add, edit=self.edit, delete=self.delete)
        self.buttons.pack(fill=X, expand=True)
        self.buttons.pack(side=BOTTOM, fill=X)

    def back(self):
        question_page.pack(fill=BOTH, expand=True)
        self.pack_forget()

    def add(self):
        AddAnswers()

    def refresh(self):
        if register_question is not None:
            results = Answer().refresh(register_question, register_quiz, register_module)            
            for result in results:
                result_in_list = list(result)
                copy = delete_element(result_in_list, 0)
                copy = delete_element(copy, len(copy)-1)
                copy = tuple(copy) 
                generic_refresh(copy, self.tree)                  
        else:  
            print("Do nothing")

    def edit(self):
        item = self.tree.selected_item()
        item = self.tree.get_item(item)
        #Do things in here

    def delete(self):
        item = self.tree.selected_item()
        carry_item = self.tree.get_item(item)
        self.tree.delete(item)
        Answer(description=carry_item[0], iscorrect=carry_item[1], why_iscorrect=carry_item[2]).delete(
            register_question,register_quiz, register_module)

#******************************************************************************************************************
class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz App")
        self.geometry("900x600")
        create()


root = App()
start_page = ModulePage(master=root)
start_page.pack(fill=BOTH, expand=True)
quiz_page = QuizPage(master=root)
question_page = QuestionPage(master=root)
answer_page=  AnswerPage(master=root)
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
