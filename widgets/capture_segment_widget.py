
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class CaptureSegmentWidget (QWidget):
    def __init__(self, parent=None):
        super(CaptureSegmentWidget, self).__init__(parent)
        self.v_box_layout = QVBoxLayout()
        self.label_text = QLabel()
        self.label_subtext = QLabel()
        self.v_box_layout.addWidget(self.label_text)
        self.v_box_layout.addWidget(self.label_subtext)
        self.setLayout(self.v_box_layout)

    def set_text(self, text):
        self.label_text.setText(text)
        return self

    def set_subtext(self, text):
        self.label_subtext.setText(text)
        return self
