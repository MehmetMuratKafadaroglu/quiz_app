from tkinter import *
from objects import *
from generic_widgets import *
from db import *

register_module = None
register_quiz = None
register_question = None
register_answer = None


class UpdateAddModule(Toplevel):
    def __init__(self, title, item=None):
        Toplevel.__init__(self)
        self.title(title)
        self.geometry('600x600')

        self.item = item

        if self.item is None:
            txt = "add"
        else:
            txt = "update"
        self.name = InputField(master=self, text="Please enter the name of the module you want to %s" % txt)
        save = Button(self, text=txt.upper(), height=5, background='green', command=self.press)
        save.pack(fill=X, expand=True)

    def press(self):
        if self.item is None:
            module_name = self.name.get_input()
            module_name = module_name.rstrip()
            module = Module(name=module_name)
            module.save()
        else:
            item = self.item[0]
            module_name = self.name.get_input()
            module_name = module_name.rstrip()
            module_id = Module(name=item).get_id()
            module = Module(name=module_name).update(pk=module_id)

        start_page.refresh()
        self.destroy()


class ModulePage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        heads = {'name': 'Your Modules'}
        self.tree = GenericTree(master=self, dict=heads)
        self.tree.bind("<Double-1>", self.delete)
        self.buttons = EditMainButtons(self, back=self.back, press=self.add, edit=self.edit, delete=self.delete,
                                       update=self.update, txt="Edit quizes of this module")
        self.buttons.pack(fill=X, expand=True)
        self.refresh()

    def back(self):
        self.destroy()

    def add(self):
        title = "Add a module"
        UpdateAddModule(title)

    def update(self):
        title = "Update module"
        item = self.tree.selected_item()
        item = self.tree.get_item(item)
        UpdateAddModule(title, item)

    def refresh(self):
        tree = self.tree
        values = Module().refresh()
        generic_refresh(values, tree)

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


# ******************************************************************************************************************
class UpdateAddQuiz(Toplevel):
    def __init__(self, is_add=True):
        Toplevel.__init__(self)
        self.is_add = is_add
        self.geometry('600x600')
        if self.is_add:
            txt = "add"
            title = "Add Quiz"
        else:
            txt = "update"
            title = "Update Quiz"
        self.title(title)

        self.name = InputField(master=self, text="Please enter the name of the quiz you want to %s" % txt)
        self.is_randomized = TwoOptionField(self, "Is the quiz randomized", options=['Randomized', 'Not Randomized'])
        save = Button(self, text=txt.upper(), height=5, background='green', command=self.press)
        save.pack(fill=X, expand=True)

    def press(self):
        quiz_name = self.name.get_input()
        quiz_name = quiz_name.rstrip()
        is_randomized = self.is_randomized.get_input()

        if is_randomized == "Randomized":
            is_randomized = 1
        else:
            is_randomized = 0

        quiz = Quiz(name=quiz_name, israndomized=is_randomized)
        if self.is_add:
            quiz.save(register_module)
        else:
            quiz.update(register_module, register_quiz)
        quiz_page.refresh()
        self.destroy()

class QuizPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        heads = {'name': 'Quiz name', 'is_randomized': 'Is randomized'}
        self.tree = GenericTree(master=self, dict=heads)
        self.tree.pack()
        self.tree.bind("<Double-1>", self.delete)
        self.buttons = EditMainButtons(self, back=self.back, press=self.add, edit=self.edit, delete=self.delete,
                                       update=self.update, txt="Edit questions of this quiz")
        self.buttons.pack(fill=X, expand=True)
        self.buttons.pack(side=BOTTOM, fill=X)

    def back(self):
        start_page.pack(fill=BOTH, expand=True)
        self.pack_forget()

    def add(self):
        UpdateAddQuiz(is_add=True)

    def get_selected_quiz(self):
        item = self.tree.selected_item()
        item = self.tree.get_item(item)
        name = item[0]
        if item[1] == 'Randomized':
            status = 1
        else:
            status = 0
        quiz = Quiz(name=name, israndomized=status)
        return quiz

    def update(self):
        quiz = self.get_selected_quiz()
        global register_quiz
        register_quiz = quiz
        UpdateAddQuiz(is_add=False)

    def refresh(self):
        if register_module is not None:
            module_id = register_module.get_id()
            results = Quiz().refresh(module_id)
            values = []
            for result in results:
                result_in_list = list(result)
                copy = del_first_and_last(result_in_list)
                if copy[1]:
                    desired_element = 'Randomized'
                else:
                    desired_element = 'Not Randomized'

                copy = replace_element(copy, copy[1], desired_element)
                copy = list(copy)
                values.append(copy)
            generic_refresh(values, self.tree)
        else:
            print("Do nothing")

    def edit(self):
        item = self.tree.selected_item()
        item = self.tree.get_item(item)

        quiz = self.get_selected_quiz()
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


# ******************************************************************************************************************
class UpdateAddQuestions(Toplevel):
    def __init__(self, is_add=True):
        Toplevel.__init__(self)
        self.is_add = is_add
        self.geometry('600x600')
        if self.is_add:
            txt = "add"
            title = "Add Question"
        else:
            txt = "update"
            title = "Update Question"
        self.title(title)

        self.name = InputField(master=self, text="Please enter the question you want to %s" % txt)
        save = Button(self, text=txt.upper(), height=5, background='green', command=self.press)
        save.pack(fill=X, expand=True)

    def press(self):
        question = self.name.get_input()
        question = question.rstrip()
        question = Question(question=question)

        if self.is_add:
            question.save(register_quiz, module_class=register_module)
        else:
            question.update(register_quiz, register_module, register_question)
        question_page.refresh()
        self.destroy()


class QuestionPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        heads = {'name': 'Questions of the Quiz'}
        self.tree = GenericTree(master=self, dict=heads)
        self.tree.pack()
        self.tree.bind("<Double-1>", self.delete)
        self.buttons = EditMainButtons(self, back=self.back, press=self.add, edit=self.edit, delete=self.delete,
                                       update=self.update, txt="Edit answers of this question")
        self.buttons.pack(fill=X, expand=True)
        self.buttons.pack(side=BOTTOM, fill=X)

    def back(self):
        quiz_page.pack(fill=BOTH, expand=True)
        self.pack_forget()

    def get_selected_question(self):
        item = self.tree.selected_item()
        item = self.tree.get_item(item)

        question = item[0]
        question = Question(question=question)
        return question

    def add(self):
        UpdateAddQuestions(True)

    def update(self):
        question = self.get_selected_question()
        global register_question
        register_question = question
        UpdateAddQuestions(False)

    def refresh(self):
        if register_quiz is not None:
            quiz_id = register_quiz.get_id(register_module)
            results = Question().refresh(foreign_key=quiz_id)
            values = []
            for result in results:
                result_in_list = list(result)
                copy = del_first_and_last(result_in_list)
                copy = list(copy)
                values.append(copy)  
            generic_refresh(values, self.tree)
        else:
            print("Do something")

    def edit(self):
        question = self.get_selected_question()
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


# ******************************************************************************************************************
class UpdateAddAnswers(Toplevel):
    def __init__(self, is_add=True):
        Toplevel.__init__(self)
        self.is_add = is_add
        self.geometry('600x600')
        if self.is_add:
            txt = "add"
            title = "Add Question"
        else:
            txt = "update"
            title = "Update Question"
        self.title(title)

        self.answer = InputField(master=self, text="Please enter the answer you want to %s" % txt)
        self.iscorrect = TwoOptionField(master=self, text="Is this answer is true or false")
        self.why_iscorrect = InputField(master=self, text="Why this answer is correct or wrong")
        save = Button(self, text=txt.upper(), height=5, background='green', command=self.press)
        save.pack(fill=X, expand=True)

    def press(self):
        description = self.answer.get_input()
        description = description.rstrip()

        why_iscorrect = self.why_iscorrect.get_input()
        why_iscorrect = why_iscorrect.rstrip()

        is_correct = self.iscorrect.get_input()
        if bool(is_correct):
            is_correct = 1
        else:
            is_correct = 0
        answer = Answer(description, is_correct, why_iscorrect)

        if self.is_add:
            answer.save(register_question, register_quiz, register_module)
        else:
            answer.update(register_question, register_quiz, register_module, register_answer)
        answer_page.refresh()
        self.destroy()


class AnswerPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        heads = {'name': 'Answers of the question', 'iscorrect': "Is this question true",
                 'why_iscorrect': "If it is true why it is"}
        self.tree = GenericTree(master=self, dict=heads)
        self.tree.pack()
        self.tree.bind("<Double-1>", self.delete)
        self.buttons = MainButtons(self, back=self.back, press=self.add, update=self.update, delete=self.delete)
        self.buttons.pack(fill=X, expand=True)
        self.buttons.pack(side=BOTTOM, fill=X)

    def back(self):
        question_page.pack(fill=BOTH, expand=True)
        self.pack_forget()

    def add(self):
        UpdateAddAnswers(True)

    def update(self):
        answer = self.get_selected_answer()
        global register_answer
        register_answer = answer
        UpdateAddAnswers(False)

    def get_selected_answer(self):
        item = self.tree.selected_item()
        item = self.tree.get_item(item)

        description = item[0]
        iscorrect = item[1]
        why_iscorrect = item[2]

        if bool(iscorrect):
            iscorrect =1 
        else:
            iscorrect = 0
        answer = Answer(description=description, iscorrect=iscorrect, why_iscorrect=why_iscorrect)
        return answer

    def refresh(self):
        if register_question is not None:
            results = Answer().refresh(register_question, register_quiz, register_module)
            values = []
            for result in results:
                result_in_list = list(result)
                copy = del_first_and_last(result_in_list)
                if copy[1]:
                    copy = replace_element(copy, copy[1], "True")
                else:
                    copy = replace_element(copy, copy[1], "False")
                values.append(copy)
            generic_refresh(values, self.tree)
        else:
            print("Do nothing")

    def delete(self):
        item = self.tree.selected_item()
        carry_item = self.tree.get_item(item)
        self.tree.delete(item)

        description =carry_item[0]
        iscorrect=carry_item[1]
        why_iscorrect=carry_item[2]

        if bool(iscorrect):
            iscorrect = 1
        else:
            iscorrect=0
        
        answer = Answer(description, iscorrect, why_iscorrect)
        answer.delete(register_question, register_quiz, register_module)


# ******************************************************************************************************************
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
answer_page = AnswerPage(master=root)
root.mainloop()
