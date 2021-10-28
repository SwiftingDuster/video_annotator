from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtWidgets import QSizePolicy, QWidget
from models import VideoAnnotationData

class WSegmentBar(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.Minimum
        )
        # Start UI with first paint event
        self.paintEvent = self.paintAction1

    # Paint event to draw empty segment bar
    def paintAction1(self, e):
        painter = QPainter(self)
        brush = QBrush()
        brush.setColor(QColor(230, 230, 230, 255))
        brush.setStyle(Qt.SolidPattern)
        rect = QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

    # Second paint event to be used after video file opened
    def paintAction2(self, e):
        painter = QPainter(self)
        brush = QBrush()
        brush.setColor(QColor(200, 200, 200, 255))
        brush.setStyle(Qt.SolidPattern)
        rect = QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        self.drawSegmentBlocks(painter, brush, self.annotation, self.duration, self.position)

    # Function to draw colored blocks on the segment bar
    def drawSegmentBlocks(self, painter, brush, annotation:VideoAnnotationData, duration, position):
        padding = 5
        brush.setColor(QColor('orange'))
        d_width = painter.device().width() - 2 * padding
        d_height = painter.device().height()
        for segment in annotation._segments:
            leftpos = int(segment.start / duration * d_width + padding)  # pos from left, pix from left/wdiget width = time at start/duration (ms)
            rectwidth = int((segment.end - segment.start) / duration * d_width)  # segment rectangle width
            if rectwidth < 1:
                rectwidth = 1
            segbox = QRect(leftpos, 0, rectwidth, d_height)
            painter.fillRect(segbox, brush)

        brush.setColor(QColor('black'))
        posTick = QRect(padding + position/duration * d_width, 0, 1, d_height)
        painter.fillRect(posTick, brush)

        painter.end()

    # sets minimum size as per size policy specified
    def sizeHint(self):
        return QSize(200, 7)

    # function to trigger switch to 2nd paint event and pass variables for drawing segment blocks
    def setData(self, annotation:VideoAnnotationData, duration, position):
        self.annotation = annotation
        if duration == 0:
            duration = 1
        self.duration = duration
        self.position = position
        self.paintEvent = self.paintAction2
        self.update()
