import PyPDF2
import re


def pdf_to_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_number in range(len(reader.pages)):
            text += reader.pages[page_number].extract_text()
    return text


titles = [
    "Methodology\n",
    "Methods\n",
    "Results\n",
    "Discussion\n",
    "Results and Discussion\n",
    "Discussion of the result\n",
]
pdf_path = "Det.pdf"  # Replace with the actual path to your PDF file
text = pdf_to_text(pdf_path)
print(text)
file_nam = "Det" + ".txt"
pattern = "|".join(titles)
matches = re.finditer(pattern, text, re.IGNORECASE)
extracted_text = []
start = 0
for match in matches:
    title = match.group()
    start_idx = match.end()
    if start != start_idx:
        extracted_text.append((title, text[start:start_idx].strip()))
        start = start_idx

    # Include the text after the last title
    extracted_text.append((titles[-1], text[start:].strip()))

print(len(extracted_text))
for i in extracted_text:
    print(i[0])
print(extracted_text[1])
# Write the full text to the text file
# with open(file_nam, "wb") as fil:
# fil.write(text.encode('utf-8'))
