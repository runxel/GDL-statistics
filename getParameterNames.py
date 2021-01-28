#!/usr/bin/env python3

__author__ = "Lucas Becker"
### tested and run with Python 3.7.3 on Windows 10

import os
import time
from lxml import etree
from collections import Counter

# Let's measure performance
start_time = time.time()

pathToFile = os.path.dirname(os.path.realpath(__file__))
PATH = os.path.join(pathToFile, "HSF 24")


#-----------------------------------------------------------------------------#

# This is a list of all Parameter Types
# Dicts are not checked, they are uninteresting,
# since they can't be set in the paramlist anyway
allParTypes = [ "Length",
                "Integer",
                "String",
                "Boolean",
                "PenColor",
                "FillPattern",
                "Material",
                "RealNum",
                "Angle",
                "BuildingMaterial"]



def readXML(file_path, parType):
    """ Uses LXML to read an xml file and returns the parameter names
        corresponding to the `parType` var.
    """
    parser = etree.XMLParser(
        strip_cdata=False, resolve_entities=False, no_network=True)
    tree = etree.parse(file_path, parser)
    root = tree.getroot()

    xml_list = root.findall(f".//{parType}")

    for i in xml_list:
        # Just put them all into one big list for now
        allPars.append(i.get("Name"))


def scantree(path, parType):
    """ Recursively yield 'DirEntry' objects for given directory. """
    # os.walk is super slow, especially on windows, instead use os.scandir
    for entry in os.scandir(path):
        if entry.is_file() and entry.name == "paramlist.xml":
            readXML(entry.path, parType)
            yield entry.path
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path, parType)


# MAIN:
for parType in allParTypes:
    for dir_ in os.scandir(PATH):
        allPars = []
        _nameParts = dir_.name.split(" ")
        dir_name = _nameParts[1].lower()
        dir_num = _nameParts[0][0]
        if dir_name != "macros":
            # Macros duplicate the parameters of the other files
            # so don't check them
            list(scantree(dir_, parType))    # creating a list will ask for the results at once

            # Count the items
            itemCount = Counter(allPars)
            mostCommon = itemCount.most_common()  # lists all
            
            with open(os.path.join(pathToFile, f'ac24_pars_{parType.lower()}_{dir_num}_{dir_name}.txt'), 'w') as f:
                for item in mostCommon:
                    f.write(f"{item[1]}\t\t{item[0]}\n")

#-----------------------------------------------------------------------------#
# perf time!
end_time = time.time()-start_time
print(f"Finished after {end_time:0.2f} seconds.")
