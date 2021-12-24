import sqlite3

def create():
    con = sqlite3.connect('main.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS 
        modules(
        id INTEGER PRIMARY KEY, 
        name VARCHAR(50),
        UNIQUE(name)
        );
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS
        quizes(
        id INTEGER PRIMARY KEY, 
        name VARCHAR(50), 
        is_randomized INTEGER, 
        module_id INTEGER,
        UNIQUE(name, module_id),
        FOREIGN KEY(module_id) REFERENCES modules(id)
        );
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS 
        questions(
        id INTEGER PRIMARY KEY, 
        question VARCHAR(500),
        quiz_id INTEGER,
        UNIQUE(question, quiz_id),
        FOREIGN KEY(quiz_id) REFERENCES quizes(id));
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS 
        answers(
        id INTEGER PRIMARY KEY, 
        description VARCHAR(500),
        iscorrect INTEGER,
        why_iscorrect VARCHAR(500),
        question_id INTEGER,
        UNIQUE(description, question_id)
        FOREIGN KEY(question_id) REFERENCES questions(id));
        """)
    con.commit()
    con.close()
