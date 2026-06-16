# code of logic_utils.py
import json
import os
import ctypes
import pyautogui
from datetime import datetime
from ui_components import *

CONFIG_FILE = "automator_premium_data.json"

class AutomatorUtils(UltraAutomatorUI):
    def __init__(self):
        super().__init__()
        self.data = self.load_initial_config()

    def load_initial_config(self):
        default_data = {"current_profile": "Default", "profiles": {"Default": {
            "text": "Line One\nLine Two",
            "typing_speed": "0.01", "min_delay": "0.01", "max_delay": "0.05",
            "message_gap": "1.5", "loops": "1", 
            "hotkey_start": "f8", "hotkey_pause": "f9", "hotkey_stop": "esc", 
            "human_mode": False, "paste_mode": False, "mouse_click": False, 
            "click_coords": "0,0", "hide_ui": False, "image_trigger": False, 
            "image_path": "", "image_confidence": 0.8,
            "timer_h": "0", "timer_m": "0", "scheduled_mode": False
        }}}
        
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
            except:
                return default_data
        return default_data

    def is_admin(self):
        try: return ctypes.windll.shell32.IsUserAnAdmin()
        except: return False

    def safe_float(self, val, default=0.0):
        try: return float(str(val).strip())
        except: return default

    def safe_int(self, val, default=1):
        try: return int(float(str(val).strip()))
        except: return default

    def write_log(self, msg):
        ts = datetime.now().strftime('%H:%M:%S')
        self.after(0, lambda: self.log_box.insert("end", f"[{ts}] {msg}\n"))
        self.after(0, self.log_box.see, "end")

    def save_settings(self):
        try:
            p = self.data["current_profile"]
            self.data["profiles"][p].update({
                "text": self.text_editor.get("1.0", "end-1c"),
                "typing_speed": self.entry_typing.get(),
                "min_delay": self.entry_min.get(),
                "max_delay": self.entry_max.get(),
                "message_gap": self.entry_gap.get(),
                "loops": self.entry_loops.get(),
                "human_mode": self.check_human.get(),
                "paste_mode": self.check_paste.get(),
                "mouse_click": self.check_mouse.get(),
                "click_coords": self.entry_coords.get(),
                "hide_ui": self.check_hide.get(),
                "image_trigger": self.check_img_trigger.get(),
                "image_path": self.entry_img_path.get(),
                "image_confidence": self.slider_conf.get(),
                "timer_h": self.entry_timer_h.get(),
                "timer_m": self.entry_timer_m.get(),
                "scheduled_mode": self.check_schedule.get()
            })
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.data, f, indent=4)
        except: pass