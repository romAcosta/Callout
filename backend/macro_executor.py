from pynput.keyboard import Key, Controller

import ctypes
from ctypes import wintypes

from backend.storage_management import Macro, MacroType

user32 = ctypes.WinDLL('user32', use_last_error=True)

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002

keyboard = Controller()





# Commands
APPCOMMAND_MEDIA_PLAY_PAUSE   = 0xB3
APPCOMMAND_MEDIA_NEXT_TRACK   = 0xB0
APPCOMMAND_MEDIA_PREV_TRACK   = 0xB1
APPCOMMAND_VOLUME_UP          = 10 << 16
APPCOMMAND_VOLUME_DOWN        = 9  << 16
APPCOMMAND_VOLUME_MUTE        = 0xAD


def send_app_command(vk):
    ctypes.windll.user32.keybd_event(vk, 0, KEYEVENTF_EXTENDEDKEY, 0)
    ctypes.windll.user32.keybd_event(vk, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)

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
            c = translate_media_command(macro["command"])
            send_app_command(c)
            pass

    return

def translate_media_command(command:str):
    print(command)
    if command == "Play/Pause":
        return APPCOMMAND_MEDIA_PLAY_PAUSE
    elif command == "Next Track":
        return APPCOMMAND_MEDIA_NEXT_TRACK
    elif command == "Previous Track":
        return APPCOMMAND_MEDIA_PREV_TRACK
    elif command == "Mute Volume":
        return APPCOMMAND_VOLUME_MUTE
    return