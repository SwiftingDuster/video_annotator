from PyQt5.QtWidgets import QApplication, QMainWindow

from gui import Ui_MainWindow
import sys


def main():
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
