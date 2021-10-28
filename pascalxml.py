import xml.etree.ElementTree as ET

from PyQt5.QtCore import QPoint, QRect

from models import VideoAnnotationData, VideoAnnotationSegment


class PascalXML:
    """Helper functions to serialize/deserialize XML annotations."""

    @staticmethod
    def load(file_path):
        """
        Load annotations in XML PASCAL VOL format return a VideoAnnotationData object.

        :param file_path: Path to XML file.
        """

        data = VideoAnnotationData()
        xml = ET.parse(file_path)

        folder, file = xml.find("folder").text, xml.find("filename").text
        fps = int(xml.find("fps").text)
        res_w = int(xml.find("size").find("width").text)
        res_h = int(xml.find("size").find("height").text)
        segments_element = xml.find("segments")
        if segments_element is not None:
            for e in xml.find("segments").findall("segment"):
                start = int(e.find("start").text)
                end = int(e.find("end").text)
                boxes = []
                boxes_element = e.find("boxes")
                if boxes_element is not None:
                    for b in boxes_element.findall("box"):
                        tlX, tlY = int(b.find("tlX").text), int(b.find("tlY").text)
                        brX, brY = int(b.find("brX").text), int(b.find("brY").text)
                        boxes.append(QRect(QPoint(tlX, tlY), QPoint(brX, brY)))
                data.add_segment(VideoAnnotationSegment(start, end, boxes))

        data.foldername = folder
        data.filename = file
        data.fps = fps
        data.resolution = (res_w, res_h)
        return data

    @staticmethod
    def save(path, annotation: VideoAnnotationData):
        """
        Convert annotation data to PASCAL VOL format and write to path.

        :param path: Destination path to write to.
        :param annotation: Annotation data.
        """
        
        root = ET.Element("Annotation")

        # Name of annotator
        annotator = ET.SubElement(root, "annotator")
        annotator.text = "Video annotator"
        # Folder name and file name
        folder = ET.SubElement(root, "folder")
        folder.text = "{}".format(annotation.foldername)
        file_name = ET.SubElement(root, "filename")
        file_name.text = "{}".format(annotation.filename)
        # Video resolution
        size = ET.SubElement(root, "size")
        width = ET.SubElement(size, "width")
        width.text = str(annotation.resolution[0])
        height = ET.SubElement(size, "height")
        height.text = str(annotation.resolution[1])
        video_resolution = ET.SubElement(root, "video_resolution")
        video_resolution.text = "{0}x{1}".format(annotation.resolution[0], annotation.resolution[1])
        # Frame rate
        fps = ET.SubElement(root, "fps")
        fps.text = "{0}".format(annotation.fps)
        # Annotation segments
        segments = ET.SubElement(root, f"segments")
        for seg in annotation.segments:
            start, end = seg.start, seg.end
            segment = ET.SubElement(segments, f"segment")
            framestart = ET.SubElement(segment, "start")
            framestart.text = str(start)
            frameend = ET.SubElement(segment, "end")
            frameend.text = str(end)
            boxes = ET.SubElement(segment, "boxes")
            for b in seg.boxes:
                box = ET.SubElement(boxes, "box")
                topleftX = ET.SubElement(box, "tlX")
                topleftX.text = str(b.topLeft().x())
                topleftY = ET.SubElement(box, "tlY")
                topleftY.text = str(b.topLeft().y())
                bottomrightX = ET.SubElement(box, "brX")
                bottomrightX.text = str(b.bottomRight().x())
                bottomrightY = ET.SubElement(box, "brY")
                bottomrightY.text = str(b.bottomRight().y())

        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write(path, encoding="utf-8")
