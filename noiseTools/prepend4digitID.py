#!/usr/bin/python
# 
# Filename:  prepend4digitID.py
#
# Version: 1.0.0
#
# Author:  Joe Gervais (TryCatchHCF)
#
# Summary:  
#
# Description:  
# 
# Example:  
#
#   $ ./prepend4digitID.py exfiltrate.txt > exfiltrateNew.txt
# 

import os, sys, getopt, codecs, random

arrayCode = list ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

if ( len(sys.argv) != 2 ):
	print "usage: prepend4digitID.py <exfilFilename>"
	exit

else:
	with open( sys.argv[1] ) as file:
    		exfilFile = file.read().splitlines()

	for i in exfilFile:
		if i != '\n':
			print 'Tag:%c%c%c%c %s' % (random.choice(arrayCode),random.choice(arrayCode),random.choice(arrayCode),random.choice(arrayCode),i)
