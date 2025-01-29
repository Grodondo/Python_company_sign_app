import fpdf as FPDF

class PDF:
    def __init__(self, trabajadores, start_datetime, end_datetime):
        self.pdf_path = f"pdf/{start_datetime}_{end_datetime}.pdf"
        self.trabajadores = trabajadores
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

    def generate(self):
        """
        Generate the PDF document
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(40, 10, 'Hello World!')
        pdf.output(self.pdf_path)

    def get_text(self):
        return 'This is a PDF document'