from PySide2 import QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from event_handlers import setupEvents
from gui import Ui_MainWindow

# Attach event handlers


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    setupEvents(ui)

    MainWindow.show()
    sys.exit(app.exec_())
