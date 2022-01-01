import sqlite3

def create():
    con = sqlite3.connect('main.db')
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
        question VARCHAR(500),
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
    con.commit()
    con.close()


def generic_refresh(values, tree):
    """
    Delete everything and do a query and insert them over again
    """
    tree.delete_everything()
    for value in values:
        arg = list(value)
        tree.insert_args(arg)
    

def delete_element(_list, index):
    copy = _list
    element = _list[index]
    copy.remove(element)       
    return copy 

def replace_element(_list, current_element, desired_element):
    copy = []
    for element in _list:
        if element == current_element:
            copy.append(desired_element)
        else:
            copy.append(element)
    return copy

def del_first_and_last(_list):
    _list = _list[:-1]
    _list = _list[1:]
    return _list