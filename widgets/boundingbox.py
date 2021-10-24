from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QMouseEvent, QPainter, QPixmap
from PyQt5.QtWidgets import (QDialog, QHBoxLayout, QLabel, QMessageBox,
                             QPushButton, QSizePolicy, QVBoxLayout)


class BBImageLabel(QLabel):
    draw_state = pyqtSignal(bool)

    def __init__(self, image, current_boxes: list[QRect]):
        super().__init__()
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

    # def keyPressEvent(self, e):
    #     k = e.key()
    #     if k == Qt.Key.Key_Space:
    #         self.toggle_draw()

    def resizeEvent(self, e):
        width, height = self.width(), self.height()
        self.setPixmap(self.image.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio))


class BoundingBoxDialog(QDialog):
    finish = pyqtSignal(list)

    def __init__(self, image, boxes):
        super().__init__()

        self.setWindowTitle("Bounding Box")

        #self.label_title = QLabel("Enclose position(s) of smoking incident with bounding box.")
        #self.label_title.setStyleSheet("font-weight: bold;font-size: 16px;")
        self.label_image = BBImageLabel(image, boxes)

        self.lower_h_layout = QHBoxLayout()
        self.button_finish = QPushButton("Finish")
        self.lower_h_layout.addWidget(self.button_finish)
        self.button_add_bbox = QPushButton()
        self.lower_h_layout.addWidget(self.button_add_bbox)

        self.main_v_layout = QVBoxLayout()
        # self.main_v_layout.addWidget(self.label_title)
        self.main_v_layout.addWidget(self.label_image)
        self.main_v_layout.addLayout(self.lower_h_layout)
        self.main_v_layout.setStretch(1, 2)
        self.setLayout(self.main_v_layout)

        size = QSize(1000, 600)
        self.setMinimumSize(size)
        self.resize(size)

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
    ui = BoundingBoxDialog(QImage("a.png"))
    ui.show()
    sys.exit(app.exec_())
