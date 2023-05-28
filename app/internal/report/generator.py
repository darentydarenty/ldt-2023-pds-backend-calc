from app.internal.calculations.models import ReportDAO


from re import template
import pdfrw


def make_pdf(input_pdf_path: str, output_pdf_path: str, report: ReportDAO) -> bool:
    ANNOT_KEY = '/Annots'
    ANNOT_FIELD_KEY = '/T'  # name
    ANNOT_FORM_type = '/FT'  # Form type (e.g. text/button)
    ANNOT_FORM_button = '/Btn'  # ID for buttons, i.e. a checkbox
    ANNOT_FORM_text = '/Tx'  # ID for textbox
    SUBTYPE_KEY = '/Subtype'
    WIDGET_SUBTYPE_KEY = '/Widget'

    data_dict = report.dict()
    for i in list(data_dict.keys()):
        data_dict[i] = str(data_dict[i])

    template_pdf = pdfrw.PdfReader(input_pdf_path)
    i = 0
    for Page in template_pdf.pages:
        if Page[ANNOT_KEY]:
            for annotation in Page[ANNOT_KEY]:
                print("Annotation: ", annotation)
                if annotation[ANNOT_FIELD_KEY] and annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]  # Remove parentheses
                    if key in data_dict.keys():
                        i += 1
                        if annotation[ANNOT_FORM_type] == ANNOT_FORM_button:
                            annotation.update(
                                pdfrw.PdfDict(V=pdfrw.PdfName(data_dict[key]), AS=pdfrw.PdfName(data_dict[key])))
                        elif annotation[ANNOT_FORM_type] == ANNOT_FORM_text:
                            annotation.update(pdfrw.PdfDict(V=data_dict[key], AP=data_dict[key]))
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

    return True
