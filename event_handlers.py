from gui import Ui_MainWindow
from PySide2.QtWidgets import QFileDialog


def setupEvents(ui: Ui_MainWindow):
    ui.action_open_file.triggered.connect(openFileNameDialog)


def openFileNameDialog():
    fileName, _ = QFileDialog.getOpenFileName(
        None, "Open Image", "", "Video Files (*.mp4)")
    if fileName:
        print(fileName)
