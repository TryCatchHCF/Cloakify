#!/usr/bin/python
# 
# Filename:  prependEmoji.py 
#
# Version: 1.0.0
#
# Author:  Joe Gervais (TryCatchHCF)
#
# Summary: Inserts a random emoji in front of each line in a file. Used to 
# add noise to a cloaked file (see cloakify.py) in order to degrade frequency 
# analysis attacks against the cloaked payload. Works well with the emoji 
# cipher.
# 
#
# Description:  
# 
# Example:  
#
#   $ ./prependEmoji.py exfiltrate.txt > exfiltrateNew.txt
# 
#   Remove prepended emoji before trying to decloak the file
# Updated to Python3 by John Aho

import os, sys, getopt, random

if ( len(sys.argv) > 2 ):
	print("usage: prependEmoji.py <exfilFilename>")
	print()
	print("Strip leading emoji prior to decloaking the cloaked file.")
	print()
	exit

else:

	# FIX PENDING - Relative pathing is for cloakifyFactory.py
	with open( "ciphers/emoji" ) as file:
		arrayCipher = file.read().splitlines()

	if ( len(sys.argv) == 1):
	# Generate sample of noise generator output
		i = 0
		while ( i<20 ):
			print( random.choice(arrayCipher) + "\n" ),
			i = i+1

	else:
	# Prepend noise generator output to file
		with open ( sys.argv[1] ) as file:
			cloakedFile = file.readlines()
	
		with open ( sys.argv[1], "w" ) as file:
			for i in cloakedFile:
				file.write( random.choice(arrayCipher) + "  " + i ),

