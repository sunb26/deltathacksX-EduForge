import fitz

def classify_text(text: str, font_size: str) -> str:
    if font_size >= 18:
        return f"<h1>{text}</h1>"
    else:
        return f"<p>{text}</p>"

def pdf_to_html_with_headers(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    html_content = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if block["type"] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        
                        # Skip spans that are just a bullet point
                        if text == "-":
                            continue

                        font_size = span["size"]
                        html_text = classify_text(text, font_size)
                        html_content.append(html_text)

    doc.close()
    return "".join(html_content)

