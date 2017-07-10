#!/usr/bin/python
# 
# Filename:  removeNoise.py
#
# Version: 1.0.0
#
# Author:  Joe Gervais (TryCatchHCF)
#
# Summary:  Removes random noise that has been prepended to a cloaked file
# (see cloakify.py). 
#
# Description:  
# Read in the noise-enhanced cloaked file and reprint each line without the
# prepended noise.
# 
# Example:  
#
#   $ ./removeNoise.py 2 noisyCloaked.txt cloaked.txt

import os, sys, getopt

if ( len(sys.argv) != 4 ):
	print("usage: removeNoise.py <numberOfColumnsToStrip> <noisyFilename> <outputFile>")
	print()
	exit

else:
	numberOfColumnsToStrip = int( sys.argv[1] )

	with open( sys.argv[2] ) as file:
    		noisyFile = file.readlines()
		file.close()

	with open( sys.argv[3], "w" ) as file:
		for line in noisyFile:
			if line != '\n':
				file.write( ' '.join(line.split(' ')[numberOfColumnsToStrip:]))
		file.close()
