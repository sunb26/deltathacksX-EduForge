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


def read_topic(username: str) -> [str]:
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, sslmode=sslmode)
    cur = conn.cursor()
    try:
        cur.execute("SELECT topic FROM topics WHERE username = %s", (username,))
        rows = cur.fetchall()
        topics = [row[0] for row in rows] 

    except Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
        return []

    finally:
        cur.close()
        conn.close()

    return topics

def read_qa(user: str) -> [dict]:
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, sslmode=sslmode)
    cur = conn.cursor()
    try:
        cur.execute("SELECT topics FROM topics WHERE username = %s", (user,))
        rows = cur.fetchall()
        topics = [row[0] for row in rows] 

    except Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
        return []

    finally:
        cur.close()
        conn.close()

    return topics

    conn.commit()
    cur.close()
    conn.close()
    return None

def read_flashcard(user:str, topic:str, flashcard_list: list) -> Error:
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




