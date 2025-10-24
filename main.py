from multiprocessing import Process, Queue

from PyQt6.QtCore import QTimer

from backend.recognizer import run_recognizer, tray_app
from gui.main_window import ActivateWindow
#
# if __name__ == "__main__":
#     control_q, result_q = Queue(), Queue()
#     recognizer_process = Process(target=run_recognizer, args=(control_q, result_q))
#     recognizer_process.start()
#     tray_app(control_q)
#     # ActivateWindow()
#     while True:
#         if not result_q.empty():
#             print("Heard:", result_q.get())
#         # stop condition example:
#         if input() == "stop":
#             control_q.put("stop")
#             recognizer_process.join()
#             break

if __name__ == "__main__":
    control_q, result_q = Queue(), Queue()
    recognizer_process = Process(target=run_recognizer, args=(control_q, result_q))
    recognizer_process.start()

    app, tray = tray_app()

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