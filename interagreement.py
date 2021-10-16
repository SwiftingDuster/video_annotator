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
        fstartstring = 'start'
        fendstring = 'end'
        for i in range(len(xmlFileIn)):
            tree = ET.parse(xmlFileIn[i])
            root = tree.getroot()
            #annotator = root.find("annotator").text
            filepath = xmlFileIn[i]
            for segment in root.iter("segment"):
                '''k = 0
                for f in segment.iter():
                    if f != segment:
                        k += 1
                for l in range(k):'''
                framestart = int(segment.find(fstartstring).text)
                frameend = int(segment.find(fendstring).text)
                annotationList.append([filepath, f"Annotation {j}", framestart, frameend])
                j += 1
        return annotationList

    # Function to calculate gamma for inter-annotator agreement. Gamma closer to 1 = higher agreement
    def computeGamma(self):
        annotationList = self.annotationList
        continuum = Continuum()  # add annotation data to continuum
        for x in annotationList:
            continuum.add(x[0], Segment(x[2], x[3]), '')
        dissim = PositionalSporadicDissimilarity(delta_empty=1.0)
        print('Starting Calculation')
        gamma_results = continuum.compute_gamma(dissim, precision_level=0.1)  # output final gamma val
        # print(f"The gamma for that annotation is f{gamma_results.gamma}") old code
        return gamma_results.gamma

    def dumbsearch(self, inlist):
        j=0
        framepair=['','']
        strlen=len(inlist)
        for i in range(strlen-1):
            if inlist[i].isdigit and inlist[i+1].isdigit:
                if framepair[j]=='':
                    framepair[j]+=inlist[i]+inlist[i+1]
                framepair[j]+=inlist[i+1]
            elif inlist[i].isdigit and not inlist[i+1].isdigit:
                if j==0:
                    j=1
        return framepair

        pass


if __name__ == "__main__":
    xmlList = ["test1.xml", "test2.xml"]  # Store xml file names/dir as strings in list
    # Example print for illustration
    xmlData = xmlCalc(xmlList)
    print(xmlData.annotationList)
    print(xmlData.computeGamma())
