# ==========================================
# File: main.py
# Project: Parking Ticket Generator
# Cty ABC
# ==========================================

import customtkinter as ctk
from gui import App


def main():

    # Giao diện
    ctk.set_appearance_mode("light")      # light / dark / system
    ctk.set_default_color_theme("blue")   # blue / green / dark-blue

    app = App()

    # Kích thước cửa sổ
    app.geometry("900x650")

    # Không cho thu nhỏ quá mức
    app.minsize(850, 600)

    # Icon (nếu có)
    try:
        app.iconbitmap("logo.ico")
    except Exception:
        pass

    app.mainloop()


if __name__ == "__main__":
    main()