from pynput.keyboard import Key, Controller



keyboard = Controller()


def execute_macro(phrases,command:str,macros):

    match = next((word for word in phrases if word in command),None)

    print(match)
    if match:
        for macro in macros:
            if match.__eq__(macro["phrase"]):
                keyboard.press(macro["command"])
                keyboard.release(macro["command"])


    return