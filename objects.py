import sqlite3


# This is an abstract class. This class is just there to give other classes certain database related methods.
class Base:
    def __init__(self):
        self.table_name = ""
        self.columns = []

        if type(self) is Base:
            raise NotImplementedError("This is an abstract class and cannot be instantiated")
        assert type(self.table_name) is str and type(self.columns) is list or type(self.columns) is tuple

    def save(self, *values):
        """
        Save method builds a sql syntax from classes own table name, columns and given parameters.
        Every class should give certain values to this so that after an object initialised with this
        method they can be saved to database.
        """
        con = sqlite3.connect('question_bank.db')
        cur = con.cursor()

        for value in values:
            if value is None or value == '':
                return False

        sql_code = "INSERT OR IGNORE INTO " + self.table_name + "("
        last_element = self.columns[len(self.columns) - 1]

        for column in self.columns:
            if column == last_element:
                sql_code = sql_code + column
            else:
                sql_code = sql_code + column + ","

        sql_code = sql_code + ") VALUES("

        val_length = len(values)
        i = 0
        while i < val_length:
            value = values[i]
            if i == val_length - 1:
                try:
                    int(value)
                    sql_code = sql_code + "%s);" % value
                except:
                    sql_code = sql_code + "'%s');" % value
            else:
                try:
                    int(value)
                    sql_code = sql_code + "%s," % value
                except:
                    sql_code = sql_code + "'%s'," % value
            i += 1
        cur.execute(sql_code)
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
        value_length = len(values)
        sql_code = "DELETE FROM " + self.table_name + " WHERE "
        i = 0
        while i < value_length:
            column, value = self.columns[i], values[i]
            try:
                int(value)
                sql_code += "%s=%s" % (column, value)
            except:
                sql_code += "%s='%s'" % (column, value)
            is_end_of_query = i == value_length - 1
            if not is_end_of_query:
                sql_code += " AND "
            i += 1
        cur.execute(sql_code)
        con.commit()
        con.close()

    def get_id(self, *values):
        """
        Get id method builds a sql syntax just like other methods.After an object 
        initialised and saved. Object's id can be taken from the database with this method.
        """
        value_length = len(values)
        query = "SELECT id FROM " + self.table_name + " WHERE "
        i = 0

        while i < value_length:
            column, value = self.columns[i], values[i]
            try:
                int(value)
                query = query + "%s=%s" % (column, value)
            except:
                query = query + "%s='%s'" % (column, value)

            is_end_of_query = (i == value_length - 1)
            if not is_end_of_query:
                query += " AND "
            i += 1
        con = sqlite3.connect('question_bank.db')
        cur = con.cursor()
        cur.execute(query)
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
        query = "SELECT * FROM %s WHERE %s=%s" % (self.table_name, foreign_key_column, foreign_key)
        cur.execute(query)
        results = cur.fetchall()
        con.close()
        return results

    def update(self, pk, **kwargs):
        """
        This is a general update statement. This updates all the places that is given in the dictionary.
        """
        table_name = self.table_name
        sql_code = "UPDATE %s SET " % (table_name)

        for item in kwargs.items():
            column = item[0]
            value = item[1]
            if value is None or value == '':
                return False
            try:
                int(value)
                sql_code += "%s=%d," % (column, value)
            except:
                sql_code += "%s='%s'," % (column, value)

        sql_code = sql_code[:-1]
        sql_code += " WHERE id=%d " % pk
        con = sqlite3.connect('question_bank.db')
        cur = con.cursor()
        cur.execute(sql_code)
        con.commit()
        con.close()
        return True


# This is module. Modules are related to quizzes
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

    def get_question_from_db(self):
        con = sqlite3.connect('question_bank.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM questions WHERE quiz_id="" ")
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
        self.question = question
        self.question_type = question_type
        self.right_answers = []
        self.answers = answers
        self.table_name = "questions"
        self.columns = ["question", "question_type", "quiz_id"]

        if answers is not None:
            for answer in answers:
                if answer.iscorrect:
                    self.right_answers.append(answer)

        assert type(self.answers) is list or type(self.answers) is tuple or self.answers is None

        if answers is not None:
            assert len(self.right_answers), "There must be an at least one right answer"
            for answer, right_answer in self.answers, self.right_answers:
                assert type(answer) is Answer and type(right_answer) is Answer
            assert len(self.right_answers) != len(answers), 'Every answer cannot be correct.' \
                                                            ' Some of them must be wrong'

    def get_answers(self):
        return self.answers

    def set_answers(self, answers):
        self.answers = answers

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
        question = self.question
        foreign_key = related_class.get_id(module_class)
        return super().delete(question, foreign_key)

    def get_question_type(self):
        typ = self.question_type
        if typ in [1, 2, 3]:
            return typ
        elif typ == 'Multiple Answer Question':
            return 1
        elif typ == 'True False Question':
            return 2
        elif typ == 'Best Match Question':
            return 3
        else:
            raise ValueError("Value must be between 1-3")

    def get_id(self, quiz, module):
        question = self.question
        question_type = self.get_question_type()
        foreign_key = quiz.get_id(module)
        return super().get_id(question, question_type, foreign_key)

    def refresh(self, foreign_key):
        return super().refresh(self.columns[2], foreign_key)

    def update(self, quiz, module, old_object):
        pk = old_object.get_id(quiz, module)
        return super().update(pk, question=self.question, question_type=self.get_question_type())

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
            question.set_answers(copy)
            final.append(question)
        return final

# This is the answer of a question. Answers are related to modules
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
        return self.why_iscorrect

    def set_why_iscorrect(self, answer_why_iscorrect):
        self.why_iscorrect = answer_why_iscorrect

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
            name VARCHAR(50),
            UNIQUE(name)
            );
            """)
        cur.execute("""CREATE TABLE IF NOT EXISTS
            quizes(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name VARCHAR(50), 
            is_randomized INTEGER, 
            module_id INTEGER,
            UNIQUE(name, module_id),
            FOREIGN KEY(module_id) REFERENCES modules(id)
            );
            """)
        cur.execute("""CREATE TABLE IF NOT EXISTS 
            questions(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            question VARCHAR(50),
            question_type INTEGER,
            quiz_id INTEGER,
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
        cur.execute("INSERT INTO results(quiz_id, correct_answers, number_of_questions) VALUES(?, ?, ?)",
                    [pk, final_result, number_of_questions])
        con.commit()
        con.close()

    @staticmethod
    def results_as_list(results):
        values = []
        for result in results:
            correct_answers = result[0]
            number_of_questions = result[1]
            quiz = result[3]
            module = result[5]
            result = '%s / %s' % (correct_answers, number_of_questions)
            value = [result, quiz, module]
            values.append(value)
        return values

    @staticmethod
    def get_results():
        con = sqlite3.connect('question_bank.db')
        cur = con.cursor()
        cur.execute("""SELECT results.correct_answers, 
        results.number_of_questions, results.quiz_id, 
        quizes.name, quizes.module_id, modules.name
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
