# interagreement.py defines functions to
from pygamma_agreement import Continuum, PositionalSporadicDissimilarity
from pyannote.core import Segment
import xml.etree.ElementTree as ET

############################################################################
# Important: add code to bring in xml files using UI (probably in main.py) #
############################################################################


xmlList = ["test1.xml", "test2.xml"]  # Store xml file names/dir as strings in list

# Make function to parse xml files, return list of ["annotator", frame start, frame end]
def xml_to_pygammaIn(xmlFileIn):
    annotationList = []
    j = 1
    framestart = f's{j}Start'
    frameend = f's{j}End'
    for i in range(len(xmlFileIn)):
        tree = ET.parse(xmlFileIn[i])
        root = tree.getroot()
        annotator = root.find("annotator").text
        for framedata in root.iter("framedata"):
            k = 0
            for f in framedata.iter():
                if f != framedata:
                    k += 1
            for l in range(k):
                annotationList.append([annotator, int(framedata.find(framestart).text), int(framedata.find(frameend).text)])
                j += 1
    return annotationList

# Function to calculate gamma for inter-annotator agreement. Gamma closer to 1 = higher agreement
def compute_Gamma(annotationList):
    continuum = Continuum()  # add annotation data to continuum
    for x in annotationList:
        continuum.add(x[0], Segment(x[1], x[2]), "")
    dissim = PositionalSporadicDissimilarity(delta_empty=1.0)
    gamma_results = continuum.compute_gamma(dissim)  # output final gamma val
    # print(f"The gamma for that annotation is f{gamma_results.gamma}") old code
    return gamma_results.gamma


# Example print for illustration
annotationList = xml_to_pygammaIn(xmlList)
print(annotationList)
print(compute_Gamma(annotationList))