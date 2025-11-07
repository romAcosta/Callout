import os
import threading
import time
from enum import Enum
import json
from pathlib import Path

import portalocker
from PyQt6.QtCore import QTimer


class MacroType(Enum):
    KEYBOARD = 1

class Macro:
    def __init__(self, phrase:str, type:MacroType, command):
        super().__init__()

        self.phrase = phrase
        self.type = type
        self.command = command

    def to_dict(self):
        return {"phrase": self.phrase, "type": self.type.value, "command": self.command}


class JsonEditor:
    def __init__(self, path):
        super().__init__()
        self.lock = threading.RLock()
        self.current_profile = "default_profile.json"
        self.path = path


    def get_profiles(self):
        folder = Path(self.path)
        files = [f.name for f in folder.iterdir() if f.is_file()]
        print(files)
        return files

    def set_profile(self, profile):
        self.current_profile = profile

    def load_profile(self,retries=3):
        current_path = self.path + "/" + self.current_profile
        os.makedirs(os.path.dirname(current_path), exist_ok=True)

        print(current_path)
        for _ in range(retries):
            try:
                with portalocker.Lock(current_path, 'r', timeout=2) as f:
                    return json.load(f)
            except json.JSONDecodeError:
                time.sleep(0.05)
        raise



    def save_profile(self, data):
        path = os.path.join(self.path, self.current_profile)

        with self.lock:
            with portalocker.Lock(path, "w") as f:
                json.dump(data, f, indent=4)

    @staticmethod
    def save_phrases(macros):
        phrases = []
        for macro in macros:
            phrases.append(macro["phrase"])
        return phrases

    def save_macro(self, macro:Macro):
        data = self.load_profile()
        data["macros"].append(macro.to_dict())
        data["phrases"] = self.save_phrases(data["macros"])
        self.save_profile(data)

    def save_macros(self, macros):
        data = self.load_profile()
        data["macros"] = macros
        data["phrases"] = self.save_phrases(data["macros"])
        self.save_profile(data)

    def remove_macro(self, index:int):

        data = self.load_profile()

        if not (0 <= index < len(data["macros"])):
            return

        data["macros"].pop(index)
        data["phrases"] = self.save_phrases(data["macros"])

        self.save_profile(data)

    def get_macros(self):
        data = self.load_profile()
        return data["macros"]

    def get_phrases(self):
        data = self.load_profile()
        return data["phrases"]



# j = JSON_Editor("../resources/profiles")
# print(j.GetProfileName("default_profile.json"))
# j.SaveMacro(Macro("portalocker.Lock",MacroType.KEYBOARD,"L"))