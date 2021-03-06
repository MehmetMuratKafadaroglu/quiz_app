import sqlite3
"""
Made by 001143514
Objects file is a file that retrives, deletes, edit data from/to main.
This file makes queries and put them to python objects when data is required.
When data needs to be edited, deleted or saved objects are initialised in main file and methods of the class is called
For instance, if a module needs to be saved module would be initialised and after that save method would be called
This file should not communicate with generic widgets file. This file should only communicate with main file.
"""


# This is an abstract class. This class is just there to give other classes certain database related methods.
class Base:
    def __init__(self):
        self.__table_name = ""
        self.__columns = []

        if type(self) is Base:
            raise NotImplementedError("This is an abstract class and cannot be instantiated")
        assert type(self.table_name) is str and type(self.columns) is list or type(self.columns) is tuple

    def where_loop(self, sql_code, index=0):
        """
        This method produces part of the sql code that is after where
        """
        sql_code += self.columns[index] + "=?"
        index += 1
        if index >= len(self.columns):
            return sql_code
        sql_code += ' AND '
        return self.where_loop(sql_code, index=index)

    def save(self, *values):
        """
        Save method builds a sql syntax from classes own table name, columns and given parameters.
        Every class should give certain values to this so that after an object initialised with this
        method they can be saved to database.
        """
        con = sqlite3.connect('question_bank.db')
        cur = con.cursor()
        for value in values:
            if value == '':
                return False

        sql_code = "INSERT OR IGNORE INTO " + self.table_name + "("
        for column in self.columns:
            sql_code = sql_code + column + ","

        sql_code = sql_code[:-1]
        sql_code += ") VALUES("

        for val in values:
            sql_code += '?,'

        sql_code = sql_code[:-1]
        sql_code += ');'
        cur.execute(sql_code, values)
        con.commit()
        con.close()
        return True

    def delete(self, *values):
        """
        Delete method builds a sql syntax from classes own table name, columns and given parameters.
        Every class should give certain values to this so that after an object initialised with this
        method they can be deleted from the database.
        """
        con = sqlite3.connect('question_bank.db')
        cur = con.cursor()
        sql_code = "DELETE FROM " + self.table_name + " WHERE "
        sql_code = self.where_loop(sql_code)
        cur.execute(sql_code, values)
        con.commit()
        con.close()

    def get_id(self, *values):
        """
        Get id method builds a sql syntax just like other methods.After an object 
        initialised and saved. Object's id can be taken from the database with this method.
        """
        query = "SELECT id FROM " + self.table_name + " WHERE "
        query = self.where_loop(query)
        con = sqlite3.connect('question_bank.db')
        cur = con.cursor()
        cur.execute(query, values)
        id = cur.fetchone()
        if id is not None:
            id = id[0]
        con.close()
        return id

    def refresh(self, foreign_key_column, foreign_key):
        """
        Refresh is to be used to get related objects of a certain class.
        """
        con = sqlite3.connect('question_bank.db')
        cur = con.cursor()
        query = "SELECT * FROM {} WHERE {}={}".format(self.table_name, foreign_key_column, foreign_key)
        cur.execute(query)
        results = cur.fetchall()
        con.close()
        return results

    def update(self, pk, **kwargs):
        """
        This is a general update statement. This updates all the places that is given in the dictionary.
        """
        table_name = self.table_name
        sql_code = "UPDATE {} SET ".format(table_name)
        values = []
        for item in kwargs.items():
            column = item[0]
            value = item[1]
            if value == '':
                return False
            values.append(value)
            sql_code += column + '=?,'

        sql_code = sql_code[:-1]
        sql_code += " WHERE id={} ".format(pk)
        con = sqlite3.connect('question_bank.db')
        cur = con.cursor()
        cur.execute(sql_code, values)
        con.commit()
        con.close()
        return True


# This is module. Modules are related to quizzes
class Module(Base):
    def __init__(self, name=None, quizes=None):
        self._name = name
        self._quizes = quizes
        self.__table_name = "modules"
        self.__columns = ["name"]

    @property
    def table_name(self):
        return self.__table_name

    @property
    def columns(self):
        return self.__columns

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def quizes(self):
        return self._quizes

    @quizes.setter
    def quizes(self, *quizes):
        if self._quizes is None:
            self._quizes = []
        if type(quizes[0]) == list:
            self.quizes = quizes[0]
        else:
            for quiz in quizes:
                self.quizes.append(quiz)

    def save(self):
        name = self.name
        is_exist = self.get_id()
        if is_exist:
            return False
        else:
            return super().save(name)

    def delete(self):
        name = self.name
        return super().delete(name)

    def get_id(self):
        name = self.name
        id = super().get_id(name)
        return id

    def refresh(self):
        con = sqlite3.connect('question_bank.db')
        cur = con.cursor()
        query = "SELECT name FROM " + self.table_name + ";"
        cur.execute(query)
        results = cur.fetchall()
        con.close()
        return results

    def update(self, pk):
        return super().update(pk, name=self.name)


# This is the quiz. A quiz have a name and a module it also may have multiple modules.
# The quiz can have selected questions or questions can be randomized
class Quiz(Base):
    def __init__(self, name=None, israndomized=False, questions=None):
        self._name = name
        self._questions = questions
        self._israndomized = israndomized
        self.__table_name = "quizes"
        self.__columns = ["name", "is_randomized", "module_id"]

    @property
    def name(self):
        return self._name

    @property
    def table_name(self):
        return self.__table_name

    @property
    def columns(self):
        return self.__columns

    @name.setter
    def name(self, quiz_name):
        self._name = quiz_name

    @property
    def questions(self):
        return self._questions

    @questions.setter
    def questions(self, questions):
        self._questions = questions

    @property
    def israndomized(self):
        return self._israndomized

    @israndomized.setter
    def israndomized(self, status):
        self.israndomized = status

    @staticmethod
    def get_quizes_with_modules():
        con = sqlite3.connect('question_bank.db')
        cur = con.cursor()
        cur.execute("""SELECT quizes.name, modules.name, quizes.is_randomized 
        FROM quizes, modules WHERE quizes.module_id=modules.id""")
        results = cur.fetchall()
        copy = []

        for result in results:
            status = result[2]

            if status:
                status = 'Randomized'
            else:
                status = 'Not Randomized'
            carry_tuple = (result[0], result[1], status)
            copy.append(carry_tuple)
        con.close()
        return copy

    def save(self, related_class):
        name, israndomized = self.name, self.israndomized
        foreign_key = related_class.get_id()
        is_exist = self.get_id(related_class)
        if is_exist:
            return False
        else:
            return super().save(name, israndomized, foreign_key)

    def delete(self, related_class):
        name, israndomized = self.name, self.israndomized
        foreign_key = related_class.get_id()
        super().delete(name, israndomized, foreign_key)

    def get_id(self, related_class):
        foreign_key = related_class.get_id()
        id = super().get_id(self.name, self.israndomized, foreign_key)
        return id

    def refresh(self, foreign_key):
        return super().refresh(self.columns[2], foreign_key)

    def update(self, related_class, old_object):
        pk = old_object.get_id(related_class)
        return super().update(pk, name=self.name, is_randomized=self.israndomized)


# Every question needs a text. question parameter stands for the question itself.
class Question(Base):
    def __init__(self, question=None, question_type=None, answers=None):
        self._question = question
        self._question_type = question_type
        self._answers = answers
        self.__table_name = "questions"
        self.__columns = ["question", "question_type", "quiz_id"]

    @property
    def answers(self):
        return self._answers

    @property
    def table_name(self):
        return self.__table_name

    @property
    def columns(self):
        return self.__columns

    @answers.setter
    def answers(self, answers):
        self._answers = answers

    @property
    def question(self):
        return self._question

    @question.setter
    def question(self, question):
        self._question = question

    @property
    def question_type(self):
        typ = self._question_type
        if typ in [1, 2, 3]:
            return typ
        elif typ == 'Multiple Answer Question':
            return 1
        elif typ == 'True False Question':
            return 2
        else:
            return 3

    @question_type.setter
    def question_type(self, question_type):
        self._question_type = question_type

    def save(self, quiz, module):
        question = self.question
        question_type = self.question_type
        foreign_key = quiz.get_id(module)
        is_exist = self.get_id(quiz, module)
        if is_exist:
            return False
        else:
            return super().save(question, question_type, foreign_key)

    def delete(self, related_class, module_class):
        foreign_key = related_class.get_id(module_class)
        return super().delete(self.question, self.question_type, foreign_key)

    def get_id(self, quiz, module):
        foreign_key = quiz.get_id(module)
        return super().get_id(self.question, self.question_type, foreign_key)

    def refresh(self, foreign_key):
        return super().refresh(self.columns[2], foreign_key)

    def update(self, quiz, module, old_object):
        pk = old_object.get_id(quiz, module)
        return super().update(pk, question=self.question, question_type=self.question_type)

    @staticmethod
    def auto_init(questions):
        values = []
        for result in questions:
            question = Question(result[1], result[2])
            values.append(question)
        return values

    @staticmethod
    def get_question_with_answers(questions, quiz, module):
        questions = Question.auto_init(questions)
        final = []
        for question in questions:
            pk = question.get_id(quiz, module)
            answers = Answer().refresh(foreign_key=pk)
            copy = Answer.auto_init(answers)
            question.answers = copy
            final.append(question)
        return final

# This is the answer of a question. Answers are related to modules
class Answer(Base):
    def __init__(self, description=None, iscorrect=None, why_iscorrect=None):
        self._description = description
        self._iscorrect = iscorrect
        self._why_iscorrect = why_iscorrect
        self.__table_name = "answers"
        self.__columns = ["description", "iscorrect", "why_iscorrect", "question_id"]

    @property
    def description(self):
        return self._description

    @property
    def table_name(self):
        return self.__table_name

    @property
    def columns(self):
        return self.__columns

    @description.setter
    def description(self, answer_description):
        self._description = answer_description

    @property
    def iscorrect(self):
        return self._iscorrect

    @iscorrect.setter
    def iscorrect(self, answer_iscorrect):
        self._iscorrect = answer_iscorrect

    @property
    def why_iscorrect(self):
        return self._why_iscorrect

    @why_iscorrect.setter
    def why_iscorrect(self, answer_why_iscorrect):
        self._why_iscorrect = answer_why_iscorrect

    def save(self, question, quiz, module):
        description, iscorrect, why_iscorrect = self.description, self.iscorrect, self.why_iscorrect
        foreign_key = question.get_id(quiz, module)
        is_exist = self.get_id(question, quiz, module)
        if is_exist:
            return False
        else:
            return super().save(description, iscorrect, why_iscorrect, foreign_key)

    def delete(self, question, quiz, module):
        iscorrect, description, why_iscorrect = self.iscorrect, self.description, self.why_iscorrect
        foreign_key = question.get_id(quiz, module)
        return super().delete(description, iscorrect, why_iscorrect, foreign_key)

    def get_id(self, question, quiz, module):
        foreign_key = question.get_id(quiz, module)
        id = super().get_id(self.description, self.iscorrect, self.why_iscorrect, foreign_key)
        return id

    def refresh(self, question=None, quiz=None, module=None, foreign_key=None):
        if foreign_key is None:
            foreign_key = question.get_id(quiz, module)
        field = self.columns[3]
        return super().refresh(field, foreign_key)

    def update(self, question, quiz, module, old_object):
        pk = old_object.get_id(question, quiz, module)
        return super().update(pk, description=self.description, iscorrect=self.iscorrect,
                              why_iscorrect=self.why_iscorrect)

    @staticmethod
    def auto_init(answers):
        values = []
        for answer in answers:
            description = answer[1]
            iscorrect = answer[2]
            why_iscorrect = answer[3]
            carry = Answer(description, iscorrect, why_iscorrect)
            values.append(carry)
        return values


class Custom:
    @staticmethod
    def create():
        con = sqlite3.connect('question_bank.db')
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS 
            modules(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name VARCHAR(500),
            UNIQUE(name)
            );
            """)
        cur.execute("""CREATE TABLE IF NOT EXISTS
            quizes(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name VARCHAR(500), 
            is_randomized INTEGER, 
            module_id INTEGER,
            UNIQUE(name, module_id),
            FOREIGN KEY(module_id) REFERENCES modules(id)
            );
            """)
        cur.execute("""CREATE TABLE IF NOT EXISTS 
            questions(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            question VARCHAR(500),
            question_type INTEGER,
            quiz_id INTEGER,
            number_of_times_taken INTEGER DEFAULT 0,
            UNIQUE(question, quiz_id),
            FOREIGN KEY(quiz_id) REFERENCES quizes(id)
            );
            """)
        cur.execute("""CREATE TABLE IF NOT EXISTS 
            answers(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            description VARCHAR(500),
            iscorrect INTEGER,
            why_iscorrect VARCHAR(500),
            question_id INTEGER,
            UNIQUE(description, question_id)
            FOREIGN KEY(question_id) REFERENCES questions(id)
            );
            """)
        cur.execute("""CREATE TABLE IF NOT EXISTS 
            results(
            id INTEGER PRIMARY KEY, 
            quiz_id INTEGER,
            correct_answers INTEGER,
            number_of_questions INTEGER, 
            date TEXT,
            FOREIGN KEY(quiz_id) REFERENCES quizes(id)
            );
            """)
        con.commit()
        con.close()

    @staticmethod
    def add_results(results, quiz_id):
        con = sqlite3.connect('question_bank.db')
        cur = con.cursor()
        pk = quiz_id
        number_of_questions = len(results)
        final_result = 0
        for result in results:
            final_result += result
        cur.execute("""INSERT INTO results
        (quiz_id, correct_answers, number_of_questions, date) 
        VALUES(?, ?, ?, DATETIME('now', 'localtime'))""",
                    [pk, final_result, number_of_questions, ])
        con.commit()
        con.close()

    @staticmethod
    def results_as_list(results):
        values = []
        for result in results:
            correct_answers = result[0]
            number_of_questions = result[1]
            date = result[2]
            quiz = result[3]
            module = result[4]
            result = '%s / %s' % (correct_answers, number_of_questions)
            value = [result, date, quiz, module]
            values.append(value)
        return values

    @staticmethod
    def get_results():
        con = sqlite3.connect('question_bank.db')
        cur = con.cursor()
        cur.execute("""SELECT results.correct_answers, 
        results.number_of_questions, results.date,
        quizes.name, modules.name
        FROM results, quizes, modules
        WHERE results.quiz_id=quizes.id
        AND quizes.module_id=modules.id
        """)
        con.commit()
        results = cur.fetchall()
        con.close()
        results = Custom.results_as_list(results)
        return results

    @staticmethod
    def delete_all_results():
        con = sqlite3.connect('question_bank.db')
        cur = con.cursor()
        cur.execute("DELETE FROM results")
        con.commit()
        con.close()

    @staticmethod
    def taken(questions):
        con = sqlite3.connect('question_bank.db')
        cur = con.cursor()
        for question in questions:
            cur.execute("UPDATE questions SET number_of_times_taken = \
            number_of_times_taken + 1 WHERE question = ?  AND question_type = ?", [question.question, question.question_type])
        con.commit()
        con.close()