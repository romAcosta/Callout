import os
import threading
import time

from enum import Enum
import json
from pathlib import Path

import portalocker
import sqlite3

import yaml
from PyQt6.QtCore import QTimer

from backend.utility import resource_path


class MacroType(Enum):
    KEYBOARD = 1
    MEDIA_CONTROL = 2
    APP_OPEN = 3

class Macro:
    def __init__(self, phrase:str, type:MacroType, command):
        super().__init__()

        self.phrase = phrase
        self.type = type
        self.command = command

    def to_dict(self):
        return {"phrase": self.phrase, "type": self.type.value, "command": self.command}


class DatabaseEditor:

    def __init__(self, db_path=resource_path("resources/callout.db")):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_profiles(self):
        with self.connect() as conn:
            return [row[0] for row in conn.execute("SELECT name FROM profiles")]

    def add_profile(self, name):
        with self.connect() as conn:
            conn.execute("INSERT OR IGNORE INTO profiles (name) VALUES (?)", (name,))
            conn.commit()

    def delete_profile(self,name):
        self.save_macros(name,[])
        with self.connect() as conn:
            cur = conn.execute("""
                DELETE FROM profiles
                WHERE profiles.name = ?
            """,(name,))


    def get_macros(self, profile_name):
        with self.connect() as conn:
            cur = conn.execute("""
                SELECT phrase, command, type
                FROM macros
                JOIN profiles ON macros.profile_id = profiles.id
                WHERE profiles.name = ?
            """, (profile_name,))
            return [{"phrase": r[0], "command": r[1], "type": r[2]} for r in cur]

    def get_phrases(self, macros):
        phrase_list = []
        for macro in macros:
            phrase_list.append(macro["phrase"])
        return phrase_list


    def save_macros(self, profile_name, macros):
        with self.connect() as conn:
            pid = conn.execute("SELECT id FROM profiles WHERE name = ?", (profile_name,)).fetchone()
            if pid is None:
                conn.execute("INSERT INTO profiles (name) VALUES (?)", (profile_name,))
                pid = conn.execute("SELECT id FROM profiles WHERE name = ?", (profile_name,)).fetchone()
            for m in macros:
                if "command" not in m or "type" not in m or "phrase" not in m:
                    print("Database Editor: Invalid Macros cannot Save")
            pid = pid[0]
            conn.execute("DELETE FROM macros WHERE profile_id = ?", (pid,))
            conn.executemany("""
                INSERT INTO macros (profile_id, phrase, command, type)
                VALUES (?, ?, ?, ?)
            """, [(pid, m["phrase"], m["command"], m.get("type", "KEYBOARD")) for m in macros])
            conn.commit()

class JsonEditor:
    def __init__(self, path = "resources"):
        super().__init__()
        self.lock = threading.RLock()

        self.path = path


    def get_profiles(self):
        folder = Path(self.path)
        files = [f.name for f in folder.iterdir() if f.is_file()]
        print(files)
        return files

    def set_profile(self, profile):
        with open(resource_path(self.path + "/settings.json"), 'r') as f:
            data = json.load(f)
        data["current_profile"] = profile
        with open(resource_path(self.path + "/settings.json"), 'w') as f:
            json.dump(data,f,indent = 4)

    def set_listening_mode(self, mode):

        data = self.get_settings()
        data["listening_mode"] = mode
        with open(resource_path(self.path + "/settings.json"), 'w') as f:
            json.dump(data,f,indent = 4)

    def set_threshold(self, threshold):

        data = self.get_settings()
        data["threshold"] = threshold
        with open(resource_path(self.path + "/settings.json"), 'w') as f:
            json.dump(data,f,indent = 4)

    def get_settings(self):
        with open(resource_path(self.path + "/settings.json"), 'r') as f:
            return json.load(f)

    def get_current_profile(self):
        return self.get_settings()["current_profile"]

class JsonPorter:
    def __init__(self):
        super().__init__()
        self.path = resource_path("exports")

    def export_profile(self, profile_name):

        db = DatabaseEditor()
        data = {"profile_name":profile_name, "macros":[]}
        macros = db.get_macros(profile_name)
        for macro in macros:
            data["macros"].append(macro)

        with open(self.path + "/" + profile_name + ".json", 'w') as f:
            # yaml.dump(data,f,sort_keys=False)
            json.dump(data,f,indent=4)



    def import_profile(self, file_path):
        data = {}
        with open(file_path,'r', encoding='utf-8-sig') as f:
            data = json.load(f)

        if "macros" not in data or "profile_name" not in data:
            print("Profile Porter: JSON missing required field")
            return None

        profile_name = data["profile_name"]
        if not isinstance(profile_name, str):
            print("Profile Porter: Profile name not of type String")
            return None

        macros = data["macros"]

        db = DatabaseEditor()
        db.add_profile(profile_name)
        db.save_macros(profile_name,macros)

        print("Profile Porter: We are okay!")
        return profile_name
