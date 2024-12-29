import atexit
import os
import subprocess
from Utils import Misc, Proxy, Certificate, Controller, Keyboard

mitmdump_process = None

def start_mitmproxy(script_dir):
    try:
        global mitmdump_process
        mitmdump_process = subprocess.Popen([
            'mitmdump',
            '-s', os.path.join(script_dir, 'Utils', 'Proxy.py'),
            '--quiet',
            '--allow-hosts', '^.*(bhvrdbd\.com|mitm\.it).*$',
            '--set', 'log_level=none',
            '--listen-port', '8082'
        ])
    except KeyboardInterrupt:
        pass

def stop_mitmproxy():
    global mitmdump_process
    if mitmdump_process:
        mitmdump_process.terminate()
        mitmdump_process.wait()

def exit_handler():
    Proxy.disable_proxy_settings()
    stop_mitmproxy()

atexit.register(exit_handler)

if __name__ == "__main__":
    keyboard_listener = None
    try:
        Misc.print_logo()
        controller = Controller.Controller()
        controller.find_controller()
        controller.start_monitoring()
        Proxy.set_proxy_settings()
        Certificate.init()
        start_mitmproxy(Misc.script_dir)
        keyboard_listener = Keyboard.KeyboardListener(controller)
        keyboard_listener.start()
        controller.exit_event.wait()
    except KeyboardInterrupt:
        controller.exit_event.set()
    except Exception as e:
        Misc.print_log(f"Error: {e}")
    finally:
        if keyboard_listener:
            keyboard_listener.join()
