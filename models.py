"""This file contains object models for the video annotator"""

import os
from dataclasses import dataclass, field

from PyQt5.QtCore import QRect

from utility import get_video_metadata


class VideoAnnotationData:
    """Object model storing annotation data of a video file."""

    def __init__(self):
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
        self.fps, self.resolution = get_video_metadata(video_path)
        self._segments: list[VideoAnnotationSegment] = []

    @property
    def segments(self):
        """
        Get list of all annotation segments sorted by start time in ascending order.  
        """
        self._segments.sort(key=lambda f: f.start)
        print(self._segments)
        return self._segments

    def add_segment(self, segment):
        """
        Add a new segment to this annotation. 

        :param segment: A VideoAnnotationSegment object.
        """
        self._segments.append(segment)

    def find_next_segment(self, position):
        """
        Find the next segment with start time greater than position.

        :param position: Time in milliseconds since start of video.
        """
        segments_after = list(filter(lambda s: position < s.start, self._segments))
        if len(segments_after) > 0:
            segments_after.sort(key=lambda s: s.start)
            return segments_after[0]
        return None

    def find_segment(self, position):
        """
        Find the first segment with that contains position in its start/end range.

        :param position: Time in milliseconds since start of video.
        """
        return next((seg for seg in self._segments if position >= seg.start and position <= seg.end), None)

    def frame_from_ms(self, ms: int):
        """
        Get frame number from video time in milliseconds.

        :param ms: Time in miliseconds since start of video.
        """
        ms_per_frame = 1000 / self.fps
        return int(ms / ms_per_frame)


@dataclass
class VideoAnnotationSegment:
    """Object model storing a single segment, or one annotation."""
    # Start/end is in miliseconds since start of video
    start: int = 0
    end: int = 0
    boxes: list[QRect] = field(default_factory=list)

    def __hash__(self):
        return self.start
