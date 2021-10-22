from PyQt5.QtCore import QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QDialog, QFrame, QLabel, QVBoxLayout


class CustomQLabel(QLabel):

    box_update = pyqtSignal(QPoint, QPoint)

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        self.box_start = event.pos()
        self.box_end = self.box_start
        self.box_update.emit(self.box_start, self.box_end)
        print("Press")

    def mouseMoveEvent(self, event):
        self.box_end = event.pos()
        self.box_update.emit(self.box_start, self.box_end)


class BoundingBoxWidget(QFrame):

    def __init__(self, parent: CustomQLabel):
        super().__init__(parent)
        # self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        # self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setStyleSheet("border:1px solid rgb(0, 255, 0);background: transparent")
        self.setBaseSize(100, 100)
        self.setMaximumSize(parent.size())

        parent.box_update.connect(self.update_box)

    def update_box(self, start: QPoint, end: QPoint):
        x1, y1 = start.x(), start.y()
        x2, y2 = end.x(), end.y()

        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        width = abs(start.x() - end.x())
        height = abs(start.y() - end.y())
        self.setFixedSize(width, height)
        self.move(x1, y1)


class BoundingBoxDialog(QDialog):
    def __init__(self, image):
        super().__init__()

        self.setWindowTitle("Image Viewer")

        self.image_label = CustomQLabel()
        self.bb_overlay = BoundingBoxWidget(self.image_label)

        self.main_v_layout = QVBoxLayout()
        self.main_v_layout.addWidget(self.image_label)
        self.main_v_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_v_layout)

        self.image = QPixmap.fromImage(image)
        self.image_label.setPixmap(self.image)
        self.image_label.setMinimumSize(1, 1)
        ratio = image.width() / image.height()
        self.resize(600 * ratio, 600)

    def resizeEvent(self, event):
        width, height = self.width(), self.height()
        self.image_label.setPixmap(self.image.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio))
        super().resizeEvent(event)
