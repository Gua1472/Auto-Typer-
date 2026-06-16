# code for ui_components.py
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PremiumInputDialog(ctk.CTkToplevel):
    def __init__(self, title, placeholder):
        super().__init__()
        self.title("")
        self.geometry("400x250")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color="#0B0E14")
        self.result = None
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (250 // 2)
        self.geometry(f"+{x}+{y}")

        ctk.CTkLabel(self, text=title, font=("Segoe UI", 20, "bold"), text_color="#3498db").pack(pady=(25, 15))
        
        self.entry = ctk.CTkEntry(self, placeholder_text=placeholder, width=320, height=45, 
                                 fg_color="#151921", border_color="#2c3e50", corner_radius=10)
        self.entry.pack(pady=10)
        self.entry.focus()
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=25)
        
        ctk.CTkButton(btn_frame, text="CREATE PROFILE", width=150, height=40, font=("Segoe UI", 12, "bold"),
                     fg_color="#2ecc71", hover_color="#27ae60", command=self.on_save).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="CANCEL", width=100, height=40, font=("Segoe UI", 12, "bold"),
                     fg_color="#e74c3c", hover_color="#c0392b", command=self.destroy).pack(side="left", padx=10)
        self.bind("<Return>", lambda e: self.on_save())

    def on_save(self):
        self.result = self.entry.get()
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return self.result

class UltraAutomatorUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ULTRA AUTOMATOR PREMIUM v2.0")
        self.geometry("1350x950")
        self.configure(fg_color="#0B0E14")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar with gradient effect
        self.sidebar = ctk.CTkFrame(self, width=350, corner_radius=0, fg_color="#151921", border_width=1, border_color="#1c222d")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        header_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header_frame.pack(fill="x", pady=(40, 20))
        
        ctk.CTkLabel(header_frame, text="ULTRA", font=("Impact", 36), text_color="#3498db").pack(side="left", padx=(40, 5))
        ctk.CTkLabel(header_frame, text="CORE", font=("Impact", 36), text_color="#ffffff").pack(side="left")
        
        self.scroll = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20)
        
        # Main Dashboard Area
        self.main_panel = ctk.CTkFrame(self, fg_color="#0B0E14", corner_radius=0)
        self.main_panel.grid(row=0, column=1, sticky="nsew")

    def setup_ui_layout(self):
        self.top_bar = ctk.CTkFrame(self.main_panel, fg_color="#151921", height=80, corner_radius=0, border_width=1, border_color="#1c222d")
        self.top_bar.pack(fill="x")
        
        status_container = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        status_container.pack(side="left", padx=30)
        
        self.status_dot = ctk.CTkLabel(status_container, text="● SYSTEM READY", font=("Segoe UI", 14, "bold"), text_color="#2ecc71")
        self.status_dot.pack(side="left")

        # Main Editor Card
        self.editor_card = ctk.CTkFrame(self.main_panel, fg_color="#151921", border_width=1, border_color="#2c3e50", corner_radius=15)
        self.editor_card.pack(fill="both", expand=True, padx=30, pady=(25, 15))
        
        editor_header = ctk.CTkFrame(self.editor_card, fg_color="transparent")
        editor_header.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(editor_header, text="COMMAND SEQUENCE EDITOR", font=("Segoe UI", 13, "bold"), text_color="#3498db").pack(side="left")
        ctk.CTkLabel(editor_header, text="TAGS: {date} {time} {random} {clipboard} {wait:x} {key:x}", font=("Consolas", 11), text_color="#7f8c8d").pack(side="right")
        
        self.text_editor = ctk.CTkTextbox(self.editor_card, font=("Consolas", 16), fg_color="#0B0E14", border_width=1, border_color="#1c222d", corner_radius=10, text_color="#ecf0f1")
        self.text_editor.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def create_card_header(self, text):
        header_f = ctk.CTkFrame(self.scroll, fg_color="transparent")
        header_f.pack(fill="x", pady=(25, 8), padx=5)
        ctk.CTkLabel(header_f, text=text, font=("Segoe UI", 12, "bold"), text_color="#3498db").pack(side="left")
        ctk.CTkFrame(header_f, height=2, fg_color="#1c222d").pack(side="left", fill="x", expand=True, padx=(10, 0))

    def setup_entry_row(self, master, label, row):
        row_f = ctk.CTkFrame(master, fg_color="transparent")
        row_f.pack(fill="x", pady=4, padx=5)
        ctk.CTkLabel(row_f, text=label, font=("Segoe UI", 12), text_color="#bdc3c7", width=100, anchor="w").pack(side="left")
        entry = ctk.CTkEntry(row_f, width=110, height=32, fg_color="#0B0E14", border_color="#2c3e50", corner_radius=8)
        entry.pack(side="right")
        return entry