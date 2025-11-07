import json
import os

import numpy as np

import vosk
import sounddevice as sd
import time
import queue
from backend.macro_executor import execute_macro
from backend.macro_json_editor import  JsonEditor



def run_recognizer(control_q, result_q):
    path = os.path.abspath("models/vosk-model-small-en-us-0.15")
    model = vosk.Model(path)

    #load macros and phrases from json
    json_ed = JsonEditor("resources/profiles")

    phrases = json_ed.get_phrases()
    macros = json_ed.get_macros()

    silence_start = time.time()
    speaking = False
    threshold = 500

    rec = vosk.KaldiRecognizer(model, 16000, json.dumps(phrases))
    listening = True
    editing = False
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
                    phrases = json_ed.get_phrases()
                    macros = json_ed.get_macros()
                    rec.SetGrammar(json.dumps(phrases))
                    print("Editing Saved")
                elif command == "get_state":
                    result_q.put({"type": "state", "paused": not listening})
                elif command == "exit":
                    break
            except queue.Empty:
                pass


            data = stream.read(4000)[0]
            arr = np.frombuffer(data, np.int16)
            level = np.max(np.abs(arr)) # absolute amplitude

            if listening and not editing:


                if level > threshold: #Checks if amplitude is at speaking threshold

                    rec.AcceptWaveform(bytes(data))
                    speaking = True
                    silence_start = time.time()
                elif speaking and time.time() - silence_start > 0.2: #Forces a speach check after x amount of time passes

                    text = rec.FinalResult()
                    execute_macro(phrases, text, macros)
                    speaking = False
                    silence_start = time.time()
            else:
                time.sleep(0.05)

