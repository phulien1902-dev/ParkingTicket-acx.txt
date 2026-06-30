import os
import customtkinter as ctk
from tkinter import filedialog, messagebox, StringVar

from qr_generator import QRGenerator
from pdf_generator import PDFGenerator
from excel_generator import ExcelGenerator


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Tạo phiếu gửi xe")
        self.geometry("900x600")

        self.output_folder = ""

        self.build_ui()

    # ================= UI =================
    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="CTY ABC",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=10)

        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame, text="Số lượng vé").grid(row=0, column=0, padx=10, pady=10)
        self.amount = ctk.CTkEntry(frame, width=120)
        self.amount.insert(0, "100")
        self.amount.grid(row=0, column=1)

        ctk.CTkLabel(frame, text="Tiền tố").grid(row=1, column=0, padx=10, pady=10)
        self.prefix = ctk.CTkEntry(frame, width=120)
        self.prefix.insert(0, "PK")
        self.prefix.grid(row=1, column=1)

        ctk.CTkLabel(frame, text="Thư mục").grid(row=2, column=0, padx=10, pady=10)

        self.path = StringVar()
        self.path_entry = ctk.CTkEntry(frame, textvariable=self.path, width=350)
        self.path_entry.grid(row=2, column=1)

        ctk.CTkButton(frame, text="Chọn", command=self.choose_folder).grid(row=2, column=2, padx=10)

        # ===== Buttons =====
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="TẠO VÉ", command=self.generate_all, fg_color="green").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="MỞ THƯ MỤC", command=self.open_folder).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="THOÁT", command=self.destroy, fg_color="red").pack(side="left", padx=10)

        # ===== Progress =====
        self.progress = ctk.CTkProgressBar(self, width=600)
        self.progress.pack(pady=10)
        self.progress.set(0)

        # ===== Log =====
        self.log_box = ctk.CTkTextbox(self, height=200)
        self.log_box.pack(fill="both", expand=True, padx=20, pady=10)

        self.log("Sẵn sàng.")

    # ================= Helpers =================
    def log(self, msg):
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = folder
            self.path.set(folder)

    # ================= MAIN PROCESS =================
    def generate_all(self):

        if not self.output_folder:
            messagebox.showwarning("Thiếu thư mục", "Hãy chọn thư mục lưu!")
            return

        try:
            amount = int(self.amount.get())
            prefix = self.prefix.get()

            self.progress.set(0.1)
            self.log("Bắt đầu tạo QR...")

            qr_folder = os.path.join(self.output_folder, "qr")
            qr = QRGenerator(qr_folder)
            tickets = qr.create_many(amount, prefix)

            self.progress.set(0.4)
            self.log("Đã tạo QR xong.")

            self.log("Đang tạo Excel...")
            excel = ExcelGenerator(self.output_folder)
            excel_file = excel.create(tickets)

            self.progress.set(0.7)
            self.log("Đã tạo Excel.")

            self.log("Đang tạo PDF...")
            pdf = PDFGenerator(self.output_folder)
            pdf_file = pdf.create(tickets)

            self.progress.set(1.0)
            self.log("Hoàn thành!")

            messagebox.showinfo(
                "Xong",
                f"Tạo xong!\n\nPDF: {pdf_file}\nExcel: {excel_file}"
            )

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def open_folder(self):
        if self.output_folder:
            os.startfile(self.output_folder)