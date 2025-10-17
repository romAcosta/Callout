from symtable import Class

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

class EditableLabel(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)


        self.label = QLabel("Click Edit to change me")
        self.label.setMaximumSize(300, 40)
        self.edit = QLineEdit(self.label.text())
        self.edit.setFixedSize(100,30)
        self.edit.hide()

        self.toggle_button = QPushButton("Edit")
        self.toggle_button.setFixedSize(30,30)
        self.toggle_button.clicked.connect(self.toggle_mode)

        self.layout.addWidget(self.toggle_button)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)
        self.layout.setSizeConstraint(self.layout.SizeConstraint.SetFixedSize)

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

class MacroUI(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)


        self.inner_widget = QFrame()
        self.inner_widget.setFrameShape(QFrame.Shape.Box)
        self.inner_widget.setLineWidth(2)
        self.inner_widget.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;    /* fill color */
                border-radius: 8px;           /* rounded corners */
                padding: 0.1px;                /* space inside border */
            }
        """)



        self.layout = QHBoxLayout(self)
        self.editableLabel = EditableLabel()
        self.text = QLabel("->")
        self.text.setFixedSize(40, 30)

        self.button = QPushButton()
        self.button.setFixedSize(50, 30)

        self.delete_button = QPushButton("X")
        self.delete_button.setFixedSize(20,20)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #4b0000;
            }
        """)
        self.delete_button.clicked.connect(self.delete_self)

        self.inner_layout = QHBoxLayout(self.inner_widget)
        self.inner_layout.addWidget(self.editableLabel)
        self.inner_layout.addWidget(self.text)
        self.inner_layout.addWidget(self.button)
        self.inner_layout.addWidget(self.delete_button)
        self.inner_layout.setSizeConstraint(self.layout.SizeConstraint.SetFixedSize)


        self.main_layout.addWidget(self.inner_widget)

    def delete_self(self):
        parent_layout = self.parentWidget().layout()
        if parent_layout:
            parent_layout.removeWidget(self)
        self.setParent(None)
        self.deleteLater()



class MacroMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.content = QWidget()

        # Scroll
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.content)
        self.scroll.setFixedWidth(400)
        self.scroll.setMinimumHeight(500)

        self.layout = QVBoxLayout(self.content)

        # Add Macro Button
        self.button = QPushButton("Add Macro")
        self.button.clicked.connect(self.add_widgets)

        self.main_layout.addWidget(self.scroll)
        self.main_layout.addWidget(self.button)

        self.layout.addStretch()

    def add_widgets(self): # Creates a Widget within the Scroll Area
        self.new_label = MacroUI()
        self.layout.insertWidget(0, self.new_label)