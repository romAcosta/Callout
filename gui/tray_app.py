﻿import sys

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMenu, QSystemTrayIcon, QApplication

from gui.main_window import MainWindow


def tray_app(control_q, result_q):
    app = QApplication(sys.argv)
    tray = QSystemTrayIcon(QIcon("assets/icon-on.png"))
    tray.setToolTip("Callout Backend")
    tray.show()

    menu = QMenu()
    start_action = QAction("Start Listening")
    stop_action = QAction("Stop Listening")
    exit_action = QAction("Exit")
    window_action = QAction("Open Window")

    w = MainWindow(control_q, result_q)

    menu.addAction(window_action)
    menu.addAction(start_action)
    menu.addAction(stop_action)
    menu.addSeparator()
    menu.addAction(exit_action)

    tray.setContextMenu(menu)
    tray.menu = menu
    tray.actions = (window_action, start_action, stop_action, exit_action)


    tray.window = w


    window_action.triggered.connect(w.show)
    start_action.triggered.connect(lambda : control_q.put("start"))
    stop_action.triggered.connect(lambda : control_q.put("pause"))
    exit_action.triggered.connect(lambda : exit_recognizer(control_q,app,tray))

    return app, tray

def exit_recognizer(control_q, app, tray):
    print("Exiting...")
    tray.hide()
    control_q.put("exit")
    app.quit()