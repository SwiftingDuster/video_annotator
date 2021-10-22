from typing import List

from PyQt5.QtCore import QPoint, QRect, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QColorConstants, QKeyEvent, QPainter, QPixmap
from PyQt5.QtWidgets import (QDialog, QHBoxLayout, QLabel, QPushButton,
                             QSizePolicy, QVBoxLayout)


class BBImageLabel(QLabel):
    draw_state = pyqtSignal(bool)
    #box_update = pyqtSignal(QPoint, QPoint)

    def __init__(self, image):
        super().__init__()
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image = QPixmap.fromImage(image)
        self.setPixmap(self.image)

        self.drawing = False

        self.box_start = self.box_end = QPoint(0, 0)

    def toggle_draw(self):
        self.drawing = not self.drawing
        self.draw_state.emit(self.drawing)

    def paintEvent(self, a0):
        super().paintEvent(a0)
        if self.drawing:
            rect = self._get_rect(self.box_start, self.box_end)
            painter = QPainter(self)
            painter.setBrush(QColor(0, 255, 0, 20))
            painter.drawRect(rect)

    def _get_rect(self, start: QPoint, end: QPoint):
        x1, y1 = start.x(), start.y()
        x2, y2 = end.x(), end.y()

        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        width = abs(x1 - x2)
        height = abs(y1 - y2)

        return QRect(x1, y1, width, height)

    def mousePressEvent(self, e):
        if self.drawing:
            self.box_start = e.pos()
            self.box_end = self.box_start
            #self.box_update.emit(self.box_start, self.box_end)
            self.update()
            print('press', e.pos())

    def mouseMoveEvent(self, e):
        if self.drawing:
            self.box_end = e.pos()
            #self.box_update.emit(self.box_start, self.box_end)
            self.update()

    # def keyPressEvent(self, e: QKeyEvent) -> None:
    #     k = e.key()
    #     if k == Qt.Key.Key_Return or k == Qt.Key.Key_Enter:
    #         print("enter")
    #     else:
    #         print(e.key())

    def resizeEvent(self, e):
        width, height = self.width(), self.height()
        self.setPixmap(self.image.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio))


class BoundingBoxDialog(QDialog):
    def __init__(self, image):
        super().__init__()

        self.setWindowTitle("Bounding Box")

        self.label_title = QLabel("Enclose position(s) of smoking incident with bounding box.")
        self.label_title.setStyleSheet("font-weight: bold;font-size: 16px;")
        self.label_image = BBImageLabel(image)

        self.lower_h_layout = QHBoxLayout()
        self.button_confirm = QPushButton("Finish")
        self.lower_h_layout.addWidget(self.button_confirm)
        self.button_add_bbox = QPushButton("New bounding box")
        self.lower_h_layout.addWidget(self.button_add_bbox)

        self.main_v_layout = QVBoxLayout()
        self.main_v_layout.addWidget(self.label_title)
        self.main_v_layout.addWidget(self.label_image)
        self.main_v_layout.addLayout(self.lower_h_layout)
        self.main_v_layout.setStretch(1, 2)
        self.setLayout(self.main_v_layout)

        size = QSize(1000, 600)
        self.setMinimumSize(size)
        self.resize(size)

        self.button_add_bbox.clicked.connect(self._button_add_bbox)
        self.label_image.draw_state.connect(self._draw_state_changed)

    def _button_add_bbox(self):
        self.label_image.toggle_draw()

    def _draw_state_changed(self, state):
        if state:
            self.button_add_bbox.setText("End bounding box")
        else:
            self.button_add_bbox.setText("New bounding box")


if __name__ == "__main__":
    import sys

    from PyQt5.QtGui import QImage
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ui = BoundingBoxDialog(QImage("a.png"))
    ui.show()
    sys.exit(app.exec_())
