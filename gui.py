from PyQt5.QtCore import QCoreApplication, QDir, QMetaObject, QRect, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaResource
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QAction, QFileDialog, QHBoxLayout, QLabel,
                             QMainWindow, QMenu, QMenuBar, QPushButton,
                             QScrollArea, QSlider, QStatusBar, QStyle,
                             QTextEdit, QVBoxLayout, QWidget)

from models import VideoAnnotationData, VideoAnnotationSegment
from utility import timestamp_from_milisec


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # The active video and capture data
        self.annotation_data = VideoAnnotationData('', (0, 0))
        self.capture = VideoAnnotationSegment(0, 0)
        self.capturing = False

    def setupUi(self, MainWindow):
        MainWindow.resize(1280, 720)
        self.central_widget = QWidget(MainWindow)
        self.vertical_layout = QVBoxLayout(self.central_widget)
        self.upper_h_layout = QHBoxLayout()
        # == Video player ==
        self.video_player_widget = QVideoWidget(self.central_widget)
        self.upper_h_layout.addWidget(self.video_player_widget)
        # Backend media player
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_player_widget)
        self.media_player.setNotifyInterval(10)

        # == Video info and event frames ==
        self.upper_right_v_layout = QVBoxLayout()
        self.label_videoinfo = QLabel(self.central_widget)
        self.upper_right_v_layout.addWidget(self.label_videoinfo)
        self.text_videoinfo = QTextEdit(self.central_widget)
        self.text_videoinfo.setReadOnly(True)
        self.upper_right_v_layout.addWidget(self.text_videoinfo)
        self.label_events = QLabel(self.central_widget)
        self.upper_right_v_layout.addWidget(self.label_events)
        self.scroll_area_events = QScrollArea(self.central_widget)
        self.scroll_area_events.setWidgetResizable(True)
        self.scroll_area_content = QWidget()
        self.scroll_area_content.setGeometry(QRect(0, 0, 271, 349))
        self.scroll_area_events.setWidget(self.scroll_area_content)
        self.upper_right_v_layout.addWidget(self.scroll_area_events)
        self.upper_right_v_layout.setStretch(1, 1)
        self.upper_right_v_layout.setStretch(3, 3)
        self.upper_h_layout.addLayout(self.upper_right_v_layout)
        self.upper_h_layout.setStretch(0, 5)
        self.upper_h_layout.setStretch(1, 1)
        self.vertical_layout.addLayout(self.upper_h_layout)

        # == Media Controls and Buttons ==
        self.lower_h_layout = QHBoxLayout()
        # Play button
        self.button_play = QPushButton(self.central_widget)
        self.button_play.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay))
        self.lower_h_layout.addWidget(self.button_play)
        # Video position
        self.label_video_position = QLabel(self.central_widget)
        self.lower_h_layout.addWidget(self.label_video_position)
        # Video seekbar
        self.seek_slider = QSlider(self.central_widget)
        self.seek_slider.setOrientation(Qt.Horizontal)
        self.lower_h_layout.addWidget(self.seek_slider)
        # Capture start button
        self.button_cap_start = QPushButton(self.central_widget)
        self.lower_h_layout.addWidget(self.button_cap_start)
        # Capture end button
        self.button_cap_end = QPushButton(self.central_widget)
        self.lower_h_layout.addWidget(self.button_cap_end)
        # Export button
        self.button_export = QPushButton(self.central_widget)
        self.lower_h_layout.addWidget(self.button_export)
        # Layouts
        self.vertical_layout.addLayout(self.lower_h_layout)
        MainWindow.setCentralWidget(self.central_widget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1280, 26))
        self.menu_file = QMenu(self.menubar)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.action_open_file = QAction(MainWindow)
        self.menu_file.addAction(self.action_open_file)
        self.menubar.addAction(self.menu_file.menuAction())

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

        # Setup default UI state
        self.label_video_position.setText("--:--")
        self.button_cap_start.setEnabled(False)
        self.button_cap_end.setEnabled(False)
        self.button_export.setEnabled(False)

        # Internal data
        self.capturing = False
        self.captured_frames = []

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_videoinfo.setText(
            _translate("MainWindow", "Video Information"))
        self.label_events.setText(_translate("MainWindow", "Event Frames"))
        self.button_cap_start.setText(
            _translate("MainWindow", "Capture Start"))
        self.button_cap_end.setText(_translate("MainWindow", "Capture End"))
        self.button_play.setText(_translate("MainWindow", "Play"))
        self.button_export.setText(_translate("MainWindow", "Export..."))
        self.menu_file.setTitle(_translate("MainWindow", "File"))
        self.action_open_file.setText(_translate("MainWindow", "Open File..."))
        self.action_open_file.setToolTip(_translate(
            "MainWindow", "Open video file for annotation"))
        self.action_open_file.setShortcut(_translate("MainWindow", "F1"))

    def setupEvents(self):
        self.action_open_file.triggered.connect(self.action_open_file_clicked)

        self.button_play.clicked.connect(self.button_play_clicked)
        self.seek_slider.sliderMoved.connect(
            self.seek_slider_position_changed)
        self.media_player.stateChanged.connect(self.media_state_changed)
        # self.media_player.mediaStatusChanged.connect(self.media_status_changed)
        self.media_player.positionChanged.connect(self.media_position_changed)
        self.media_player.durationChanged.connect(self.media_duration_changed)

        self.button_cap_start.clicked.connect(self.button_start_capture)
        self.button_cap_end.clicked.connect(self.button_end_capture)

    # [Event] Called when open file action is triggered.
    def action_open_file_clicked(self):
        fileName, _ = QFileDialog.getOpenFileName(
            None, 'Open Image', '', 'Video Files (*.mp4)')
        if fileName:
            self.media_player.setMedia(
                QMediaContent(QUrl.fromLocalFile(fileName)))
            self.media_player.setVolume(100)
            self.button_play.setEnabled(True)
            self.seek_slider.setEnabled(True)
            self.text_videoinfo.setText(fileName)

            # Set video info
            self.text_videoinfo.setText("Filename: %s" % fileName)

    # [Event] Called when play/pause button is clicked.
    def button_play_clicked(self):
        if self.media_player.mediaStatus() == QMediaPlayer.MediaStatus.NoMedia:
            self.action_open_file_clicked()

        if self.media_player.state() == QMediaPlayer.State.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()
            if not self.capturing:
                # Enable capture start button
                self.button_cap_start.setEnabled(True)

    # [Event] Called when capture start button is clicked.
    def button_start_capture(self):
        self.capturing = True
        self.capture.frame_start = self.media_player.position()
        self.button_cap_start.setEnabled(False)

    # [Event] Called when capture end button is clicked.
    def button_end_capture(self):
        self.capture.frame_end = self.media_player.position()

        if self.capturing and self.capture.frame_start > self.capture.frame_end:
            # Prevent capture from ending if frame end is earlier than start.
            # TODO: Error message dialog or disable button
            return

        self.capturing = False
        self.annotation_data.frames.append(
            (self.capture.frame_start, self.capture.frame_end))
        print('Captured frames:', self.annotation_data.frames)
        self.button_cap_start.setEnabled(True)
        self.button_cap_end.setEnabled(False)

    # [Event] Called when manually moving seek slider in UI.
    def seek_slider_position_changed(self, position):
        self.media_player.setPosition(position)

    # [Event] Called when mediaplayer changed to playing or paused and vice versa.
    def media_state_changed(self, state):
        if state == QMediaPlayer.State.PlayingState:
            self.button_play.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
            self.button_play.setText("Pause")
        else:
            self.button_play.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
            self.button_play.setText("Play")

    # [Event] Called when status changes when loading new video.
    # def media_status_changed(self, status: QMediaPlayer.MediaStatus):
    #     if status == QMediaPlayer.MediaStatus.LoadedMedia or status == QMediaPlayer.MediaStatus.BufferedMedia:
    #         pass

    # [Event] Called every "notify interval" miliseconds when mediaplayer is playing.
    def media_position_changed(self, position):
        # Update seek slider progress
        self.seek_slider.setValue(position)
        # Update timestamp
        self.label_video_position.setText(timestamp_from_milisec(position))

        # When capturing, update enabled state of end capture button based on whether end frame is after start frame.
        if self.capturing:
            if self.capture.frame_start < self.media_player.position():
                if not self.button_cap_end.isEnabled():
                    self.button_cap_end.setEnabled(True)
            else:
                if self.button_cap_end.isEnabled():
                    self.button_cap_end.setEnabled(False)

    # [Event] Called when the total duration of the video changes, such as opening a new video file.
    def media_duration_changed(self, duration):
        self.seek_slider.setRange(0, duration)
