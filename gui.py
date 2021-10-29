import platform

from PyQt5.QtCore import (QCoreApplication, QDir, QMetaObject, QModelIndex,
                          QRect, Qt, QUrl)
from PyQt5.QtMultimedia import (QMediaContent, QMediaPlayer, QVideoFrame,
                                QVideoProbe)
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QAbstractItemView, QAction, QFileDialog,
                             QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
                             QMainWindow, QMenu, QMenuBar, QMessageBox,
                             QPushButton, QSlider, QStyle, QTextEdit,
                             QVBoxLayout, QWidget)

from framegrabber import FrameGrabber
from models import VideoAnnotationData, VideoAnnotationSegment
from pascalxml import PascalXML
from utility import timestamp_from_ms
from widgets.agreementdialog import AgreementDialog
from widgets.boundingboxdialog import BoundingBoxDialog
from widgets.capturesegment import CaptureSegmentWidget
from widgets.segmentbar import WSegmentBar


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi()
        self.setupEvents()

        # The active video and capture data
        self.annotation: VideoAnnotationData = None
        self.seg_to_listwidget = {}
        self.capture: VideoAnnotationSegment = None
        self.capturing = False
        self.is_highlighting = False

    def setupUi(self):
        self.resize(1280, 720)
        self.central_widget = QWidget(self)
        self.main_vertical_layout = QVBoxLayout(self.central_widget)
        self.upper_h_layout = QHBoxLayout()

        # == Video player ==
        self.video_player_widget = QVideoWidget()
        self.upper_h_layout.addWidget(self.video_player_widget)
        self.video_player_widget.setStyleSheet('background-color: black')

        # Backend media player
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setNotifyInterval(10)

        if platform.system() == "Linux":
            # On linux use QVideoProbe to get video frame due to problems with gstreamer.
            self.media_player.setVideoOutput(self.video_player_widget)
        else:
            self.frame_grabber = FrameGrabber(self)  # Used to get video frame
            self.media_player.setVideoOutput([self.video_player_widget.videoSurface(), self.frame_grabber])

        # == Information Panel ==
        self.upper_right_v_layout = QVBoxLayout()
        # Video Info
        self.label_videoinfo = QLabel()
        self.upper_right_v_layout.addWidget(self.label_videoinfo)
        self.text_videoinfo = QTextEdit()
        self.text_videoinfo.setReadOnly(True)
        self.upper_right_v_layout.addWidget(self.text_videoinfo)
        # Capture frames
        self.label_capture_frames = QLabel()
        self.upper_right_v_layout.addWidget(self.label_capture_frames)
        # Load/export buttons
        self.h_layout = QHBoxLayout()
        self.button_load = QPushButton()
        self.h_layout.addWidget(self.button_load)
        self.button_export = QPushButton()
        self.h_layout.addWidget(self.button_export)
        self.upper_right_v_layout.addLayout(self.h_layout)
        # Segment listview
        self.listwidget_captures = QListWidget()
        self.upper_right_v_layout.addWidget(self.listwidget_captures)

        # Layouts
        self.upper_right_v_layout.setStretch(1, 1)
        self.upper_right_v_layout.setStretch(4, 3)
        self.upper_h_layout.addLayout(self.upper_right_v_layout)
        self.upper_h_layout.setStretch(0, 5)
        self.upper_h_layout.setStretch(1, 1)
        self.main_vertical_layout.addLayout(self.upper_h_layout)

        # == Media Controls and Buttons ==
        self.lower_h_layout = QHBoxLayout()
        # Prev Button
        self.button_prev = QPushButton()
        self.lower_h_layout.addWidget(self.button_prev)
        # Next Button
        self.button_next = QPushButton()
        self.lower_h_layout.addWidget(self.button_next)
        # Play button
        self.button_play = QPushButton()
        self.button_play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.lower_h_layout.addWidget(self.button_play)
        # Video position
        self.label_video_position = QLabel()
        self.lower_h_layout.addWidget(self.label_video_position)
        # Video seekbar
        self.segment_bar = WSegmentBar(self.media_player)
        self.seek_layout = QVBoxLayout()
        self.seek_layout.addWidget(self.segment_bar)
        self.seek_slider = QSlider()
        self.seek_slider.setOrientation(Qt.Horizontal)
        self.seek_layout.addWidget(self.seek_slider)
        self.lower_h_layout.addLayout(self.seek_layout)
        # Volume slider
        vol_box = QHBoxLayout()
        self.volume_slider = QSlider()
        self.volume_slider.setOrientation(Qt.Horizontal)
        self.volume_slider.setMaximumSize(100, 20)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        vol_box.addWidget(QLabel(alignment=Qt.AlignCenter, text='-'))
        vol_box.addWidget(self.volume_slider, alignment=Qt.AlignCenter)
        vol_box.addWidget(QLabel(alignment=Qt.AlignCenter, text='+'))
        self.lower_h_layout.addLayout(vol_box)
        # Capture start button
        self.button_cap_start = QPushButton()
        self.lower_h_layout.addWidget(self.button_cap_start)
        # Capture end button
        self.button_cap_end = QPushButton()
        self.lower_h_layout.addWidget(self.button_cap_end)

        # Layouts
        self.main_vertical_layout.addLayout(self.lower_h_layout)
        self.setCentralWidget(self.central_widget)

        # Menu Bar
        self.menubar = QMenuBar()
        self.menu_file = QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        self.action_open_file = QAction(self)
        self.action_calc_agreement = QAction(self)
        self.about = QAction(self)
        self.menu_file.addAction(self.action_open_file)
        self.menu_file.addAction(self.action_calc_agreement)
        self.menu_file.addAction(self.about)
        self.menubar.addAction(self.menu_file.menuAction())

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

        # Setup startup UI state
        self.label_video_position.setText("--:--")
        self.button_prev.setEnabled(False)
        self.button_next.setEnabled(False)
        self.button_cap_start.setEnabled(False)
        self.button_cap_end.setEnabled(False)
        self.button_load.setEnabled(False)
        self.button_export.setEnabled(False)
        self.segment_bar.setEnabled(False)
        self.seek_slider.setEnabled(False)
        self.volume_slider.setEnabled(False)
        self.listwidget_captures.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Video Annotator"))
        self.label_videoinfo.setText(_translate("MainWindow", "Video Information"))
        self.label_capture_frames.setText(_translate("MainWindow", "Captured Frames"))
        self.button_cap_start.setText(_translate("MainWindow", "Start Capture (Z)"))
        self.button_cap_start.setShortcut(_translate("MainWindow", "Z"))
        self.button_cap_end.setText(_translate("MainWindow", "End Capture (X)"))
        self.button_cap_end.setShortcut(_translate("MainWindow", "X"))
        self.button_prev.setText(_translate("MainWindow", "Prev (N)"))
        self.button_prev.setShortcut(_translate("MainWindow", "N"))
        self.button_next.setText(_translate("MainWindow", "Next (M)"))
        self.button_next.setShortcut(_translate("MainWindow", "M"))
        self.button_play.setText(_translate("MainWindow", "Play"))
        self.button_play.setShortcut(_translate("MainWindow", "Space"))
        self.button_load.setText(_translate("MainWindow", "Load"))
        self.button_export.setText(_translate("MainWindow", "Export..."))
        self.menu_file.setTitle(_translate("MainWindow", "File"))
        self.action_open_file.setText(_translate("MainWindow", "Open File..."))
        self.action_open_file.setToolTip(_translate("MainWindow", "Open video file for annotation"))
        self.action_open_file.setShortcut(_translate("MainWindow", "F1"))
        self.about.setText(_translate("MainWindow", "About"))

        self.action_calc_agreement.setText(_translate("MainWindow", "Calculate..."))
        self.action_open_file.setToolTip(_translate("MainWindow", "Open XML Files"))
        self.action_calc_agreement.setShortcut(_translate("MainWindow", "F2"))

    def setupEvents(self):
        self.action_open_file.triggered.connect(self._action_open_file_clicked)
        self.action_calc_agreement.triggered.connect(self._action_interagreement_click)
        self.about.triggered.connect(self._action_about_clicked)

        self.button_play.clicked.connect(self._button_play_clicked)
        self.button_prev.clicked.connect(self._button_prev_clicked)
        self.button_next.clicked.connect(self._button_next_clicked)
        self.button_cap_start.clicked.connect(self._button_start_capture_clicked)
        self.button_cap_end.clicked.connect(self._button_end_capture_clicked)
        self.button_load.clicked.connect(self._button_load_clicked)
        self.button_export.clicked.connect(self._button_export_clicked)

        self.seek_slider.sliderMoved.connect(self._seek_slider_position_changed)
        self.seek_slider.valueChanged.connect(self._seek_slider_value_changed)
        self.volume_slider.sliderMoved.connect(self._volume_slider_position_changed)

        self.media_player.stateChanged.connect(self._media_state_changed)
        self.media_player.positionChanged.connect(self._media_position_changed)
        self.media_player.durationChanged.connect(self._media_duration_changed)

        self.listwidget_captures.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.listwidget_captures.customContextMenuRequested.connect(self._listwidget_captures_contextmenu_open)
        self.listwidget_captures.model().rowsInserted.connect(self._listwidget_captures_row_inserted)
        self.listwidget_captures.model().rowsRemoved.connect(self._listwidget_captures_row_removed)

    # [Event] Prompts open file dialog.
    def _action_open_file_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(None, 'Open Video', QDir.homePath(), 'Video Files (*.mp4)')
        if file_path:
            # Init new video annotation data
            self.annotation = VideoAnnotationData()
            self.annotation.load(file_path)
            self.listwidget_captures.clear()
            self.seg_to_listwidget.clear()

            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            # Set video info
            self.text_videoinfo.setText("Filename: {0}\nFPS: {1}\nResolution: {2}x{3}".format(self.annotation.filename,
                                        self.annotation.fps, self.annotation.resolution[0], self.annotation.resolution[1]))
            # Update annotations displayed in segment bar
            self.segment_bar.set_data(self.annotation)

            self.segment_bar.setEnabled(True)
            self.seek_slider.setEnabled(True)
            self.volume_slider.setEnabled(True)
            self.button_prev.setEnabled(True)
            self.button_next.setEnabled(True)
            self.button_load.setEnabled(True)
            self.capturing = False

    # [Event] Shows inter agreement calculator dialog.

    def _action_interagreement_click(self):
        self.dialog = AgreementDialog()
        self.dialog.setWindowFlag(Qt.WindowType.Window)
        self.dialog.show()

    # [Event] Shows about message.
    def _action_about_clicked(self):
        about = QMessageBox()
        about.setWindowTitle("About")
        about.setInformativeText("")
        about.setDetailedText("Python Team P8-53\nPython Video Annotator")
        about.setText("Created By\n\nTan Jia Ding [2102238]\nWang Ting Wei [2101332]\nTam Wei Cheng [2100977]"
                      "\nEric Cheong [2103020]\nDylan Teo [2101920]")
        about.exec()

    # [Event] Called when play/pause button is clicked.
    def _button_play_clicked(self):
        if self.media_player.mediaStatus() == QMediaPlayer.MediaStatus.NoMedia:
            self._action_open_file_clicked()

        if self.media_player.state() == QMediaPlayer.State.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()
            if not self.capturing:
                # Enable capture start button
                self.button_cap_start.setEnabled(True)

    # [Event] Called when prev button is clicked.
    def _button_prev_clicked(self):
        new_pos = self.media_player.position() - 150
        if self.capturing and self.annotation.find_segment(new_pos) is not None:
            print("Entering segment")
            return

        self.media_player.setPosition(new_pos)

    # [Event] Called when next button is clicked.
    def _button_next_clicked(self):
        new_pos = self.media_player.position() + 150
        if self.capturing and self.annotation.find_segment(new_pos) is not None:
            print("Entering segment")
            return

        self.media_player.setPosition(new_pos)

    # [Event] Called when start capture button is clicked.
    def _button_start_capture_clicked(self):
        self.capturing = True
        start_ms = self.media_player.position()
        self.capture = VideoAnnotationSegment(start_ms)
        self.button_cap_start.setEnabled(False)

        # Find the last valid position this segment can end
        seg = self.annotation.find_next_segment(self.media_player.position())
        frame_time = 1000 / self.annotation.fps  # Subtract frame time to end at previous frame
        self.capture_max = self.media_player.duration() if seg == None else (seg.start - frame_time)

    # [Event] Called when end capture button is clicked.
    def _button_end_capture_clicked(self):
        self.capture.end = self.media_player.position()
        self.annotation.add_segment(self.capture)

        # Update UI state
        self._add_capture_segment(self.annotation, self.capture)
        self.capturing = False
        self.button_cap_start.setEnabled(True)
        self.button_cap_end.setEnabled(False)

    # [Event] Called when export button is clicked.
    def _button_load_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None, 'Load Annotations', QDir.homePath(), 'XML Files (*.xml)')
        if file_path:
            annotation = PascalXML.load(file_path)
            if annotation.fps != self.annotation.fps or annotation.resolution != self.annotation.resolution:
                # Annotation data wrong
                prompt = QMessageBox()
                prompt.setIcon(QMessageBox.Icon.Warning)
                prompt.setWindowTitle("Error")
                prompt.setText("Annotation data mismatch with video.")
                prompt.setInformativeText("Load anyway?")
                prompt.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                prompt.setDefaultButton(QMessageBox.StandardButton.No)
                r = prompt.exec()
                if r != QMessageBox.StandardButton.Yes:
                    return

            self.annotation = annotation
            self._update_capture_segments()

    # [Event] Called when export button is clicked.
    def _button_export_clicked(self):
        # Write output to file
        file_path, _ = QFileDialog.getSaveFileName(None, 'Export PASCAL VOL', QDir.currentPath(), 'XML files (*.xml)')
        if file_path:
            if not file_path.endswith(".xml"):
                file_path += ".xml"
            PascalXML.save(file_path, self.annotation)

    # [Event] Called when bounding box button is clicked.
    def _button_bbox_clicked(self, segment: VideoAnnotationSegment):
        # Seek to segment start and get video frame
        self.media_player.setPosition(segment.start)

        if platform.system() == "Linux":
            # Use QVideoProbe on linux because gstreamer errors out the normal way.
            self.probe = QVideoProbe()
            self.probe.setSource(self.media_player)
            self.probe.videoFrameProbed.connect(self._bbox_frame_available)
        else:
            self.frame_grabber.frameAvailable.connect(self._bbox_frame_available)

    # Frame grabber callback
    def _bbox_frame_available(self, frame: QVideoFrame):
        # Disconnect from signal because this is a one time event.
        if platform.system() == "Linux":
            self.probe.videoFrameProbed.disconnect(self._bbox_frame_available)
        else:
            self.frame_grabber.frameAvailable.disconnect(self._bbox_frame_available)

        self.media_player.pause()
        pos = frame.startTime() // 1000  # startTime() returns microseconds
        seg = self.annotation.find_segment(pos)
        # Retrieved frame is used for bounding box drawing
        self.bb_window = BoundingBoxDialog(frame.image(), seg.boxes)
        self.bb_window.finish.connect(lambda boxes: self._save_bbox(frame, boxes))
        self.bb_window.exec()

    # Bounding box dialog finished callback
    def _save_bbox(self, frame: QVideoFrame, boxes: list[QRect]):
        pos = frame.startTime() // 1000  # startTime() returns microseconds
        seg = self.annotation.find_segment(pos)
        if seg is not None:
            seg.boxes = boxes

    # [Event] Called when manually moving seek slider in UI.
    def _seek_slider_position_changed(self, position):
        self.media_player.setPosition(position)
        # Update timestamp
        self._update_label_timestamp(position)

    # [Event] Called when seek slider value changed due to dragging or setValue().
    def _seek_slider_value_changed(self, position):
        if self.capturing:
            # Restrict slider to valid values and not conflicting with existing segment.
            if position < self.capture.start:
                self.seek_slider.setValue(self.capture.start + 1)
            elif position > self.capture_max:
                self.seek_slider.setValue(self.capture_max)

    # [Event] Called when manually moving volume slider in UI.
    def _volume_slider_position_changed(self, position):
        self.media_player.setVolume(position)

    # [Event] Called when mediaplayer changed to playing or paused and vice versa.
    def _media_state_changed(self, state):
        if state == QMediaPlayer.State.PlayingState:
            self.button_play.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
            self.button_play.setText("Pause")
        else:
            if state == QMediaPlayer.State.StoppedState:
                # MediaPlayer reaches end of stream.
                self.button_cap_start.setEnabled(False)
            self.button_play.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
            self.button_play.setText("Play")

    # [Event] Called every "notify interval" miliseconds when mediaplayer is playing.
    def _media_position_changed(self, position):
        # Update seek slider progress
        self.seek_slider.setValue(position)
        # Update timestamp
        self._update_label_timestamp(position)

        # Highlight segment in list if its currently playing
        seg = self.annotation.find_segment(position)
        if seg is not None:
            self.is_highlighting = True
            item = self.seg_to_listwidget[seg]
            self.listwidget_captures.setCurrentItem(item)
        else:
            if self.is_highlighting:
                self.is_highlighting = False
                self.listwidget_captures.setCurrentIndex(QModelIndex())

        # Update enabled state of capture buttons.
        if self.capturing:
            # If we encounter another segment while capturing, go to max end value and pause video
            if self.is_highlighting:
                self.is_highlighting = False  # Prevent highlight getting cleared when seeking back
                self.media_player.setPosition(self.capture_max)
                self.media_player.pause()
            # Prevent capture from ending if end frame is earlier than start. (Dragging slider back)
            start_bef_end = self.capture.start < self.media_player.position()
            if start_bef_end:
                if not self.button_cap_end.isEnabled():
                    self.button_cap_end.setEnabled(True)
            else:
                if self.button_cap_end.isEnabled():
                    self.button_cap_end.setEnabled(False)
        else:
            # Prevent capture from starting if the current position is contained in captured segments
            if not self.is_highlighting:
                if not self.button_cap_start.isEnabled():
                    self.button_cap_start.setEnabled(True)
            else:
                if self.button_cap_start.isEnabled():
                    self.button_cap_start.setEnabled(False)

    # [Event] Called when the total duration of the video changes, such as opening a new video file.
    def _media_duration_changed(self, duration):
        self.seek_slider.setRange(0, duration)

    # [Event] Called when adding new segment to annotation.
    def _listwidget_captures_row_inserted(self, parent, first, last):
        if self.listwidget_captures.count() > 0:
            self.button_export.setEnabled(True)

    # [Event] Called when adding deleting segment from annotation.
    def _listwidget_captures_row_removed(self, parent, first, last):
        if self.listwidget_captures.count() == 0:
            self.button_export.setEnabled(False)

    # [Event] Called when right clicking segment in annotation list.
    def _listwidget_captures_contextmenu_open(self, pos):
        if self.listwidget_captures.itemAt(pos) == None:
            # Right click outside a segment widget
            return

        context_actions = QMenu()
        selected_count = len(self.listwidget_captures.selectedItems())
        context_actions.addAction(f"Delete Selection ({selected_count})", self._delete_selected_segments)

        global_pos = self.listwidget_captures.mapToGlobal(pos)
        context_actions.exec(global_pos)

    # Update timestamp text.
    def _update_label_timestamp(self, position):
        self.label_video_position.setText('{0} / {1}'.format(timestamp_from_ms(position), timestamp_from_ms(self.media_player.duration())))

    # Add new segment to annotaion. Called when finished capturing.
    def _add_capture_segment(self, annotation, segment):
        count = self.listwidget_captures.count() + 1
        listwidget_item = QListWidgetItem(self.listwidget_captures)

        seg_widget = CaptureSegmentWidget(count, annotation, segment, listwidget_item)
        seg_widget.play.connect(lambda segment: self._seek_slider_position_changed(segment.start))
        seg_widget.bound_box.connect(self._button_bbox_clicked)
        seg_widget.delete.connect(lambda item: self._delete_segment(item))

        listwidget_item.setSizeHint(seg_widget.sizeHint())

        self.listwidget_captures.addItem(listwidget_item)
        self.listwidget_captures.setItemWidget(listwidget_item, seg_widget)
        self.seg_to_listwidget[segment] = listwidget_item

    # Rebuild segments listwidget from annotation data
    def _update_capture_segments(self):
        self.listwidget_captures.clear()
        for s in self.annotation.segments:
            self._add_capture_segment(self.annotation, s)

    # Delete all annotation segments currently selected.
    def _delete_selected_segments(self):
        items = self.listwidget_captures.selectedItems()
        for item in items:
            self._delete_segment(item)

    # Delete a single annotation segment
    def _delete_segment(self, item):
        # Remove from UI
        index = self.listwidget_captures.row(item)
        self.listwidget_captures.takeItem(index)
        # Remove in captured frames too
        self.annotation.segments.pop(index)

        self._update_capture_segments()
