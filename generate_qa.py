from dotenv import load_dotenv
import os
import redis
from redis.commands.search.query import Query
import cohere
import json
import re

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


r = redis.Redis(
  host=REDIS_HOST,
  port=17885,
  password=REDIS_PASSWORD)

co = cohere.Client(COHERE_API_KEY)


def parse_qa(gen_type: str, text: str) -> (str, str):
    """
    Parses a question and answer pair from LLM response into a question and answer.
    """
    question_regex, solution_regex = "", ""

    if gen_type == "qa":
      # Regex patterns for extracting question and solution
      question_regex = r"Question:\s+(.*?)\n\nSolution:"
      solution_regex = r"Solution:\s*(.*?)\s*\[END\]"
    
    elif gen_type == "flashcard":
      # Regex patterns for extracting question and solution
      question_regex = r"Term:\s+(.*?)\n\nSolution:"
      solution_regex = r"Definition:\s*(.*?)\s*\[END\]"
      
    # Finding and extracting the question and solution using regex
    question_match = re.search(question_regex, text, re.DOTALL)
    solution_match = re.search(solution_regex, text, re.DOTALL)

    question_text = question_match.group(1) if question_match else None
    solution_text = solution_match.group(1) if solution_match else None
    
    return question_text, solution_text


def generate(gen_type: str, user: str, topic: str) -> [str]:
    """
    Generates a question and answer pair for a given user and topic.
    """

    query_str = f'@topic:"{topic}" @user:"{user}"'

    index = r.ft("idx:notes")

    res = index.search(Query(query_str))

    qa_pairs = []
    for result in res.docs:
        context = json.loads(result.json)
        
        prompt = prompt.format(topic, topic, context)
        response = co.chat(
          prompt, 
          model="command", 
          temperature=0.0
        )

        print("Response: ", response)
        q, a = parse_qa(gen_type, response.text)

        qa_pairs.append({"question": q, "answer": a})

    
    return qa_pairs
  

print(generate("joe", "example topic"))



