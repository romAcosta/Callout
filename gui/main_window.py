from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
import sys

from gui.ui_compenents import EditableLabel, MacroUI, MacroMenu



class LabeledSlider(QWidget):
    def __init__(self, label_text):
        super().__init__()
        self.label = QLabel(label_text)
        self.slider = QSlider(Qt.Orientation.Horizontal)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.slider)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setWindowTitle("My App")

        label = MacroMenu()

        slider = LabeledSlider("her ye")


        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        button.clicked.connect(self.the_button_was_toggled)
        button.setFixedSize(60, 40)


        layout.addWidget(button)
        layout.addWidget(slider)
        layout.addWidget(label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    def the_button_was_clicked(self):
        print("Clicked!")

    def the_button_was_toggled(self, checked):
        print("Checked?", checked)


app = QApplication(sys.argv)
app.setStyle("Fusion")


window = MainWindow()
window.show()

app.exec()
