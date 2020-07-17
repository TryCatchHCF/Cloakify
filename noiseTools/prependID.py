#!/usr/bin/python
# 
# Filename:  prependID.py
#
# Version: 1.0.1
#
# Author:  Joe Gervais (TryCatchHCF)
#
# Summary:  Inserts a randomized tag in front of each line of a file. Used to
# add noise to a cloaked file (see cloakify.py) in order to degrade frequency
# analysis attacks against the cloaked payload.
#
# Description:  
# Generates a random 4-character ID and prints it in front of each line of the
# file, in the form of "Tag:WXYZ". Modify the write statement below to tailor
# to your needs.
# 
# Example:  
#
#   $ ./prependID.py cloaked.txt > exfiltrateMe.txt
# 
#   Remove tag before trying to decloak the file
#
#   $ cat exfiltrateMe.txt | cut -d" " -f 2- > cloaked.txt
# Updated to Python3 by John Aho

import os, sys, getopt, codecs, random

arrayCode = list ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

if ( len(sys.argv) > 2 ):
	print("usage: prepend4digitID.py <exfilFilename>")
	print()
	print("Strip tag prior to decloaking the cloaked file.")
	print()
	exit

else:

	if ( len(sys.argv) == 1):

		i = 0
		while ( i<20 ):

			print( "Tag: " + 
				random.choice(arrayCode) + 
				random.choice(arrayCode) + 
				random.choice(arrayCode) + 
				random.choice(arrayCode))
			i = i+1

	else:
		with open( sys.argv[1] ) as file:
    			exfilFile = file.read().splitlines()

		with open( sys.argv[1], "w" ) as file:
			for i in exfilFile:
				if i != '\n':
					file.write( "Tag: " + 
						random.choice(arrayCode) + 
						random.choice(arrayCode) + 
						random.choice(arrayCode) + 
						random.choice(arrayCode) + 
						" " + i + "\n" )
