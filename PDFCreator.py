from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm, mm

pdf: canvas.Canvas
styles = getSampleStyleSheet()
#Register fonts:
# pdfmetrics.registerFont(TTFont('LiberationSans-Regular', 'LiberationSans-Regular.ttf'))
# pdfmetrics.registerFont(TTFont('SabonBol', 'SabonBol.ttf'))
# pdfmetrics.registerFont(TTFont('SabonIta', 'SabonIta.ttf'))
# pdfmetrics.registerFont(TTFont('SabonBolIta', 'SabonBolIta.ttf'))

def create_document(name: str, amount_of_pages: int, width: float, height: float) -> None:
    global pdf
    pdf = canvas.Canvas(filename=name+".pdf", pagesize=(width, height))
    print(f"Name: {pdf._filename}")


def set_to_pivot(pos: float, size: float, pivot: float) -> float:
    # top left is 0,0. bottom right is 1,1
    return pos - (size * pivot)


def draw_RTF_string(document_name, rtf_text: str, page_nr: int, font_family: str, font_size: float, font_style: int, alignment: int,
                    line_space: float, paragraph_space: float, pivot_x: float, pivot_y: float, size_x: float, size_y: float,
                    pos_x: float, pos_y: float) -> None:

    pdf.setFont('Helvetica', font_size)
    pdf.drawString(pos_x, pos_y, rtf_text)
    # print(font_family)
    # style = ParagraphStyle(document_name, fontName=font_family, fontSize=font_size, alignment=alignment)
    text = Paragraph(rtf_text, style)
    # pdf.drawText(text)
    # print(f"text: {text}")


def draw_image(document_name, image_path: str, page_nr, pivot_x: float, pivot_y: float, width: float, height: float, pos_x: float,
               pos_y: float, ) -> None:

    x = set_to_pivot(pos_x, width, pivot_x)
    y = set_to_pivot(pos_y, height, pivot_y)
    pdf.drawImage(image_path, x, y, width, height, preserveAspectRatio=True)
    print(f"image: {image_path}, loc: {(x, y)}")


def save_document() -> None:
    pdf.save()


# pdf.drawString(500, 500, "<b> hello! </b>")
# fonts = pdf.getAvailableFonts()
# print(fonts)
# pdf.save()

# def tuple_inter(a=(5, 2, 600, 1,2,3,4), b=(600,1,2,0,4)):
#     return sorted(list(set(b) - set(a)))

# print(tuple_inter())
