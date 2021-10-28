from PyQt5.QtCore import pyqtSignal
from PyQt5.QtMultimedia import (QAbstractVideoBuffer, QAbstractVideoSurface,
                                QVideoFrame)


class FrameGrabber(QAbstractVideoSurface):
    """Custom sink for QMediaPlayer output to get video frames."""

    frameAvailable = pyqtSignal(QVideoFrame)

    def __init__(self, parent=None):
        super().__init__(parent)

    def supportedPixelFormats(self, handleType=QAbstractVideoBuffer.NoHandle):
        formats = [QVideoFrame.PixelFormat()]
        if handleType == QAbstractVideoBuffer.NoHandle:
            for f in [
                QVideoFrame.Format_RGB32,
                QVideoFrame.Format_ARGB32,
                QVideoFrame.Format_ARGB32_Premultiplied,
                QVideoFrame.Format_RGB565,
                QVideoFrame.Format_RGB555,
            ]:
                formats.append(f)
        return formats

    # Called when frame is ready to be presented.
    def present(self, frame):
        self.frameAvailable.emit(frame)
        return True
