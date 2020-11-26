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

import os, sys, getopt, random


def prependEmoji(cloakedFilename, emojiCipherPath="ciphers/emoji"):
	with open(emojiCipherPath, encoding="utf-8") as file:
		arrayCipher = file.read().splitlines()

	if cloakedFilename:
		# Prepend noise generator output to file
		with open(cloakedFilename, encoding="utf-8") as file:
			cloakedFile = file.readlines()
	
		with open(cloakedFilename, "w", encoding="utf-8") as file:
			for line in cloakedFile:
				file.write(f"{random.choice(arrayCipher)} {line}"),
	else:
		# Generate sample of noise generator output
		for _ in range(20):
			print(random.choice(arrayCipher))


if __name__ == "__main__":
	if len(sys.argv) == 2:
		emojiCipherPath = os.path.abspath(os.path.join("../", "ciphers", "emoji"))
		prependEmoji(sys.argv[1], emojiCipherPath)
	else:
		print("usage: prependEmoji.py <exfilFilename>")
		print()
		print("Strip leading emoji prior to decloaking the cloaked file.")
		print()

