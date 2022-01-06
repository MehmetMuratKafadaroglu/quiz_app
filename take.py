import objects
from generic_widgets import *
from objects import *
from db import *

class App(Tk):
    def __init__(self):
        super().__init__()
        self.height = 600
        self.title("Quiz App")
        self.geometry("900x600")

    def adjust_height(self, number):
        self.geometry("900x%s" % number)


root = App()


class QuestionView(Frame):
    def __init__(self, master, questions):
        Frame.__init__(self, master)
        self.master = master
        self.questions = questions
        self.question_index = 0
        self.question = self.questions[self.question_index]

        self.text = StringVar()
        self.text.set(self.question.get_question())

        self.label = Label(self, textvariable=self.text, height=8, relief='solid')
        self.label.pack(fill=X, expand=True)
        self.btn = AnswerButtons(self, self.question)
        self.btn.pack()

    def next_question(self):
        self.label.destroy()
        self.btn.destroy()
        self.increment()

        self.label = Label(self, textvariable=self.text, height=8, relief='solid')
        self.label.pack(fill=X, expand=True)
        self.btn = AnswerButtons(self, self.question)
        self.btn.pack()

    def increment(self):
        self.question_index += 1
        self.question = self.questions[self.question_index]

    def adjust_height(self, number):
        number *= 200
        self.master.adjust_height(number)

class Listview(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
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

    def get_questions_of_selected_quiz(self):
        quiz = self.get_selected_quiz()
        module = self.get_selected_module()
        quiz_id = quiz.get_id(module)
        questions = objects.Question().refresh(quiz_id)
        questions = objects.Question.get_question_with_answers(questions, quiz, module)
        return questions

    def increment_index(self):
        self.index += 1

    def take(self):
        questions = self.get_questions_of_selected_quiz()
        question_view = QuestionView(root, questions)
        question_view.pack()
        self.pack_forget()

    def back(self):
        self.destroy()

    def refresh(self):
        results = Quiz.get_quizes_with_modules()
        generic_refresh(results, self.tree)


main_view = Listview(root)
main_view.pack(fill=BOTH, expand=True)
root.mainloop()
