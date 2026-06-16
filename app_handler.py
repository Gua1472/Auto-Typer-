# code of app_handler.py
import pyautogui
import keyboard
import time
import threading
from tkinter import filedialog
from ui_components import PremiumInputDialog

class AutomatorHandlers:
    def update_status(self, text, color): 
        self.status_dot.configure(text=f"● {text}", text_color=color)

    def toggle_timer_ui(self):
        if self.check_schedule.get(): self.timer_frame.pack(fill="x", pady=(0, 5), padx=10)
        else: self.timer_frame.pack_forget()

    def toggle_human_ui(self): 
        if self.check_human.get(): self.h_frame.pack(fill="x", pady=(0, 5), padx=10)
        else: self.h_frame.pack_forget()

    def toggle_mouse_ui(self): 
        if self.check_mouse.get(): self.m_frame.pack(fill="x", pady=(0, 5), padx=10)
        else: self.m_frame.pack_forget()

    def toggle_image_ui(self): 
        if self.check_img_trigger.get(): self.img_ui_frame.pack(fill="x", pady=(0, 5), padx=10)
        else: self.img_ui_frame.pack_forget()
    
    def select_image_file(self):
        p = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.bmp")])
        if p: 
            self.entry_img_path.delete(0, "end")
            self.entry_img_path.insert(0, p)

    def get_mouse_pos(self):
        def cap():
            self.write_log("📍 Move mouse to target. Capturing in 3s...")
            time.sleep(3)
            pos = pyautogui.position()
            self.entry_coords.delete(0, "end")
            self.entry_coords.insert(0, f"{pos.x},{pos.y}")
            self.write_log(f"✅ Captured: {pos.x}, {pos.y}")
        threading.Thread(target=cap, daemon=True).start()

    def capture_key(self, target):
        self.write_log(f"⌨️ Press any key for {target.split('_')[-1].upper()}...")
        def listen():
            ev = keyboard.read_event()
            if ev.event_type == keyboard.KEY_DOWN:
                self.data["profiles"][self.data["current_profile"]][target] = ev.name
                self.after(0, self.load_profile_data)
                self.after(0, self.bind_hotkeys)
                self.write_log(f"✅ Bound: {ev.name.upper()}")
        threading.Thread(target=listen, daemon=True).start()

    def add_profile_premium(self):
        dialog = PremiumInputDialog("New Profile", "Enter name...")
        name = dialog.get_input()
        if name:
            self.data["profiles"][name] = self.data["profiles"]["Default"].copy()
            self.profile_dropdown.configure(values=list(self.data["profiles"].keys()))
            self.change_profile(name)

    def delete_profile_premium(self):
        if self.data["current_profile"] != "Default":
            del self.data["profiles"][self.data["current_profile"]]
            self.profile_dropdown.configure(values=list(self.data["profiles"].keys()))
            self.change_profile("Default")

    def change_profile(self, name):
        self.save_settings()
        self.data["current_profile"] = name
        self.load_profile_data()
        self.bind_hotkeys()

    def load_profile_data(self):
        prof = self.data["profiles"][self.data["current_profile"]]
        self.text_editor.delete("1.0", "end")
        self.text_editor.insert("1.0", prof.get("text", ""))
        
        fields = [
            (self.entry_typing, "typing_speed"), (self.entry_min, "min_delay"), 
            (self.entry_max, "max_delay"), (self.entry_gap, "message_gap"), 
            (self.entry_loops, "loops"), (self.entry_coords, "click_coords"), 
            (self.entry_img_path, "image_path"), (self.entry_timer_h, "timer_h"),
            (self.entry_timer_m, "timer_m")
        ]
        
        for entry, key in fields:
            val = str(prof.get(key, "0" if "timer" in key or "loops" in key else ""))
            entry.delete(0, "end")
            entry.insert(0, val)
        
        self.slider_conf.set(float(prof.get("image_confidence", 0.8)))
        
        cb_map = [
            (self.check_human, "human_mode"), (self.check_paste, "paste_mode"), 
            (self.check_mouse, "mouse_click"), (self.check_hide, "hide_ui"), 
            (self.check_img_trigger, "image_trigger"), (self.check_schedule, "scheduled_mode")
        ]
        
        for cb, key in cb_map:
            if prof.get(key): cb.select()
            else: cb.deselect()

        self.btn_hk_start.configure(text=f"START: {str(prof.get('hotkey_start', 'F8')).upper()}")
        self.btn_hk_pause.configure(text=f"PAUSE: {str(prof.get('hotkey_pause', 'F9')).upper()}")
        self.btn_hk_stop.configure(text=f"STOP: {str(prof.get('hotkey_stop', 'ESC')).upper()}")
        
        self.toggle_human_ui()
        self.toggle_mouse_ui()
        self.toggle_image_ui()
        self.toggle_timer_ui()
        self.profile_dropdown.set(self.data["current_profile"])