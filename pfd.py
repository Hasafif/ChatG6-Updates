import pdfplumber

def extract_text_from_pdf(pdf_path, output_path):
    with pdfplumber.open(pdf_path) as pdf:
        with open(output_path, 'w', encoding='utf-8') as file:
            for page in pdf.pages:
                text = page.extract_text()
                file.write(text)

# Provide the paths to your PDF file and output text file
pdf_path = "Com.pdf"
output_path = "Com.txt"

# Call the function to extract and write the text
extract_text_from_pdf(pdf_path, output_path)
