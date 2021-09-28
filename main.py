from PyQt5.QtWidgets import QApplication, QMainWindow

from gui import Ui_MainWindow

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    ui.setupEvents()

    MainWindow.show()
    sys.exit(app.exec_())
