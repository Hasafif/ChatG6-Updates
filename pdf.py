import PyPDF2


def pdf_to_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_number in range(len(reader.pages)):
            text += reader.pages[page_number].extract_text()
    return text


pdf_path = "Ass.pdf"  # Replace with the actual path to your PDF file
text = pdf_to_text(pdf_path)
print(text)
file_nam = "Ass2" + ".txt"

# Write the full text to the text file
with open(file_nam, "wb") as fil:
    fil.write(text.encode("utf-8"))
