#!/usr/bin/python
# 
# Filename:  prependLatLonCoords.py
#
# Version: 1.0.0
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

if ( len(sys.argv) != 2 ):
	print "usage: prependLatLonCoords.py <cloakedFilename>"
	print
	print "Strip the coordinates prior to decloaking the cloaked file."
	print
	exit

else:
	with open( sys.argv[1] ) as file:
    		cloakedFile = file.readlines()

	# Geocoords for Denver, USA. Replace with whatever is best for your needs
	baseLat = 39.739236
	baseLon = -104.990251

	# AT LATITUDE 40 DEGREES (NORTH OR SOUTH)
	# One minute of latitude =    1.85 km or 1.15 mi
	# One minute of longitude =   1.42 km or 0.88 mi

	sizeLat = 0.0002
	sizeLon = 0.0002

	# Generate a random with enough range to look good, scale with vals above

	for i in cloakedFile:
		lat = baseLat + (sizeLat * random.randint(0,2000))
		lon = baseLon + (sizeLon * random.randint(0,2000))

		print lat, lon, i,

