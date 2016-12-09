#!/usr/bin/python
#
# Filename:  decloakify.py
#
# Author:  Joe Gervais (TryCatchHCF)
#
# Summary:  Exfiltration toolset (see cloakify.py) that transforms data into lists 
# of words / phrases / Unicode to ease exfiltration of data across monitored networks, 
# essentially hiding the data in plain sight, and facilitate social engineering attacks 
# against human analysts and their workflows. Bonus Feature: Defeats signature-based 
# malware detection tools (cloak your other tools).
#
# Used by cloakifyFactory.py, can be used as a standalone script as well (example below).
#
# Description:  Decodes the output of cloakify.py into its underlying Base64 format, 
# then does Base64 decoding to unpack the cloaked payload file. Requires the use of the 
# same cipher that was used to cloak the file prior to exfitration, of course.
#
# Prepackaged ciphers include: lists of desserts in English, Arabic, Thai, Russian, 
# Hindi, Chinese, Persian, and Muppet (Swedish Chef); Top 100 IP Addresses; GeoCoords of 
# World Capitols; MD5 Password Hashes; An Emoji cipher; Star Trek characters; Geocaching 
# Locations; Amphibians (Scientific Names); and evadeAV cipher, a simple cipher that 
# minimizes the size of the resulting obfuscated data.
# 
# Example:  
#
#   $ ./decloakify.py cloakedPayload.txt ciphers/desserts.ciph 


import sys, getopt, base64

array64 = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/+=")

def Decloakify( arg1, arg2, arg3 ):

	with open( arg1 ) as file:
    		listExfiltrated = file.readlines()

	with open( arg2) as file:
    		arrayCipher = file.readlines()

	clear64 = ""

	for word in listExfiltrated:
		clear64 +=  array64[ arrayCipher.index(word) ]

	if ( arg3 != "" ):
		with open( arg3, "w" ) as outFile:
			outFile.write( base64.b64decode( clear64 ))

	else:
		print base64.b64decode( clear64 ),


if __name__ == "__main__":
        if (len(sys.argv) != 3):
                print "usage: decloakify.py <cloakedFilename> <cipherFilename>"
                exit
	else:
        	Decloakify( sys.argv[1], sys.argv[2], "" )

