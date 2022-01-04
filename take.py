from generic_widgets import *
from objects import *
from db import *

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz App")
        self.geometry("900x600")
root = App()

class Listview(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        heads = {'name': 'Quiz name', 'module': 'Module of the quiz'}
        self.tree = GenericTree(master=self, dict=heads)
        self.tree.pack()
        self.tree.bind("<Double-1>", self.take)
        buttons = TakeQuizButtons(self, self.back, self.take)
        buttons.pack()
        self.refresh()
    def take(self):
        self.pack_forget()
    def back(self):
        self.destroy()
    def refresh(self):
        results = Quiz.get_quizes_with_modules()
        generic_refresh(results, self.tree)

main_view = Listview(root)
main_view.pack(fill=BOTH, expand=True)
root.mainloop()

