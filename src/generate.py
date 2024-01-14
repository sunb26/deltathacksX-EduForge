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
      solution_regex = r"Solution:\s*(.*?)(\s*\[END\]|\n)"
    
    elif gen_type == "flashcard":
      # Regex patterns for extracting question and solution
      question_regex = r"Term:\s+(.*?)\n\nDefinition:"
      solution_regex = r"Definition:\s*(.*?)(\s*\[END\]|\n)"
      
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
    system_prompt = ""
    user_prompt = ""
    wrong_assistant_prompt = ""
    correct_assistant_prompt = ""
    prompt = ""
    try:
        with open('prompts.json', 'r') as file:
            data = json.load(file)
            cfgs = data["configs"]
            for cfg in cfgs:
                if cfg["type"] == gen_type:
                    system_prompt = cfg["system_prompt"]
                    user_prompt = cfg["user_prompt"]
                    wrong_assistant_prompt = cfg["wrong_assistant_prompt"]
                    correct_assistant_prompt = cfg["correct_assistant_prompt"]
                    prompt = cfg["new_prompt"]
                    break

    except FileNotFoundError:
        print("The file was not found")
    
    if not prompt:
        print("error: empty prompt")
        return []

    chat_history = [
        {"user_name": "system", "text": system_prompt},
        {"user_name": "user", "text": user_prompt},
        {"user_name": "chatbot", "text": wrong_assistant_prompt},
        {"user_name": "user", "text": "No that response is not formatted correctly. The end of the solution or definition must be marked with [END]. Please try again."},
        {"user_name": "chatbot", "text": correct_assistant_prompt}
    ]
    query_str = f'@topic:"{topic}" @user:"{user}"'

    index = r.ft("idx:notes")

    res = index.search(Query(query_str))

    qa_pairs = []
    counter = 0
    for result in res.docs:
        temp_chat_history = chat_history
        print(result)
        context = json.loads(result.json)["text"].replace("\n", " ")
        print(context)
        
        input_prompt = prompt.format(topic, context)
        print("Prompt: ", input_prompt)
        print("======================")
        print("Chat History: ", chat_history)
        print("======================")
        for i in range(2):
          response = co.chat(
            input_prompt, 
            chat_history=temp_chat_history,
            model="command", 
            temperature=0.0,
            prompt_truncation='AUTO'
          )

          print("Response: ", response.text)
          print("======================")
          q, a = parse_qa(gen_type, response.text)
          if q and a: 
            qa_pairs.append({"question": q, "answer": a})
            break
          
          else:
            temp_chat_history.append({"user_name": "user", "text": input_prompt}),
            temp_chat_history.append({"user_name": "chatbot", "text": response.text}),
            if gen_type == "qa":
              temp_chat_history.append({"user_name": "user", "text": "No that response is not formatted correctly. The format must be 'Question: [Question]\n Solution: [Solution] \n [END]'. The end of the solution must be marked with [END]. Please try again."}),
            elif gen_type == "flashcards":
              temp_chat_history.append({"user_name": "user", "text": "No that response is not formatted correctly. The format must be 'Term: [Term]\n Definition: [Definition] \n [END]'. The end of the definition must be marked with [END]. Please try again."}),

        if counter > 2:
          break
        counter += 1

    
    return qa_pairs
  



