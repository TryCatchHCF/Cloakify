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

import os, sys, getopt, datetime, random

MIN_DAYS_BACK = 1011
MAX_DAYS_BACK = 1104

MIN_SECONDS_STEP = 0
MAX_SECONDS_STEP = 664


TODAY = datetime.date.today()
START_DATE = TODAY - datetime.timedelta(days=random.randint(MIN_DAYS_BACK, MAX_DAYS_BACK))
STEP = datetime.timedelta(seconds=random.randint(MIN_SECONDS_STEP, MAX_SECONDS_STEP))
T = datetime.time( random.randint(0,23),random.randint(0,59),random.randint(0,59) )


def prependTimestamps(cloakedFilename:str):
	fakeDate = datetime.datetime.combine(START_DATE, T)
	if cloakedFilename:
		# Prepend noise generator output to file
		with open(cloakedFilename, encoding="utf-8") as file:
			cloakedFile = file.readlines()
	
		with open(cloakedFilename, "w", encoding="utf-8") as file:
			for line in cloakedFile:
				file.write(f"{fakeDate} {line}"),
				step = datetime.timedelta(seconds=random.randint(MIN_SECONDS_STEP, MAX_SECONDS_STEP))
				fakeDate += step
	else:
		# Generate sample of noise generator output
		for _ in range(20):
			print(f"{fakeDate}")
			step = datetime.timedelta(seconds=random.randint(MIN_SECONDS_STEP, MAX_SECONDS_STEP))
			fakeDate += step


if __name__ == "__main__":
	if len(sys.argv) == 2:
		prependTimestamps(sys.argv[1])
	else:
		print("usage: prependTimestamps.py <exfilFilename>")
		print()
		print("Strip leading timestamps prior to decloaking the cloaked file.")
		print()


