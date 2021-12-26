import sqlite3
from tkinter import Variable

#Base class purely exists to give database related functionalities to other classes 
#This class is not made to be used but inherited from
class Base:
    def __init__(self):
        self.table_name = "This must be Over written"
        self.columns = []
        assert self.table_name is str and self.columns is list or self.columns is tuple

    def save(self, *values):
        """
        Save method builds a sql syntax from classes own table name, columns and given parameters.
        Every class should give certain values to this so that after an object initialised with this
        method they can be saved to database.
        """
        
        con = sqlite3.connect('main.db')
        cur = con.cursor()
        sql_code = "INSERT OR IGNORE INTO " + self.table_name + "("
        last_element = self.columns[len(self.columns) - 1]

        for column in self.columns:
            if column == last_element:
                sql_code = sql_code + column
            else:
                sql_code = sql_code + column + ","

        sql_code = sql_code + ") VALUES("

        last_element = values[ - 1]
        val_length = len(values)
        i = 0
        while i < val_length:
            value = values[i]
            if i == val_length -1:
                try:
                    int(value)
                    sql_code = sql_code + "%s);" %value
                except:
                    sql_code = sql_code + "'%s');" %value
            else:
                try:
                    int(value)
                    sql_code = sql_code + "%s," %value
                except:
                    sql_code = sql_code + "'%s'," %value
            i +=1
            
        cur.execute(sql_code)
        con.commit()
        con.close()
        
    def delete(self, *values):
        """
        Delete method builds a sql syntax from classes own table name, columns and given parameters.
        Every class should give certain values to this so that after an object initialised with this
        method they can be deleted from the database.
        """
        value_length, column_length = len(values), len(self.columns)
        
        con = sqlite3.connect('main.db')
        cur = con.cursor()

        sql_code = "DELETE FROM " + self.table_name + " WHERE "
        i = 0
        last_element = self.columns[column_length - 1]

        while i < value_length:
            column, value = self.columns[i], values[i]
            if last_element == column:
                try:
                    int(value)
                    sql_code = sql_code + "%s=%s;" % (column, value)
                except:
                    sql_code = sql_code + "%s='%s';" % (column, value)
            else:
                try:
                    int(value)
                    sql_code = sql_code + "%s=%s AND " % (column, value)
                except:
                    sql_code = sql_code + "%s='%s' AND " % (column, value)
            i += 1
        print(sql_code)
        cur.execute(sql_code)
        con.commit()
        con.close()
        
    def get_id(self, *values):
        """
        Get id method builds a sql syntax just like other methods.After an object 
        initialised and saved. Object's id can be taken from the database with this method.
        """
        
        value_length, column_length = len(values), len(self.columns)
        assert value_length == column_length

        con = sqlite3.connect('main.db')
        cur = con.cursor()

        query = "SELECT id FROM " + self.table_name + " WHERE "
        i = 0
        last_element = self.columns[column_length - 1]

        while i < value_length:
            column, value = self.columns[i], values[i]
            if last_element == self.columns[i]:
                query = query + "%s='%s';" % (column, value)
            else:
                query = query + "%s='%s' AND " % (column, value)
            i += 1
        cur.execute(query)
        id = cur.fetchone()
        if id is not None:
            id = id[0]
        con.close()
        return id
        
    def refresh(self, foreign_key_column, foreign_key):
        """
        Refresh is to be used to get related objects of a certain class
        """
        con = sqlite3.connect('main.db')
        cur = con.cursor()
        query = "SELECT * FROM %s WHERE %s=%s" %(self.table_name, foreign_key_column, foreign_key)
        cur.execute(query)
        results = cur.fetchall()
        con.close()
        return results


# This is module. Modules are related to quizes
class Module(Base):
    def __init__(self, name=None, quizes=None):
        self.name = name
        self.quizes = quizes
        self.table_name = "modules"
        self.columns = ["name"]

    def get_name(self):
        return self.name

    def set_name(self, module_name):
        self.name = module_name

    def get_quizes(self):
        return self.quizes

    def set_quiz(self, *quizes):
        if self.quizes is None:
            self.quizes = []
        for quiz in quizes:
            self.quizes.append(quiz)
        
    def get_quiz_names(self):
        if self.quizes is None:
            return None
        else:
            quiz_names = []
            for quiz in self.quizes:
                name = quiz.get_name()
                quiz_names.append(name)
            return quiz_names

    def save(self):
        name = self.name
        super().save(name)

    def delete(self):
        name = self.name
        return super().delete(name)

    def get_id(self):
        name = self.name
        id = super().get_id(name)
        return id

    def refresh(self):
        con = sqlite3.connect('main.db')
        cur = con.cursor()
        query = "SELECT name FROM " + self.table_name + ";"
        cur.execute(query)
        results = cur.fetchall()
        con.close()
        return results


# This is the quiz. A quiz have a name and a module it also may have multiple modules.
# The quiz can have selected questions or questions can be randomized
class Quiz(Base):
    def __init__(self, name=None, israndomized=False,questions=None):
        self.name = name
        self.questions = questions
        self.israndomized = israndomized
        self.table_name = "quizes"
        self.columns = ["name", "is_randomized", "module_id"]

        if self.questions is not None:
            for question in self.questions:
                assert question is Question 

    def get_name(self):
        return self.name

    def set_name(self, quiz_name):
        self.name = quiz_name

    def get_questions(self):
        return self.questions

    def set_question(self, *questions):
        if self.questions is None:
            self.questions = []
        for question in questions: 
            self.questions.append(question)
           
    def get_randomisation_status(self):
        return self.israndomized

    def set_randomisation_status(self, status):
        self.israndomized = status

    def save(self, related_class):
        name, israndomized = self.name, self.israndomized
        foreign_key = related_class.get_id()
        super().save(name, israndomized, foreign_key)

    def delete(self, related_class):
        name, israndomized = self.name, self.israndomized
        foreign_key = related_class.get_id()
        super().delete(name, israndomized, foreign_key)

    def get_id(self, related_class):
        name, israndomized = self.name, self.israndomized
        foreign_key = related_class.get_id()
        id = super().get_id(name, israndomized, foreign_key)
        return id

    def refresh(self, foreign_key):
        return super().refresh(self.columns[2], foreign_key)


# Every question needs a text. question parameter stands for the question itself.
class Question(Base):
    def __init__(self, question=None, answers=None):
        self.question = question
        self.right_answers = []
        self.answers = answers
        self.table_name = "questions"
        self.columns = ["question", "quiz_id"]

        if answers is not None:
            for answer in answers:
                if answer.iscorrect:
                    self.right_answers.append(answer)

        assert self.answers is list or self.answers is tuple or self.answers is None

        if answers is not None:
            assert len(self.right_answers), "There must be an at least one right answer"
            for answer, right_answer in self.answers, self.right_answers:
                assert answer is Answer and right_answer is Answer
            assert len(self.right_answers) != len(answers), 'Every answer cannot be correct.' \
                                                            ' Some of them must be wrong'

    def get_answers(self):
        return self.answers

    def set_answer(self, *answers):
        if self.answers is None:
            self.answers = []
        for answer in answers:
            self.answers.append(answer)

    def get_question(self):
        return self.question

    def set_question(self, question_itself):
        self.question = question_itself

    def get_right_answers(self):
        return self.right_answers

    def save(self, related_class, module_class):
        question = self.question
        foreign_key = related_class.get_id(module_class)
        super().save(question, foreign_key)

    def delete(self, related_class, module_class):
        question = self.question
        foreign_key = related_class.get_id(module_class)
        return super().delete(question, foreign_key)

    def get_id(self, quiz, module):
        question = self.question
        foreign_key = quiz.get_id(module)
        id = super().get_id(question, foreign_key)
        return id

    def refresh(self, foreign_key):
        return super().refresh(self.columns[1], foreign_key)

# This is the answer of an question. Answers are related to modules
class Answer(Base):
    def __init__(self, description=None, iscorrect=None, why_iscorrect=None):
        self.description = description
        self.iscorrect = iscorrect
        self.why_iscorrect = why_iscorrect
        self.table_name = "answers"
        self.columns = ["description", "iscorrect", "why_iscorrect", "question_id"]
        
    def get_description(self):
        return self.description

    def set_description(self, answer_description):
        self.description = answer_description

    def get_iscorrect(self):
        return self.iscorrect

    def set_iscorrect(self, answer_iscorrect):
        self.iscorrect = answer_iscorrect

    def get_why_iscorrect(self):
        self.why_iscorrect

    def set_why_iscorrect(self, answer_why_iscorrect):
        self.why_iscorrect = answer_why_iscorrect

    def save(self, related_class,quiz, module):
        description, iscorrect,  why_iscorrect = self.description, self.iscorrect,self.why_iscorrect
        foreign_key = related_class.get_id(quiz, module)
        super().save(description, iscorrect, why_iscorrect, foreign_key)

    def delete(self, related_class,quiz, module):
        iscorrect, description, why_iscorrect = self.iscorrect, self.description, self.why_iscorrect
        foreign_key = related_class.get_id(quiz, module)
        return super().delete(iscorrect, description, why_iscorrect, foreign_key)

    def get_id(self, related_class ,quiz, module):
        iscorrect, description, why_iscorrect = self.iscorrect, self.description, self.why_iscorrect
        foreign_key = related_class.get_id(quiz, module)
        id = super().get_id(iscorrect, description, why_iscorrect, foreign_key)
        return id

    def refresh(self, question,quiz, module):
        foreign_key = question.get_id(quiz, module)
        return super().refresh(self.columns[3], foreign_key)
