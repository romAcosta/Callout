import os
import threading
from enum import Enum
import json
from pathlib import Path

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


class JSON_Editor:
    def __init__(self, path):
        super().__init__()
        self.lock = threading.Lock()
        self.current_profile = "default_profile.json"
        self.path = path

    def GetProfileName(self,profile:str = None):
        data = self.LoadProfile(profile)
        return data["profile_name"]

    def GetProfiles(self):
        folder = Path(self.path)
        files = [f.name for f in folder.iterdir() if f.is_file()]
        print(files)
        return files

    def SetProfile(self,profile):
        self.current_profile = profile

    def LoadProfile(self, profile:str = None ):
        current_path = self.path + "/"
        if profile is not None:
            current_path += profile
        else:
            current_path += self.current_profile

        with self.lock:
            if not os.path.exists(current_path) or os.path.getsize(current_path) == 0:
                return {}
            with open(current_path, "r") as f:
                return json.load(f)



    def SaveProfile(self,data):
        path = os.path.join(self.path, self.current_profile)

        with self.lock:
            with open(path, "w") as f:
                json.dump(data, f, indent=4)

    def SavePhrases(self,macros):
        phrases = []
        for macro in macros:
            phrases.append(macro["phrase"])
        return phrases

    def SaveMacro(self, macro:Macro):
        data = self.LoadProfile()
        data["macros"].append(macro.to_dict())
        data["phrases"] = self.SavePhrases(data["macros"])
        self.SaveProfile(data)

    def SaveMacros(self, macros):
        data = self.LoadProfile()
        data["macros"] = macros
        data["phrases"] = self.SavePhrases(data["macros"])
        self.SaveProfile(data)

    def RemoveMacro(self, index:int):

        data = self.LoadProfile()

        if not (0 <= index < len(data["macros"])):
            return

        data["macros"].pop(index)
        data["phrases"] = self.SavePhrases(data["macros"])

        self.SaveProfile(data)

    def GetMacros(self):
        data = self.LoadProfile()
        return data["macros"]

    def GetPhrases(self):
        data = self.LoadProfile()
        return data["phrases"]



# j = JSON_Editor("../resources/profiles")
# print(j.GetProfileName("default_profile.json"))
# j.SaveMacro(Macro("Open",MacroType.KEYBOARD,"L"))