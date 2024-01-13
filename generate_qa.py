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


def parse_qa(text: str) -> (str, str):
    """
    Parses a question and answer pair from LLM response into a question and answer.
    """


    # Regex patterns for extracting question and solution
    question_regex = r"Question:\s+(.*?)\n\nSolution:"
    solution_regex = r"Solution:\s*(.*?)\s*\[END\]"

    # Finding and extracting the question and solution using regex
    question_match = re.search(question_regex, text, re.DOTALL)
    solution_match = re.search(solution_regex, text, re.DOTALL)

    question_text = question_match.group(1) if question_match else None
    solution_text = solution_match.group(1) if solution_match else None
    
    
    return question_text, solution_text


def generate_practice_qa(user: str, topic: str) -> [str]:
    """
    Generates a question and answer pair for a given user and topic.
    """

    query_str = f'@topic:"{topic}" @user:"{user}"'

    index = r.ft("idx:notes")

    res = index.search(Query(query_str))

    qa_pairs = []
    for result in res.docs:
        context = json.loads(result.json)

        prompt = f"""You are a professor who is an expert in the field of {topic}. Given the following context related to {topic}, come up with a question that you would ask your students to test their understanding of the topic. You can assume that your students have a basic understanding of the topic.
        After providing the question, write out a step-by-step comprehensive solution in detail. It is critical that your solution is correct. Return your response in the provided format. Please denote the end of step-by-step solution by appending [END] to the end of your solution:
        

        Example Response Format (DO NOT INCLUDE AS CONTEXT IN YOUR RESPONSE):

        Question: Why is the sky blue?

        Solution: The sky is blue because of Rayleigh scattering. [END]


        Context: {context}
        
        
        """
        
        print(prompt)
        response = co.chat(
          prompt, 
          model="command", 
          temperature=0.0
        )

        print("Response: ", response)
        q, a = parse_qa(response.text)

        qa_pairs.append({"question": q, "answer": a})

    
    return qa_pairs


print(generate_practice_qa("joe", "example topic"))



