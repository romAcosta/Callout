from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import *
import sys

from gui.ui_compenents import EditableLabel, MacroUI, MacroMenu





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setWindowTitle("Callout")
        self.setWindowIcon(QIcon("assets/icon.png"))
        label = MacroMenu()




        button = QPushButton("Press Me!")
        button.setCheckable(True)

        button.setFixedSize(60, 40)


        layout.addWidget(button)
        layout.addWidget(label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def closeEvent(self, event):
        event.ignore()
        self.hide()

def ActivateWindow():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")


    window = MainWindow()
    window.show()

    app.exec()

# ActivateWindow()