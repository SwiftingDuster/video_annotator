from PyQt5.QtCore import QObject, QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QMouseEvent, QPainter
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QFrame, QWidget


class BBVideoWidget(QVideoWidget):
    update_box = pyqtSignal(QPoint, QPoint)

    def __init__(self):
        super().__init__()
        self.can_draw_box = False

    def mousePressEvent(self, event: QMouseEvent):
        self.box_start = event.pos()
        self.box_end = self.box_start
        print("Press")

    def mouseMoveEvent(self, event: QMouseEvent):
        self.box_end = event.pos()
        self.update_box.emit(self.box_start, self.box_end)


class BoundingBoxWidget(QFrame):

    def __init__(self, parent: BBVideoWidget):
        super().__init__(parent)
        # self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        # self.setVisible(False)
        self.setStyleSheet("border:1px solid rgb(0, 255, 0);background: transparent")
        self.setBaseSize(100, 100)
        self.setMaximumSize(parent.size())

        parent.update_box.connect(self.update_box)

    def paintEvent(self, event):
        super().paintEvent(event)
        self.raise_()

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
