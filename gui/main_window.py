
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import *
import sys


from backend.storage_management import Macro, MacroType, JsonEditor, DatabaseEditor
from gui.new_profile_menu import NewProfileMenu
from gui.ui_compenents import MacroUI, MacroMenu, ProfileDropdown
from PyQt6.QtCore import QSize

class MainWindow(QMainWindow ):
    def __init__(self, control_q, result_q):
        super().__init__()
        self.w = None
        self.db_editor = DatabaseEditor()
        self.json_editor = JsonEditor()

        # Set Queues
        self.control_q = control_q
        self.result_q = result_q
        self.paused = False

        edit_profile_layout = QHBoxLayout()
        layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        self.setWindowTitle("Callout")
        self.setWindowIcon(QIcon("assets/icon.png"))

        self.menu = MacroMenu(self.db_editor, self.json_editor)
        self.menu.setEnabled(False)
        self.profile_dropdown = ProfileDropdown(self.db_editor,self.json_editor, self.menu, self.profile_changed)
        self.add_profile_button = QPushButton("Add Profile")
        self.add_profile_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.add_profile_button.adjustSize()



        self.enable_button = QPushButton("Edit")
        self.enable_button.setCheckable(True)
        self.enable_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.enable_button.adjustSize()

        self.pause_button = QPushButton("Pause")
        self.pause_button.setCheckable(True)
        self.pause_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.pause_button.adjustSize()

        self.settings_button = QPushButton()
        self.settings_button.setFixedSize(20, 20)
        self.settings_button.setIcon(QIcon("assets/settings-icon.png"))
        self.settings_button.setIconSize(QSize(20, 20))
        self.settings_button.setFlat(True)
        self.settings_button.setStyleSheet("background: transparent;")

        edit_profile_layout.addWidget(self.enable_button)
        edit_profile_layout.addWidget(self.profile_dropdown)
        edit_profile_layout.addWidget(self.add_profile_button)

        top_layout.addWidget(self.pause_button,alignment=Qt.AlignmentFlag.AlignLeft)
        top_layout.addWidget(self.settings_button, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(top_layout)
        layout.addLayout(edit_profile_layout)
        layout.addWidget(self.menu)


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


        self.pause_button.toggled.connect(self.the_button_was_toggled)
        self.enable_button.toggled.connect(self.enable_macro_menu)
        self.add_profile_button.clicked.connect(self.open_new_profile_menu)

        # Start timer to begin polling backend
        self.timer = QTimer()
        self.timer.timeout.connect(self.poll_results)
        QTimer.singleShot(0, lambda: self.timer.start(50))


        # Get the backends current state
        self.control_q.put("get_state")


    def open_new_profile_menu(self):
        self.w = NewProfileMenu(self.db_editor,self.profile_dropdown)
        self.w.show()

    def enable_macro_menu(self, checked):
        if(checked):
            self.control_q.put("edit")
            self.enable_button.setText("Save")
            self.menu.setEnabled(True)
        else:
            self.save_macros()

            self.enable_button.setText("Edit")
            self.menu.setEnabled(False)

            self.control_q.put("save")

    def profile_changed(self):
        print("(DEBUG) Profile Changed")
        self.control_q.put("save")

    def save_macros(self):

        macros = []
        for i in range(self.menu.layout.count()):
            item = self.menu.layout.itemAt(i)
            widget = item.widget()
            if widget and hasattr(widget, "edit_box") and hasattr(widget, "macro_button"):
                phrase = widget.edit_box.text()
                command = widget.macro_button.text()
                macros.append(Macro(phrase,MacroType.KEYBOARD,command).to_dict())

        self.db_editor.save_macros(self.json_editor.get_current_profile(),macros)

        print(macros)

    def the_button_was_toggled(self, checked):
        if(checked):
            self.control_q.put("pause")
            self.pause_button.setText("Start")
        else:
            self.control_q.put("start")
            self.pause_button.setText("Pause")

    def poll_results(self):
        while not self.result_q.empty():
            message = self.result_q.get()

            if isinstance(message, dict) and message.get("type") == "state":
                paused = message["paused"]
                self.pause_button.setChecked(paused)
                self.paused = paused
                if paused:
                    self.pause_button.setText("Start")
                print("Backend says paused:", paused)
            else:
                pass

    def reload_window(self):
        self.hide()
        self.new_window = MainWindow(self.control_q,self.result_q)
        self.new_window.show()

    def closeEvent(self, event):
        event.ignore()
        if self.enable_button.isChecked():
            self.enable_button.toggle()

        self.hide()
        self.timer.stop()

    def showEvent(self, event):
        super().showEvent(event)

        self.control_q.put("get_state")
        if not self.timer.isActive():
            self.timer.start(50)

            print("Polling restarted")



