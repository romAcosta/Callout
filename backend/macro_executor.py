from pynput.keyboard import Key, Controller



keyboard = Controller()

valid_keys = {k.name for k in Key}  # collect valid Key names

def is_valid_key(key: str) -> bool:
    return key in valid_keys or len(key) == 1

def execute_macro(phrases,command:str,macros):

    match = next((word for word in phrases if word in command),None)

    print(match)
    if match:
        for macro in macros:

           if match.__eq__(macro["phrase"]) and is_valid_key(macro["command"]):

                keyboard.press(macro["command"])
                keyboard.release(macro["command"])

    return

