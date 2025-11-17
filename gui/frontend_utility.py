def show_window(window):
    window.show()
    if window.isMinimized():
        window.showNormal()
    window.raise_()
    window.activateWindow()
