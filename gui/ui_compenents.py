from symtable import Class

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import *

from backend.macro_json_editor import  JSON_Editor






class MacroUI(QWidget):
    def __init__(self, phrase = None, command = None):
        super().__init__()
        self.listening = False
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

        #macro button
        self.macro_button = QPushButton()
        self.macro_button.setFixedSize(50, 30)
        self.macro_button.setCheckable(True)

        self.macro_button.clicked.connect(self.listen_macro)

        editable_label_text = None
        if phrase is not None and command is not None:
            editable_label_text = phrase
            self.macro_button.setText(command)

        self.layout = QHBoxLayout(self)
        self.edit_box = QLineEdit(editable_label_text)
        self.edit_box.setFixedSize(100, 30)

        self.text = QLabel("->")
        self.text.setFixedSize(40, 30)



        self.delete_button = QPushButton("X")
        self.delete_button.setFixedSize(20,20)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #4b0000;
            }
        """)
        self.delete_button.clicked.connect(self.delete_self)




        self.inner_layout = QHBoxLayout(self.inner_widget)
        self.inner_layout.addWidget(self.edit_box)
        self.inner_layout.addWidget(self.text)
        self.inner_layout.addWidget(self.macro_button)
        self.inner_layout.addWidget(self.delete_button)
        self.inner_layout.setSizeConstraint(self.layout.SizeConstraint.SetFixedSize)


        self.main_layout.addWidget(self.inner_widget)

    def listen_macro(self,checked):
        if checked:
            self.listening = True
            self.macro_button.setEnabled(False)
            self.setFocus()
            print("UI: Listening for a key press...")

    def keyPressEvent(self, event):
        if self.listening:
            key_name = QKeySequence(event.key()).toString()
            print(f"Key pressed: {key_name}")
            self.stop_listening(key_name.lower())

    #TODO Get mouse working

    # def mousePressEvent(self, event):
    #     if self.listening:
    #         button_map = {
    #             Qt.MouseButton.LeftButton: "Left Click",
    #             Qt.MouseButton.RightButton: "Right Click",
    #             Qt.MouseButton.MiddleButton: "Middle Click",
    #         }
    #         btn_name = button_map.get(event.button(), "Other Button")
    #         print(f"Mouse pressed: {btn_name}")
    #         self.stop_listening(f"Mouse: {btn_name}")

    def stop_listening(self, text):
        self.listening = False
        self.macro_button.setEnabled(True)
        self.macro_button.setChecked(False)
        self.macro_button.setText(text)


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

        #import and add macros to UI
        json_ed = JSON_Editor("resources/default_profile.json")
        macros = json_ed.GetMacros()
        for macro in macros:
            self.new_label = MacroUI(macro["phrase"],macro["command"])
            self.layout.insertWidget(self.layout.count() - 1, self.new_label)

    def add_widgets(self): # Creates a Widget within the Scroll Area
        self.new_label = MacroUI()
        self.layout.insertWidget(self.layout.count() - 1, self.new_label)


