import json
import os
import sys
import numpy as np
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QAction, QCursor
import vosk
import sounddevice as sd
import time
import queue
from backend.macro_executor import execute_macro
from backend.macro_json_editor import  JSON_Editor
from gui.main_window import MainWindow


def run_recognizer(control_q, result_q):
    path = os.path.abspath("models/vosk-model-small-en-us-0.15")
    model = vosk.Model(path)

    #load macros and phrases from json
    json_ed = JSON_Editor("resources/default_profile.json")

    phrases = json_ed.GetPhrases()
    macros = json_ed.GetMacros()

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
                    phrases = json_ed.GetPhrases()
                    macros = json_ed.GetMacros()
                    rec = vosk.KaldiRecognizer(model, 16000, json.dumps(phrases))
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

def tray_app(control_q, result_q):
    app = QApplication(sys.argv)
    tray = QSystemTrayIcon(QIcon("assets/icon-on.png"))
    tray.setToolTip("Callout Backend")
    tray.show()

    menu = QMenu()
    start_action = QAction("Start Listening")
    stop_action = QAction("Stop Listening")
    exit_action = QAction("Exit")
    window_action = QAction("Open Window")

    w = MainWindow(control_q, result_q)

    menu.addAction(window_action)
    menu.addAction(start_action)
    menu.addAction(stop_action)
    menu.addSeparator()
    menu.addAction(exit_action)

    tray.setContextMenu(menu)
    tray.menu = menu
    tray.actions = (window_action, start_action, stop_action, exit_action)


    tray.window = w


    window_action.triggered.connect(w.show)
    start_action.triggered.connect(lambda : control_q.put("start"))
    stop_action.triggered.connect(lambda : control_q.put("pause"))
    exit_action.triggered.connect(lambda : exit_recognizer(control_q,app,tray))

    return app, tray

def exit_recognizer(control_q, app, tray):
    print("Exiting...")
    tray.hide()
    control_q.put("exit")
    app.quit()