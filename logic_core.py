# code of logic_core.py
import time
import os
import pyautogui
import pygetwindow as gw
from action_processor import AutomatorActions

class AutomatorCore(AutomatorActions):
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.is_paused = False

    def smart_sleep(self, seconds):
        end_time = time.time() + seconds
        while time.time() < end_time and self.is_running:
            if self.is_paused:
                time.sleep(0.1)
                end_time += 0.1
                continue
            time.sleep(0.05)

    def run_bot(self, settings):
        try:
            # 1. FIX: Robust Scheduled Execution
            if settings.get('scheduled_mode'):
                h = self.safe_int(settings.get('timer_h'), 0)
                m = self.safe_int(settings.get('timer_m'), 0)
                total_wait_seconds = (h * 3600) + (m * 60)
                
                if total_wait_seconds > 0:
                    self.write_log(f"⏳ Scheduler Active: Starting in {h}h {m}m...")
                    
                    # Real-time countdown loop
                    while total_wait_seconds > 0 and self.is_running:
                        if total_wait_seconds % 60 == 0:
                            self.write_log(f"🕒 Timer: {total_wait_seconds // 60} minutes remaining...")
                        elif total_wait_seconds < 10:
                            self.write_log(f"🕒 Starting in {total_wait_seconds}s...")
                        
                        time.sleep(1)
                        total_wait_seconds -= 1
                    
                    if self.is_running:
                        self.write_log("🔔 Timer finished! Initiating automation...")

            if not self.is_running: return

            # 2. Window Detection (Broad Search)
            target_keywords = ["WhatsApp", "Chrome", "Edge", "Firefox"] 
            target_win = None
            
            # WhatsApp ya browser window dhundna
            all_windows = gw.getAllTitles()
            found_title = ""
            for title in all_windows:
                if "whatsapp" in title.lower():
                    found_title = title
                    break
            
            if found_title:
                try:
                    target_win = gw.getWindowsWithTitle(found_title)[0]
                    if target_win.isMinimized: target_win.restore()
                    target_win.activate()
                    self.write_log(f"🎯 Focused: {found_title[:20]}...")
                    self.smart_sleep(1.5) # Focus hone ka wait
                except Exception as e:
                    self.write_log("⚠️ Focus failed, trying to continue...")
            else:
                self.write_log("⚠️ WhatsApp not detected in window titles.")
                # Agar window nahi mili to rukna nahi hai, shayad user ne khud focus rakha ho
            
            # 3. Data Preparation
            loops = self.safe_int(settings.get('loops'), 1)
            m_gap = self.safe_float(settings.get('message_gap'), 1.0)
            text_raw = settings.get('text', '')
            lines = [l.strip() for l in text_raw.split("\n") if l.strip()]
            
            if not lines:
                self.write_log("❌ Error: No text found in editor.")
                self.after(0, self.stop_automation)
                return

            total_actions = len(lines) * loops
            count = 0

            # 4. Main Engine Loop
            for i in range(loops):
                if not self.is_running: break
                
                # Pre-Click (Stealth Mode)
                if settings.get('mouse_click'):
                    self.execute_click(settings.get('click_coords'))
                    self.smart_sleep(0.5)

                for msg in lines:
                    if not self.is_running: break
                    while self.is_paused and self.is_running: time.sleep(0.1)

                    # Dynamic Tags
                    final_msg = self.resolve_tags(msg)
                    
                    # Simulation
                    self.simulate_input(final_msg, settings, lambda: self.is_running, lambda: self.is_paused, self.smart_sleep)

                    if not self.is_running: break
                    
                    # Enter press logic
                    pyautogui.press("enter")
                    
                    count += 1
                    progress = min(count / total_actions, 1.0)
                    self.after(0, lambda p=progress: self.progress_bar.set(p))
                    self.write_log(f"✅ Sent {count}/{total_actions}")
                    
                    if count < total_actions: 
                        self.smart_sleep(m_gap)

        except Exception as e:
            self.write_log(f"❌ Critical Error: {str(e)}")
        finally:
            self.after(0, self.stop_automation)