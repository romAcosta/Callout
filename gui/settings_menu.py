from PyQt6.QtGui import QWindow
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QLineEdit

from backend.storage_management import DatabaseEditor, JsonEditor
from gui.ui_compenents import ProfileDropdown

class SettingsMenu(QWidget):
    def __init__(self,json_editor: JsonEditor, profile_dropdown: ProfileDropdown):
        super().__init__()
        self.profile_dropdown = profile_dropdown
        self.json_editor = json_editor

        layout = QVBoxLayout()
        button_layout =QHBoxLayout()

        self.cancel_button = QPushButton("Cancel")
        self.create_button = QPushButton("Create")

        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.create_button)

        self.label = QLabel("Create New Profile")

        self.error_label = QLabel("Name cannot be empty!")
        self.error_label.hide()
        self.error_label.setStyleSheet("""
            color:#ff3d28;
        """)

        self.text_box = QLineEdit()
        self.text_box.setPlaceholderText("Profile Name")

        # self.create_button.clicked.connect(self.create_profile)
        # self.cancel_button.clicked.connect(self.close)


        layout.addWidget(self.label)
        layout.addWidget(self.error_label)
        layout.addWidget(self.text_box)
        layout.addLayout(button_layout)

        self.setLayout(layout)