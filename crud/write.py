import psycopg2
from psycopg2 import Error
import re
from dotenv import load_dotenv
import os

load_dotenv()

pattern = r"postgresql://([^:]+):([^@]+)@([^/]+)/([^?]+)\?sslmode=(.+)"
db_string = os.getenv("DB_URL")

match = re.search(pattern, db_string)
if match:
    user = match.group(1)
    password = match.group(2)
    host = match.group(3)
    dbname = match.group(4)
    sslmode = match.group(5)
else:
    raise ValueError("Invalid database connection string format")


def new_topic(user:str, topic:str) -> bool:
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, sslmode=sslmode)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO topics (username, topic) VALUES (%s, %s)", (user, topic))
    except Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
        return Error

    conn.commit()
    cur.close()
    conn.close()
    return None

def new_qa(user:str, topic:str, qa_list: list) -> bool:
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, sslmode=sslmode)
    cur = conn.cursor()

    for qa in qa_list:
        q = qa["term"]
        a = qa["definition"]
        try:
            cur.execute("INSERT INTO qa (username, topic, question, answer) VALUES (%s, %s, %s, %s)", (user, topic, q, a))
        except Error as e:
            print(f"An error occurred: {e}")
            conn.rollback()
            return Error

    conn.commit()
    cur.close()
    conn.close()
    return None

def new_flashcard(user:str, topic:str, flashcard_list: list) -> Error:
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, sslmode=sslmode)
    cur = conn.cursor()

    for flashcard in flashcard_list:
        term = flashcard["term"]
        definition = flashcard["definition"]
        try:
            cur.execute("INSERT INTO flashcard (username, topic, term, definition) VALUES (%s, %s, %s, %s)", (user, topic, term, definition))
        except Error as e:
            print(f"An error occurred: {e}")
            conn.rollback()
            return Error

    conn.commit()
    cur.close()
    conn.close()
    return None




