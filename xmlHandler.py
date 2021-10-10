import xml.etree.ElementTree as ET
from xml.dom import minidom

class XMLhandler:

    def __init__(self,filename):

        self.filename=filename


    #accepts element name and element value to be changed

    def modifyXML(self,element,data):
        self.element = element
        self.data = data
        tree = ET.parse(self.filename)

        root = tree.getroot()
        for item in root.iter(self.element):
            item.text=self.data

        tree.write(self.filename)

# create an xml object to store xml stuff




    def GenerateXML(self,annotator_value,
                    foldername_value,database_value,
                    width_value,height_value,depth_value,
                    video_resolution_value,
                    segmented_value,
                    name_value,pose_value,
                    truncated_value,difficult_value,
                    xmin_value,ymin_value,
                    xmax_value,ymax_value,
                    s1Start_value,s1End_value):
    # create the file structure

        self.annotator_value=annotator_value
        self.foldername_value=foldername_value
        self.database_value=database_value
        self.width_value=width_value
        self.height_value=height_value
        self.depth_value=depth_value
        self.video_resolution_value=video_resolution_value
        self.segmented_value=segmented_value
        self.name_value=name_value
        self.pose_value=pose_value
        self.truncated_value=truncated_value
        self.difficult_value=difficult_value
        self.xmin_value=xmin_value
        self.ymin_value=ymin_value
        self.xmax_value=xmax_value
        self.ymax_value=ymax_value
        self.s1Start_value=s1Start_value
        self.s1End_value=s1End_value




        root = ET.Element("annotation")
        annotator = ET.SubElement(root,"annotator")
        annotator.text = self.annotator_value
        folderName = ET.SubElement(root, "folder")
        folderName.text = self.foldername_value
        file_name = ET.SubElement(root, "filename")
        file_name.text=self.filename
        source = ET.SubElement(root, "source")
        database = ET.SubElement(source, "database")
        database.text = self.database_value
        size = ET.SubElement(root, "size")
        width = ET.SubElement(size, "width")
        width.text = self.width_value
        height = ET.SubElement(size, "height")
        height.text = self.height_value
        depth = ET.SubElement(size, "depth")
        depth.text = self.depth_value
        video_resolution=ET.SubElement(root,"video_resolution")
        video_resolution.text=self.video_resolution_value

        #get list of segments
        for item in range(len(self.segmented_value)):
            segmented = ET.SubElement(root, f"segmented{item+1}")
            segmented.text = str(self.segmented_value[item])
        object = ET.SubElement(root, "object")
        name = ET.SubElement(object, "name")
        name.text = self.name_value
        pose = ET.SubElement(object, "pose")
        pose.text = self.pose_value
        truncated = ET.SubElement(object, "truncated")
        truncated.text = self.truncated_value
        difficult = ET.SubElement(object, "difficult")
        difficult.text = self.difficult_value
        boundbox = ET.SubElement(object, "boundbox")
        xmin = ET.SubElement(boundbox, "xmin")
        xmin.text = self.xmin_value
        ymin = ET.SubElement(boundbox, "ymin")
        ymin.text = self.ymin_value
        xmax = ET.SubElement(boundbox, "xmax")
        xmax.text = self.xmax_value
        ymax = ET.SubElement(boundbox, "ymax")
        ymax.text = self.ymax_value
        framedata = ET.SubElement(object, "framedata")
        #returns list of start frames and end frames
        for item in range(len(self.s1Start_value)):
            s1Start = ET.SubElement(framedata, f"s{item+1}Start")
            s1Start.text = str(self.s1Start_value[item])
            s1End = ET.SubElement(framedata, f"s{item+1}End")
            s1End.text = str(self.s1End_value[item])






        # prettify the xml data
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write(self.filename, encoding="utf-8")

if __name__ == "__main__":
    #example: modifying foldername to file1
    xmlinput=XMLhandler("testtest.xml")

    # if you want to generate a XML file structure
    # with dummy data, use the function below
    #changed segmented to get a list
    seg_list = ["data1", "data2",
                  "data3", "data4", "data5"]
    startFramelist=["10","100","20","235"]
    endFramelist=["12","15","22","33"]
    xmlinput.GenerateXML("nameless",
                    "File2","ImageNet database","200",
                    "222","2","1920x1020",
                    seg_list,"obj1","Unspecified",
                    "0","0","160","50","200","130",startFramelist,endFramelist)

    #calling the modifyXML to modify the xml element data
    #modifying width to 100
    #format: element_name,element_value
    xmlinput.modifyXML("width","100")





