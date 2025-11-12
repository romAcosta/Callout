import json
import os
import threading
from enum import Enum

import numpy as np

import vosk
import sounddevice as sd
import time
import queue
from backend.macro_executor import execute_macro
from backend.storage_management import JsonEditor, DatabaseEditor


class ListenMode(Enum):
    OPEN_MIC = 1
    PUSH_TO_TALK = 2
    VOICE_ACTIVATION = 3

timer = None
active_listening = True

def run_recognizer(control_q, result_q):
    global active_listening
    path = os.path.abspath("models/vosk-model-small-en-us-0.15")
    model = vosk.Model(path)

    #load macros and phrases from json
    db_editor = DatabaseEditor()
    json_editor = JsonEditor()

    command_word = json_editor.get_settings()["command_word"]
    macros = db_editor.get_macros(json_editor.get_current_profile())
    phrases = db_editor.get_phrases(macros)

    silence_start = time.time()
    speaking = False
    threshold = 500

    listening_mode = ListenMode(json_editor.get_settings()["listening_mode"])
    active_listening = False

    rec = vosk.KaldiRecognizer(model, 16000)
    if phrases: rec.SetGrammar(json.dumps(phrases))
    listening = True
    editing = False

    print("Listening Mode: " + str(listening_mode))

    with sd.RawInputStream(samplerate=16000, blocksize=2048, dtype='int16',
                           channels=1, latency='low') as stream:
        while True:

            try:
                command = control_q.get_nowait()
                if command == "exit":
                    break
                elif command == "start":
                    listening = True
                    print("Listening started")

                elif command == "pause":
                    listening = False
                    print("Listening paused")

                elif command == "edit":
                    editing = True

                    print("Editing Started")

                elif command == "save":
                    editing = False
                    macros = db_editor.get_macros(json_editor.get_current_profile())
                    phrases = db_editor.get_phrases(macros)
                    phrases.append(command_word)
                    if phrases: #rec.SetGrammar(json.dumps(phrases))
                        stream.stop()
                        rec = vosk.KaldiRecognizer(model, 16000, json.dumps(phrases))
                        stream.start()
                    print("Editing Saved")

                elif command == "get_state":
                    result_q.put({"type": "state", "paused": not listening})
                elif command == "exit":
                    break
            except queue.Empty:
                pass

            if listening_mode == ListenMode.OPEN_MIC:
                pass



            data = stream.read(4000)[0]
            arr = np.frombuffer(data, np.int16)
            level = np.max(np.abs(arr)) # absolute amplitude

            if listening and not editing:

                if listening_mode == ListenMode.PUSH_TO_TALK:  # TODO
                    continue
                if level > threshold: #Checks if amplitude is at speaking threshold

                    rec.AcceptWaveform(bytes(data))
                    speaking = True
                    silence_start = time.time()
                elif speaking and time.time() - silence_start > 0.2: #Forces a speach check after x amount of time passes

                    text = rec.FinalResult()
                    if listening_mode == ListenMode.VOICE_ACTIVATION:  # TODO
                        if listen_for_name(text,command_word):# and not active_listening:
                            active_listening = True
                            print("is_ready =", active_listening)
                            start_or_reset_timer()
                            pass
                        elif not active_listening:

                            continue
                    execute_macro(phrases, text, macros)
                    speaking = False
                    silence_start = time.time()
            else:
                time.sleep(0.05)

def set_active_listening_false():
    global active_listening
    active_listening = False
    print("is_ready =", active_listening)

def start_or_reset_timer():
    global timer
    if timer is not None:
        timer.cancel()
    timer = threading.Timer(3.0, set_active_listening_false)
    timer.start()
    print("Timer started/reset")

def listen_for_name(text:str, command_word):
    if text.__contains__(command_word):

        return True
    return False