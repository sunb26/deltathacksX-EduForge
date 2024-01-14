from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def pdfCreate(text, topic):
    # pdf folder path
    pdf_folder_path = os.path.join(os.getcwd(), "pdfs")
    os.makedirs(pdf_folder_path, exist_ok=True)
    pdf_file_path = os.path.join(pdf_folder_path, f"{topic}.pdf")

    # Create a PDF document with the specified filename
    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)

    # Create a list to hold the flowables (content elements) of the document
    story = []

    # Define the text string
    textString = text
    
    # Create a style for the text
    style = getSampleStyleSheet()['Normal']

    # Split the text into paragraphs based on the delimiter '\n\n'
    paragraphs = textString.split('\n')

    # Create a Paragraph object for each paragraph and add it to the story
    for paragraph_text in paragraphs:
        paragraph = Paragraph(paragraph_text, style)
        story.append(paragraph)
        # Add some space between paragraphs
        story.append(Spacer(1, 12))

    # Build the PDF document
    doc.build(story)

