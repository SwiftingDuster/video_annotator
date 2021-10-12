from gui import Ui_MainWindow
from PySide2.QtWidgets import QFileDialog
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtCore import QUrl
from lxml import etree as ET
#import xml.etree.ElementTree as ET
import cv2
import os

captures = []
metadata = {}

def setupEvents(ui: Ui_MainWindow):
    ui.action_open_file.triggered.connect(lambda _: openFileNameDialog(ui))
    ui.play_button.clicked.connect(lambda _: playVideo(ui))
    ui.pause_button.clicked.connect(lambda _: playVideo(ui))
    
    ui.mediaPlayer.stateChanged.connect(lambda state: stateChanged(ui, state))
    ui.mediaPlayer.durationChanged.connect(lambda duration: durationChanged(ui, duration))
    ui.mediaPlayer.positionChanged.connect(lambda position: positionChanged(ui, position))
    ui.seek_slider.sliderMoved.connect(lambda position: setPosition(ui, position))
    ui.volume_slider.sliderMoved.connect(lambda volume: setVolume(ui, volume))

    ui.cap_start_button.clicked.connect(lambda _: startCapture(ui))
    ui.cap_end_button.clicked.connect(lambda _: endCapture(ui))
    ui.export_button.clicked.connect(lambda _: exportData(ui))

def openFileNameDialog(ui: Ui_MainWindow):
    fileName, _ = QFileDialog.getOpenFileName(
        None, 'Open Image', '', 'Video Files (*.mp4)')
    if fileName:
        ui.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
        ui.mediaPlayer.setVolume(70)
        ui.play_button.setEnabled(True)
        ui.seek_slider.setEnabled(True)
        ui.volume_slider.setEnabled(True)
        ui.text_videoinfo.setText(get_properties(ui, fileName))

def playVideo(ui: Ui_MainWindow):
    if ui.mediaPlayer.state() == QMediaPlayer.PlayingState:
        ui.mediaPlayer.pause()
        ui.play_button.setEnabled(True)
        ui.pause_button.setEnabled(False)
    else:
        ui.mediaPlayer.play()
        ui.play_button.setEnabled(False)
        ui.pause_button.setEnabled(True)
        ui.cap_start_button.setEnabled(True)
        ui.export_button.setEnabled(True)

def stateChanged(ui: Ui_MainWindow, position):
    if ui.mediaPlayer.state() == QMediaPlayer.StoppedState:
        ui.play_button.setEnabled(True)
        ui.pause_button.setEnabled(False)
        ui.cap_start_button.setEnabled(False)

def positionChanged(ui: Ui_MainWindow, position):
    ui.seek_slider.setValue(position)

def setPosition(ui: Ui_MainWindow, position):
    ui.mediaPlayer.setPosition(position)

def setVolume(ui: Ui_MainWindow, volume):
    ui.mediaPlayer.setVolume(volume)

def durationChanged(ui: Ui_MainWindow, duration):
    ui.seek_slider.setRange(0, duration)
    ui.label_maximum.setText(_formatTime(ui.mediaPlayer.duration()))
    ui.label_elapsed.setText('00:00:00')


def startCapture(ui: Ui_MainWindow):
    timestamp = _formatTime(ui.mediaPlayer.position())
    captures.append({'capture_start_time': timestamp})
    ui.scroll_area_label.setText(f'{ui.scroll_area_label.text()}\nstarting capture {len(captures)} at {timestamp}')
    ui.cap_start_button.setEnabled(False)
    ui.cap_end_button.setEnabled(True)


def endCapture(ui: Ui_MainWindow):
    timestamp = _formatTime(ui.mediaPlayer.position())
    captures[-1]['capture_end_time']= timestamp
    ui.scroll_area_label.setText(f'{ui.scroll_area_label.text()}\nended capture {len(captures)} at {timestamp}')
    ui.cap_start_button.setEnabled(True)
    ui.cap_end_button.setEnabled(False)

def _formatTime(time):
    second = time//1000
    minute = second//60
    hour = minute//60
    #milli = time%1000
    return f"{'0' if hour < 10 else ''}{hour}:{'0' if minute < 10 else ''}{minute}:{'0' if second < 10 else ''}{second}"

def _getSize(fileobject):
    fileobject.seek(0,2) # move the cursor to the end of the file
    size = fileobject.tell()
    return size/(1024**2)

def exportData(ui: Ui_MainWindow):
    filename = QFileDialog.getSaveFileName(None, 'Save File', os.path.basename(metadata['name']).split('.')[0]+'_annotations.xml', 'XML Files (*.xml)')
    if filename[0] != '':
        # filename[0].setNameFilters(["*.xml"])
        # filename[0].selectNameFilter("XML Files (*.xml)")
        xml_tree = _parseXML(filename[0])
        xml_tree.write(filename[0], pretty_print=True)


def _parseXML(filename):
    annotation = ET.Element('annotation')
    # header
    ET.SubElement(annotation, 'path').text = os.path.dirname(metadata['name'])
    ET.SubElement(annotation, 'filename').text = os.path.basename(metadata['name'])
    ET.SubElement(annotation, 'size').text = str(metadata['size'])
    ET.SubElement(annotation, 'size_unit').text = metadata['size_unit']
    ET.SubElement(annotation, 'height').text = str(metadata['height'])
    ET.SubElement(annotation, 'width').text = str(metadata['width'])
    ET.SubElement(annotation, 'dimension_units').text = metadata['dimension_units']
    ET.SubElement(annotation, 'duration').text = str(metadata['duration'])
    ET.SubElement(annotation, 'duration_unit').text = metadata['duration_unit']
    
    capture_list = ET.SubElement(annotation, 'captures')
    for capture in captures:
        cap = ET.SubElement(capture_list, 'capture')
        ET.SubElement(cap, 'starttime').text = capture.get('capture_start_time')
        ET.SubElement(cap, 'endtime').text = capture.get('capture_end_time')

    tree = ET.ElementTree(annotation)
    return tree

def get_properties(ui: Ui_MainWindow, fileName):
    with open(fileName, 'rb') as file:
        size = _getSize(file)
    cv2video = cv2.VideoCapture(fileName)
    height = cv2video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cv2video.get(cv2.CAP_PROP_FRAME_WIDTH)

    framecount = cv2video.get(cv2.CAP_PROP_FRAME_COUNT ) 
    frames_per_sec = cv2video.get(cv2.CAP_PROP_FPS)
    duration = framecount / frames_per_sec
    metadata['name'] = fileName
    metadata['size'] = round(size, 3)
    metadata['size_unit'] = 'MB'
    metadata['height'] = int(height)
    metadata['width'] = int(width)
    metadata['dimension_units'] = 'px'
    metadata['duration'] = int(duration)
    metadata['duration_unit'] = 'seconds'

    return f'{os.path.basename(fileName)}\nSize: {round(size, 3)} MB\nDuration: {int(duration)}s\nVideo Dimension: {int(width)} x {int(height)}\n'