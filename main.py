# code of main.py
import customtkinter as ctk  
import threading
import keyboard
from logic_core import AutomatorCore
from app_layout import AutomatorLayout
from app_handler import AutomatorHandlers

class UltraAutomatorPremium(AutomatorCore, AutomatorLayout, AutomatorHandlers):
    def __init__(self):
        super().__init__()
        self.setup_ui_layout()
        self.build_sidebar_elements()
        self.build_bottom_elements()
        if not self.is_admin(): self.write_log("⚠️ Non-Admin Mode.")
        self.load_profile_data()
        self.bind_hotkeys()

    def toggle_automation(self):
        if not self.is_running:
            # Settings dictionary se auto-launch ki fields nikaal di hain
            current_settings = {
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
                "image_trigger": self.check_img_trigger.get(),
                "image_path": self.entry_img_path.get(),
                "image_confidence": self.slider_conf.get(),
                "timer_h": self.entry_timer_h.get(),
                "timer_m": self.entry_timer_m.get(),
                "scheduled_mode": self.check_schedule.get()
            }
            self.is_running = True
            self.is_paused = False
            if self.check_hide.get(): self.withdraw()
            self.update_status("ENGINE ACTIVE", "#28a745")
            self.start_btn.configure(text="STOP ENGINE (ESC)", fg_color="#da3633", hover_color="#f85149")
            t = threading.Thread(target=self.run_bot, args=(current_settings,), daemon=True)
            t.start()
        else:
            self.stop_automation()

    def stop_automation(self):
        if not self.is_running: return
        self.is_running = False
        self.is_paused = False
        self.after(0, self.deiconify)
        self.after(0, lambda: self.update_status("READY", "#28a745"))
        self.after(0, lambda: self.start_btn.configure(text="START AUTOMATION ENGINE", fg_color="#238636", hover_color="#2ea043"))
        self.after(0, lambda: self.progress_bar.set(0))
        self.write_log("🛑 System Halted.")

    def bind_hotkeys(self):
        try:
            keyboard.unhook_all()
            p = self.data["profiles"][self.data["current_profile"]]
            keyboard.add_hotkey(p.get("hotkey_start", "f8"), self.toggle_automation, suppress=True)
            keyboard.add_hotkey(p.get("hotkey_pause", "f9"), self.toggle_pause, suppress=True)
            keyboard.add_hotkey(p.get("hotkey_stop", "esc"), self.stop_automation, suppress=True)
        except: pass

    def toggle_pause(self):
        if not self.is_running: return
        self.is_paused = not self.is_paused
        self.write_log("⏸ Paused" if self.is_paused else "▶️ Resumed")
        self.update_status("PAUSED" if self.is_paused else "ENGINE ACTIVE", "#d29922" if self.is_paused else "#28a745")

    def on_closing(self):
        self.save_settings()
        keyboard.unhook_all()
        self.destroy()

if __name__ == "__main__":
    app = UltraAutomatorPremium()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()