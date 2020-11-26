#!/usr/bin/python
# 
# Filename:  cloakify.py 
#
# Version: 1.1.0
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

import base64
import os
import random
import sys

array64 = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/+=")

def Cloakify(payloadPath:str, cipherPath:str, outputPath:str="", password:str=None):
	"""Payload file's binary contents will be read and converted into base64.
	Cipher file will be read into a list that will be used for the payload's obfuscation.
	If an output path is defined the obfuscated content will be written to that otherwise,
	it will print it out to the console.

	Args:
		payloadPath (str): Path to the file that will be encoded
		cipherPath (str): Path to the file used as the base64 cipher
		outputPath (str): Path to write out the obfuscated payload
	"""

	try:
		with open(payloadPath, 'rb') as payloadFile:
			payloadRaw = payloadFile.read()
			payloadB64 = base64.encodebytes(payloadRaw)
			payloadB64 = payloadB64.decode("ascii").replace("\n", "")
	except Exception as e:
		print("Error reading payload file {}: {}".format(payloadPath, e))

	payloadOrdering = None
	if password:
		random.seed(password)
		# Get a list of each line number in the cloaked file
		payloadOrdering = [i for i in range(len(payloadB64))]
		# Shuffle the order of the lines
		random.shuffle(payloadOrdering)

	try:
		with open(cipherPath, encoding="utf-8") as file:
			cipherArray = file.readlines()
	except Exception as e:
		print("Error reading cipher file {}: {}".format(cipherPath, e))

	if outputPath:
		try:
			with open(outputPath, "w+", encoding="utf-8") as outFile:
				if payloadOrdering:
					# Iterate through the randomized line order and write each line to the file
					for randomLoc in payloadOrdering:
						outFile.write(cipherArray[array64.index(payloadB64[randomLoc])])
				else:
					for char in payloadB64:
						outFile.write(cipherArray[array64.index(char)])
		except Exception as e:
			print("Error writing to output file {}: {}".format(outputPath, e))

	else:
		for char in payloadB64:
			print(cipherArray[array64.index(char)].strip())


if __name__ == "__main__":
	if len(sys.argv) == 3:
		Cloakify( sys.argv[1], sys.argv[2])
	elif len(sys.argv) == 4:
		Cloakify(sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		print("usage: cloakify.py <payloadFilename> <cipherFilename> <outputFileName-optional>")
		exit(-1)
