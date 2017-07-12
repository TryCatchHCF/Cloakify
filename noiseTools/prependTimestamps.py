#!/usr/bin/python
# 
# Filename:  prependTimestamps.py
#
# Version: 1.0.1
#
# Author:  Joe Gervais (TryCatchHCF)
#
# Summary:  Inserts datetimestamps in front of each line of a file. Used to 
# add noise to a cloaked file (see cloakify.py) in order to degrade frequency 
# analysis attacks against the cloaked payload.
#
# Description:  
# Takes current date and randomly subtracts 1011-1104 days to generate a 
# starting date. Then starts randomly incrementing the datetimestamp (between 
# 0-664 seconds) for each entry in the cloaked file. If the datetimestamp 
# reaches the current date, repeats the above steps to avoid generating 
# timestamps into the future.
#
# Example:  
#
#   $ ./prependTimestamps.py cloaked.txt > exfiltrateMe.txt
# 
#   Remove timestamps before trying to decloak the file
#
#   $ cat exfiltrateMe.txt | cut -d" " -f 3- > cloaked.txt
# Updated to Python3 by John Aho

import os, sys, getopt, datetime, random

minDaysBack = 1011
maxDaysBack = 1104

minSecondsStep = 0
maxSecondsStep = 664

if ( len(sys.argv) > 2 ):
	print "usage: prependTimestamps.py <cloakedFilename>"
	print
	print "Strip timestamps prior to decloaking the cloaked file."
	print
	exit

else:
	# Set the start date back around 2 years from today (give or take) for entropy range
	# Randomize a little for each run to avoid a pattern in the first line of each file

	today = datetime.date.today()
	startDate = today - datetime.timedelta(days=random.randint(minDaysBack,maxDaysBack))
	step = datetime.timedelta(seconds=random.randint(minSecondsStep,maxSecondsStep))
	t = datetime.time( random.randint(0,23),random.randint(0,59),random.randint(0,59) )
	fakeDate = datetime.datetime.combine( startDate, t )

	if ( len(sys.argv) == 1 ):
	# Generate sample of noise generator output
		i = 0;
		while (i<20):
			print( str( fakeDate ))
			step = datetime.timedelta(seconds=random.randint(minSecondsStep,maxSecondsStep))
			fakeDate += step
			i = i+1
		

	else:
	# Prepend noise generator output to file
		with open( sys.argv[1] ) as file:
    			cloakedFile = file.readlines()

		with open( sys.argv[1], "w" ) as file:
			for i in cloakedFile:
				file.write( str( fakeDate ) + " " + i )
				step = datetime.timedelta(seconds=random.randint(minSecondsStep,maxSecondsStep))
				fakeDate += step
				if fakeDate.date() > today:
					startDate = today - datetime.timedelta(days=random.randint(minDaysBack,maxDaysBack))
					fakeDate = datetime.datetime.combine( startDate, datetime.time( random.randint(0,23),random.randint(0,59),random.randint(0,59) ) )

