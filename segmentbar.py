from PyQt5 import QtCore, QtGui, QtWidgets
from models import VideoAnnotationData, VideoAnnotationSegment

class WSegmentBar(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.paintEvent = self.paintAction1

    def paintAction1(self,e):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(230,230,230,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

    def paintAction2(self, e):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(200,200,200,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        self.drawSegmentBlocks(painter, brush, self.annotation, self.duration)

    def drawSegmentBlocks(self, painter, brush, annotation:VideoAnnotationData, duration):
        brush.setColor(QtGui.QColor('red'))
        d_width = painter.device().width()
        d_height = painter.device().height()
        for segment in annotation._segments:
            leftpos = int(segment.start / duration * d_width)  # pos from left, pix from left/wdiget width = time at start/duration (ms)
            rectwidth = int((segment.end - segment.start)/duration*d_width) # segment rectangle width
            rect = QtCore.QRect(
                leftpos,
                0,
                rectwidth,
                d_height
            )
            painter.fillRect(rect, brush)

        painter.end()
        
    def sizeHint(self):
        return QtCore.QSize(10,5)

    def setData(self, annotation:VideoAnnotationData, duration):
        self.annotation = annotation
        self.duration = duration
        self.paintEvent = self.paintAction2

    def refresh(self):
        self.update()