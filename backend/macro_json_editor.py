from enum import Enum
import json

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
        self.path = path

    def SavePhrases(self,macros):
        phrases = []
        for macro in macros:
            phrases.append(macro["phrase"])
        return phrases

    def SaveMacro(self, macro:Macro):
        with open(self.path, "r") as f:
            data = json.load(f)
        data["macros"].append(macro.to_dict())
        data["phrases"] = self.SavePhrases(data["macros"])
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    def RemoveMacro(self, index:int):

        with open(self.path, "r") as f:
            data = json.load(f)

        if not (0 <= index < len(data["macros"])):
            return

        data["macros"].pop(index)
        data["phrases"] = self.SavePhrases(data["macros"])
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    def GetMacros(self):
        with open(self.path, "r") as f:
            data = json.load(f)
        return data["macros"]

    def GetPhrases(self):
        with open(self.path, "r") as f:
            data = json.load(f)
        return data["phrases"]


