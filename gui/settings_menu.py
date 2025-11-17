from multiprocessing.queues import Queue

from PyQt6.QtGui import QWindow
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QLineEdit, QComboBox


from backend.storage_management import DatabaseEditor, JsonEditor
from gui.ui_compenents import ProfileDropdown

class SettingsMenu(QWidget):
    def __init__(self,json_editor: JsonEditor, control_q: Queue):
        super().__init__()

        self.control_q = control_q
        self.json_editor = json_editor

        layout = QVBoxLayout()


        self.label = QLabel("Settings")
        self.listen_mode_layout = QHBoxLayout()
        self.command_word_layout = QHBoxLayout()

        self.listen_mode_label = QLabel("Listening Mode:")
        self.listen_mode_dropdown = QComboBox()

        self.listen_mode_dropdown.addItem("Open Microphone")
        self.listen_mode_dropdown.addItem("Push to Talk")
        self.listen_mode_dropdown.addItem("Voice Activation")
        self.listen_mode_dropdown.setCurrentIndex(json_editor.get_settings()["listening_mode"] - 1)

        self.listen_mode_layout.addWidget(self.listen_mode_label)
        self.listen_mode_layout.addWidget(self.listen_mode_dropdown)


        #TODO Maybe include customization for listening mode





        # self.create_button.clicked.connect(self.create_profile)
        # self.cancel_button.clicked.connect(self.close)

        layout.addWidget(self.label)
        layout.addLayout(self.listen_mode_layout)
        layout.addLayout(self.command_word_layout)

        self.listen_mode_dropdown.currentIndexChanged.connect(self.change_listening_mode)

        self.setLayout(layout)

    def change_listening_mode(self):
        self.json_editor.set_listening_mode(self.listen_mode_dropdown.currentIndex()+1)
        self.control_q.put("listen_mode_changed")
