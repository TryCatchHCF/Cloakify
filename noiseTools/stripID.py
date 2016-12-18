#!/usr/bin/python
#
# Filename:  stripID.py
#
# Version: 1.0.0
#

# Summary:  remove timestamps implemented in <prependID.py>
#
# Description:
# Regex to find prepended information
#
# Example:
#
#   $ ./noiseTools/stripID.py sample_out_prepended.txt > strippedFile.txt

import re
import sys

pattern = re.compile("Tag:[A-z,0-9]{4}")

if(len(sys.argv) !=  2):
    print "usage: decloakify.py <prependedCloackedFilename>"
    exit

else:
    for i, line in enumerate(open(sys.argv[1])):
        for match in re.finditer(pattern, line):
            foo = re.sub(pattern, '',line)
            foo = foo.lstrip()
            print foo,
