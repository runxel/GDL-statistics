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

allCalledMacros = []


def readXML(file_path):
    """ Uses LXML to read an xml file and extract some CDATA. """
    # LXML is the only parser to work with CDATA
    # So let's instruct it to not strip it
    parser = etree.XMLParser(
        strip_cdata=False, resolve_entities=False, no_network=True)
    tree = etree.parse(file_path, parser)
    root = tree.getroot()

    xml_list = root.findall(".//MName")

    for i in xml_list:
        # Just put them all into one big list for now
        allCalledMacros.append(i.text)


def scantree(path):
    """ Recursively yield 'DirEntry' objects for given directory. """
    # os.walk is super slow, especially on windows, instead use os.scandir
    for entry in os.scandir(path):
        if entry.is_file() and entry.name == "calledmacros.xml":
            readXML(entry.path)
            yield entry.path
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)


for dir_ in os.scandir(PATH):
    # This is the preparation if I ever want to split 
    # the result by type, or exlude macros inside macros, or etc.
    list(scantree(dir_))


# Count the items
itemCount = Counter(allCalledMacros)
mostCommon = itemCount.most_common()

with open(os.path.join(pathToFile, 'ac24_all_macro_calls.txt'), 'w') as f:
    for item in mostCommon:
        f.write(f"{item[1]}\t\t{item[0]}\n")

#-----------------------------------------------------------------------------#
# perf time!
end_time = time.time()-start_time
print(f"Finished after {end_time:0.2f} seconds.")
