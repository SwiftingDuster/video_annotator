# interagreement.py defines functions to
import os
import xml.etree.ElementTree as ET

from pyannote.core import Segment
from pygamma_agreement import Continuum, PositionalSporadicDissimilarity

# Initialize InterAgreement class with input of a list of xml
# .computeGamma() to calculate inter-annotator agreement
# .annotationList to return list of annotations


class InterAgreement:
    """Helper class to calculate Inter Annotator Agreement"""

    def __init__(self, xml_files):
        self.annotationList = self.xml_to_list(xml_files)

    # Parse xml files, return list of elements of ["annotator", frame start, frame end]
    def xml_to_list(self, xmlFileIn):
        annotationList = []
        j = 1
        fstartstring = 'start'
        fendstring = 'end'
        for i in range(len(xmlFileIn)):
            tree = ET.parse(xmlFileIn[i])
            root = tree.getroot()
            #annotator = root.find("annotator").text
            filename = os.path.basename(xmlFileIn[i])
            for segment in root.iter("segment"):
                '''k = 0
                for f in segment.iter():
                    if f != segment:
                        k += 1
                for l in range(k):'''
                framestart = int(segment.find(fstartstring).text)
                frameend = int(segment.find(fendstring).text)
                annotationList.append(
                    [filename, f"Annotation {j}", framestart, frameend])
                j += 1
        return annotationList

    # Function to calculate gamma for inter-annotator agreement. Gamma closer to 1 = higher agreement
    def compute_gamma(self):
        annotationList = self.annotationList
        continuum = Continuum()  # add annotation data to continuum
        for x in annotationList:
            continuum.add(x[0], Segment(x[2], x[3]), '')
        dissim = PositionalSporadicDissimilarity(delta_empty=1.0)
        print('Starting Calculation')
        gamma_results = continuum.compute_gamma(
            dissim, precision_level=0.1, fast=True)  # output final gamma val
        # print(f"The gamma for that annotation is f{gamma_results.gamma}") old code
        return gamma_results.gamma
