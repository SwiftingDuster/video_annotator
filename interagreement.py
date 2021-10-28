# interagreement.py defines functions to
import os
import xml.etree.ElementTree as ET

from pyannote.core import Segment
from pygamma_agreement import Continuum, PositionalSporadicDissimilarity

# .compute_gamma() to calculate inter-annotator agreement
# .parse_xml_files() to return list of annotations

class InterAgreement:
    """Helper class to calculate Inter Annotator Agreement"""

    @staticmethod
    def parse_xml_files(xml_files):
        """
        Parse xml files to suitable format for calculation, return list of elements of ["file name", frame start, frame end]
        """
        annotations = []
        fstartstring = 'start'
        fendstring = 'end'
        for i, file in enumerate(xml_files):
            tree = ET.parse(file)
            filename = os.path.basename(file)
            for segment in tree.iter("segment"):
                framestart = int(segment.find(fstartstring).text)
                frameend = int(segment.find(fendstring).text)
                annotations.append(
                    [filename, f"Annotation {i + 1}", framestart, frameend])
        return annotations

    # Calculate gamma for inter-annotator agreement. Gamma closer to 1 = higher agreement
    @staticmethod
    def compute_gamma(xml_files):
        """
        Compute inter annotator agreement for two or more XML annotation data.

        :param xml_files: List of xml file paths.
        """

        annotations = InterAgreement.parse_xml_files(xml_files)
        continuum = Continuum()
        # add annotation data to continuum
        for x in annotations:
            continuum.add(x[0], Segment(x[2], x[3]), '')
        dissim = PositionalSporadicDissimilarity(delta_empty=1.0)
        print('Starting Calculation')
        gamma_results = continuum.compute_gamma(
            dissim, precision_level=0.1, fast=True)  # output final gamma val
        return gamma_results.gamma
