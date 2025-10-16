from pynput.keyboard import Key, Controller


keyboard = Controller()


def execute_macro(command:str):
    if(command.__contains__("reload")):
        keyboard.press('a')
        keyboard.release('a')
    return