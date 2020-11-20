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

import base64
import random
import sys

array64 = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/+=")

def Decloakify(cloakedPath:str, cipherPath:str, outputPath:str="", password:str=""):
	"""Cipher file will be read into a list that will be used for the payload's deobfuscation.
	Cloaked file's contents will be read in line by line mapping the line to a base64 character.
	If an output path is defined the base64 contents will be decoded and written to the output
	file otherwise it will be written to the console.

	Args:
		cloakedPath (str): Path to the file that is encoded
		cipherPath (str): Path to the file used as the base64 cipher
		outputPath (str): Path to write out the decoded
	"""
	with open(cipherPath, encoding="utf-8") as file:
		arrayCipher = file.readlines()
	
	clear64 = ""
	with open(cloakedPath, encoding="utf-8") as file:
		if password:
			random.seed(password)
			lines = file.readlines()
			# Get a list of each line number in the cloaked file
			decodeOrdering = [i for i in range(len(lines))]
			# Shuffle the order of the lines to what they were during encoding
			random.shuffle(decodeOrdering)
			# Map the index of the original payload to the index in the cloaked file
			decodeOrdering = {k: v for v, k in enumerate(decodeOrdering)}
			# Iterate through the proper line order and reconstruct the unshuffled base64 payload
			for i in range(len(lines)):
				clear64 += array64[arrayCipher.index(lines[decodeOrdering[i]])]
		else:
			for line in file:
				clear64 +=  array64[arrayCipher.index(line)]

	payload = base64.b64decode(clear64)
	if outputPath:
		with open(outputPath, "wb") as outFile:
			outFile.write(payload)
	else:
		print(payload)


if __name__ == "__main__":
	if len(sys.argv) == 3:
		Decloakify(sys.argv[1], sys.argv[2])
	elif len(sys.argv) == 4:
		Decloakify(sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		print("usage: decloakify.py <cloakedFilename> <cipherFilename> <outputFileName-optional>")
		exit(-1)
