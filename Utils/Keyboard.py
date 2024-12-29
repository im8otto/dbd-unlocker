import threading
import keyboard
import time

class KeyboardListener(threading.Thread):
    def __init__(self, controller, exit_key='ctrl+f4'):
        super().__init__()
        self.controller = controller
        self.exit_key = exit_key

    def run(self):
        while not self.controller.exit_event.is_set():
            if keyboard.is_pressed(self.exit_key):
                self.controller.exit_event.set()
                return
            time.sleep(0.1)
