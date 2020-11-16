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

def removeNoise(numberOfColumnsToStrip:str, noisyCloakedPath:str, outputPath:str):
	numberOfColumnsToStrip = int(numberOfColumnsToStrip)

	with open(noisyCloakedPath, encoding="utf-8") as noisyFile, open(outputPath, "w", encoding="utf-8") as outputFile:
		for line in noisyFile:
			if line != "\n":
				outputFile.write( ' '.join(line.split(' ')[numberOfColumnsToStrip:]))


if __name__ == "__main__":
	if len(sys.argv) != 4 :
		print("usage: removeNoise.py <numberOfColumnsToStrip> <noisyFilename> <outputFile>")
		exit(-1)
