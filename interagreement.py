# interagreement.py defines functions to
from pygamma_agreement import Continuum, PositionalSporadicDissimilarity
from pyannote.core import Segment
import xml.etree.ElementTree as ET

# Initialize xmlCalc() class with input of a list of xml
# .computeGamma() to calculate inter-annotator agreement
# .annotationList to return list of annotations
class xmlCalc:
    def __init__(self, inList):
        self.annotationList = self.xml_to_list(inList)

    # Make function to parse xml files, return list of elements of ["annotator", frame start, frame end]
    def xml_to_list(self, xmlFileIn):
        annotationList = []
        j = 1
        fstartstring = f's{j}Start'
        fendstring = f's{j}End'
        for i in range(len(xmlFileIn)):
            tree = ET.parse(xmlFileIn[i])
            root = tree.getroot()
            #annotator = root.find("annotator").text
            filepath = xmlFileIn[i]
            for framedata in root.iter("framedata"):
                k = 0
                for f in framedata.iter():
                    if f != framedata:
                        k += 1
                for l in range(k):
                    framestart = int(framedata.find(fstartstring).text)
                    frameend = int(framedata.find(fendstring).text)
                    annotationList.append([filepath, f"Annotation {j}", framestart, frameend])
                    j += 1
        return annotationList

    # Function to calculate gamma for inter-annotator agreement. Gamma closer to 1 = higher agreement
    def computeGamma(self):
        annotationList = self.annotationList
        continuum = Continuum()  # add annotation data to continuum
        for x in annotationList:
            continuum.add(x[0], Segment(x[2], x[3]), "")
        dissim = PositionalSporadicDissimilarity(delta_empty=1.0)
        gamma_results = continuum.compute_gamma(dissim)  # output final gamma val
        # print(f"The gamma for that annotation is f{gamma_results.gamma}") old code
        return gamma_results.gamma

if __name__ == "__main__":
    xmlList = ["test1.xml", "test2.xml"]  # Store xml file names/dir as strings in list
    # Example print for illustration
    xmlData = xmlCalc(xmlList)
    print(xmlData.annotationList)
    print(xmlData.computeGamma())
