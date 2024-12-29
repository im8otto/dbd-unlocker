import threading
from inputs import devices, get_gamepad
from Utils import Misc
import time

class Controller:
    def __init__(self):
        self.controller = None
        self.running = True
        self.select_pressed = False
        self.start_pressed = False
        self.exit_event = threading.Event()
        
    def find_controller(self):
        gamepads = devices.gamepads
        if not gamepads:
            Misc.print_log("No gamepad found.")
            return
        self.controller = gamepads[0]
        Misc.print_log(f"Controller found: {self.controller}")

    def monitor_controller(self):
        if self.controller is None:
            return
        while not self.exit_event.is_set():
            events = get_gamepad()
            for event in events:
                if event.code == "BTN_SELECT" and event.state == 1:
                    self.select_pressed = True
                elif event.code == "BTN_SELECT" and event.state == 0:
                    self.select_pressed = False

                if event.code == "BTN_START" and event.state == 1:
                    self.start_pressed = True
                elif event.code == "BTN_START" and event.state == 0:
                    self.start_pressed = False

                if self.select_pressed and self.start_pressed:
                    self.exit_event.set()
                    return
            time.sleep(0.1)

    def start_monitoring(self):
        if self.controller is None:
            return
        controller_thread = threading.Thread(target=self.monitor_controller, daemon=True)
        controller_thread.start()
