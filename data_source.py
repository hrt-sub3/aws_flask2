import mysql.connector

connect = mysql.connector.connect(
    host="localhost",
    user="flask",
    password="password",
    database="hrt_sub")

cursor = connect.cursor()
INSERT_PROG_SQL = "INSERT INTO programs (lang, src, exec) VALUES (%s, %s, %s)"
GET_ID_LIST_SQL = "SELECT id FROM programs"
GET_LAST_ID_SQL = "SELECT LAST_INSERT_ID() from programs;"
GET_LANG_SQL = "SELECT lang FROM programs WHERE id = %s"
GET_PROG_SQL = "SELECT src, exec FROM programs WHERE id = %s"
GET_SRC_SQL = "SELECT src FROM programs WHERE id = %s"
GET_EXEC_SQL = "SELECT exec FROM programs WHERE id = %s"
DELETE_PROG_SQL = "DELETE FROM programs WHERE id = %s;"


def init_cursor():
    cursor.execute("USE hrt_sub")
    connect.commit()

def insert_program(lang, src, exe):
    cursor.execute(INSERT_PROG_SQL, (lang, src, exe))
    connect.commit()
    cursor.execute(GET_LAST_ID_SQL)
    return cursor.fetchone()[0]

def get_id_list():
    cursor.execute(GET_ID_LIST_SQL)
    rows = cursor.fetchall()
    res = list(map(lambda r: r[0], rows))
    return res

def get_lang(id):
    cursor.execute(GET_LANG_SQL, (id,))
    row = cursor.fetchone()
    return row[0]

def get_program(id):
    cursor.execute(GET_PROG_SQL, (id,))
    row = cursor.fetchone()
    return row[0], row[1]

def get_src(id):
    cursor.execute(GET_SRC_SQL, (id,))
    row = cursor.fetchone()
    return row[0]

def get_exec(id):
    cursor.execute(GET_EXEC_SQL, (id,))
    row = cursor.fetchone()
    return row[0]

def delete_program(id):
    cursor.execute(DELETE_PROG_SQL, (id,))
    connect.commit()