from PyQt5.QtCore import QCoreApplication, QDir, QMetaObject, QRect, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QAbstractItemView, QAction, QFileDialog,
                             QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
                             QMainWindow, QMenu, QMenuBar, QPushButton,
                             QSlider, QStatusBar, QStyle, QTextEdit,
                             QVBoxLayout, QWidget, QMessageBox, QDialog)

from models import VideoAnnotationData, VideoAnnotationSegment
from utility import timestamp_from_ms, write_annotator_xml
from widgets.capture_segment_widget import CaptureSegmentWidget
from agreementdialog import agreement_dialog
from xmlHandler import XMLhandler


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # The active video and capture data
        self.annotation: VideoAnnotationData = None
        self.capture: VideoAnnotationSegment = None
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

        # == Information Panel ==
        self.upper_right_v_layout = QVBoxLayout()
        # Video Info
        self.label_videoinfo = QLabel(self.central_widget)
        self.upper_right_v_layout.addWidget(self.label_videoinfo)
        self.text_videoinfo = QTextEdit(self.central_widget)
        self.text_videoinfo.setReadOnly(True)
        self.upper_right_v_layout.addWidget(self.text_videoinfo)
        # Captured Frames
        self.label_events = QLabel(self.central_widget)
        self.upper_right_v_layout.addWidget(self.label_events)
        self.listwidget_captures = QListWidget(self.central_widget)
        self.upper_right_v_layout.addWidget(self.listwidget_captures)

        # Layouts
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
        # # Volume slider
        # self.lower_h_layout.addWidget(QLabel(text='Volume -'))
        # self.volume_slider = QSlider(self.central_widget)
        # self.volume_slider.setOrientation(Qt.Horizontal)
        # self.volume_slider.setMaximumSize(100, 20)
        # self.volume_slider.setRange(0, 100)
        # self.volume_slider.setValue(70)
        # self.lower_h_layout.addWidget(self.volume_slider)
        # self.lower_h_layout.addWidget(QLabel(text='+'))
        vol_box = QVBoxLayout()
        vol_box.addWidget(QLabel(alignment=Qt.AlignCenter, text='Volume'))
        self.volume_slider = QSlider(self.central_widget)
        self.volume_slider.setOrientation(Qt.Horizontal)
        self.volume_slider.setMaximumSize(100, 20)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        vol_box.addWidget(self.volume_slider, alignment=Qt.AlignCenter)
        vol_box.addWidget(QLabel(alignment=Qt.AlignCenter, text='-                       +'))
        self.lower_h_layout.addLayout(vol_box)

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

        # Menu Bar
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1280, 26))
        self.menu_file = QMenu(self.menubar)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.action_open_file = QAction(MainWindow)
        self.menu_file.addAction(self.action_open_file)
        self.menubar.addAction(self.menu_file.menuAction())

        self.action_calc_agreement = QAction(MainWindow)
        self.menu_file.addAction(self.action_calc_agreement)
        self.menubar.addAction(self.menu_file.menuAction())

        self.about = QAction(MainWindow)
        self.menu_file.addAction(self.about)
        self.menubar.addAction(self.menu_file.menuAction())

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

        # Setup UI state
        self.label_video_position.setText("--:--")
        self.button_cap_start.setEnabled(False)
        self.button_cap_end.setEnabled(False)
        self.button_export.setEnabled(False)
        self.seek_slider.setEnabled(False)
        self.volume_slider.setEnabled(False)
        self.listwidget_captures.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection)

        # Internal data
        self.capturing = False

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Video Annotator"))
        self.label_videoinfo.setText(
            _translate("MainWindow", "Video Information"))
        self.label_events.setText(_translate("MainWindow", "Capture Frames"))
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
        self.about.setText(_translate("MainWindow", "About"))

        self.action_calc_agreement.setText(_translate("MainWindow", "Calculate..."))
        self.action_open_file.setToolTip(_translate(
            "MainWindow", "Open XML Files"))
        self.action_calc_agreement.setShortcut(_translate("MainWindow", "F2"))

    def setupEvents(self):
        self.action_open_file.triggered.connect(self.action_open_file_clicked)
        self.action_calc_agreement.triggered.connect(self.on_menu_calc_click)
        self.about.triggered.connect(self.action_about_clicked)

        self.button_play.clicked.connect(self.button_play_clicked)
        self.seek_slider.sliderMoved.connect(
            self.seek_slider_position_changed)
        self.volume_slider.sliderMoved.connect(self.volume_slider_position_changed)
        self.media_player.stateChanged.connect(self.media_state_changed)
        # self.media_player.mediaStatusChanged.connect(self.media_status_changed)
        self.media_player.positionChanged.connect(self.media_position_changed)
        self.media_player.durationChanged.connect(self.media_duration_changed)

        self.button_cap_start.clicked.connect(
            self.button_start_capture_clicked)
        self.button_cap_end.clicked.connect(self.button_end_capture_clicked)
        self.button_export.clicked.connect(self.button_export_clicked)

        self.listwidget_captures.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.listwidget_captures.customContextMenuRequested.connect(
            self.listwidget_captures_contextmenu_open)
        self.listwidget_captures.model().rowsInserted.connect(
            self.listwidget_captures_row_inserted)
        self.listwidget_captures.model().rowsRemoved.connect(
            self.listwidget_captures_row_removed)

    # [Event] Called when open file action is triggered.
    def action_open_file_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None, 'Open Video', QDir.homePath(), 'Video Files (*.mp4)')
        if file_path:
            self.media_player.setMedia(
                QMediaContent(QUrl.fromLocalFile(file_path)))

            self.seek_slider.setEnabled(True)
            self.listwidget_captures.clear()
            # Init new video annotation data
            self.annotation = VideoAnnotationData(file_path)
            # Set video info
            self.text_videoinfo.setText(
                "Filename: {0}\nFPS: {1}\nResolution: {2}x{3}".format(self.annotation.filename, self.annotation.fps, self.annotation.resolution[0], self.annotation.resolution[1]))

            self.volume_slider.setEnabled(True)


    def action_about_clicked(self):
        about = QMessageBox()
        about.setWindowTitle("About")
        about.setInformativeText("")
        about.setDetailedText("Python Team P8-53\nPython Video Annotator")
        about.setText("Created By\n\nTan Jia Ding [2102238]\nWang Ting Wei [2101332]\nTam Wei Cheng [2100977]"
                      "\nEric Cheong [2103020]\nDylan Teo [2101920]")

        x = about.exec_()


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

    # [Event] Called when start capture button is clicked.
    def button_start_capture_clicked(self):
        self.capturing = True
        start_ms = self.media_player.position()
        self.capture = VideoAnnotationSegment(start_ms, 0)
        self.button_cap_start.setEnabled(False)

    # [Event] Called when end capture button is clicked.
    def button_end_capture_clicked(self):
        self.capture.frame_end_ms = self.media_player.position()

        if self.capturing and self.capture.frame_start_ms > self.capture.frame_end_ms:
            # Prevent capture from ending if frame end is earlier than start. (Dragging slider back)
            return

        self.annotation.frames.append(self.capture)

        # Update UI state
        self.__add_capture_segment(
            self.capture.frame_start_ms, self.capture.frame_end_ms)
        self.capturing = False
        self.button_cap_start.setEnabled(True)
        self.button_cap_end.setEnabled(False)

    # [Event] Called when export button is clicked.
    def button_export_clicked(self):
        # Write output to file
        path, _ = QFileDialog.getSaveFileName(
            None, 'Export PASCAL VOL', QDir.currentPath(), 'XML files (*.xml)')
        # TODO: Implement export to XML
        write_annotator_xml(self.annotation, path)
        print('Exported XML to', path)

    # [Event] Called when manually moving seek slider in UI.
    def seek_slider_position_changed(self, position):
        self.media_player.setPosition(position)

    def volume_slider_position_changed(self, position):
        self.media_player.setVolume(position)

    # [Event] Called when mediaplayer changed to playing or paused and vice versa.
    def media_state_changed(self, state):
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

    # [Event] Called when status changes when loading new video.
    # def media_status_changed(self, status: QMediaPlayer.MediaStatus):
    #     if status == QMediaPlayer.MediaStatus.LoadedMedia or status == QMediaPlayer.MediaStatus.BufferedMedia:
    #         pass

    # [Event] Called every "notify interval" miliseconds when mediaplayer is playing.
    def media_position_changed(self, position):
        # Update seek slider progress
        self.seek_slider.setValue(position)
        # Update timestamp
        self.label_video_position.setText('{0} / {1}'.format(timestamp_from_ms(
            position), timestamp_from_ms(self.media_player.duration())))

        # When capturing, update enabled state of end capture button based on whether end frame is after start frame.
        if self.capturing:
            # Prevent capture from ending if end frame is earlier than start. (Dragging slider back)
            if self.capture.frame_start_ms < self.media_player.position():
                if not self.button_cap_end.isEnabled():
                    self.button_cap_end.setEnabled(True)
            else:
                if self.button_cap_end.isEnabled():
                    self.button_cap_end.setEnabled(False)

    # [Event] Called when the total duration of the video changes, such as opening a new video file.
    def media_duration_changed(self, duration):
        self.seek_slider.setRange(0, duration)

    def listwidget_captures_row_inserted(self, parent, first, last):
        if self.listwidget_captures.count() > 0:
            self.button_export.setEnabled(True)

    def listwidget_captures_row_removed(self, parent, first, last):
        if self.listwidget_captures.count() == 0:
            self.button_export.setEnabled(False)

    def listwidget_captures_contextmenu_open(self, pos):
        if self.listwidget_captures.itemAt(pos) == None:
            # Right click outside a segment widget
            return

        global_pos = self.listwidget_captures.mapToGlobal(pos)

        context_actions = QMenu()
        context_actions.addAction("Play")
        context_actions.addAction("Delete", self.__delete_selected_segments)

        context_actions.exec(global_pos)

    def __delete_selected_segments(self):
        items = self.listwidget_captures.selectedItems()
        for item in items:
            index = self.listwidget_captures.row(item)
            self.__delete_segment(index)

        self.__update_capture_segments()

    def __delete_segment(self, index):
        # Remove from UI
        self.listwidget_captures.takeItem(index)
        # Remove in captured frames too
        self.annotation.frames.pop(index)

    def __add_capture_segment(self, frame_start_ms, frame_end_ms):
        count = self.listwidget_captures.count() + 1
        time_start = timestamp_from_ms(frame_start_ms, True)
        time_end = timestamp_from_ms(frame_end_ms, True)
        frame_start = self.annotation.frame_from_ms(frame_start_ms)
        frame_end = self.annotation.frame_from_ms(frame_end_ms)
        segment_text = "{0}: Frames {1} - {2}".format(
            count, frame_start, frame_end)

        seg_widget = CaptureSegmentWidget()
        seg_widget.set_text(segment_text).set_subtext(time_start, time_end)
        # seg_widget.button_delete_clicked(self.__delete_selected_segments)
        listwidget_item = QListWidgetItem(self.listwidget_captures)
        listwidget_item.setSizeHint(seg_widget.sizeHint())

        self.listwidget_captures.addItem(listwidget_item)
        self.listwidget_captures.setItemWidget(
            listwidget_item, seg_widget)

    def __update_capture_segments(self):
        # Refresh listview
        self.listwidget_captures.clear()
        for f in self.annotation.frames:
            self.__add_capture_segment(
                f.frame_start_ms, f.frame_end_ms)

    def on_menu_calc_click(self):
        dialog = createAgreementDialog(self)
        dialog.exec()

class createAgreementDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = agreement_dialog()
        self.ui.setupUi(self)
        self.ui.sig_slot_link(self)
