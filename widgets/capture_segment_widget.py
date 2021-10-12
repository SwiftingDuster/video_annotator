
from typing import Callable

from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                             QStyle, QVBoxLayout, QWidget)


class CaptureSegmentWidget (QWidget):
    def __init__(self, parent=None):
        super(CaptureSegmentWidget, self).__init__(parent)
        self.h_box_layout = QHBoxLayout()

        # Information label on the left
        self.v_box_left_layout = QVBoxLayout()
        self.label_text = QLabel()
        self.label_subtext = QLabel()
        self.label_subtext2 = QLabel()
        self.v_box_left_layout.addWidget(self.label_text)
        self.v_box_left_layout.addWidget(self.label_subtext)
        self.v_box_left_layout.addWidget(self.label_subtext2)

        # Buttons on the right
        self.v_box_right_layout = QVBoxLayout()
        self.button_play = QPushButton()
        self.button_delete = QPushButton()
        self.v_box_right_layout.addWidget(self.button_play)
        self.v_box_right_layout.addWidget(self.button_delete)

        self.h_box_layout.addLayout(self.v_box_left_layout)
        self.h_box_layout.addLayout(self.v_box_right_layout)
        self.setLayout(self.h_box_layout)

        self.button_play.setIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_MediaPlay))
        self.button_delete.setIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_TrashIcon))

        # Make buttons have fixed width
        policy = QSizePolicy(QSizePolicy.Policy.Fixed,
                             QSizePolicy.Policy.Preferred)
        policy.setWidthForHeight(True)
        self.button_play.setSizePolicy(policy)
        self.button_delete.setSizePolicy(policy)

    def set_text(self, text):
        self.label_text.setText(text)
        return self

    def set_subtext(self, text, text2):
        self.label_subtext.setText(text)
        self.label_subtext2.setText(text2)
        return self

    def button_play_clicked(self, handler: Callable[[bool], None]):
        self.button_play.clicked.connect(handler)

    def button_delete_clicked(self, handler: Callable[[bool], None]):
        self.button_delete.clicked.connect(handler)
