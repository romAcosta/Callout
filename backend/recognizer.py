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

from backend.macro_executor import execute_macro
from backend.macros import GetPhrases, GetMacros


# path = os.path.abspath("../models/vosk-model-small-en-us-0.15")
# model = vosk.Model(path)
# rec = vosk.KaldiRecognizer(model, 16000,json.dumps(["open browser", "close window", "reload"]))
# rec.SetWords(['reload','next','hello'])
# with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1) as stream:
#     while True:
#         data = stream.read(4000)[0]
#         if rec.AcceptWaveform(bytes(data)):
#             print(rec.Result())
#
#         execute_macro(rec.Result())




def run_recognizer(control_q, result_q):
    path = os.path.abspath("models/vosk-model-small-en-us-0.15")
    model = vosk.Model(path)

    #load macros and phrases from json
    phrases = GetPhrases()
    macros = GetMacros()

    silence_start = time.time()
    speaking = False
    threshold = 500

    rec = vosk.KaldiRecognizer(model, 16000, json.dumps(phrases))

    with sd.RawInputStream(samplerate=16000, blocksize=2048, dtype='int16',
                           channels=1, latency='low') as stream:
        while True:
            if not control_q.empty() and control_q.get() == "stop":
                break


            data = stream.read(4000)[0]
            arr = np.frombuffer(data, np.int16)
            level = np.max(np.abs(arr))  # absolute amplitude

            if level > threshold: #Checks if amplitude is at speaking threshold

                rec.AcceptWaveform(bytes(data))
                speaking = True
                silence_start = time.time()
            elif speaking and time.time() - silence_start > 0.2: #Forces a speach check after x amount of time passes

                text = rec.FinalResult()
                execute_macro(phrases, text, macros)
                speaking = False
                silence_start = time.time()

def tray_app():
    app = QApplication(sys.argv)
    tray = QSystemTrayIcon(QIcon("assets/icon.png"))
    tray.setToolTip("Callout Backend")
    tray.show()

    menu = QMenu()
    start_action = QAction("Start Listening")
    stop_action = QAction("Stop Listening")
    exit_action = QAction("Exit")

    menu.addAction(start_action)
    menu.addAction(stop_action)
    menu.addSeparator()
    menu.addAction(exit_action)

    tray.setContextMenu(menu)
    tray.menu = menu
    tray.actions = (start_action, stop_action, exit_action)




    exit_action.triggered.connect(app.quit)

    return app, tray

