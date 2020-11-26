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

import os, sys, getopt, codecs, random

arrayCode = list ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")


def prependID(cloakedFilename:str):
	if cloakedFilename:
		# Prepend noise generator output to file
		with open(cloakedFilename, encoding="utf-8") as file:
			cloakedFile = file.readlines()
	
		with open(cloakedFilename, "w", encoding="utf-8") as file:
			for line in cloakedFile:
				file.write(f"Tag: {random.choice(arrayCode)}{random.choice(arrayCode)}{random.choice(arrayCode)}{random.choice(arrayCode)} {line}"),
	else:
		# Generate sample of noise generator output
		for _ in range(20):
			print(f"Tag: {random.choice(arrayCode)}{random.choice(arrayCode)}{random.choice(arrayCode)}{random.choice(arrayCode)}")


if __name__ == "__main__":
	if len(sys.argv) == 2:
		prependID(sys.argv[1])
	else:
		print("usage: prependID.py <exfilFilename>")
		print()
		print("Strip leading ID prior to decloaking the cloaked file.")
		print()

