from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):

        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 600)

        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.verticalLayout = QVBoxLayout(self.central_widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.upper_h_layout = QHBoxLayout()
        self.upper_h_layout.setObjectName("upper_h_layout")

        # == Video player ==
        self.video_player_widget = QVideoWidget(self.central_widget)
        self.video_player_widget.setObjectName("video_player_widget")
        self.upper_h_layout.addWidget(self.video_player_widget)

        # Backend media player
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_player_widget)

        # == Video info and event frames ==
        self.upper_right_v_layout = QVBoxLayout()
        self.upper_right_v_layout.setObjectName("upper_right_v_layout")
        self.label_videoinfo = QLabel(self.central_widget)
        self.label_videoinfo.setObjectName("label_videoinfo")
        self.upper_right_v_layout.addWidget(self.label_videoinfo)
        self.text_videoinfo = QTextEdit(self.central_widget)
        self.text_videoinfo.setReadOnly(True)
        self.text_videoinfo.setObjectName("text_videoinfo")
        self.upper_right_v_layout.addWidget(self.text_videoinfo)
        self.label_events = QLabel(self.central_widget)
        self.label_events.setObjectName("label_events")
        self.upper_right_v_layout.addWidget(self.label_events)
        self.scroll_area_events = QScrollArea(self.central_widget)
        self.scroll_area_events.setWidgetResizable(True)
        self.scroll_area_events.setObjectName("scroll_area_events")
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 271, 349))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scroll_area_events.setWidget(self.scrollAreaWidgetContents)
        self.upper_right_v_layout.addWidget(self.scroll_area_events)
        self.upper_right_v_layout.setStretch(1, 1)
        self.upper_right_v_layout.setStretch(3, 3)
        self.upper_h_layout.addLayout(self.upper_right_v_layout)
        self.upper_h_layout.setStretch(0, 5)
        self.upper_h_layout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.upper_h_layout)

        # == Media Controls and Buttons ==
        self.lower_h_layout = QHBoxLayout()
        self.lower_h_layout.setObjectName("lower_h_layout")
        # Play button
        self.play_button = QPushButton(self.central_widget)
        self.play_button.setObjectName("play_button")
        self.play_button.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay))
        self.lower_h_layout.addWidget(self.play_button)
        self.play_button.setEnabled(False)
        
        # Video seekbar
        self.seek_slider = QSlider(self.central_widget)
        self.seek_slider.setOrientation(Qt.Horizontal)
        self.seek_slider.setObjectName("seek_slider")
        self.seek_slider.setEnabled(False)
        
        self.lower_h_layout.addWidget(self.seek_slider)
        
        # Capture start button
        self.cap_start_button = QPushButton(self.central_widget)
        self.cap_start_button.setObjectName("cap_start_button")
        self.cap_start_button.setEnabled(False)        
        
        self.lower_h_layout.addWidget(self.cap_start_button)
        
        # Capture end button
        self.cap_end_button = QPushButton(self.central_widget)
        self.cap_end_button.setObjectName("cap_end_button")
        self.cap_end_button.setEnabled(False)        
        
        self.lower_h_layout.addWidget(self.cap_end_button)
        
        # Export button
        self.export_button = QPushButton(self.central_widget)
        self.export_button.setObjectName("export_button")
        self.export_button.setEnabled(False)
        
        self.lower_h_layout.addWidget(self.export_button)
        
        # Layouts
        self.verticalLayout.addLayout(self.lower_h_layout)
        MainWindow.setCentralWidget(self.central_widget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1280, 26))
        self.menubar.setObjectName("menubar")
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_open_file = QAction(MainWindow)
        self.action_open_file.setObjectName("action_open_file")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.menu_file.addAction(self.action_open_file)
        self.menubar.addAction(self.menu_file.menuAction())

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_videoinfo.setText(
            _translate("MainWindow", "Video Information"))
        self.label_events.setText(_translate("MainWindow", "Event Frames"))
        self.cap_start_button.setText(
            _translate("MainWindow", "Capture Start"))
        self.cap_end_button.setText(_translate("MainWindow", "Capture End"))
        self.play_button.setText(_translate("MainWindow", "Play"))
        self.export_button.setText(_translate("MainWindow", "Export..."))
        self.menu_file.setTitle(_translate("MainWindow", "File"))
        self.action_open_file.setText(_translate("MainWindow", "Open File..."))
        self.action_open_file.setToolTip(_translate(
            "MainWindow", "Open video file for annotation"))
        self.action_open_file.setShortcut(_translate("MainWindow", "F1"))
        self.actionSave_As.setText(_translate("MainWindow", "PASCAL VOL"))

    def setupEvents(self):
        self.action_open_file.triggered.connect(self.openFile)
        self.play_button.clicked.connect(self.play)
        self.media_player.stateChanged.connect(self.mediaStateChanged)
        self.media_player.positionChanged.connect(self.positionChanged)
        self.media_player.durationChanged.connect(self.durationChanged)
        self.seek_slider.sliderMoved.connect(self.setPosition)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(
            None, 'Open Image', '', 'Video Files (*.mp4)')
        if fileName:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.media_player.setVolume(100)
            self.play_button.setEnabled(True)
            self.seek_slider.setEnabled(True)
            #self.volume_slider.setEnabled(True)
            self.text_videoinfo.setText(fileName)

    def play(self):
        if self.media_player.state() == QMediaPlayer.State.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def mediaStateChanged(self, state):
        if self.media_player.state() == QMediaPlayer.State.PlayingState:
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
            self.play_button.setText("Pause")
        else:
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
            self.play_button.setText("Play")

    def positionChanged(self, position):
        self.seek_slider.setValue(position)

    def durationChanged(self, duration):
        self.seek_slider.setRange(0, duration)

    def setPosition(self, position):
        self.media_player.setPosition(position)
