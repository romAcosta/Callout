from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import *
import sys
from gui.ui_compenents import EditableLabel, MacroUI, MacroMenu


class MainWindow(QMainWindow ):
    def __init__(self, control_q, result_q):
        super().__init__()

        # Set Queues
        self.control_q = control_q
        self.result_q = result_q
        self.paused = False

        layout = QVBoxLayout()
        self.setWindowTitle("Callout")
        self.setWindowIcon(QIcon("assets/icon.png"))


        self.menu = MacroMenu()
        self.menu.setEnabled(False)



        self.enable_button = QPushButton("Edit")
        self.enable_button.setCheckable(True)
        self.enable_button.setFixedSize(40, 20)

        self.button = QPushButton("Pause")
        self.button.setCheckable(True)
        self.button.setFixedSize(60, 40)


        layout.addWidget(self.button)
        layout.addWidget(self.enable_button)
        layout.addWidget(self.menu)


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


        self.button.toggled.connect(self.the_button_was_toggled)
        self.enable_button.toggled.connect(self.enable_macro_menu)


        # Start timer to begin polling backend
        self.timer = QTimer()
        self.timer.timeout.connect(self.poll_results)
        QTimer.singleShot(0, lambda: self.timer.start(50))


        # Get the backends current state
        self.control_q.put("get_state")




    def enable_macro_menu(self, checked):
        if(checked):
            self.enable_button.setText("Save")
            self.menu.setEnabled(True)
        else:
            self.enable_button.setText("Edit")
            self.menu.setEnabled(False)


    def the_button_was_toggled(self, checked):
        print("Checked?", checked)
        if(checked):
            self.control_q.put("pause")
            self.button.setText("Start")
        else:
            self.control_q.put("start")
            self.button.setText("Pause")

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
                pass


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



