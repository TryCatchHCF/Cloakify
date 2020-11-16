#!/usr/bin/python
# 
# Filename:  prependLatLonCoords.py
#
# Version: 1.0.1
#
# Author:  Joe Gervais (TryCatchHCF)
#
# Summary:  Inserts random Lat/Lon coordinates in front of each line of a file. 
# Used to add noise to a cloaked file (see cloakify.py) in order to degrade 
# frequency analysis attacks against the cloaked payload.
#
# Description:  
# Uses a bounding rectangle to generate random lat/lon coordinate pairs and
# insert them in the front of each line in a file. Defaults to Denver, with a 
# bounding rectangle roughly 10 miles / 16km per side (varies with latitude, 
# because sphere.
#
# Example:  
#
#   $ ./prependLatLonCoords.py cloaked.txt > exfiltrateMe.txt
# 
#   Remove coordinate pairs before trying to decloak the file
#
#   $ cat exfiltrateMe.txt | cut -d" " -f 3- > cloaked.txt


import os, sys, getopt, random

# Geocoords for Denver, USA. Replace with whatever is best for your needs
BASE_LAT = 39.739236
BASE_LON = -104.990251

# AT LATITUDE 40 DEGREES (NORTH OR SOUTH)
# One minute of latitude =    1.85 km or 1.15 mi
# One minute of longitude =   1.42 km or 0.88 mi
SIZE_LAT = 0.0002
SIZE_LON = 0.0002


def prependLatLonCoords(cloakedFilename:str):
	if cloakedFilename:
		# Prepend noise generator output to file
		with open(cloakedFilename, encoding="utf-8") as file:
			cloakedFile = file.readlines()
	
		with open(cloakedFilename, "w", encoding="utf-8") as file:
			for line in cloakedFile:
				lat = BASE_LAT + (SIZE_LAT * random.randint(0,2000))
				lon = BASE_LON + (SIZE_LON * random.randint(0,2000))
				file.write(f"{lat} {lon} {line}"),
	else:
		# Generate sample of noise generator output
		for _ in range(20):
			lat = BASE_LAT + (SIZE_LAT * random.randint(0,2000))
			lon = BASE_LON + (SIZE_LON * random.randint(0,2000))
			print(f"{lat} {lon}")


if __name__ == "__main__":
	if len(sys.argv) == 2:
		prependLatLonCoords(sys.argv[1])
	else:
		print("usage: prependLatLonCoords.py <exfilFilename>")
		print()
		print("Strip leading coordinates prior to decloaking the cloaked file.")
		print()

