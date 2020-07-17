#!/usr/bin/python
# 
# Filename:  cloakify.py 
#
# Version: 1.1.1
#
# Author:  Joe Gervais (TryCatchHCF)
#
# Summary:  Exfiltration toolset (see decloakify.py) that transforms any filetype (binaries,
# archives, images, etc.) into lists of words / phrases / Unicode to ease exfiltration of 
# data across monitored networks, hiding the data in plain sight. Also facilitates social 
# engineering attacks against human analysts and their workflows. Bonus Feature: Defeats 
# signature-based malware detection tools (cloak your other tools during an engagement).
#
# Used by cloakifyFactory.py, can be used as a standalone script as well (example below).
#
# Description:  Base64-encodes the given payload and translates the output using a list 
# of words/phrases/Unicode provided in the cipher. This is NOT a secure encryption tool, 
# the output is vulnerable to frequency analysis attacks. Use the Noise Generator scripts
# to add entropy to your cloaked file. You should encrypt the file before cloaking if
# secrecy is needed.
#
# Prepackaged ciphers include: lists of desserts in English, Arabic, Thai, Russian, 
# Hindi, Chinese, Persian, and Muppet (Swedish Chef); PokemonGo creatures; Top 100 IP 
# Addresses; Top Websites; GeoCoords of World Capitols; MD5 Password Hashes; An Emoji 
# cipher; Star Trek characters; Geocaching Locations; Amphibians (Scientific Names); 
# evadeAV cipher (simple cipher that minimizes size of the resulting obfuscated data).
#
# To create your own cipher:
#
#	- Generate a list of at least 66 unique words (Unicode-16 accepted)
#	- Remove all duplicate entries and blank lines
# 	- Randomize the list (see 'randomizeCipherExample.txt' in Cloakify directory)
#	- Provide the file as the cipher argument to the script.
#	- ProTip: Place your cipher in the "ciphers/" directory and cloakifyFactory 
#	  will pick it up automatically as a new cipher
# 
# Example:  
#
#   $ ./cloakify.py payload.txt ciphers/desserts > exfiltrate.txt
# 
# Updated to Python3 by John Aho

import os, sys, getopt, base64

array64 = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/+=")

def Cloakify( arg1, arg2, arg3 ):

	payloadFile = open( arg1, 'rb' )
	payloadRaw = payloadFile.read()
	payloadB64 = base64.encodebytes( payloadRaw)

	try:
		with open( arg2 ) as file:
    			cipherArray = file.readlines()
	except:
		print("")
		print("!!! Oh noes! Problem reading cipher '", arg2, "'")
		print("!!! Verify the location of the cipher file" )
		print("")

	if ( arg3 != "" ):
		try:
			with open( arg3, "w+" ) as outFile:
				for char2 in payloadB64:
					char = chr(char2)
					if char != '\n':
						outFile.write( cipherArray[ array64.index(char) ] )
		except Exception as ex:
			print("")
			print("!!! Oh noes! Problem opening or writing to file '", arg3, "'", ex)
			print("")
	else:
		for char in payloadB64:
			if char != '\n':
				print( cipherArray[ array64.index(char) ],)


if __name__ == "__main__":
	if ( len(sys.argv) != 3 ):
		print("usage: cloakify.py <payloadFilename> <cipherFilename>")
		exit

	else:
		Cloakify( sys.argv[1], sys.argv[2], "" )

