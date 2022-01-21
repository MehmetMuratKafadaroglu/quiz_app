from http.client import PROXY_AUTHENTICATION_REQUIRED
from objects import *
from generic_widgets import *
import random

""""
Main file where we put everything together.
This file takes the data from objects and takes the UI widgets from generic widgets.
This file is the file where things are put together.
Also main should not communicate with database directly if data needs to be inserted/manipulated this file 
should communicate with objects file.
"""

register_module = None
register_quiz = None
register_question = None
register_answer = None


class App(Tk):
    def __init__(self):
        super().__init__()
        self.height = 600
        self.title("Quiz App")
        self.start_geom = "900x600"
        self.geometry(self.start_geom)
        Custom.create()

    def adjust_height(self, number):
        self.geometry("900x%s" % number)

    def go_back_to_start_geom(self):
        self.geometry(self.start_geom)


root = App()


class StartPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        take_a_quiz = Button(self, text="Take a Quiz!", command=self.take, height=6, width=60)
        see_your_previous_results = Button(self, text="See your previous results", command=self.previous_results,
                                           height=6,
                                           width=60)
        add_and_edit_your_quizzes = Button(self, text="Add and edit your quizes", command=self.edit_and_add, height=6,
                                           width=60)
        quit_button = Button(self, text="Quit", command=self.master.destroy, height=6,
                                           width=60)
        take_a_quiz.pack(pady=20)
        see_your_previous_results.pack(pady=20)
        add_and_edit_your_quizzes.pack(pady=20)
        quit_button.pack(pady=20)

    def take(self):
        Listview(root).pack()
        self.pack_forget()

    def previous_results(self):
        PreviousResults(root).pack()
        self.pack_forget()

    def edit_and_add(self):
        module_page.pack()
        self.pack_forget()


start = StartPage(root)
start.pack(fill=BOTH, expand=True)


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

    def raise_message(self):
        RaiseMessage("Module name must not be taken or blank")

    def get_module(self):
        module_name = self.name.get_input()
        module_name = module_name.rstrip()
        return Module(name=module_name)

    def press(self):
        module = self.get_module()
        if self.item is None:
            is_saved = module.save()
        else:
            item = self.item[0]
            module_id = Module(name=item).get_id()
            is_saved = module.update(pk=module_id)
        if not is_saved:
            self.raise_message()
        module_page.refresh()
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
        start.pack()
        self.pack_forget()

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
        if item is None:
            return
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
        self.is_randomized = OptionField(self, "Is the quiz randomized", options=['Randomized', 'Not Randomized'])
        save = Button(self, text=txt.upper(), height=5, background='green', command=self.press)
        save.pack(fill=X, expand=True)

    def raise_message(self):
        RaiseMessage("Quiz name must not be taken or blank")

    def get_quiz(self):
        quiz_name = self.name.get_input()
        quiz_name = quiz_name.rstrip()
        is_randomized = self.is_randomized.get_input()
        if is_randomized == "Randomized":
            is_randomized = 1
        else:
            is_randomized = 0
        return Quiz(name=quiz_name, israndomized=is_randomized)

    def press(self):
        quiz = self.get_quiz()
        if self.is_add:
            is_saved = quiz.save(register_module)
        else:
            is_saved = quiz.update(register_module, register_quiz)
        if not is_saved:
            self.raise_message()
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
        module_page.pack(fill=BOTH, expand=True)
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

                copy = replace_elements(copy, copy[1], desired_element)
                copy = list(copy)
                values.append(copy)
            generic_refresh(values, self.tree)

    def edit(self):
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
            carry_item = replace_elements(carry_item, "Randomized", 1)
        else:
            carry_item = replace_elements(carry_item, "Not Randomized", 0)
        Quiz(name=carry_item[0], israndomized=carry_item[1]).delete(register_module)


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
        self.options = ['MCQ', 'TF', 'Best Match']
        self.question_type = OptionField(self, "Choose the question type", options=self.options)
        self.question_type.pack(fill=X, expand=True)
        save = Button(self, text=txt.upper(), height=5, background='green', command=self.press)
        save.pack(fill=X, expand=True)

    def raise_message(self):
        RaiseMessage("Question values must not be taken or blank")

    def get_question_type(self):
        question_type = self.question_type.get_input()
        if question_type == self.options[0]:
            return 1
        elif question_type == self.options[1]:
            return 2
        elif question_type == self.options[2]:
            return 3
        else:
            print(self.options)
            raise ValueError("Question type must be one of the options")

    def get_question(self):
        question = self.name.get_input()
        question = question.rstrip()
        question_type = self.get_question_type()
        return Question(question=question, question_type=question_type)

    def press(self):
        question = self.get_question()
        if self.is_add:
            is_saved = question.save(register_quiz, register_module)
        else:
            is_saved = question.update(register_quiz, register_module, register_question)
        if not is_saved:
            self.raise_message()
        question_page.refresh()
        self.destroy()


class QuestionPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        heads = {'name': 'Questions of the Quiz', 'type': 'Type of Question'}
        self.tree = GenericTree(master=self, dict=heads)
        self.tree.pack()
        self.tree.bind("<Double-1>", self.delete)
        self.buttons = EditMainButtons(self, back=self.back, press=self.add, edit=self.edit, delete=self.delete,
                                       update=self.update, txt="Edit answers of this question")
        self.buttons.pack(fill=X, expand=True)

    def back(self):
        quiz_page.pack(fill=BOTH, expand=True)
        self.pack_forget()

    def get_selected_question(self):
        item = self.tree.selected_item()
        item = self.tree.get_item(item)

        question = item[0]
        question_type = item[1]
        question = Question(question=question, question_type=question_type)
        return question

    def add(self):
        UpdateAddQuestions(True)

    def update(self):
        question = self.get_selected_question()
        global register_question
        register_question = question
        UpdateAddQuestions(False)

    def get_question_type(self, number):
        if number == 1:
            return 'Multiple Answer Question'
        elif number == 2:
            return 'True False Question'
        elif number == 3:
            return 'Best Match Question'
        else:
            raise ValueError("Numbers must be between 1-3")

    def refresh(self):
        if register_quiz is not None:
            quiz_id = register_quiz.get_id(register_module)
            results = Question().refresh(foreign_key=quiz_id)
            values = []
            for result in results:
                result_in_list = list(result)
                copy = del_first_and_last(result_in_list)
                copy = list(copy)
                question_type = self.get_question_type(copy[1])
                copy = replace_elements(copy, copy[1], question_type)
                values.append(copy)
            generic_refresh(values, self.tree)

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
        question_type = carry_item[1]
        Question(question=carry_item[0], question_type=question_type).delete(register_quiz, register_module)


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
        self.iscorrect = OptionField(master=self, text="Is this answer is true or false")
        self.why_iscorrect = InputField(master=self, text="Why this answer is correct or wrong")
        save = Button(self, text=txt.upper(), height=5, background='green', command=self.press)
        save.pack(fill=X, expand=True)

    def raise_message(self):
        RaiseMessage("Answer values must not be taken or blank")

    def get_answer(self):
        description = self.answer.get_input()
        description = description.rstrip()

        why_iscorrect = self.why_iscorrect.get_input()
        why_iscorrect = why_iscorrect.rstrip()

        is_correct = self.iscorrect.get_input()
        if bool(is_correct):
            is_correct = 1
        else:
            is_correct = 0
        return Answer(description, is_correct, why_iscorrect)

    def press(self):
        answer = self.get_answer()
        if self.is_add:
            is_saved = answer.save(register_question, register_quiz, register_module)
        else:
            is_saved = answer.update(register_question, register_quiz, register_module, register_answer)
        if not is_saved:
            self.raise_message()
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
        self.buttons = EditMainButtons(self, back=self.back, press=self.add, update=self.update, delete=self.delete,
                                       edit=None)
        self.buttons.edit_button.grid_forget()
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
            iscorrect = 1
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
                    copy = replace_elements(copy, copy[1], "True")
                else:
                    copy = replace_elements(copy, copy[1], "False")
                values.append(copy)
            generic_refresh(values, self.tree)

    def delete(self):
        item = self.tree.selected_item()
        carry_item = self.tree.get_item(item)
        self.tree.delete(item)

        description = carry_item[0]
        iscorrect = carry_item[1]
        why_iscorrect = carry_item[2]

        if bool(iscorrect):
            iscorrect = 1
        else:
            iscorrect = 0

        answer = Answer(description, iscorrect, why_iscorrect)
        answer.delete(register_question, register_quiz, register_module)


class PreviousResults(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.values = []
        self.tree = GenericTree(self, {'result': 'Result', 'date': 'Date', 'quiz': 'Quiz', 'module': 'Module'})
        self.tree.pack()
        self.refresh()
        btn = TakeQuizButtons(self, self.press, self.delete_result, txt="Delete All Results")
        btn.pack()

    def press(self):
        start.pack()
        root.go_back_to_start_geom()
        self.pack_forget()

    def refresh(self):
        self.values = Custom.get_results()
        generic_refresh(self.values, self.tree)

    def delete_result(self):
        Custom.delete_all_results()
        self.refresh()


class ResultPage(Frame):
    def __init__(self, master, results, why_iscorrect):
        Frame.__init__(self, master)
        self.master = master
        self.results = results
        self.why_iscorrect = why_iscorrect
        Results(self, self.results, self.why_iscorrect).pack(fill=BOTH, expand=True)

    def exit(self):
        Listview(root).pack(fill=BOTH, expand=True)
        root.go_back_to_start_geom()
        self.pack_forget()


class AnswerView(Frame):
    def __init__(self, master, questions, quiz_id):
        Frame.__init__(self, master)
        self.master = master
        self.questions = questions
        self.question_index = 0
        self.quiz_id = quiz_id
        self.why_iscorrect = []
        self.question = self.questions[self.question_index]
        self.results = []

        self.btn = AnswersAndLabel(master=self, question=self.question)
        self.btn.pack()

    def next_question(self, iscorrect, why_iscorrect):
        self.results.append(iscorrect)
        self.btn.pack_forget()
        self.why_iscorrect.append(why_iscorrect)
        is_end = self.question_index == len(self.questions) - 1
        if is_end:
            self.go_to_results_page()
        else:
            self.add_new_question()

    def go_to_results_page(self):
        Custom.add_results(self.results, self.quiz_id)
        ResultPage(root, self.results, self.why_iscorrect).pack(fill=BOTH, expand=1)
        self.pack_forget()

    def add_new_question(self):
        self.increment()
        self.btn = AnswersAndLabel(self, self.question)
        self.btn.pack()

    def increment(self):
        self.question_index += 1
        self.question = self.questions[self.question_index]

    def adjust_height(self, number):
        number *= 180
        self.master.adjust_height(number)


class Listview(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.quiz_id = None
        self.master = master
        self.index = 0
        heads = {'name': 'Quiz name', 'module': 'Module of the quiz', 'israndomized': 'Is quiz Randomized'}
        self.tree = GenericTree(master=self, dict=heads)
        self.tree.pack()
        self.tree.bind("<Double-1>", self.take)
        buttons = TakeQuizButtons(self, self.back, self.take)
        buttons.pack()
        self.refresh()

    @staticmethod
    def get_status(status):
        if status == 'Randomized':
            return 1
        elif status == 'Not Randomized':
            return 0
        else:
            return status

    def get_selected_module(self):
        item = self.tree.selected_item()
        item = self.tree.get_item(item)
        module = Module(name=item[1])
        return module

    def get_selected_quiz(self):
        item = self.tree.selected_item()
        item = self.tree.get_item(item)
        quiz = item[0]
        status = Listview.get_status(item[2])
        quiz = Quiz(quiz, status)
        return quiz

    def get_questions_of_selected_quiz(self, quiz, module):
        self.quiz_id = quiz.get_id(module)
        questions = Question().refresh(self.quiz_id)
        questions = Question.get_question_with_answers(questions, quiz, module)
        return questions

    def increment_index(self):
        self.index += 1

    def take(self):
        quiz = self.get_selected_quiz()
        module = self.get_selected_module()
        questions = self.get_questions_of_selected_quiz(quiz, module)
        if quiz.israndomized:
            random.shuffle(questions)
        question_view = AnswerView(root, questions, self.quiz_id)
        question_view.pack()
        self.pack_forget()

    def back(self):
        start.pack()
        self.pack_forget()

    def refresh(self):
        results = Quiz.get_quizes_with_modules()
        generic_refresh(results, self.tree)


module_page = ModulePage(master=root)
quiz_page = QuizPage(master=root)
question_page = QuestionPage(master=root)
answer_page = AnswerPage(master=root)
root.mainloop()
