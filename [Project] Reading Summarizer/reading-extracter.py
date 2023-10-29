import PyPDF2
import os

os.system('clear')
# Open the PDF file in read-binary mode
pdf_file = open('pdfs/doing-theo-in-a-dumpsite.pdf', 'rb')
file_name = input("What would you like to name your file? ").lower()

# Create a PDF reader object
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Create a text file for writing
txt_file = open(f'{file_name}_summary.txt', 'w')

# Loop through each page and extract text
for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    txt_file.write(page.extract_text())

# Close the files
pdf_file.close()
txt_file.close()