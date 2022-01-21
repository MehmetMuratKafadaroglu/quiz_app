import unittest
import objects
import os

"""
Test file exist for test purposes and to insert data to database for examples.
"""

class TestObjects(unittest.TestCase):
    def setUp(self):
        os.remove('question_bank.db')
        objects.Custom.create()
        self.test_module = objects.Module("Paradigms of Programming")
        self.is_saved = self.test_module.save()
        self.module_id = self.test_module.get_id()
        
        self.test_quiz = objects.Quiz("General Computer Science Quiz", True)
        self.is_quiz_saved = self.test_quiz.save(self.test_module)
        self.quiz_id = self.test_quiz.get_id(self.test_module)

        self.test_question = objects.Question("Is python supports functional programming ?", 2)
        self.is_question_saved = self.test_question.save(self.test_quiz, self.test_module)
        self.question_id = self.test_question.get_id(self.test_quiz, self.test_module)

        self.test_question2 = objects.Question("Who is considered founder of computer science ?", 1)
        self.is_question2_saved = self.test_question2.save(self.test_quiz, self.test_module)
        self.test_question2_id = self.test_question2.get_id(self.test_quiz, self.test_module)

        self.test_question3 = objects.Question("What is the first high level language ?", 1)
        self.is_question3_saved = self.test_question3.save(self.test_quiz, self.test_module)
        self.test_question3_id = self.test_question3.get_id(self.test_quiz, self.test_module)
        
        self.test_question4 = objects.Question("Is python statically typed language", 2)
        self.is_question4_saved = self.test_question4.save(self.test_quiz, self.test_module)
        self.test_question4_id = self.test_question4.get_id(self.test_quiz, self.test_module)
        
        self.test_question5 = objects.Question("Which option is not a python data type", 3)
        self.is_question5_saved = self.test_question5.save(self.test_quiz, self.test_module)
        self.test_question5_id = self.test_question5.get_id(self.test_quiz, self.test_module)
        
        self.answer1 = objects.Answer("Yes, it does", 1, "Python is a multi-paradigm programming language")
        self.answer2 = objects.Answer("No, it does not", 0, "Python is a multi-paradigm programming language")

        self.test_question2_answer1 = objects.Answer("Boris Johnson", 0, "Boris Johnson has nothing to do with computer science")
        self.test_question2_answer2 = objects.Answer("Edsger W. Dijkstra", 0, """Although 
Dijkstra was awell known early computer scientist he is not considered founder of computer science""")
        self.test_question2_answer3 = objects.Answer("Alan Turing", 1, """Alan Turing is considered founder of computer science
because of Turing machine""")
        self.test_question2_answer4 = objects.Answer("Dennis Ritchie", 0, "No Dennis Ritchie is not considered")

        self.test_question3_answer1 = objects.Answer("Lisp", 0, "Lisp is second you were close! answer is Fortran")
        self.test_question3_answer2 = objects.Answer("Fortran", 1, "Yes fortan is first high level language")
        self.test_question3_answer3 = objects.Answer("C", 0, "No C is not, answer is Fortran")
        self.test_question3_answer4 = objects.Answer("Pascal", 0, "No Pascal is not, answer is Fortran")

        self.is_answer1_saved = self.answer1.save(self.test_question, self.test_quiz, self.test_module)
        self.is_answer2_saved = self.answer2.save(self.test_question, self.test_quiz, self.test_module)

        self.test_question2_answer1.save(self.test_question2, self.test_quiz, self.test_module)
        self.test_question2_answer2.save(self.test_question2, self.test_quiz, self.test_module)
        self.test_question2_answer3.save(self.test_question2, self.test_quiz, self.test_module)
        self.test_question2_answer4.save(self.test_question2, self.test_quiz, self.test_module)

        self.test_question3_answer1.save(self.test_question3, self.test_quiz, self.test_module)
        self.test_question3_answer2.save(self.test_question3, self.test_quiz, self.test_module)
        self.test_question3_answer3.save(self.test_question3, self.test_quiz, self.test_module)
        self.test_question3_answer4.save(self.test_question3, self.test_quiz, self.test_module)

        self.test_question4_answer1 = objects.Answer("Yes, it is", 1, "Python is a dynamically typed")
        self.test_question4_answer2 = objects.Answer("No, it is not", 0, "Python is a dynamically typed")
        self.test_question4_answer1.save(self.test_question4, self.test_quiz, self.test_module)
        self.test_question4_answer2.save(self.test_question4, self.test_quiz, self.test_module)

        self.test_question5_answer1 = objects.Answer("Array", 1, "Array is not a python data type")
        self.test_question5_answer2 = objects.Answer("Integer", 0, "Integer is a python data type")
        self.test_question5_answer3 = objects.Answer("Float", 1, "Float is a python data type")
        self.test_question5_answer4 = objects.Answer("String", 1, "String is a python data type")
        self.test_question5_answer5 = objects.Answer("List", 1, "List is a python data type")
        self.test_question5_answer6 = objects.Answer("Dictionary", 1, "Dictionary is a python data type")

        self.test_question5_answer1.save(self.test_question5, self.test_quiz, self.test_module)
        self.test_question5_answer2.save(self.test_question5, self.test_quiz, self.test_module)
        self.test_question5_answer3.save(self.test_question5, self.test_quiz, self.test_module)
        self.test_question5_answer4.save(self.test_question5, self.test_quiz, self.test_module)
        self.test_question5_answer5.save(self.test_question5, self.test_quiz, self.test_module)
        self.test_question5_answer6.save(self.test_question5, self.test_quiz, self.test_module)
    """
    def tearDown(self):
        os.remove('question_bank.db')"""
        

    def test_save(self):
        self.assertIsNotNone(self.is_saved)
        self.assertIsNotNone(self.is_quiz_saved)
        self.assertIsNotNone(self.is_question_saved)
        self.assertIsNotNone(self.is_answer1_saved)
        self.assertIsNotNone(self.is_answer2_saved)

    def test_auto_init(self):
        quiz_id = self.quiz_id
        questions = self.test_question.refresh(quiz_id)
        questions = objects.Question.auto_init(questions)

        self.assertIsInstance(questions, list)
        for question in questions:
            self.assertIsInstance(question, objects.Question)

        answers = self.answer1.refresh(foreign_key=self.question_id)
        answers = objects.Answer.auto_init(answers)

        self.assertIsInstance(answers, list)
        for answer in answers:
            self.assertIsInstance(answer, objects.Answer)

    def test_final(self):
        questions = objects.Question().refresh(self.quiz_id)
        questions = objects.Question.get_question_with_answers(questions, self.test_quiz, self.test_module)

        self.assertIsInstance(questions, list)
        for question in questions:
            self.assertIsInstance(question, objects.Question)
            for answer in question.answers:
                self.assertIsInstance(answer, objects.Answer)


if __name__ == 'main':
    unittest.main()
