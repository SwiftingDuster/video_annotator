from PyQt5 import QtWidgets
from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QMouseEvent, QPainter, QPixmap
from PyQt5.QtWidgets import (QDialog, QGridLayout, QLabel, QMessageBox,
                             QPushButton, QSizePolicy)


class BBImageLabel(QLabel):
    """Custom QLabel for image display and bounding box functionality."""

    def __init__(self, image, current_boxes: list[QRect]):
        super().__init__()
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Display image passed from constructor
        self.image = QPixmap.fromImage(image)
        self.setPixmap(self.image)

        self.drawing = False
        # When drawing, this stores the current box represented by a QRectF.
        # Interally stores every box using a ratio value by representing coordinates between 0 and 1.
        # For example, (0.5, 0.5) would refer to the point at the center of the image.
        self.box_rect = None
        # Load existing bounding boxes if any
        self.boxes = [] if current_boxes is None else [self.image_to_ratio(b) for b in current_boxes]

    def toggle_draw(self):
        """Toggles from viewing mode to box drawing mode and vice versa."""
        self.drawing = not self.drawing
        if self.drawing:  # Start drawing
            self.box_rect = QRectF()
        else:  # End drawing
            if self.box_rect.width() == 0 and self.box_rect.height() == 0:
                # No box was drawn, don't do anything
                pass
            elif self.box_rect.width() < 0.01 or self.box_rect.height() < 0.01:
                # Box is too small (length/width less than 1% of original image)
                self.drawing = True  # Don't end drawing
                prompt = QMessageBox()
                prompt.setWindowTitle("Error")
                prompt.setText("Please draw a bigger box.")
                prompt.exec()
            else:
                self.boxes.append(self.box_rect)

        self.update()
        return self.drawing

    def _get_box(self, start: QPoint, end: QPoint):
        """Return a normalized QRect with non negative width and height."""
        return QRect(start, end).normalized()

    def _view_to_ratio(self, box: QRect, size: QSize = None):
        """
        Convert coordinates to ratio using viewport size as reference.

        :param box: Bounding box in viewport coordinates.
        :param size: Use specified size instead of viewport size as reference.
        """
        view_w = self.width() if size is None else size.width()
        view_h = self.height() if size is None else size.height()
        tl = box.topLeft()
        br = box.bottomRight()
        ratio_box = QRectF()
        ratio_box.setTopLeft(QPointF(tl.x() / view_w, tl.y() / view_h))
        ratio_box.setBottomRight(QPointF(br.x() / view_w, br.y() / view_h))
        return ratio_box

    def _ratio_to_view(self, ratio_box: QRectF, size: QSize = None):
        """
        Convert ratio to viewport coordinates.

        :param box: Bounding box in ratio coordinates.
        :param size: Use specified size instead of viewport size as reference.
        """
        view_w = self.width() if size is None else size.width()
        view_h = self.height() if size is None else size.height()
        tl = ratio_box.topLeft()
        br = ratio_box.bottomRight()
        box = QRect()
        box.setTopLeft(QPoint(round(tl.x() * view_w), round(tl.y() * view_h)))
        box.setBottomRight(QPoint(round(br.x() * view_w), round(br.y() * view_h)))
        return box

    def image_to_ratio(self, box: QRect):
        """
        Convert coordinates to ratio using original image size as reference.

        :param box: Bounding box in image coordinates.
        """
        return self._view_to_ratio(box, self.image.size())

    def ratio_to_image(self, ratio_box: QRectF):
        """
        Convert ratio to image coordinates.

        :param box: Bounding box in ratio coordinates.
        """
        return self._ratio_to_view(ratio_box, self.image.size())

    # [Event] Called when mouse button is clicked.
    def mousePressEvent(self, e: QMouseEvent):
        # Start drawing
        if self.drawing and e.button() == Qt.MouseButton.LeftButton:
            self.box_start = e.pos()

    # [Event] Called when mouse button is held down and moving.
    def mouseMoveEvent(self, e):
        # Update box size when dragging
        if self.drawing:
            box_end = e.pos()
            self.box_rect = self._view_to_ratio(self._get_box(self.box_start, box_end))
            self.update()  # Request repaint, calls paintEvent()

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        # Draw existing bounding boxes with red brush
        painter.setBrush(QColor(255, 0, 0, 20))
        for box in self.boxes:
            painter.drawRect(self._ratio_to_view(box))
        # If drawing, draw box with green brush
        if self.drawing:
            rect = self._ratio_to_view(self.box_rect)
            painter.setBrush(QColor(0, 255, 0, 20))
            painter.drawRect(rect)

    # [Event] Called when widget is resized.
    def resizeEvent(self, e):
        # Respect aspect ratio when scaling image down to fit viewport.
        width, height = self.width(), self.height()
        self.setPixmap(self.image.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio))

    def minimumSizeHint(self):
        # Size is calculated in sizeHint() and fixed.
        return self.sizeHint()

    def sizeHint(self):
        # Constrain the image size to 80% of monitor width and height.
        # If image does not exceed dimensions, show image at original size.
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
    """Popup dialog to draw bounding boxes on a frame."""

    finish = pyqtSignal(list)  # Emitted when dialog closes by clicking finish

    def __init__(self, image, boxes):
        super().__init__()

        self.setWindowTitle("Bounding Box")

        self.label_image = BBImageLabel(image, boxes)
        self.button_finish = QPushButton("Finish")
        self.button_add_bbox = QPushButton("New bounding box")

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.label_image, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.button_finish, 1, 0)
        self.grid_layout.addWidget(self.button_add_bbox, 1, 1)
        self.setLayout(self.grid_layout)

        self.setFixedSize(self.sizeHint())  # Disable resizing

        self.button_finish.clicked.connect(self._button_finish_clicked)
        self.button_add_bbox.clicked.connect(self._button_add_bbox_clicked)

    # [Event] Called when finish button clicked
    def _button_finish_clicked(self):
        # If currently drawing, save the box
        if self.label_image.drawing:
            self.label_image.toggle_draw()
        # Convert into image coordinates
        boxes = [self.label_image.ratio_to_image(b) for b in self.label_image.boxes]
        self.accept()  # Closes dialog
        self.finish.emit(boxes)  # Emit signal with boxes for mainwindow to process

    # [Event] Called when new bounding box button clicked
    def _button_add_bbox_clicked(self):
        state = self.label_image.toggle_draw()
        if state:
            self.button_add_bbox.setText("End bounding box")
        else:
            self.button_add_bbox.setText("New bounding box")
