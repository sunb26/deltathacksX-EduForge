import psycopg2
from psycopg2 import Error
import re
from dotenv import load_dotenv
import os
from typing import List, Tuple

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

def read_qa(username: str, topic: str) -> List[Tuple[str, str]]:
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, sslmode=sslmode)
    cur = conn.cursor()
    try:
        cur.execute("SELECT question, answer FROM qa WHERE username = %s AND topic = %s", (username, topic))
        rows = cur.fetchall()
        qa_pairs = [(row[0], row[1]) for row in rows]  

    except psycopg2.Error as e:  
        print(f"An error occurred: {e}")
        conn.rollback()
        return []

    finally:
        cur.close()
        conn.close()

    return qa_pairs

def read_flashcard(username:str, topic:str) -> List[Tuple[str, str]]:
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, sslmode=sslmode)
    cur = conn.cursor()
    try:
        cur.execute("SELECT term, def FROM flashcards WHERE username = %s AND topic = %s", (username, topic))
        rows = cur.fetchall()
        td_pairs = [(row[0], row[1]) for row in rows] 

    except psycopg2.Error as e: 
        print(f"An error occurred: {e}")
        conn.rollback()
        return []

    finally:
        cur.close()
        conn.close()

    return td_pairs



