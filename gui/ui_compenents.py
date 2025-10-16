from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

class EditableLabel(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)

        # Create both widgets
        self.label = QLabel("Click Edit to change me")
        self.edit = QLineEdit(self.label.text())
        self.edit.setFixedSize(100,30)
        self.edit.hide()  # start hidden

        self.toggle_button = QPushButton("Edit")
        self.toggle_button.setFixedSize(30,30)
        self.toggle_button.clicked.connect(self.toggle_mode)

        self.layout.addWidget(self.toggle_button)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)

        self.edit.returnPressed.connect(self.commit_text)

    def toggle_mode(self):
        if self.label.isVisible():
            self.label.hide()
            self.edit.show()
            self.edit.setText(self.label.text())
            self.toggle_button.setText("Save")
            self.edit.setFocus()
        else:
            self.commit_text()

    def commit_text(self):
        self.label.setText(self.edit.text())
        self.edit.hide()
        self.label.show()
        self.toggle_button.setText("Edit")