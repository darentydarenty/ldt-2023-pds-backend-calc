from app.internal.calculations.models import ReportResult

from borb.pdf import Document
from borb.pdf import PDF
from borb.toolkit.export.html_to_pdf.html_to_pdf import HTMLToPDF


class ReportGenerator:
    def __init__(self):
        pass

    def make_pdf(self, params: ReportResult):
        with open("", 'wb') as pdf_file:
            pass
