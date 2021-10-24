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
        self.paintEvent = self.paintAction1

    def paintAction1(self, e):
        painter = QPainter(self)
        brush = QBrush()
        brush.setColor(QColor(230, 230, 230, 255))
        brush.setStyle(Qt.SolidPattern)
        rect = QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

    def paintAction2(self, e):
        painter = QPainter(self)
        brush = QBrush()
        brush.setColor(QColor(200, 200, 200, 255))
        brush.setStyle(Qt.SolidPattern)
        rect = QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        self.drawSegmentBlocks(painter, brush, self.annotation, self.duration)

    def drawSegmentBlocks(self, painter, brush, annotation:VideoAnnotationData, duration):
        padding = 5
        brush.setColor(QColor('red'))
        d_width = painter.device().width() - 2 * padding
        d_height = painter.device().height()
        for segment in annotation._segments:
            leftpos = int(segment.start / duration * d_width + padding)  # pos from left, pix from left/wdiget width = time at start/duration (ms)
            rectwidth = int((segment.end - segment.start)/duration*d_width) # segment rectangle width
            if rectwidth < 1:
                rectwidth = 1
            rect = QRect(leftpos, 0, rectwidth, d_height)
            painter.fillRect(rect, brush)

        painter.end()
        
    def sizeHint(self):
        return QSize(200,5)

    def setData(self, annotation:VideoAnnotationData, duration):
        self.annotation = annotation
        self.duration = duration
        self.paintEvent = self.paintAction2
        self.update()