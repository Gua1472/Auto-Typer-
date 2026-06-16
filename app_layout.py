# code of app_layout.py
import customtkinter as ctk

class AutomatorLayout:
    def build_sidebar_elements(self):
        # 1. Hotkeys
        self.create_card_header("⌨️ MASTER CONTROL")
        hk_frame = ctk.CTkFrame(self.scroll, fg_color="#0d1117", border_width=1, border_color="#30363d")
        hk_frame.pack(fill="x", pady=5, padx=2)
        
        self.btn_hk_start = ctk.CTkButton(hk_frame, text="START: F8", height=35, fg_color="#21262d", hover_color="#30363d", command=lambda: self.capture_key("hotkey_start"))
        self.btn_hk_start.pack(fill="x", pady=5, padx=10)
        self.btn_hk_pause = ctk.CTkButton(hk_frame, text="PAUSE: F9", height=35, fg_color="#21262d", hover_color="#30363d", command=lambda: self.capture_key("hotkey_pause"))
        self.btn_hk_pause.pack(fill="x", pady=5, padx=10)
        self.btn_hk_stop = ctk.CTkButton(hk_frame, text="STOP: ESC", height=35, fg_color="#da3633", hover_color="#f85149", command=lambda: self.capture_key("hotkey_stop"))
        self.btn_hk_stop.pack(fill="x", pady=5, padx=10)

        # 2. Performance
        self.create_card_header("⚡ PERFORMANCE")
        t_frame = ctk.CTkFrame(self.scroll, fg_color="#0d1117", border_width=1, border_color="#30363d")
        t_frame.pack(fill="x", pady=5, padx=2)
        self.entry_typing = self.setup_entry_row(t_frame, "Type Speed:", 0)
        self.entry_gap = self.setup_entry_row(t_frame, "Msg Gap:", 1)
        self.entry_loops = self.setup_entry_row(t_frame, "Total Loops:", 2)

        self.create_card_header("⚙️ ADVANCED ENGINE")

        # 3. Scheduler (Cleaned)
        self.schedule_section = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.schedule_section.pack(fill="x")
        self.check_schedule = ctk.CTkCheckBox(self.schedule_section, text="Scheduled Execution", font=("Arial", 12, "bold"), command=self.toggle_timer_ui)
        self.check_schedule.pack(anchor="w", pady=8, padx=10)
        self.timer_frame = ctk.CTkFrame(self.schedule_section, fg_color="#0d1117", border_width=1, border_color="#30363d")
        self.entry_timer_h = self.setup_entry_row(self.timer_frame, "Hours:", 0)
        self.entry_timer_m = self.setup_entry_row(self.timer_frame, "Minutes:", 1)

        # 4. Pre-Click
        self.mouse_section = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.mouse_section.pack(fill="x")
        self.check_mouse = ctk.CTkCheckBox(self.mouse_section, text="Pre-Click Action", font=("Arial", 12, "bold"), command=self.toggle_mouse_ui)
        self.check_mouse.pack(anchor="w", pady=8, padx=10)
        self.m_frame = ctk.CTkFrame(self.mouse_section, fg_color="#0d1117", border_width=1, border_color="#30363d")
        self.entry_coords = ctk.CTkEntry(self.m_frame, placeholder_text="X, Y", fg_color="#010409")
        self.entry_coords.pack(fill="x", padx=10, pady=(10,5))
        ctk.CTkButton(self.m_frame, text="🎯 CAPTURE POS", height=28, command=self.get_mouse_pos).pack(fill="x", padx=10, pady=10)

        # 5. Image Recognition
        self.img_section = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.img_section.pack(fill="x")
        self.check_img_trigger = ctk.CTkCheckBox(self.img_section, text="Image Recognition", font=("Arial", 12, "bold"), command=self.toggle_image_ui)
        self.check_img_trigger.pack(anchor="w", pady=8, padx=10)
        self.img_ui_frame = ctk.CTkFrame(self.img_section, fg_color="#0d1117", border_width=1, border_color="#30363d")
        self.entry_img_path = ctk.CTkEntry(self.img_ui_frame, placeholder_text="target.png", height=30, fg_color="#010409")
        self.entry_img_path.pack(fill="x", padx=10, pady=(10,5))
        ctk.CTkButton(self.img_ui_frame, text="📁 SELECT IMAGE", height=28, fg_color="#238636", command=self.select_image_file).pack(fill="x", padx=10, pady=5)
        self.slider_conf = ctk.CTkSlider(self.img_ui_frame, from_=0.1, to=1.0, number_of_steps=9)
        self.slider_conf.pack(fill="x", padx=10, pady=10)

        # 6. Human Simulation
        self.human_section = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.human_section.pack(fill="x")
        self.check_human = ctk.CTkCheckBox(self.human_section, text="Human Simulation", font=("Arial", 12, "bold"), command=self.toggle_human_ui)
        self.check_human.pack(anchor="w", pady=8, padx=10)
        self.h_frame = ctk.CTkFrame(self.human_section, fg_color="#0d1117", border_width=1, border_color="#30363d")
        self.entry_min = self.setup_entry_row(self.h_frame, "Min Delay:", 0)
        self.entry_max = self.setup_entry_row(self.h_frame, "Max Delay:", 1)

        self.check_paste = ctk.CTkCheckBox(self.scroll, text="Instant Paste Mode", font=("Arial", 12))
        self.check_paste.pack(anchor="w", pady=5, padx=10)
        self.check_hide = ctk.CTkCheckBox(self.scroll, text="Stealth Mode (Hide)", font=("Arial", 12))
        self.check_hide.pack(anchor="w", pady=5, padx=10)

    def build_bottom_elements(self):
        bottom_frame = ctk.CTkFrame(self.main_panel, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=25, pady=20)
        self.log_box = ctk.CTkTextbox(bottom_frame, height=130, font=("Consolas", 12), fg_color="#010409", border_width=1, border_color="#30363d")
        self.log_box.pack(fill="x", pady=(0, 15))
        self.start_btn = ctk.CTkButton(bottom_frame, text="START AUTOMATION ENGINE", height=55, font=("Arial", 16, "bold"), fg_color="#238636", hover_color="#2ea043", corner_radius=8, command=self.toggle_automation)
        self.start_btn.pack(fill="x")
        self.progress_bar = ctk.CTkProgressBar(bottom_frame, height=8, progress_color="#2f81f7")
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(15, 0))

        prof_f = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        prof_f.pack(side="right", padx=20)
        self.profile_dropdown = ctk.CTkOptionMenu(prof_f, values=list(self.data["profiles"].keys()), fg_color="#21262d", button_color="#30363d", command=self.change_profile)
        self.profile_dropdown.pack(side="left", padx=5)
        ctk.CTkButton(prof_f, text="+", width=35, fg_color="#238636", command=self.add_profile_premium).pack(side="left", padx=2)
        ctk.CTkButton(prof_f, text="-", width=35, fg_color="#da3633", command=self.delete_profile_premium).pack(side="left", padx=2)

    def create_card_header(self, text):
        ctk.CTkLabel(self.scroll, text=text, font=("Arial", 11, "bold"), text_color="#8b949e").pack(anchor="w", pady=(20, 5), padx=5)

    def setup_entry_row(self, master, label, row):
        row_f = ctk.CTkFrame(master, fg_color="transparent")
        row_f.pack(fill="x", padx=5, pady=3)
        ctk.CTkLabel(row_f, text=label, font=("Arial", 12), text_color="#c9d1d9", width=80, anchor="w").pack(side="left", padx=10)
        entry = ctk.CTkEntry(row_f, width=100, height=28, fg_color="#010409", border_color="#30363d")
        entry.pack(side="right", padx=10)
        return entry