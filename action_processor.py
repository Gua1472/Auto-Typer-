# code of action_processor.py
import time
import random
import re
import pyautogui
import pyperclip
from datetime import datetime
from logic_utils import AutomatorUtils

# Pure speed settings
pyautogui.PAUSE = 0
pyautogui.MINIMUM_DURATION = 0
pyautogui.FAILSAFE = True

class AutomatorActions(AutomatorUtils):
    def __init__(self):
        super().__init__()

    def resolve_tags(self, msg):
        def repl(m):
            tag = m.group(0).lower()
            if tag == "{time}": return datetime.now().strftime("%H:%M:%S")
            if tag == "{date}": return datetime.now().strftime("%Y-%m-%d")
            if tag == "{random}": return str(random.randint(1000, 9999))
            if tag == "{clipboard}": 
                try: return str(pyperclip.paste())
                except: return ""
            return m.group(0)
        return re.sub(r'(?i)\{(time|date|random|clipboard)\}', repl, msg)

    def execute_click(self, coords_str):
        try:
            if not coords_str or "," not in coords_str: return False
            x_str, y_str = coords_str.split(",")
            tx, ty = int(x_str.strip()), int(y_str.strip())
            
            # Teleport click: duration 0 means no visible movement
            # _pause=False ensures no delay after click
            pyautogui.click(x=tx, y=ty, duration=0, _pause=False)
            return True
        except Exception as e:
            self.write_log(f"⚠️ Click Error: {e}")
            return False

    def simulate_input(self, msg, settings, is_running_check, pause_check, sleep_func):
        if not is_running_check(): return

        if settings.get('paste_mode'):
            pyperclip.copy(msg)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
        else:
            # Smart Regex for tags like {wait:2} or {key:f5}
            parts = re.split(r'(?i)(\{wait:\d+\.?\d*\}|\{tab\}|\{enter\}|\{backspace\}|\{key:\w+\})', msg)
            mn = self.safe_float(settings.get('min_delay'), 0.01)
            mx = self.safe_float(settings.get('max_delay'), 0.05)
            spd = self.safe_float(settings.get('typing_speed'), 0.01)

            for p in parts:
                if not p or not is_running_check(): continue
                while pause_check() and is_running_check(): time.sleep(0.1)
                
                p_low = p.lower()
                if "{wait:" in p_low:
                    try:
                        s = float(re.search(r"\d+\.?\d*", p).group())
                        sleep_func(s)
                    except: pass
                elif p_low == "{tab}": pyautogui.press("tab")
                elif p_low == "{enter}": pyautogui.press("enter")
                elif p_low == "{backspace}": pyautogui.press("backspace")
                elif "{key:" in p_low:
                    try:
                        k = re.search(r"key:(\w+)", p_low).group(1)
                        pyautogui.press(k)
                    except: pass
                else:
                    # Direct typing
                    pyautogui.write(p, interval=spd if not settings.get('human_mode') else 0)
                    
                    if settings.get('human_mode'):
                        for _ in p:
                            if not is_running_check(): break
                            time.sleep(random.uniform(mn, mx))