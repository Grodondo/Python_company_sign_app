import fpdf
from datetime import datetime, timedelta
from db_py.queries import Query

class PDF:
    def __init__(self, trabajadores, start_datetime, end_datetime):
        self.trabajadores = trabajadores
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        
        self.total_time = 0
        
        # Formatear las fechas y horas para el nombre del archivo
        self.date_start_str = self._format_datetime(start_datetime, "yyyy-MM-dd_HH-mm-ss")
        self.date_end_str = self._format_datetime(end_datetime, "yyyy-MM-dd_HH-mm-ss")
        self.pdf_path = f"PDF/check_ins/check_ins_{self.date_start_str}-to-{self.date_end_str}.pdf"

    def _format_datetime(self, dt, format_str):
        """Maneja la conversión de QDateTime a cadena"""
        if hasattr(dt, 'dateTime'):
            return dt.dateTime().toString(format_str)
        return dt.toString(format_str)

    def generate(self):
        """Genera el reporte PDF con datos de check-in"""
        pdf = fpdf.FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Configurar estilo formal
        self._create_header(pdf)
        
        # Agregar secciones para cada trabajador
        for trabajador in self.trabajadores:
            self._add_worker_section(pdf, trabajador)
            
        self._add_footer(pdf)
        
        # Guardar PDF
        try:
            pdf.output(self.pdf_path)
            print(f"PDF generado: {self.pdf_path}")
        except Exception as e:
            print("Error al generar PDF:", e)

    def _create_header(self, pdf):
        """Agregar cabecera del reporte"""
        pdf.image('assets/logo.png', 15, 5, 25)
        pdf.ln(5)
        
        pdf.set_font('Times', 'B', 16)
        pdf.cell(0, 10, 'Reporte de Check-ins', 0, 1, 'C')
        
        pdf.set_font('Times', '', 12)
        start_str = self._format_datetime(self.start_datetime, "yyyy-MM-dd HH:mm:ss")
        end_str = self._format_datetime(self.end_datetime, "yyyy-MM-dd HH:mm:ss")
        pdf.cell(0, 10, f'Período: {start_str} - {end_str}', 0, 1, 'C')
        pdf.ln(15)

    def _add_worker_section(self, pdf, trabajador):
        worker_id = trabajador[0]
        nombre = f"{trabajador[1]} {trabajador[2]}"
        dni = trabajador[3]
        codigo = trabajador[4]
        estado = trabajador[5]

        # Cabecera del trabajador
        pdf.set_font('Times', 'B', 12)
        pdf.cell(0, 10, f'Trabajador: {nombre}', 0, 1)
        pdf.set_font('Times', '', 12)
        pdf.cell(0, 10, f'DNI: {dni} - Código: {codigo}', 0, 1)
        pdf.cell(0, 10, f'Estado Actual: {estado.upper()}', 0, 1)
        pdf.ln(5)
        
        # Obtener check-ins usando el método centralizado de consulta
        checkins = Query.entries_between_datetimes(
            'reloj',
            self._format_datetime(self.start_datetime, "yyyy-MM-dd HH:mm:ss"),
            self._format_datetime(self.end_datetime, "yyyy-MM-dd HH:mm:ss"),
            worker_id
        )
        
        # Procesar check-ins y obtener tiempo total
        total_seconds = 0
        if checkins:
            total_seconds = self._create_checkins_table(pdf, checkins)
        else:
            pdf.cell(0, 10, 'No se encontraron check-ins en este período.', 0, 1)
            pdf.ln(10)
        
        # Mostrar tiempo total
        total_time_str = self._format_elapsed(total_seconds)
        pdf.cell(0, 10, f'Tiempo total: {total_time_str}', 0, 1)
        pdf.ln(5)

        # Verificar salto de página
        if pdf.get_y() > 250:
            pdf.add_page()

    def _create_checkins_table(self, pdf, checkins):
        """Crear tabla formateada de check-ins y retornar el tiempo total acumulado"""
        pdf.set_font('Times', 'B', 11)
        col_widths = [40, 30, 30, 40]
        
        # Cabecera de la tabla
        pdf.cell(col_widths[0], 10, 'Fecha', 1, 0, 'C')
        pdf.cell(col_widths[1], 10, 'Hora', 1, 0, 'C')
        pdf.cell(col_widths[2], 10, 'Estado', 1, 0, 'C')
        pdf.cell(col_widths[3], 10, 'Tiempo Checkin', 1, 1, 'C')
        
        sorted_checkins = sorted(checkins, key=self._entry_to_datetime)
        
        pdf.set_font('Times', '', 11)
        last_in = None
        total_seconds = 0  # Inicializar el total de segundos
        for entry in sorted_checkins:
            dt = self._entry_to_datetime(entry)
            fecha_display = dt.strftime("%Y-%m-%d")
            hora_display = dt.strftime("%H:%M:%S")
            estado = entry[5].strip().lower()
            
            if estado == "in":
                last_in = dt
                elapsed_str = "----------"
            elif estado == "out":
                if last_in is not None:
                    elapsed = dt - last_in
                    elapsed_str = self._format_elapsed(elapsed)
                    total_seconds += int(elapsed.total_seconds())  # Acumular tiempo
                    last_in = None
                else:
                    elapsed_str = "N/A"
            else:
                elapsed_str = ""
            
            pdf.cell(col_widths[0], 10, fecha_display, 1, 0, 'C')
            pdf.cell(col_widths[1], 10, hora_display, 1, 0, 'C')
            pdf.cell(col_widths[2], 10, estado.upper(), 1, 0, 'C')
            pdf.cell(col_widths[3], 10, elapsed_str, 1, 1, 'C')
        
        pdf.ln(10)
        return total_seconds  # Retornar el total acumulado

    def _entry_to_datetime(self, entry):
        """Convierte una entrada de check-in a un objeto datetime."""
        fecha = entry[3]
        hora = entry[4]
        # Convertir la fecha si está en formato DD/MM/YYYY
        if '/' in fecha:
            day, month, year = fecha.split('/')
            fecha = f"{year}-{month}-{day}"
        dt_str = f"{fecha} {hora}"
        try:
            return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        
    def _format_elapsed(self, elapsed):
        """Formatea el tiempo transcurrido como Hh Mm Ss. Acepta timedelta o segundos."""
        if isinstance(elapsed, timedelta):
            total_seconds = int(elapsed.total_seconds())
        else:
            total_seconds = int(elapsed)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours}h {minutes}m {seconds}s"

    def _add_footer(self, pdf):
        """Agregar pie de página al reporte."""
        pdf.set_y(-15)
        pdf.set_font('Times', 'I', 8)
        pdf.cell(0, 10, f'Generado el {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 0, 'C')
