#TODO  DO THIS NEXT

pyqt6_special_keys = [
    "alt",
    "alt",           # Qt has no left/right alt distinction
    "alt",
    "backspace",
    "capsLock",
    "meta",
    "meta",
    "meta",
    "control",
    "control",
    "control",
    "delete",
    "down",
    "end",
    "return",
    "escape",
    "f1",
    "f2",
    "f3",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8",
    "f9",
    "f10",
    "f11",
    "f12",
    "home",
    "insert",
    "left",
    "mediatoggleplaypause",
    "volumemute",
    "volumedown",
    "volumeup",
    "pagedown",
    "pageup",
    "pause",
    "print",
    "right",
    "scrolllock",
    "shift",
    "shift",
    "shift",
    "space",
    "tab",
    "up"
]

pynput_special_keys = [
    "alt",
    "alt_l",
    "alt_r",
    "backspace",
    "caps_lock",
    "cmd",
    "cmd_l",
    "cmd_r",
    "ctrl",
    "ctrl_l",
    "ctrl_r",
    "delete",
    "down",
    "end",
    "enter",
    "esc",
    "f1",
    "f2",
    "f3",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8",
    "f9",
    "f10",
    "f11",
    "f12",
    "home",
    "insert",
    "left",
    "media_play_pause",
    "media_volume_mute",
    "media_volume_down",
    "media_volume_up",
    "page_down",
    "page_up",
    "pause",
    "print_screen",
    "right",
    "scroll_lock",
    "shift",
    "shift_l",
    "shift_r",
    "space",
    "tab",
    "up"
]


def translate_pynput_to_pyqt(key):
    if not pynput_special_keys.__contains__(key):
        print("Key Translator: Special Pynput Key Not Found")
        return key
    index = pynput_special_keys.index(key)
    return pyqt6_special_keys[index]

def translate_pyqt_to_pynput(key):
    if not pyqt6_special_keys.__contains__(key):
        print("Key Translator: Special Pyqt Key Not Found")
        return key
    index = pyqt6_special_keys.index(key)
    return pynput_special_keys[index]