from pynput.keyboard import Key, Controller

import ctypes
from ctypes import wintypes

from backend.storage_management import Macro, MacroType

user32 = ctypes.WinDLL('user32', use_last_error=True)

HWND_BROADCAST = 0xFFFF
WM_APPCOMMAND = 0x0319

keyboard = Controller()





# Commands
APPCOMMAND_MEDIA_PLAY_PAUSE   = 14 << 16
APPCOMMAND_MEDIA_NEXT_TRACK   = 11 << 16
APPCOMMAND_MEDIA_PREV_TRACK   = 12 << 16
APPCOMMAND_VOLUME_UP          = 10 << 16
APPCOMMAND_VOLUME_DOWN        = 9  << 16
APPCOMMAND_VOLUME_MUTE        = 8  << 16


def send_app_command(cmd):
    user32.PostMessageW(HWND_BROADCAST, WM_APPCOMMAND, 0, cmd)

def send_keyboard_command(command):
    key_name = command
    if len(str(key_name)) < 2:
        pynput_key = key_name
    else:
        pynput_key = getattr(Key, key_name)
    keyboard.press(pynput_key)
    keyboard.release(pynput_key)

def execute_macro(phrases,command:str,macros):

    match = next((word for word in phrases if word in command),None)
    print(match)
    if not match:
        return
    for macro in macros:

        if not match.__eq__(macro["phrase"]):
            continue
        type = MacroType(int(macro["type"]))

        if type == MacroType.KEYBOARD:
            send_keyboard_command(macro["command"])
        elif type == MacroType.MEDIA_CONTROL:
            pass

    return
