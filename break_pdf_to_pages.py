from PyPDF2 import PdfReader, PdfWriter

# Input PDF file
input_pdf = "McKinley_Human Anatomy 6e-Final.pdf"

# Read the PDF
reader = PdfReader(input_pdf)

# Loop through all pages
for i in range(2):
    writer = PdfWriter()
    writer.add_page(reader.pages[i])
    
    # Save each page as a new PDF
    output_filename = f"page_{i+1}.pdf"
    with open(output_filename, "wb") as output_pdf:
        writer.write(output_pdf)

    print(f"Created: {output_filename}")