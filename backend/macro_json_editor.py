import os
import threading
import time

from enum import Enum
import json
from pathlib import Path

import portalocker
import sqlite3
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


class DatabaseEditor:
    def __init__(self, db_path="resources/callout.db"):
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
            pid = pid[0]
            conn.execute("DELETE FROM macros WHERE profile_id = ?", (pid,))
            conn.executemany("""
                INSERT INTO macros (profile_id, phrase, command, type)
                VALUES (?, ?, ?, ?)
            """, [(pid, m["phrase"], m["command"], m.get("type", "KEYBOARD")) for m in macros])
            conn.commit()

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

# conn = sqlite3.connect("../resources/callout.db")
# cursor = conn.cursor()
#
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS profiles (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT UNIQUE NOT NULL
# )
# """)
#
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS macros (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     profile_id INTEGER,
#     phrase TEXT NOT NULL,
#     command TEXT NOT NULL,
#     type TEXT,
#     FOREIGN KEY(profile_id) REFERENCES profiles(id)
# )
# """)

# db = DatabaseEditor()
# # db.add_profile("default")
#
#
# print(db.get_macros("default"))
#
# conn.commit()
# conn.close()


# j = JSON_Editor("../resources/profiles")
# print(j.GetProfileName("default_profile.json"))
# j.SaveMacro(Macro("portalocker.Lock",MacroType.KEYBOARD,"L"))