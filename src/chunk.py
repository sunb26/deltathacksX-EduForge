from bs4 import BeautifulSoup
import html2text
from dotenv import load_dotenv
import os
import redis
from redis.commands.search.query import Query
import cohere
import json
import re

load_dotenv()

converter = html2text.HTML2Text()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

r = redis.Redis(
  host=REDIS_HOST,
  port=17885,
  password=REDIS_PASSWORD)



def chunk_html(topic: str, html: str) -> list[str]:
    # Convert markdown to HTML
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Iterate through the elements and associate headers with content
    headers = ['title', 'h1', 'h2']
    segments = []
    current_header = None
    for element in soup.children:
        if element.name in headers:
            current_header = element.getText()
            segments.append(element.getText())
        elif current_header:
            content = converter.handle(str(element))
            segments[-1] = segments[-1] + " " + content
    
    
    index = r.ft("idx:notes")
    for i, segment in enumerate(segments):
        r.json().set(f"notes:{i}", '$', {"user": "joe", "topic": topic, "text": segment})

    return segments