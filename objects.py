import sqlite3

class Base:
    def __init__(self):
        self.table_name = "This must be Over written"
        self.columns = []
        assert self.table_name is str and self.columns is list or self.columns is tuple
    
    def save(self, *values):
        con = sqlite3.connect('main.db')
        cur = con.cursor()
        sql_code = "INSERT OR IGNORE INTO %s("%(self.table_name)
        last_element = self.columns[len(self.columns) -1]

        for column in self.columns:
            if column == last_element:
                sql_code = sql_code + column
            else:
                sql_code = sql_code + column+ ","
        
        sql_code = sql_code + ") VALUES("
        
        last_element = values[len(values) -1]
        for value in values:
            if value == last_element:
                sql_code = sql_code + "'%s');" %value
            else:
                sql_code = sql_code + value + "," 
        cur.execute(sql_code)
        con.commit()
        con.close()
            
    def delete(self, *values):
        value_length, column_length = len(values), len(self.columns)
        assert value_length == column_length

        con = sqlite3.connect('main.db')
        cur = con.cursor()
        sql_code = "DELETE FROM %s WHERE "%(self.table_name)
        i = 0
        last_element = self.columns[column_length -1] 

        while i < value_length:
            column, value = self.columns[i], values[i]
            if last_element == column:
                sql_code = sql_code + "%s='%s';"%(column, value)
            else:
                sql_code = sql_code + "%s='%s' AND"%(column, value)
            i += 1
        cur.execute(sql_code)
        con.commit()
        con.close()

    def get_id(self, *values):
        value_length, column_length = len(values), len(self.columns)
        assert value_length == column_length        

        con = sqlite3.connect('main.db')
        cur = con.cursor()
        
        query = "SELECT id FROM " + self.table_name + " WHERE "
        i = 0
        last_element = self.columns[column_length -1] 

        while i < value_length:
            column, value = self.columns[i], values[i]
            if last_element == self.columns[i]:
                query = query + "%s='%s';"%(column, value)
            else:
                query = query + "%s='%s' AND"%(column, value)
            i +=1
        cur.execute(query)
        id = cur.fetchone()
        con.close()
        return id

    def refresh(self, foreign_key_column, foreign_key):        
        con = sqlite3.connect('main.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM %s WHERE %s='%s'", [self.table_name, foreign_key_column, foreign_key])
        results = cur.fetchall()
        con.close()
        return results
           

#This is module. Every module is related to a subject and it has questions
class Module(Base):
    def __init__(self, name=None, quizes=None):
        self.name = name
        self.quizes = quizes
        self.table_name = "modules"
        self.columns = ["name"]

        assert self.quizes is list or self.quizes is tuple or self.quizes is None
        
        if self.quizes is not None:
            for quiz in self.quizes:
                assert quiz is Quiz
        
    def get_name(self):
        return self.name

    def set_name(self, module_name):
        self.name = module_name
    
    def get_quizes(self):
        return self.quizes

    def set_quiz(self, quiz):
        if self.quizes is None:
            self.quizes = []
            self.quizes.append(quiz)
        else:
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

#This is the quiz. A quiz have a name and a module it also may have multiple modules.
#The quiz can have selected questions or questions can be randomized
class Quiz(Base):
    def __init__(self, name, questions=None, israndomized=False):
        self.name = name
        self.questions = questions
        self.israndomized = israndomized
        self.table_name ="quizes"
        self.columns = ["name", "is_randomized", "module_id"]

        assert self.israndomized is bool, "This argument must be a boolean"
        assert self.questions is list or self.questions is tuple or self.questions is None, "This argument must be a list or tuple"
        assert self.name is str, "This argument must be a string"
        assert len(self.questions) > 1, "A Quiz cannot have a single question"
        
        if self.questions is not None:
            for question in self.questions:
                assert question is Question or \
                    question is TrueOrFalseQuestion or\
                    question is MultipleAnswerQuestion  or\
                    question is StandardQuestion

    def get_name(self):
        return self.name
    
    def set_name(self, quiz_name):
        self.name = quiz_name
    
    def get_questions(self):
        return self.questions

    def set_questions(self, quiz_questions):
        self.questions = quiz_questions
    
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
        return super().delete(name, israndomized, foreign_key)

    def get_id(self, related_class):
        name, israndomized = self.name, self.israndomized
        foreign_key = related_class.get_id()
        id = super().get_id(name, israndomized,foreign_key)
        return id

    def refresh(self, foreign_key):
        return super().refresh(self.columns[2], foreign_key)

#Every question needs a text. question parameter stands for the question itself.
class Question(Base):
    def __init__(self, question, answers=None):
        self.question = question 
        self.right_answers = []
        self.answers = answers
        self.table_name = "questions"
        self.columns = ["question", "quiz_id"]

        if answers is not None:
            for answer in answers:
                if answer.iscorrect:
                    self.right_answers.append(answer)
            
        assert self.question is str, "Question must be string"
        assert self.answers is list or self.answers is tuple or self.answers is None
        
        if answers is not None:
            assert len(self.right_answers), "There must be an at least one right answer"
            for answer, right_answer in self.answers, self.right_answers:
                assert answer is Answer and right_answer is Answer
        
    def get_answers(self):
        return self.answers

    def set_answer(self, *args):
        for arg in args:
            self.answers.append(arg)
    
    def get_question(self):
        return self.question
    
    def set_question(self, question_itself):
        self.question = question_itself
    
    def get_right_answers(self):
        return self.right_answers

    def save(self, related_class):
        question= self.question
        foreign_key = related_class.get_id()
        super().save(question, foreign_key)    

    def delete(self, related_class):
        question= self.question
        foreign_key = related_class.get_id()
        return super().delete(question, foreign_key)

    def get_id(self, related_class):
        question= self.question
        foreign_key = related_class.get_id()
        id = super().get_id(question,foreign_key)
        return id

    def refresh(self, foreign_key):
        return super().refresh(self.columns[1], foreign_key)
    
#This is multiple answer question. It can have multiple true answers and number of answers are not standard.
class MultipleAnswerQuestion(Question):
    def __init__(self, question,answers):
        super().__init__(question, answers)
        
        if self.answers is not None:
            assert len(self.right_answers) != len(answers),'Every answer cannot be correct.'\
                                                                ' Some of them must be wrong'
    
        

#This is the standard question. This question has four answers and only one of them can be true
class StandardQuestion(Question):
    def __init__(self, question,answers):
        super().__init__(question, answers)

        if self.answers is not None:
            assert len(answers) == 4, "Please write four answers"
            assert len(self.right_answers) == 1,'You add more or less than one correct answers.'\
                                                        'Please change the question type or'\
                                                        ' delete some of the answers'
    def get_right_answers(self):
        return self.right_answers[0]



#This is the true or false question and it only has two answers and just one of them can be true
class TrueOrFalseQuestion(Question):
    def __init__(self, question, answers):
        super().__init__(question, answers)

        if self.question is not None:
            assert len(self.answers) == 2, "There cannot be more than two answers"
            assert len(self.right_answers) == 1,'You add more or less than one correct answers.'\
                                                    'Please change the question type or'\
                                                        ' delete some of the answers'    

    def get_right_answers(self):
        return self.right_answers[0]
        
        

#This is the answer of an question. Answers are related to modules
class Answer(Base):
    def __init__(self, description, iscorrect, why_iscorrect):
        self.description = description
        self.iscorrect = iscorrect
        self.why_iscorrect = why_iscorrect
        self.table_name ="answers"
        self.columns =["description", "iscorrect", "why_iscorrect", "question_id"]
        assert self.description is str 
        assert self.why_iscorrect is str, "Description and Why the question is correct must be a string"
        assert self.iscorrect is bool, "Is correct attribute must be boolean"

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
    
    def save(self, related_class):
        iscorrect, description, why_iscorrect= self.iscorrect, self.description, self.why_iscorrect
        foreign_key = related_class.get_id()
        super().save(iscorrect, description, why_iscorrect, foreign_key)    

    def delete(self, related_class):
        iscorrect, description, why_iscorrect= self.iscorrect, self.description, self.why_iscorrect
        foreign_key = related_class.get_id()
        return super().delete(iscorrect, description, why_iscorrect, foreign_key)

    def get_id(self, related_class):
        iscorrect, description, why_iscorrect= self.iscorrect, self.description, self.why_iscorrect
        foreign_key = related_class.get_id()
        id = super().get_id(iscorrect, description, why_iscorrect,foreign_key)
        return id
    
    def refresh(self, foreign_key):
        return super().refresh(self.columns[3], foreign_key)