import json
import os
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QAction, QCursor
import vosk
import sounddevice as sd
from backend.macro_executor import execute_macro

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
    rec = vosk.KaldiRecognizer(model, 16000, json.dumps(["open browser", "close window", "reload"]))
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1) as stream:
        while True:
            if not control_q.empty() and control_q.get() == "stop":
                break
            data = stream.read(4000)[0]
            if rec.AcceptWaveform(bytes(data)):
                text = json.loads(rec.Result())["text"]
                result_q.put(text)
            execute_macro(rec.Result())


def tray_app(control_q):
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

