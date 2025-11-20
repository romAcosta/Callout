import sys
# import ctypes
# from ctypes import wintypes


from multiprocessing import Process, Queue
from PyQt6.QtCore import QTimer
from backend.recognizer import run_recognizer
from backend.utility import resource_path
from gui.tray_app import tray_app
import multiprocessing


if __name__ == "__main__":
    multiprocessing.freeze_support()
    control_q, result_q = Queue(), Queue()

    recognizer_process = Process(target=run_recognizer, args=(control_q, result_q))
    recognizer_process.start()

    app, tray = tray_app(control_q, result_q)

    def poll_results():
        if not result_q.empty():
            text = result_q.get()
            print("Heard:", text)


    timer = QTimer()
    timer.timeout.connect(poll_results)
    timer.start(100)
    with open(resource_path("gui/styles.qss"), "r") as f:
        qss = f.read()
        app.setStyleSheet(qss)

    # app.setStyle("Fusion")
    app.exec()

    control_q.put("stop")
    recognizer_process.join()