from bs4 import BeautifulSoup
import html2text

converter = html2text.HTML2Text()

def segment_html(html: str) -> list[str]:
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
    return segments