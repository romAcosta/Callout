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

def SavePhrases(macros):
    phrases = []
    for macro in macros:
        phrases.append(macro["phrase"])
    return phrases

def SaveMacro(macro:Macro):
    with open("resources/default_profile.json", "r") as f:
        data = json.load(f)
    data["macros"].append(macro.to_dict())
    data["phrases"] = SavePhrases(data["macros"])
    with open("resources/default_profile.json", "w") as f:
        json.dump(data, f, indent=4)

def RemoveMacro(index:int):
    with open("resources/default_profile.json", "r") as f:
        data = json.load(f)
    data["macros"].pop(index)
    data["phrases"] = SavePhrases(data["macros"])
    with open("resources/default_profile.json", "w") as f:
        json.dump(data, f, indent=4)

def GetMacros():
    with open("resources/default_profile.json", "r") as f:
        data = json.load(f)
    return data["macros"]

def GetPhrases():
    with open("resources/default_profile.json", "r") as f:
        data = json.load(f)
    return data["phrases"]


