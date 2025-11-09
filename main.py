from multiprocessing import Process, Queue

from PyQt6.QtCore import QTimer

from backend.storage_management import JsonEditor
from backend.recognizer import run_recognizer
from gui.tray_app import tray_app

if __name__ == "__main__":
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
    app.setStyle("Fusion")
    app.exec()

    control_q.put("stop")
    recognizer_process.join()