import xml.etree.ElementTree as ET

from PyQt5.QtCore import QPoint, QRect

from models import VideoAnnotationData, VideoAnnotationSegment


class XMLUtils:

    def __init__(self, filename, path):
        self.filename = filename
        self.path = path

    # accepts element name and element value to be changed
    def modifyXML(self, element, data):
        self.element = element
        self.data = data
        tree = ET.parse(self.filename)

        root = tree.getroot()
        for item in root.iter(self.element):
            item.text = self.data

        tree.write(self.filename)

    @staticmethod
    def loadXML(file_path):
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

    # create an xml object to store xml stuff
    def saveXML(self, foldername_value, width_value, height_value, fps_value, segmented_value):
        # create the file structure
        self.root_value = "Annotation"
        self.annotator_value = "Video Annotator"
        self.foldername_value = foldername_value

        self.width_value = width_value
        self.height_value = height_value

        self.video_resolution_value = f"{width_value}x{height_value}"
        self.fps_value = fps_value
        self.segmented_value = segmented_value


        root = ET.Element(self.root_value)
        annotator = ET.SubElement(root, "annotator")
        annotator.text = self.annotator_value
        folderName = ET.SubElement(root, "folder")
        folderName.text = self.foldername_value

        file_name = ET.SubElement(root, "filename")
        file_name.text = self.filename




        size = ET.SubElement(root, "size")
        width = ET.SubElement(size, "width")
        width.text = self.width_value
        height = ET.SubElement(size, "height")
        height.text = self.height_value


        video_resolution = ET.SubElement(root, "video_resolution")
        video_resolution.text = self.video_resolution_value
        fps = ET.SubElement(root, "fps")
        fps.text = self.fps_value

        # get list of segments

        segments = ET.SubElement(root, f"segments")

        for item in self.segmented_value:
            start, end = item.start, item.end

            segment = ET.SubElement(segments, f"segment")
            framestart = ET.SubElement(segment, "start")
            framestart.text = str(start)
            frameend = ET.SubElement(segment, "end")
            frameend.text = str(end)
            boxes = ET.SubElement(segment, "boxes")
            for b in item.boxes:
                box = ET.SubElement(boxes, "box")
                topleftX = ET.SubElement(box, "tlX")
                topleftX.text = str(b.topLeft().x())
                topleftY = ET.SubElement(box, "tlY")
                topleftY.text = str(b.topLeft().y())
                bottomrightX = ET.SubElement(box, "brX")
                bottomrightX.text = str(b.bottomRight().x())
                bottomrightY = ET.SubElement(box, "brY")
                bottomrightY.text = str(b.bottomRight().y())





        # prettify the xml data

        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        # ET.dump(root)

        tree.write(self.path, encoding="utf-8")


if __name__ == "__main__":
    # example: modifying foldername to file1
    xmlinput = XMLUtils("testxml.xml")



    #For testing
    xmlinput.saveXML("Foldername", "width",
                     "height", "fps", "seg_value")
