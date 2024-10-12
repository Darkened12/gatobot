import os
import subprocess
import ctypes
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw
from dotenv import load_dotenv
import time
import pygetwindow as gw

# Initialize the state variable
state = False
load_dotenv()
WINDOW_TITLE = f"Terminal - {os.environ.get('APP_NAME')}"


def start_script():
    # Start the script with a new console
    process = subprocess.Popen(
        ['run_bot.bat'],
        creationflags=subprocess.CREATE_NEW_CONSOLE  # Change this to the path of your script
    )
    print(process.args)
    # Allow some time for the window to be created
    time.sleep(0.5)  # Shortened sleep time

    # Find the window using the process's PID
    hwnd = find_window_by_pid(process.pid)
    if hwnd:
        print(f"Found window with PID: {process.pid}")
        set_window_title(hwnd, WINDOW_TITLE)  # Set the window title
        window = find_window_by_title(WINDOW_TITLE)
        if window:
            print(f"Found window with title: {WINDOW_TITLE}")
            hide_window(hwnd)  # Initially hide the window
        else:
            print(f"Window with title '{WINDOW_TITLE}' not found.")
    else:
        print(f"Window with PID '{process.pid}' not found.")

    return process


def find_window_by_pid(pid):
    hwnds = []

    def callback(hwnd, lParam):
        pid_out = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid_out))
        if pid_out.value == pid:
            hwnds.append(hwnd)
        return True

    ctypes.windll.user32.EnumWindows(ctypes.WINFUNCTYPE(
        ctypes.c_bool, ctypes.c_int, ctypes.c_void_p)(callback), 0)

    return hwnds[0] if hwnds else None


def find_window_by_title(title):
    windows = gw.getWindowsWithTitle(title)
    return windows[0] if windows else None


def set_window_title(hwnd, title):
    ctypes.windll.user32.SetWindowTextW(hwnd, title)


def hide_window(hwnd):
    ctypes.windll.user32.ShowWindow(hwnd, 0)


def show_window(hwnd):
    ctypes.windll.user32.ShowWindow(hwnd, 5)


def show_hide_window():
    if process is None or process.poll() is not None:
        print("Process not running or not found.")
        return  # No process or process not running

    hwnd = find_window_by_pid(process.pid)
    if hwnd:
        is_visible = ctypes.windll.user32.IsWindowVisible(hwnd)
        if is_visible:
            print(f"Hiding window: {WINDOW_TITLE}")
            hide_window(hwnd)
        else:
            print(f"Showing window: {WINDOW_TITLE}")
            show_window(hwnd)
    else:
        print(f"Window with PID '{process.pid}' not found.")


def on_clicked(icon, item):
    global state, process
    show_hide_window()
    state = not state
    icon.update_menu()


def on_exit(icon, item):
    global process
    if process:
        process.terminate()
        process.wait()  # Wait for process to terminate
    icon.stop()


# Load the custom icon
icon_path = os.path.join('assets', 'gato-redondo.ico')
custom_icon = Image.open(icon_path)

# Create the icon and menu
tray_icon = icon(
    'test',
    custom_icon,
    title="Gatobot",
    menu=menu(
        item(
            'Terminal',
            on_clicked,
            checked=lambda item: state
        ),
        item(
            'Exit',
            on_exit
        )
    )
)

process = start_script()
tray_icon.run()
