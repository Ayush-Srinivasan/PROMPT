import sys
from PySide6.QtWidgets import QApplication

from GUI.ui import MainWindow
from GUI.controller import MainController

def main():
    app = QApplication(sys.argv)

    w = MainWindow()
    controller = MainController(w)  # keep reference if you want: w.controller = controller

    w.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


