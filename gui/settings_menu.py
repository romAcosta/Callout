from multiprocessing.queues import Queue

from PyQt6.QtGui import QWindow, QKeySequence
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QLineEdit, QComboBox

import sounddevice as sd
from backend.storage_management import DatabaseEditor, JsonEditor
from gui.ui_compenents import ProfileDropdown

class SettingsMenu(QWidget):
    def __init__(self,json_editor: JsonEditor, control_q: Queue):
        super().__init__()

        self.control_q = control_q
        self.json_editor = json_editor

        layout = QVBoxLayout()
        settings = json_editor.get_settings()





        self.label = QLabel("Settings")
        self.listen_mode_layout = QHBoxLayout()


        self.listen_mode_label = QLabel("Listening Mode:")
        self.listen_mode_dropdown = QComboBox()

        self.listen_mode_dropdown.addItem("Open Microphone")
        self.listen_mode_dropdown.addItem("Push to Talk")
        self.listen_mode_dropdown.addItem("Voice Activation")
        self.listen_mode_dropdown.setCurrentIndex(settings["listening_mode"] - 1)

        self.listen_mode_layout.addWidget(self.listen_mode_label)
        self.listen_mode_layout.addWidget(self.listen_mode_dropdown)

        # self.ptt_button_label = QLabel("Listening Mode:")
        # self.ptt_button = QPushButton(settings["command_key"])



        #TODO Maybe include customization for listening mode





        # self.create_button.clicked.connect(self.create_profile)
        # self.cancel_button.clicked.connect(self.close)

        layout.addWidget(self.label)
        layout.addLayout(self.listen_mode_layout)


        self.listen_mode_dropdown.currentIndexChanged.connect(self.change_listening_mode)

        self.setLayout(layout)

    def change_listening_mode(self):
        self.json_editor.set_listening_mode(self.listen_mode_dropdown.currentIndex()+1)
        self.control_q.put({"command":"listen_mode_changed"})

    # def listen_macro(self,checked):
    #     if checked:
    #         self.listening = True
    #         self.macro_button.setEnabled(False)
    #         self.setFocus()
    #         print("UI: Listening for a key press...")
    #
    # def keyPressEvent(self, event):
    #     if self.listening:
    #         key_name = QKeySequence(event.key()).toString()
    #         print(f"Key pressed: {key_name}")
    #         self.stop_listening(key_name.lower())
    #
    #
    # def stop_listening(self, text):
    #     self.listening = False
    #     self.macro_button.setEnabled(True)
    #     self.macro_button.setChecked(False)
    #     self.macro_button.setText(text)




def get_input_devices():
    devices = sd.query_devices()

    mics = []
    for i, dev in enumerate(devices):
        if dev["max_input_channels"] > 0 and dev["hostapi"] == sd.default.hostapi:
            mics.append((i, dev["name"]))
    return mics