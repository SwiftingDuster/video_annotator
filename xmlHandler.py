import xml.etree.ElementTree as ET
from xml.dom import minidom

class XMLhandler:

    def __init__(self,filename):

        self.filename=filename


    #accepts element name and element value to be changed
    #e.g. modifyXML(
    def modifyXML(self,element,data):
        self.element = element
        self.data = data
        tree = ET.parse(self.filename)

        root = tree.getroot()
        for item in root.iter(self.element):
            item.text=self.data

        tree.write(self.filename)

# create an xml object to store xml stuff

    # def addFramedata(self):
    #
    #     tree=ET.parse(self.filename)
    #     root=tree.getroot()

        # for framedata in root.iter(self.element):
        #     k = 0
        #     for f in framedata.iter():
        #         if f != framedata:
        #             k+=1
        #         for i in range(k):
        #             ET.SubElement(root,f"s{i}Start")

    # def addData(self):
    #



    def GenerateXML(self,root_name,annotator_name,annotator_value,foldername,
                    foldername_value,file_name,file_name_value,source,database_name,database_value,
                    size,width,width_value,
                    height,height_value,depth,depth_value,
                    video_resolution,video_resolution_value,
                    segmented,segmented_value,object,
                    name,name_value,pose,pose_value,truncated,
                    truncated_value,difficult,difficult_value,
                    boundbox,xmin,xmin_value,ymin,ymin_value,
                    xmax,xmax_value,ymax,ymax_value,framedata,
                    s1Start,s1Start_value,s1End,s1End_value):
    # create the file structure

        self.root_name=root_name
        self.annotator_name=annotator_name
        self.annotator_value=annotator_value
        self.foldername=foldername
        self.foldername_value=foldername_value
        self.file_name=file_name
        self.file_name_value=file_name_value
        self.source=source
        self.database_name=database_name
        self.database_value=database_value
        self.size=size
        self.width=width
        self.width_value=width_value
        self.height=height
        self.height_value=height_value
        self.depth=depth
        self.depth_value=depth_value
        self.video_resolution=video_resolution
        self.video_resolution_value=video_resolution_value
        self.segmented=segmented
        self.segmented_value=segmented_value
        self.object=object
        self.name=name
        self.name_value=name_value
        self.pose=pose
        self.pose_value=pose_value
        self.truncated=truncated
        self.truncated_value=truncated_value
        self.difficult=difficult
        self.difficult_value=difficult_value
        self.boundbox=boundbox
        self.xmin=xmin
        self.xmin_value=xmin_value
        self.ymin=ymin
        self.ymin_value=ymin_value
        self.xmax=xmax
        self.xmax_value=xmax_value
        self.ymax=ymax
        self.ymax_value=ymax_value
        self.framedata=framedata
        self.s1Start=s1Start
        self.s1Start_value=s1Start_value
        self.s1End=s1End
        self.s1End_value=s1End_value




        root = ET.Element(self.root_name)
        annotator = ET.SubElement(root, self.annotator_name)
        annotator.text = self.annotator_value
        folderName = ET.SubElement(root, self.foldername)
        folderName.text = self.foldername_value
        file_name = ET.SubElement(root, self.file_name)
        file_name.text=self.filename
        source = ET.SubElement(root, self.source)
        database = ET.SubElement(source, self.database_name)
        database.text = self.database_value
        size = ET.SubElement(root, self.size)
        width = ET.SubElement(size, self.width)
        width.text = self.width_value
        height = ET.SubElement(size, self.height)
        height.text = self.height_value
        depth = ET.SubElement(size, self.depth)
        depth.text = self.depth_value
        video_resolution=ET.SubElement(root,self.video_resolution)
        video_resolution.text=self.video_resolution_value


        #get list of segments
        for item in range(len(self.segmented_value)):
            segmented = ET.SubElement(root, self.segmented)
            segmented.text = str(self.segmented_value[item])
        object = ET.SubElement(root, self.object)
        name = ET.SubElement(object, self.name)
        name.text = self.name_value
        pose = ET.SubElement(object, self.pose)
        pose.text = self.pose_value
        truncated = ET.SubElement(object, self.truncated)
        truncated.text = self.truncated_value
        difficult = ET.SubElement(object, self.difficult)
        difficult.text = self.difficult_value
        boundbox = ET.SubElement(object, self.boundbox)
        xmin = ET.SubElement(boundbox, self.xmin)
        xmin.text = self.xmin_value
        ymin = ET.SubElement(boundbox, self.ymin)
        ymin.text = self.ymin_value
        xmax = ET.SubElement(boundbox, self.xmax)
        xmax.text = self.xmax_value
        ymax = ET.SubElement(boundbox, self.ymax)
        ymax.text = self.ymax_value

        framedata = ET.SubElement(object, self.framedata)
        s1Start = ET.SubElement(framedata, self.s1Start)
        s1Start.text = self.s1Start_value
        s1End = ET.SubElement(framedata, self.s1End)
        s1End.text = self.s1End_value


        # prettify the xml data
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write(self.filename, encoding="utf-8")

if __name__ == "__main__":
    #this is modify the xml: filename,element,data that you want to set
    #example: modifying foldername to file1
    xmlinput=XMLhandler("testtest.xml")

    # if you want to generate a XML file structure
    # with dummy data, use the function below
    #changed segmented to get a list
    seg_list = ["segment1", "segment2",
                  "segment3", "segment4", "segment5"]
    xmlinput.GenerateXML("annotation","annotator","nameless","folder",
                    "File2","filename","n000786","source","database","ImageNet database",
                    "size","width","200",
                    "height","222","depth","2",
                    "video_resolution","1920x1020",
                    "segmented",seg_list,"object",
                    "name","testname","pose","Unspecified","truncated",
                    "0","difficult","0",
                    "boundbox","xmin","160","ymin","50",
                    "xmax","200","ymax","130","framedata",
                    "s1Start","10","s1End","200")

    #calling the modifyXML to modify the xml element data
    #modifying width to 100
    #format: element_name,element_value
    xmlinput.modifyXML("width","100")





