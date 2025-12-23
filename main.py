import sys
from PySide6.QtWidgets import QApplication

from GUI.ui import MainWindow
#from GUI.controller import MainController
from GUI.dark_theme import apply_dark_theme

def main():
    app = QApplication(sys.argv)

    apply_dark_theme(app)

    w = MainWindow()
    #controller = MainController(w)  # keep reference if you want: w.controller = controller

    w.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


