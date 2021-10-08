"""This file stores object models used in the project"""

import os
from dataclasses import dataclass
from typing import List

from utility import get_video_metadata


class VideoAnnotationData:
    def __init__(self, full_path):
        """
        Constructor.

        :param path: Full path to video file.
        :param res: Resolution of video represented by a tuple. (width, height)
        """
        self.foldername = os.path.dirname(full_path)
        self.filename = os.path.basename(full_path)
        self.fps, self.resolution, _ = get_video_metadata(full_path)
        self.frames: List[VideoAnnotationSegment] = []

    def frame_from_ms(self, ms: int):
        ms_per_frame = int(1000 / self.fps)
        return ms // ms_per_frame


@dataclass
class VideoAnnotationSegment:
    frame_start_ms: int
    frame_end_ms: int
