from PyQt5 import QtWidgets
from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QMouseEvent, QPainter, QPixmap
from PyQt5.QtWidgets import (QDialog, QGridLayout, QHBoxLayout, QLabel, QMessageBox,
                             QPushButton, QSizePolicy, QVBoxLayout)


class BBImageLabel(QLabel):
    draw_state = pyqtSignal(bool)

    def __init__(self, image, current_boxes: list[QRect]):
        super().__init__()
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.image = QPixmap.fromImage(image)
        self.setPixmap(self.image)

        self.drawing = False
        self.box_rect = None
        self.boxes = [] if current_boxes is None else [self.image_to_ratio(b) for b in current_boxes]

    def toggle_draw(self):
        self.drawing = not self.drawing
        if self.drawing:  # Start drawing
            self.box_rect = QRectF()
        else:  # End drawing
            if self.box_rect.width() == 0 and self.box_rect.height() == 0:
                # No box was drawn, don't do anything
                print("No box")
            elif self.box_rect.width() < 0.01 or self.box_rect.height() < 0.01:
                self.drawing = True  # Don't end drawing
                prompt = QMessageBox()
                prompt.setWindowTitle("Error")
                prompt.setText("Please draw a bigger box.")
                prompt.exec()
            else:
                self.boxes.append(self.box_rect)

        self.draw_state.emit(self.drawing)
        self.update()

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setBrush(QColor(255, 0, 0, 20))
        for box in self.boxes:
            painter.drawRect(self._ratio_to_view(box))
        if self.drawing:
            rect = self._ratio_to_view(self.box_rect)
            painter.setBrush(QColor(0, 255, 0, 20))
            painter.drawRect(rect)

    def _get_box(self, start: QPoint, end: QPoint):
        # Normalize returns a rect with non negative width/height.
        return QRect(start, end).normalized()

    def _view_to_ratio(self, box: QRect, relative_size: QSize = None):
        view_w = self.width() if relative_size is None else relative_size.width()
        view_h = self.height() if relative_size is None else relative_size.height()
        tl = box.topLeft()
        br = box.bottomRight()
        ratio_box = QRectF()
        ratio_box.setTopLeft(QPointF(tl.x() / view_w, tl.y() / view_h))
        ratio_box.setBottomRight(QPointF(br.x() / view_w, br.y() / view_h))
        return ratio_box

    def _ratio_to_view(self, ratio_box: QRectF, relative_size: QSize = None):
        view_w = self.width() if relative_size is None else relative_size.width()
        view_h = self.height() if relative_size is None else relative_size.height()
        tl = ratio_box.topLeft()
        br = ratio_box.bottomRight()
        box = QRect()
        box.setTopLeft(QPoint(round(tl.x() * view_w), round(tl.y() * view_h)))
        box.setBottomRight(QPoint(round(br.x() * view_w), round(br.y() * view_h)))
        return box

    def image_to_ratio(self, box: QRect):
        return self._view_to_ratio(box, self.image.size())

    def ratio_to_image(self, ratio_box: QRectF):
        return self._ratio_to_view(ratio_box, self.image.size())

    def mousePressEvent(self, e: QMouseEvent):
        if self.drawing and e.button() == Qt.MouseButton.LeftButton:
            self.box_start = e.pos()

    def mouseMoveEvent(self, e):
        if self.drawing:
            box_end = e.pos()
            self.box_rect = self._view_to_ratio(self._get_box(self.box_start, box_end))
            self.update()

    def resizeEvent(self, e):
        width, height = self.width(), self.height()
        self.setPixmap(self.image.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio))

    def minimumSizeHint(self):
        return self.sizeHint()

    def sizeHint(self):
        # Constrain the image size to 80% of monitor width and height.
        hint = super().sizeHint()
        w, h = hint.width(), hint.height()
        ratio = w / h
        screen_size = QtWidgets.QDesktopWidget().screenGeometry(0)
        max_w = round(screen_size.width() * 0.8)
        max_h = round(screen_size.height() * 0.8)
        if w > max_w:
            w, h = max_w, round(max_w / ratio)
        if h > max_h:
            w, h = round(max_h * ratio), max_h
        return QSize(w, h)


class BoundingBoxDialog(QDialog):
    finish = pyqtSignal(list)

    def __init__(self, image, boxes):
        super().__init__()

        self.setWindowTitle("Bounding Box")

        self.label_image = BBImageLabel(image, boxes)
        self.button_finish = QPushButton("Finish")
        self.button_add_bbox = QPushButton()

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.label_image, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.button_finish, 1, 0)
        self.grid_layout.addWidget(self.button_add_bbox, 1, 1)
        self.setLayout(self.grid_layout)

        self.setFixedSize(self.sizeHint())  # Disable resizing
        self.button_finish.setDefault(True)
        self._draw_state_changed(False)

        self.button_finish.clicked.connect(self._button_finish)
        self.button_add_bbox.clicked.connect(self._button_add_bbox)
        self.label_image.draw_state.connect(self._draw_state_changed)

    def _button_finish(self):
        if self.label_image.drawing:
            self.label_image.toggle_draw()

        boxes = [self.label_image.ratio_to_image(b) for b in self.label_image.boxes]
        self.accept()
        self.finish.emit(boxes)

    def keyPressEvent(self, e):
        super().keyPressEvent(e)
        if e.key() == Qt.Key.Key_B:
            self._button_add_bbox()

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
    ui = BoundingBoxDialog(QImage("c.png"), [])
    ui.show()
    sys.exit(app.exec_())
