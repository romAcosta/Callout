from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import *
import sys

from gui.ui_compenents import EditableLabel, MacroUI, MacroMenu





class MainWindow(QMainWindow ):
    def __init__(self, control_q, result_q):
        super().__init__()
        layout = QVBoxLayout()
        self.paused = False
        self.setWindowTitle("Callout")
        self.setWindowIcon(QIcon("assets/icon.png"))
        label = MacroMenu()

        self.control_q = control_q
        self.result_q = result_q


        self.button = QPushButton("Pause")
        self.button.setCheckable(True)
        self.button.setFixedSize(60, 40)


        layout.addWidget(self.button)
        layout.addWidget(label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


        self.button.toggled.connect(self.the_button_was_toggled)

        self.timer = QTimer()
        self.timer.timeout.connect(self.poll_results)
        QTimer.singleShot(0, lambda: self.timer.start(50))


        # --- Ask backend for its current state ---
        self.control_q.put("get_state")

    def poll_results(self):
        while not self.result_q.empty():
            message = self.result_q.get()
            if isinstance(message, dict) and message.get("type") == "state":
                paused = message["paused"]
                self.button.setChecked(paused)
                self.paused = paused
                if paused:
                    self.button.setText("Start")
                print("Backend says paused:", paused)
            else:
                # handle normal recognition results here
                pass





    def the_button_was_toggled(self, checked):
        print("Checked?", checked)
        if(checked):
            self.control_q.put("pause")
            self.button.setText("Start")
        else:
            self.control_q.put("start")
            self.button.setText("Pause")

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.timer.stop()

    def showEvent(self, event):
        super().showEvent(event)
        self.control_q.put("get_state")
        if not self.timer.isActive():
            self.timer.start(50)

            print("Polling restarted")

def ActivateWindow():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")


    window = MainWindow()
    window.show()

    app.exec()

# ActivateWindow()