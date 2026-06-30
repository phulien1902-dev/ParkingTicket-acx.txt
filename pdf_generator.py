# pdf_generator.py

import os
from datetime import datetime

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Đăng ký font Unicode
pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))


class PDFGenerator:

    def __init__(self, output_folder):

        self.output_folder = output_folder

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    def create(self, tickets):

        pdf_file = os.path.join(
            self.output_folder,
            "PhieuGuiXe.pdf"
        )

        c = canvas.Canvas(pdf_file, pagesize=A4)

        page_width, page_height = A4

        cols = 2
        rows = 4

        margin = 20

        ticket_width = (page_width - margin * 2) / cols
        ticket_height = (page_height - margin * 2) / rows

        index = 0

        for ticket in tickets:

            page = index // (cols * rows)

            if page > 0 and index % 8 == 0:
                c.showPage()
                c.setFont("Arial", 10)

            pos = index % 8

            row = pos // cols
            col = pos % cols

            x = margin + col * ticket_width
            y = page_height - margin - (row + 1) * ticket_height

            self.draw_ticket(
                c,
                x,
                y,
                ticket_width,
                ticket_height,
                ticket
            )

            index += 1

        c.save()

        return pdf_file

    def draw_ticket(
            self,
            c,
            x,
            y,
            w,
            h,
            ticket
    ):

        c.rect(x, y, w, h)

        c.setFont("Arial", 12)

        c.drawCentredString(
            x + w / 2,
            y + h - 18,
            "CTY ABC"
        )

        c.setFont("Arial", 11)

        c.drawCentredString(
            x + w / 2,
            y + h - 38,
            "PHIẾU GỬI XE"
        )

        c.setFont("Arial", 10)

        c.drawString(
            x + 12,
            y + h - 65,
            f"Mã vé: {ticket['code']}"
        )

        c.drawString(
            x + 12,
            y + h - 82,
            "Ngày: " +
            datetime.now().strftime("%d/%m/%Y")
        )

        c.drawString(
            x + 12,
            y + h - 99,
            "Giờ : " +
            datetime.now().strftime("%H:%M")
        )

        qr_size = 80

        c.drawImage(
            ticket["file"],
            x + w - qr_size - 15,
            y + 35,
            qr_size,
            qr_size
        )

        c.drawString(
            x + 12,
            y + 30,
            "Biển số xe:"
        )

        c.line(
            x + 80,
            y + 28,
            x + 180,
            y + 28
        )

        c.setFont("Arial", 9)

        c.drawCentredString(
            x + w / 2,
            y + 10,
            ticket["code"]
        )