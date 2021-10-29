from models import VideoAnnotationData
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QSizePolicy, QWidget


class WSegmentBar(QWidget):
    """
    Widget providing an overview of annotated segments in the form of a colour coded segment bar. 
    """

    def __init__(self, media_player: QMediaPlayer):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Subscribe to mediaplayer events
        media_player.positionChanged.connect(self.mediaplayer_position_changed)
        media_player.durationChanged.connect(self.mediaplayer_duration_changed)

        self.position = 0
        self.duration = 1

    # Set annotation data for drawing segment blocks
    def set_data(self, annotation: VideoAnnotationData):
        self.annotation = annotation
        self.update()

    # Paint the segment bar and the annotation blocks.
    def paintEvent(self, e):
        painter = QPainter(self)
        segmentbar_rect = QRect(0, 0, painter.device().width(), painter.device().height())
        # Widget is enabled externally when a video file is loaded
        if not self.isEnabled():
            # Draw segment bar (greyed out)
            bar_brush = QBrush(QColor(230, 230, 230, 255), Qt.BrushStyle.SolidPattern)
            painter.fillRect(segmentbar_rect, bar_brush)
        else:
            # Draw segment bar
            bar_brush = QBrush(QColor(200, 200, 200, 255), Qt.BrushStyle.SolidPattern)
            painter.fillRect(segmentbar_rect, bar_brush)
            # Draw segment blocks
            self.draw_segment_blocks(painter)

    # Draw colored blocks on the segment bar
    def draw_segment_blocks(self, painter: QPainter):
        annotation = self.annotation
        duration = self.duration
        block_brush = QBrush(QColor('orange'), Qt.BrushStyle.SolidPattern)

        # Draw annotation segments as blocks
        padding = 5
        d_width = painter.device().width() - 2 * padding
        d_height = painter.device().height()
        for segment in annotation._segments:
            leftpos = int(segment.start / duration * d_width + padding)  # pos from left, pix from left/wdiget width = time at start/duration (ms)
            rectwidth = int((segment.end - segment.start) / duration * d_width)  # segment rectangle width
            if rectwidth < 1:
                rectwidth = 1
            segbox = QRect(leftpos, 0, rectwidth, d_height)
            painter.fillRect(segbox, block_brush)

        # Draw marker for current position of mediaplayer
        position = self.position
        position_brush = QBrush(QColor('black'), Qt.BrushStyle.SolidPattern)
        posTick = QRect(round(padding + position/duration * d_width), 0, 2, d_height)
        painter.fillRect(posTick, position_brush)

    # Callback from mediaplayer at close intervals (<10ms) when video is playing.
    def mediaplayer_position_changed(self, pos):
        if not self.isEnabled():
            return
        self.position = pos
        self.update()

    # Callback from mediaplayer when total duration of video change.
    def mediaplayer_duration_changed(self, duration):
        if not self.isEnabled():
            return
        self.duration = duration
        self.update()

    # Sets desired size as per size policy specified
    def sizeHint(self):
        return QSize(200, 7)
