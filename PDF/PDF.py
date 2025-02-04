import fpdf
from datetime import datetime
from db_py.queries import Query

class PDF:
    def __init__(self, trabajadores, start_datetime, end_datetime):
        self.trabajadores = trabajadores
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        
        # Format datetimes for filename
        self.date_start_str = self._format_datetime(start_datetime, "yyyy-MM-dd_HH-mm-ss")
        self.date_end_str = self._format_datetime(end_datetime, "yyyy-MM-dd_HH-mm-ss")
        self.pdf_path = f"PDF/check_ins/check_ins_{self.date_start_str}-to-{self.date_end_str}.pdf"

    def _format_datetime(self, dt, format_str):
        """Handle QDateTime to string conversion"""
        if hasattr(dt, 'dateTime'):
            return dt.dateTime().toString(format_str)
        return dt.toString(format_str)

    def generate(self):
        """Generate PDF report with check-in data"""
        pdf = fpdf.FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Set formal styling
        self._create_header(pdf)
        
        # Add worker sections
        for trabajador in self.trabajadores:
            self._add_worker_section(pdf, trabajador)
            
        self._add_footer(pdf)
        
        # Save PDF
        try:
            pdf.output(self.pdf_path)
            print(f"PDF generado: {self.pdf_path}")
        except Exception as e:
            print("Error al generar PDF:", e)

    def _create_header(self, pdf):
        """Add report header"""
        pdf.image('logo.png', 15, 5, 25)
        pdf.ln(5)
        
        pdf.set_font('Times', 'B', 16)
        pdf.cell(0, 10, 'Reporte de Check-ins', 0, 1, 'C')
        
        pdf.set_font('Times', '', 12)
        start_str = self._format_datetime(self.start_datetime, "yyyy-MM-dd HH:mm:ss")
        end_str = self._format_datetime(self.end_datetime, "yyyy-MM-dd HH:mm:ss")
        pdf.cell(0, 10, f'Período: {start_str} - {end_str}', 0, 1, 'C')
        pdf.ln(15)

    def _add_worker_section(self, pdf, trabajador):
        """Add section for each worker"""
        worker_id = trabajador[0]
        nombre = f"{trabajador[1]} {trabajador[2]}"
        dni = trabajador[3]
        codigo = trabajador[4]
        estado = trabajador[5]

        # Worker header
        pdf.set_font('Times', 'B', 12)
        pdf.cell(0, 10, f'Trabajador: {nombre}', 0, 1)
        pdf.set_font('Times', '', 12)
        pdf.cell(0, 10, f'DNI: {dni} - Código: {codigo}', 0, 1)
        pdf.cell(0, 10, f'Estado Actual: {estado.upper()}', 0, 1)
        pdf.ln(5)

        # Get check-ins using centralized query method
        checkins = Query.entries_between_datetimes(
            'reloj',
            self._format_datetime(self.start_datetime, "yyyy-MM-dd HH:mm:ss"),
            self._format_datetime(self.end_datetime, "yyyy-MM-dd HH:mm:ss"),
            worker_id
        )
        
        # Add check-in table
        if checkins:
            self._create_checkins_table(pdf, checkins)
        else:
            pdf.cell(0, 10, 'No se encontraron check-ins en este período.', 0, 1)
            pdf.ln(10)

        # Page break check
        if pdf.get_y() > 250:
            pdf.add_page()

    def _create_checkins_table(self, pdf, checkins):
        """Create formatted check-ins table"""
        pdf.set_font('Times', 'B', 11)
        col_widths = [60, 40, 30]
        
        # Table header
        pdf.cell(col_widths[0], 10, 'Fecha', 1, 0, 'C')
        pdf.cell(col_widths[1], 10, 'Hora', 1, 0, 'C')
        pdf.cell(col_widths[2], 10, 'Estado', 1, 1, 'C')
        
        # Table rows
        pdf.set_font('Times', '', 11)
        for entry in checkins:
            fecha = entry[3]  # Assuming fecha is at index 3
            hora = entry[4]   # Assuming hora is at index 4
            estado = entry[5] # Assuming estado is at index 5
            
            # Format date if necessary (DD/MM/YYYY to YYYY-MM-DD)
            if len(fecha.split('/')) == 3:
                day, month, year = fecha.split('/')
                fecha = f"{year}-{month}-{day}"
            
            pdf.cell(col_widths[0], 10, fecha, 1)
            pdf.cell(col_widths[1], 10, hora, 1)
            pdf.cell(col_widths[2], 10, estado.upper(), 1, 1)
        
        pdf.ln(10)

    def _add_footer(self, pdf):
        """Add report footer"""
        pdf.set_y(-15)
        pdf.set_font('Times', 'I', 8)
        pdf.cell(0, 10, f'Generado el {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 0, 'C')

    def get_text(self):
        return 'Documento PDF generado'