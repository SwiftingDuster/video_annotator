import typing
from typing import Tuple

import cv2

from xmlHandler import XMLhandler



def get_video_metadata(path) -> Tuple[int, Tuple[int, int], int]:
    cap = cv2.VideoCapture(path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    resolution = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()
    return (fps, resolution, total_frames)


def timestamp_from_ms(ms, show_milisecs=False):
    seconds = (ms/1000) % 60
    seconds = int(seconds)
    minutes = (ms/(1000*60)) % 60
    minutes = int(minutes)
    if not show_milisecs:
        hours = (ms/(1000*60*60)) % 24
        if hours < 1:
            return "%02d:%02d" % (minutes, seconds)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
    else:
        milisecs = ms % 1000
        if minutes < 1:
            return "%02ds:%03dms" % (seconds, milisecs)
        return "%02dm:%02ds:%03dms" % (minutes, seconds, milisecs)


def write_annotator_xml(annotation,file_path):
    xmlinput=XMLhandler(annotation.filename,file_path)
    xmlinput.GenerateXML("Annotation","Video Annotator",annotation.foldername,
                                                    str(annotation.resolution[0]),str(annotation.resolution[1]),
                                                    f"{annotation.resolution[0]}x{annotation.resolution[1]}",
                         str(annotation.fps),annotation.frames)



