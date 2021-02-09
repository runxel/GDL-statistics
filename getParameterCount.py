#!/usr/bin/env python3

__author__ = "Lucas Becker"
### tested and run with Python 3.7.3 on Windows 10

import os
import time
from lxml import etree

# Let's measure performance
start_time = time.time()

pathToFile = os.path.dirname(os.path.realpath(__file__))
PATH = os.path.join(pathToFile, "HSF 24")


#-----------------------------------------------------------------------------#

# List of all Parameter Types
allParTypes = [ "Length",
                "Integer",
                "String",
                "RealNum",
                "Boolean",
                "Angle",
                "PenColor",
                "FillPattern",
                "Material",
                "BuildingMaterial",
                "Dictionary"]


def readXML(file_path):
    """ Uses LXML to read an xml file and returns the parameter count.
    """
    parser = etree.XMLParser(
        strip_cdata=False, resolve_entities=False, no_network=True)
    tree = etree.parse(file_path, parser)
    root = tree.getroot()

    _pars = []

    for _pt in allParTypes:
        xml_list = root.findall(f".//{_pt}")
        _pars.append(len(xml_list))
    
    return sum(_pars)


def scantree(path):
    """ Recursively yield 'DirEntry' objects for given directory. """
    # os.walk is super slow, especially on windows, instead use os.scandir
    for entry in os.scandir(path):
        if entry.is_file() and entry.name == "paramlist.xml":
            sum = readXML(entry.path)
            yield os.path.basename(os.path.dirname(entry.path)), sum
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)


# MAIN:
parCount = list(scantree(PATH))

parCountSorted = reversed(sorted(parCount, key=lambda x: x[1]))

with open(os.path.join(pathToFile, 'ac24', 'ac24_parscount.txt'), 'w') as f:
    f.write("Objekt\t\tAnzahl der Parameter\n")
    f.write("=====================================\n")
    for item in parCountSorted:
        f.write(f"{item[0]}\t\t{item[1]}\n")

#-----------------------------------------------------------------------------#
# perf time!
end_time = time.time()-start_time
print(f"Finished after {end_time:0.2f} seconds.")
