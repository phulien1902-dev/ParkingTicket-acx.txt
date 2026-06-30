# ==========================================
# File: qr_generator.py
# ==========================================

import os
import json
from datetime import datetime

import qrcode
from qrcode.constants import ERROR_CORRECT_M


class QRGenerator:
    """
    Tạo QR Code cho phiếu gửi xe
    """

    def __init__(self, output_folder):

        self.output_folder = output_folder

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    # -----------------------------------------

    def create_one(self, ticket_code):
        """
        Tạo một QR Code
        """

        now = datetime.now()

        data = {
            "Cty": "Cty ABC",
            "ticket": ticket_code,
            "date": now.strftime("%d/%m/%Y"),
            "time": now.strftime("%H:%M:%S")
        }

        qr = qrcode.QRCode(
            version=2,
            error_correction=ERROR_CORRECT_M,
            box_size=8,
            border=3
        )

        qr.add_data(
            json.dumps(
                data,
                ensure_ascii=False
            )
        )

        qr.make(fit=True)

        img = qr.make_image(
            fill_color="black",
            back_color="white"
        )

        filename = os.path.join(
            self.output_folder,
            ticket_code + ".png"
        )

        img.save(filename)

        return {
            "code": ticket_code,
            "file": filename,
            "date": now.strftime("%d/%m/%Y"),
            "time": now.strftime("%H:%M:%S")
        }

    # -----------------------------------------

    def create_many(
            self,
            amount=100,
            prefix="PK",
            start_number=1):

        tickets = []

        for i in range(start_number, start_number + amount):

            ticket_code = f"{prefix}{i:06d}"

            ticket = self.create_one(ticket_code)

            tickets.append(ticket)

        return tickets


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    qr = QRGenerator("qr")

    tickets = qr.create_many(
        amount=100,
        prefix="PK"
    )

    print("Đã tạo", len(tickets), "QR Code")

    for t in tickets[:5]:
        print(t)