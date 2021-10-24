"""This file stores object models used in the project"""

import os
from dataclasses import dataclass, field

from PyQt5.QtCore import QRect

from utility import get_video_metadata


class VideoAnnotationData:

    def __init__(self):
        """
        Constructor.
        """
        self.foldername = self.filename = self.fps = ""
        self.resolution = 0, 0
        self._segments: list[VideoAnnotationSegment] = []

    def load(self, video_path):
        """
        Load information from video metadata.

        :param video_path: Full path to video file.
        """
        self.foldername = os.path.dirname(video_path)
        self.filename = os.path.basename(video_path)
        self.fps, self.resolution, _ = get_video_metadata(video_path)
        self._segments: list[VideoAnnotationSegment] = []

    @property
    def segments(self):
        self._segments.sort(key=lambda f: f.start)
        return self._segments

    def add_segment(self, segment):
        self._segments.append(segment)

    def find_next_segment(self, position):
        """
        Find the closest segment with start greater than position.
        """
        segments_after = list(filter(lambda s: position < s.start, self._segments))
        if len(segments_after) > 0:
            segments_after.sort(key=lambda s: s.start)
            return segments_after[0]
        return None

    def find_segment(self, position):
        return next((seg for seg in self._segments if position >= seg.start and position <= seg.end), None)

    def frame_from_ms(self, ms: int):
        ms_per_frame = 1000 / self.fps
        return int(ms / ms_per_frame)


@dataclass
class VideoAnnotationSegment:
    start: int = 0
    end: int = 0
    boxes: list[QRect] = field(default_factory=list)

    def __hash__(self):
        return self.start
