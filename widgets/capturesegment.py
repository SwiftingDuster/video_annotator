from PyQt5.QtCore import pyqtSignal

from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QListWidgetItem, QPushButton, QSizePolicy,
                             QStyle, QVBoxLayout, QWidget)
from models import VideoAnnotationData, VideoAnnotationSegment

from utility import timestamp_from_ms


class CaptureSegmentWidget(QWidget):
    play = pyqtSignal(VideoAnnotationSegment)
    bound_box = pyqtSignal(VideoAnnotationSegment)
    delete = pyqtSignal(QListWidgetItem)

    def __init__(self, number, annotation: VideoAnnotationData, segment: VideoAnnotationSegment, widget_item: QListWidgetItem):
        super().__init__()
        self.h_box_layout = QHBoxLayout()

        # Information label on the left
        self.v_box_left_layout = QVBoxLayout()
        self.label_frame_range = QLabel()
        self.label_timestamp_start = QLabel()
        self.label_timestamp_end = QLabel()
        self.v_box_left_layout.addWidget(self.label_frame_range)
        self.v_box_left_layout.addWidget(self.label_timestamp_start)
        self.v_box_left_layout.addWidget(self.label_timestamp_end)

        # Buttons on the right
        self.v_box_right_layout = QVBoxLayout()
        self.button_play = QPushButton()
        self.button_boundbox = QPushButton()
        self.button_delete = QPushButton()
        self.v_box_right_layout.addWidget(self.button_play)
        self.v_box_right_layout.addWidget(self.button_boundbox)
        self.v_box_right_layout.addWidget(self.button_delete)

        self.h_box_layout.addLayout(self.v_box_left_layout, 4)
        self.h_box_layout.addLayout(self.v_box_right_layout, 1)
        self.setLayout(self.h_box_layout)

        # Button icons and size
        self.button_play.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        # self.button_boundbox.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop))
        self.button_boundbox.setText("BB")
        self.button_delete.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon))
        policy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.button_play.setSizePolicy(policy)
        self.button_boundbox.setSizePolicy(policy)
        self.button_delete.setSizePolicy(policy)
        self.button_play.setMaximumWidth(32)
        self.button_boundbox.setMaximumWidth(32)
        self.button_delete.setMaximumWidth(32)

        self.button_play.clicked.connect(self.button_play_clicked)
        self.button_boundbox.clicked.connect(self.button_boundbox_clicked)
        self.button_delete.clicked.connect(self.button_delete_clicked)

        self.number = number
        self.annotation = annotation
        self.segment = segment
        self.item = widget_item

        frame_start = annotation.frame_from_ms(segment.start)
        frame_end = annotation.frame_from_ms(segment.end)
        time_start = timestamp_from_ms(segment.start, True)
        time_end = timestamp_from_ms(segment.end, True)
        self.label_frame_range.setText("{0}: {1} - {2}".format(
            number, frame_start, frame_end))
        self.label_timestamp_start.setText(time_start)
        self.label_timestamp_end.setText(time_end)

    def button_play_clicked(self):
        self.play.emit(self.segment)

    def button_boundbox_clicked(self):
        self.bound_box.emit(self.segment)

    def button_delete_clicked(self):
        self.delete.emit(self.item)
