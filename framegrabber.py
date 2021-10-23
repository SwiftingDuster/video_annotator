from PyQt5.QtCore import pyqtSignal
from PyQt5.QtMultimedia import (QAbstractVideoBuffer, QAbstractVideoSurface,
                                QVideoFrame)


class FrameGrabber(QAbstractVideoSurface):
    frameAvailable = pyqtSignal(QVideoFrame)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_frame = QVideoFrame()

    @property
    def current_frame(self):
        return self._current_frame

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

    def present(self, frame):
        self._current_frame = frame
        self.frameAvailable.emit(frame)
        return True
