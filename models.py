"""This file stores object models used in the project"""

import os
from dataclasses import dataclass
from typing import List, Tuple


class VideoAnnotationData:
    def __init__(self, path, resolution: Tuple[int, int]):
        """
        Constructor.

        :param path: Full path to video file.
        :param res: Resolution of video represented by a tuple. (width, height)
        """
        self.foldername = os.path.dirname(path)
        self.filename = os.path.basename(path)
        self.resolution = resolution
        self.frames: List[VideoAnnotationSegment] = []


@dataclass
class VideoAnnotationSegment:
    frame_start: int
    frame_end: int
