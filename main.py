from PyQt5 import QtWidgets

from gui import Ui_MainWindow

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    ui.setupEvents()

    MainWindow.show()
    sys.exit(app.exec_())
