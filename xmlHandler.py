import xml.etree.ElementTree as ET
from xml.dom import minidom

class XMLhandler:

    def __init__(self,filename,element,data):

        self.filename=filename
        self.element=element
        self.data=data

    def modifyXML(self):
        tree = ET.parse(self.filename)

        root = tree.getroot()
        for item in root.iter(self.element):
            item.text=self.data

        tree.write(self.filename)

# create an xml object to store xml stuff

    def addFramedata(self):

        tree=ET.parse(self.filename)
        root=tree.getroot()

        # for framedata in root.iter(self.element):
        #     k = 0
        #     for f in framedata.iter():
        #         if f != framedata:
        #             k+=1
        #         for i in range(k):
        #             ET.SubElement(root,f"s{i}Start")

    # def addData(self):
    #



    def GenerateXML(self):
    # create the file structure
        root = ET.Element('annotation')
        annotator = ET.SubElement(root, 'annotator')
        annotator.text = 'Name1'
        folderName = ET.SubElement(root, "folder")
        folderName.text = "n00007846"
        source = ET.SubElement(root, "source")
        database = ET.SubElement(source, "database")
        database.text = "ImageNet database"
        size = ET.SubElement(root, "size")
        width = ET.SubElement(size, "width")
        width.text = "500"
        height = ET.SubElement(size, "height")
        height.text = "333"
        depth = ET.SubElement(size, "depth")
        depth.text = "3"
        video_resolution=ET.SubElement(root,"video_resolution")
        video_resolution.text="1920x1080"
        segmented = ET.SubElement(root, "segmented")
        segmented.text = "0"
        object = ET.SubElement(root, "object")
        name = ET.SubElement(object, "name")
        name.text = "n0007846"
        pose = ET.SubElement(object, "pose")
        pose.text = "Unspecified"
        truncated = ET.SubElement(object, "truncated")
        truncated.text = "0"
        difficult = ET.SubElement(object, "difficult")
        difficult.text = "0"
        boundbox = ET.SubElement(object, "bndbox")
        xmin = ET.SubElement(boundbox, "xmin")
        xmin.text = "161"
        ymin = ET.SubElement(boundbox, "ymin")
        ymin.text = "52"
        xmax = ET.SubElement(boundbox, "xmax")
        xmax.text = "285"
        ymax = ET.SubElement(boundbox, "ymax")
        ymax.text = "247"

        framedata = ET.SubElement(object, "framedata")
        s1Start = ET.SubElement(framedata, "s1Start")
        s1Start.text = "582"
        s1End = ET.SubElement(framedata, "s1End")
        s1End.text = "400"
        s2Start = ET.SubElement(framedata, "s2Start")
        s2Start.text = "7393"
        s2End = ET.SubElement(framedata, "s2End")
        s2End.text = "81034"

        # prettify the xml data
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write(self.filename, encoding="utf-8")

if __name__ == "__main__":
    #this is modify the xml: filename,element,data that you want to set
    #example: modifying foldername to file1
    xmlinput=XMLhandler("testtest.xml","folder","file1")

    # if you want to generate a XML file structure
    # with dummy data, use the function below
    # xmlinput.GenerateXML()

    #calling teh modifyXML to modify the xml element data
    xmlinput.modifyXML()





