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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
import sys
import base64

array64 = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/+=")

if len(sys.argv) != 3:
	print("usage: decloakify.py <cloakedFilename> <cipherFilename>")
	exit()

else:
	with open(sys.argv[1]) as file:
		listExfiltrated = file.readlines()

	with open(sys.argv[2]) as file:
		arrayCipher = file.readlines()

	clear64 = ""

	for word in listExfiltrated:
		clear64 += array64[arrayCipher.index(word)]

	print(base64.b64decode(clear64).decode('utf-8'))
