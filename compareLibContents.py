#!/usr/bin/env python3

__author__ = "Lucas Becker"
### tested and run with Python 3.7.3 on Windows 10

import os
import time

# Let's measure performance
start_time = time.time()
VERSION = 24
pathToFile = os.path.dirname(os.path.realpath(__file__))
PATH_GER = os.path.join(pathToFile, f"ac{VERSION}", f"ac{VERSION}_total_list.txt")
PATH_CHE = os.path.join(pathToFile, f"ac{VERSION}_che", f"ac{VERSION}_che_total_list.txt")


#-----------------------------------------------------------------------------#

# Make two empty sets
german_objects = set()
swiss_objects = set()


with open(PATH_GER, encoding='utf-8') as file:
    for line in file:
        if ".gsm" in line:
            german_objects.add(line.strip())

with open(PATH_CHE, encoding='utf-8') as file:
    for line in file:
        if ".gsm" in line:
            swiss_objects.add(line.strip())

# Symmetric difference:
# diff_sym = german_objects.symmetric_difference(swiss_objects)
# Files that are in the German Library, but not in the Swiss
diff_in_ger = german_objects - swiss_objects
# Files that are in the Swiss Library, but not in the German
diff_in_che = swiss_objects - german_objects

# Sort the Set, so we get a nice alphabetical list.
diff_in_ger = sorted(diff_in_ger)
diff_in_che = sorted(diff_in_che)

with open(os.path.join(pathToFile, f"ac{VERSION}_che", f"ac{VERSION}_diff_inGER.txt"), 'w', encoding='utf-8') as f:
    for item in diff_in_ger:
        f.write(item)
        f.write("\n")

with open(os.path.join(pathToFile, f"ac{VERSION}_che", f"ac{VERSION}_diff_inCHE.txt"), 'w', encoding='utf-8') as f:
    for item in diff_in_che:
        f.write(item)
        f.write("\n")
        
#-----------------------------------------------------------------------------#
# perf time!
end_time = time.time()-start_time
print(f"Finished after {end_time:0.2f} seconds.")
