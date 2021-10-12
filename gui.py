# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'Video AnnotatorWVGNCS.ui'
##
# Created by: Qt User Interface Compiler version 5.15.2
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtMultimedia import QMediaPlayer
from PySide2.QtMultimediaWidgets import QVideoWidget

def formatTime(time: int):
    second = time//1000
    minute = second//60
    hour = minute//60
    return f"{'0' if hour < 10 else ''}{hour}:{'0' if minute < 10 else ''}{minute}:{'0' if second < 10 else ''}{second}"

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        
        # Window
        MainWindow.resize(1127, 608)
        self.action_open_file = QAction(MainWindow)
        self.action_open_file.setObjectName(u"action_open_file")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.verticalLayout = QVBoxLayout(self.central_widget)
        
        # Video Area
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.upper_h_layout = QHBoxLayout()
        self.upper_h_layout.setObjectName(u"upper_h_layout")
        self.video_player_widget = QVideoWidget(self.central_widget)
        self.video_player_widget.setObjectName(u"video_player_widget")

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self.video_player_widget)

        self.upper_h_layout.addWidget(self.video_player_widget)
        
        # Video Information
        self.upper_right_v_layout = QVBoxLayout()
        self.upper_right_v_layout.setObjectName(u"upper_right_v_layout")
        self.label_videoinfo = QLabel(self.central_widget)
        self.label_videoinfo.setObjectName(u"label_videoinfo")

        self.upper_right_v_layout.addWidget(self.label_videoinfo)

        self.text_videoinfo = QTextEdit(self.central_widget)
        self.text_videoinfo.setObjectName(u"text_videoinfo")
        self.text_videoinfo.setReadOnly(True)

        self.upper_right_v_layout.addWidget(self.text_videoinfo)

        # Events Area
        self.label_events = QLabel(self.central_widget)
        self.label_events.setObjectName(u"label_events")

        self.upper_right_v_layout.addWidget(self.label_events)

        self.scroll_area_events = QScrollArea(self.central_widget)
        self.scroll_area_events.setObjectName(u"scroll_area_events")
        self.scroll_area_events.setWidgetResizable(True)
        
        self.scrollLayout = QVBoxLayout()
        self.scrollAreaWidgetContents = QWidget(self.scroll_area_events)
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 271, 349))
        self.scrollAreaWidgetContents.setLayout(self.scrollLayout)

        self.scroll_area_label = QLabel(alignment=Qt.AlignTop)
        
        self.scroll_area_events.setWidget(self.scroll_area_label)
        self.scrollLayout.addWidget(self.scroll_area_label)
        vbar = self.scroll_area_events.verticalScrollBar()
        vbar.setValue(vbar.maximum())

        self.upper_right_v_layout.addWidget(self.scroll_area_events)
        

        self.upper_right_v_layout.setStretch(1, 1)
        self.upper_right_v_layout.setStretch(3, 3)

        self.upper_h_layout.addLayout(self.upper_right_v_layout)

        self.upper_h_layout.setStretch(0, 3)
        self.upper_h_layout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.upper_h_layout)

        # Capture buttons
        self.lower_h_layout = QHBoxLayout()
        self.lower_h_layout.setObjectName(u"lower_h_layout")
        self.cap_start_button = QPushButton(self.central_widget)
        self.cap_start_button.setObjectName(u"cap_start_button")
        self.cap_start_button.setEnabled(False)

        self.lower_h_layout.addWidget(self.cap_start_button)

        self.cap_end_button = QPushButton(self.central_widget)
        self.cap_end_button.setObjectName(u"cap_end_button")
        self.cap_end_button.setEnabled(False)

        self.lower_h_layout.addWidget(self.cap_end_button)

        # Seek Slider, Volume Slider and Times
        control_box = QHBoxLayout()
        self.seek_slider = QSlider(self.central_widget)
        self.seek_slider.setObjectName(u"seek_slider")
        self.seek_slider.setOrientation(Qt.Horizontal)
        self.seek_slider.setRange(0, 0)
        self.seek_slider.setEnabled(False)

        slider_box = QVBoxLayout()

        slider_box.addWidget(self.seek_slider)
        slider_box.setContentsMargins(0, 30, 0, 0)
        slider_box.setSpacing(0)

        self.label_elapsed = QLabel(alignment=Qt.AlignLeft, text='--:--:--')
        self.label_maximum = QLabel(alignment=Qt.AlignRight, text='--:--:--')

        duration_box = QHBoxLayout()
        duration_box.setContentsMargins(0, 0, 0, 0)
        duration_box.addWidget(self.label_elapsed)
        duration_box.addWidget(self.label_maximum)
        slider_box.addLayout(duration_box)
        
        control_box.addLayout(slider_box)
        
        ## Volume slider 
        # self.volume_slider = phonon.Phonon.VolumeSlider( None )
        # self.volume_slider.setOrientation( Qt.Vertical )
        volume_box = QVBoxLayout()
        volume_box.setContentsMargins(0, 0, 0, 0)
        volume_box.addWidget(QLabel(alignment=Qt.AlignTop, text='Volume'))
        self.volume_slider = QSlider(self.central_widget)
        self.volume_slider.setObjectName(u"volume_slider")
        self.volume_slider.setOrientation(Qt.Vertical)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setEnabled(False)
        volume_box.addWidget(self.volume_slider, alignment=Qt.AlignCenter)
        # self.volume_slider.setMaximumSize(30, 60)
        self.volume_slider.setMinimumSize(30, 40)
        control_box.addLayout(volume_box)
        # control_box.setMaximumHeight(40)

        self.lower_h_layout.addLayout(control_box)
        
        self.seek_slider.valueChanged.connect(lambda value: self.label_elapsed.setText(formatTime(value)))

        # Play, Pause and Export buttons
        self.play_button = QPushButton(self.central_widget)
        self.play_button.setObjectName(u"play_button")
        self.play_button.setEnabled(False)

        self.lower_h_layout.addWidget(self.play_button)

        self.pause_button = QPushButton(self.central_widget)
        self.pause_button.setObjectName(u"pause_button")
        self.pause_button.setEnabled(False)

        self.lower_h_layout.addWidget(self.pause_button)

        self.export_button = QPushButton(self.central_widget)
        self.export_button.setObjectName(u"export_button")
        self.export_button.setEnabled(False)

        self.lower_h_layout.addWidget(self.export_button)

        self.verticalLayout.addLayout(self.lower_h_layout)

        # Menu bar
        MainWindow.setCentralWidget(self.central_widget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1127, 26))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menu_file.addAction(self.action_open_file)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"Python Video Annotator", None))
        self.action_open_file.setText(QCoreApplication.translate(
            "MainWindow", u"Open File...", None))
# if QT_CONFIG(tooltip)
        self.action_open_file.setToolTip(QCoreApplication.translate(
            "MainWindow", u"Open video file for annotation", None))
#endif // QT_CONFIG(tooltip)
# if QT_CONFIG(shortcut)
        self.action_open_file.setShortcut(
            QCoreApplication.translate("MainWindow", u"F1", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_As.setText(QCoreApplication.translate(
            "MainWindow", u"PASCAL VOL", None))
        self.label_videoinfo.setText(QCoreApplication.translate(
            "MainWindow", u"Video Information", None))
        self.label_events.setText(QCoreApplication.translate(
            "MainWindow", u"Event Frames", None))
        self.cap_start_button.setText(QCoreApplication.translate(
            "MainWindow", u"Capture Start", None))
        self.cap_end_button.setText(QCoreApplication.translate(
            "MainWindow", u"Capture End", None))
        self.play_button.setText(
            QCoreApplication.translate("MainWindow", u"Play", None))
        self.pause_button.setText(
            QCoreApplication.translate("MainWindow", u"Pause", None))
        self.export_button.setText(QCoreApplication.translate(
            "MainWindow", u"Export...", None))
        self.menu_file.setTitle(
            QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi
