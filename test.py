import unittest
import objects
from db import create
import os
class TestObjects(unittest.TestCase):
    def setUp(self):
        create()
        self.test_module = objects.Module("test_module")
        self.is_saved = self.test_module.save()
        self.module_id = self.test_module.get_id()

        self.test_quiz = objects.Quiz("test_quiz", False)
        self.is_quiz_saved = self.test_quiz.save(self.test_module)
        self.quiz_id = self.test_quiz.get_id(self.test_module)

        self.test_question = objects.Question("Is Taiwan a country", 1)
        self.is_question_saved = self.test_question.save(self.test_quiz, self.test_module)
        self.question_id = self.test_question.get_id(self.test_quiz, self.test_module)

        self.test_question2 = objects.Question("What happened in Tienanmen Square", 1)
        self.is_question2_saved = self.test_question2.save(self.test_quiz, self.test_module)
        self.test_question2_id = self.test_question2.get_id(self.test_quiz, self.test_module)

        self.answer1 = objects.Answer("Yes, it is", 0, "Because it is a country")
        self.answer2 = objects.Answer("No, it is not", 1, "Because it is a country")

        self.test_question2_answer1 = objects.Answer("Nothing", 1, "Because nothing have happened")
        self.test_question2_answer2 = objects.Answer("People celebrated mao", 0, "Because nothing have happened")
        self.test_question2_answer3 = objects.Answer("Touristic activity", 0, "Because nothing have happened")
        self.test_question2_answer4 = objects.Answer("Massacre", 0, "Because nothing have happened")

        self.is_answer1_saved = self.answer1.save(self.test_question, self.test_quiz, self.test_module)
        self.is_answer2_saved = self.answer2.save(self.test_question, self.test_quiz, self.test_module)

        self.test_question2_answer1.save(self.test_question2, self.test_quiz, self.test_module)
        self.test_question2_answer2.save(self.test_question2, self.test_quiz, self.test_module)
        self.test_question2_answer3.save(self.test_question2, self.test_quiz, self.test_module)
        self.test_question2_answer4.save(self.test_question2, self.test_quiz, self.test_module)

    """def tearDown(self):
        os.remove('question_bank.db')"""

    def test_name(self):
        self.assertIsNotNone(self.test_module.get_name())
        self.assertIsNotNone(self.test_quiz.get_name())

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
            for answer in question.get_answers():
                self.assertIsInstance(answer, objects.Answer)


if __name__ == 'main':
    unittest.main()
