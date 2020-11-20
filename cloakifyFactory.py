#!/usr/bin/python
# 
# Filename:  cloakifyFactory.py 
#
# Version: 1.0.1
#
# Author:  Joe Gervais (TryCatchHCF)
#
# Summary:  Cloakify Factory is part of the Cloakify Exfiltration toolset that transforms 
# any fileype into lists of words / phrases / Unicode to ease exfiltration of data across 
# monitored networks, defeat data whitelisting restrictions, hiding the data in plain 
# sight, and facilitates social engineering attacks against human analysts and their 
# workflows. Bonus Feature: Defeats signature-based malware detection tools (cloak your 
# other tools). Leverages other scripts of the Cloakify Exfiltration Toolset, including
# cloakify.py, decloakify.py, and the noise generator scripts.
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
# 	- Randomize the list
#	- Place in the 'ciphers/' subdirectory
#	- Relaunch cloakifyFactory and it will automatically detect the new cipher
# 
# Example:  
#
#   $ ./cloakifyFactory.py 
# 

# Standard Python Libraries
import base64
from getpass import getpass
import os
import random
import sys

# Local Python Imports
import cloakify
import decloakify
from removeNoise import removeNoise
from noiseTools import *

# Dictionary to map the file selection options to the corresponding folder
NOISE_GENERATOR = 0
CIPHER = 1
optionFolders = {
	NOISE_GENERATOR: "noiseTools",
	CIPHER: "ciphers"
}
noiseFuncs = {
	"prependEmoji.py": prependEmoji,
	"prependID.py": prependID,
	"prependLatLonCoords.py": prependLatLonCoords,
	"prependTimestamps.py": prependTimestamps
}

# Load list of ciphers
gCipherFiles = next(os.walk("./ciphers/"))[2]

# Load list of noise generators
gNoiseScripts = []
for root, dirs, files in os.walk( "./noiseTools" ):
	for file in files:
		if file.endswith('.py') and "__init__" not in file:
			gNoiseScripts.append(os.path.basename(file))


def CloakifyFile():
	print("")
	print("====  Cloakify a File  ====")
	print("")
	sourceFile = input("Enter filename to cloak (e.g. ImADolphin.exe or /foo/bar.zip): ")
	print("")
	cloakedFile = input("Save cloaked data to filename (default: 'tempList.txt'): ")

	if cloakedFile == "":
		cloakedFile = "tempList.txt"

	cipherPath = SelectFile(gCipherFiles, CIPHER)

	choice = input("Add noise to cloaked file? (y/n): ")
	if choice == "y":
		noisePath = SelectFile(gNoiseScripts, NOISE_GENERATOR)
	else:
		noisePath = None
	
	choice = input("Protect cloaked file with a password: (y/n): ")
	password = None
	if choice == "y":
		password = getPassword(True)

	print("")
	print(f"Creating cloaked file using cipher: {cipherPath}")

	try:
		cloakify.Cloakify(sourceFile, os.path.join(".", "ciphers", cipherPath), cloakedFile, password)
	except:
		print("")
		print("!!! Well that didn't go well. Verify that your cipher is in the 'ciphers/' subdirectory.")
		print("")

	if noisePath:
		print(f"Adding noise to cloaked file using noise generator: {noisePath}")
		try:
			noiseFuncs[noisePath](cloakedFile)
		except:
			print("")
			print("!!! Well that didn't go well. Verify that '", cloakedFile, "'")
			print("!!! is in the current working directory or try again giving full filepath.") 
			print("")

	print("")
	print("Cloaked file saved to:", cloakedFile)
	print("")

	choice = input( "Preview cloaked file? (y/n): " )
	if choice == "y":
		print("")
		with open(cloakedFile, encoding="utf-8") as file:
			for _ in range(20):
				print(file.readline())
		print("")

	choice = input( "Press return to continue... " )


def DecloakifyFile():

	decloakTempFile = "decloakTempFile.txt"

	print("")
	print("====  Decloakify a Cloaked File  ====")
	print("")
	sourceFile = input("Enter filename to decloakify (e.g. /foo/bar/MyBoringList.txt): ")
	print("")
	decloakedFile = input("Save decloaked data to filename (default: 'decloaked.file'): ")
	print("")

	if decloakedFile == "":
		decloakedFile = "decloaked.file"

	# Reviewing the cloaked file within cloakifyFactory will save a little time for those who
	# forgot the format of the cloaked file and don't want to hop into a new window just to look

	choice = input("Preview cloaked file? (y/n default=n): ")

	if choice == "y":
		print("")
		try:
			with open(sourceFile, encoding="utf-8") as file:
				for _ in range(20):
					print(file.readline())
			print("")
		except:
			print("")
			print("!!! Well that didn't go well. Verify that '", sourceFile, "'")
			print("!!! is in the current working directory or the filepath you gave.")
			print("")
		
	choice = input("Was noise added to the cloaked file? (y/n default=n): ")

	if choice == "y":
		noisePath = SelectFile(gNoiseScripts, NOISE_GENERATOR)

		stripColumns = 2

		# No upper bound checking, relies on SelectNoise() returning valid value, fix in next release
		try:
			# Remove Noise, overwrite the source file with the stripped contents
			print(f"Removing noise from cloaked file.")
			removeNoise(stripColumns, sourceFile, decloakTempFile)

			# Copy decloak temp filename to sourceFile so that Decloakify() gets the right filename
			sourceFile = decloakTempFile
		except:
			print("!!! Error while removing noise from file.\n")

	cipherPath = SelectFile(gCipherFiles, CIPHER)

	choice = input("Was a password used for this file? (y/n default=n): ")

	password = None
	if choice == "y":
		password = getPassword()

	print(f"Decloaking file using cipher: {cipherPath}")

	# Call Decloakify()
	try:
		decloakify.Decloakify(sourceFile, os.path.join(".", "ciphers", cipherPath), decloakedFile, password)

		print("")
		print(f"Decloaked file {sourceFile}, saved to {decloakedFile}")
	except:
		print("")
		print("!!! Oh noes! Error decloaking file (did you select the same cipher it was cloaked with?)")
		print("")

	try:
		os.remove(decloakTempFile)
	except:
		print("")
		print("!!! Oh noes! Error while deleting temporary file:", decloakTempFile)
		print("")

	choice = input("Press return to continue... ")


def SelectFile(files:list, option:str):
	print("")
	print(f"{option}:")
	print("")
	for fileCount, fileName in enumerate(files, start=1):
		print(f"{fileCount}-{fileName}")
	print("")

	selection = -1
	while not(0 <= selection <= (fileCount-1)):
		try:
			fileNum = input(f"Enter {option} #: " )

			selection = int (fileNum) - 1
			if not(0 <= selection <= (fileCount-1)):
				print(f"Invalid {option} number, try again...")	
		except ValueError:
			print(f"Invalid {option} number, try again...")
	print("")
	if option == NOISE_GENERATOR:
		print(gNoiseScripts[selection])
		print(noiseFuncs[gNoiseScripts[selection]])
	return files[selection] if option == CIPHER else gNoiseScripts[selection]


def BrowseFiles(files:list, option:str):
	print("")
	print(f"========  Preview {option}  ========")
	filePath = SelectFile(files, option)
	print(f"=====  {option}: {filePath} =====")
	print("")

	try:
		if option == NOISE_GENERATOR:
			print(f"Sample output of prepended strings, using noise generator: {filePath}\n")
			noiseFuncs[filePath](None)
		else:
			filePath = os.path.join(".", optionFolders[option], filePath)
			with open(filePath, encoding="utf-8") as file:
				cipher = file.read()
				print(cipher)
	except:
		print(f"!!! Error opening {option} file.\n")

	choice = input( "Press return to continue... " )


def getPassword(confirm=False):
	password = getpass(prompt="Enter password: ")

	if confirm:
		confirm_password = getpass(prompt="Confirm password: ")

		while password != confirm_password:
			print("Passwords do not match...please retry")
			password = getpass(prompt="Enter password: ")
			confirm_password = getpass(prompt="Confirm password: ")
		
	return password


def Help():
	print("")
	print("=====================  Using Cloakify Factory  =====================")
	print("")
	print("For background and full tutorial, see the presentation slides at")
	print("https://github.com/TryCatchHCF/Cloakify")
	print("")
	print("WHAT IT DOES:")
	print("")
	print("Cloakify Factory transforms any filetype (e.g. .zip, .exe, .xls, etc.) into")
	print("a list of harmless-looking strings. This lets you hide the file in plain sight,")
	print("and transfer the file without triggering alerts. The fancy term for this is")
	print("'text-based steganography', hiding data by making it look like other data.")
	print("")
	print("For example, you can transform a .zip file into a list made of Pokemon creatures")
	print("or Top 100 Websites. You then transfer the cloaked file however you choose,")
	print("and then decloak the exfiltrated file back into its original form. The ciphers")
	print("are designed to appear like harmless / ignorable lists, though some (like MD5")
	print("password hashes) are specifically meant as distracting bait.")
	print("")
	print("BASIC USE:")
	print("")
	print("Cloakify Factory will guide you through each step. Follow the prompts and")
	print("it will show you the way.")
	print("")
	print("Cloakify a Payload:")
	print("- Select 'Cloakify a File' (any filetype will work - zip, binaries, etc.)")
	print("- Enter filename that you want to Cloakify (can be filename or filepath)")
	print("- Enter filename that you want to save the cloaked file as")
	print("- Select the cipher you want to use")
	print("- Select a Noise Generator if desired")
	print("- Preview cloaked file if you want to check the results")
	print("- Transfer cloaked file via whatever method you prefer")
	print("")
	print("Decloakify a Payload:")
	print("- Receive cloaked file via whatever method you prefer")
	print("- Select 'Decloakify a File'")
	print("- Enter filename of cloaked file (can be filename or filepath)")
	print("- Enter filename to save decloaked file to")
	print("- Preview cloaked file to review which Noise Generator and Cipher you used")
	print("- If Noise Generator was used, select matching Generator to remove noise")
	print("- Select the cipher used to cloak the file")
	print("- Your decloaked file is ready to go!")
	print("")
	print("You can browse the ciphers and outputs of the Noise Generators to get")
	print("an idea of how to cloak files for your own needs.")
	print("")
	print("Anyone using the same cipher can decloak your cloaked file, but you can")
	print("randomize (scramble) the preinstalled ciphers. See 'randomizeCipherExample.txt'")
	print("in the Cloakify directory for an example.")
	print("")
	print("NOTE: Cloakify is not a secure encryption scheme. It's vulnerable to")
	print("frequency analysis attacks. Use the 'Add Noise' option to add entropy when")
	print("cloaking a payload to help degrade frequency analysis attacks. Be sure to")
	print("encrypt the file prior to cloaking if secrecy is needed.")

def About():
	print("")
	print("=====================  About Cloakify Factory  =====================")
	print("")
	print("            \"Hide & Exfiltrate Any Filetype in Plain Sight\"")
	print("")
	print("                        Written by TryCatchHCF")
	print("                https://github.com/TryCatchHCF/Cloakify")
	print("")
	print("Data Exfiltration In Plain Sight; Evade DLP/MLS Devices; Social Engineering")
	print("of Analysts; Defeat Data Whitelisting Controls; Evade AV Detection. Text-based")
	print("steganography usings lists. Convert any file type (e.g. executables, Office,")
	print("Zip, images) into a list of everyday strings. Very simple tools, powerful")
	print("concept, limited only by your imagination.")
	print("")
	print("Cloakify Factory uses Python scripts to cloak / uncloak any file type using")
	print("list-based ciphers (text-based steganography). Allows you to transfer data")
	print("across a secure network's perimeter without triggering alerts, defeating data")
	print("whitelisting controls, and derailing analyst's review via social engineering")
	print("attacks against their workflows. As a bonus, cloaked files defeat signature-")
	print("based malware detection tools.")
	print("")
	print("NOTE: Cloakify is not a secure encryption scheme. It's vulnerable to")
	print("frequency analysis attacks. Use the 'Add Noise' option to add entropy when")
	print("cloaking a payload to help degrade frequency analysis attacks. Be sure to")
	print("encrypt the file prior to cloaking if secrecy is needed.")
	print("")
	print("DETAILS:")
	print("")
	print("Cloakify first Base64-encodes the payload, then applies a cipher to generate")
	print("a list of strings that encodes the Base64 payload. Once exfiltrated, use")
	print("Decloakify with the same cipher to decode the payload. The ciphers are")
	print("designed to appear like harmless / ingorable lists, though some (like MD5")
	print("password hashes) are specifically meant as distracting bait.")
	print("")
	print("Prepackaged ciphers include lists of:")
	print("")
	print("- Amphibians (scientific names)")
	print("- Belgian Beers")
	print("- Desserts in English, Arabic, Thai, Russian, Hindi, Chinese, Persian, and")
	print("  Muppet (Swedish Chef)")
	print("- Emoji")
	print("- evadeAV (smallest cipher space, x3 payload size)")
	print("- GeoCoords World Capitals (Lat/Lon)")
	print("- GeoCaching Coordinates (w/ Site Names)")
	print("- IPv4 Addresses of Popular Websites")
	print("- MD5 Password Hashes")
	print("- PokemonGo Monsters")
	print("- Top 100 Websites")
	print("- Ski Resorts")
	print("- Status Codes (generic)")
	print("- Star Trek characters")
	print("- World Beaches")
	print("- World Cup Teams")
	print("")
	print("Prepackaged scripts for adding noise / entropy to your cloaked payloads:")
	print("")
	print("- prependEmoji.py: Adds a randomized emoji to each line")
	print("- prependID.py: Adds a randomized ID tag to each line")
	print("- prependLatLonCoords.py: Adds random LatLong coordinates to each line")
	print("- prependTimestamps.py: Adds timestamps (log file style) to each line")
	print("")
	print("CREATE YOUR OWN CIPHERS:")
	print("")
	print("Cloakify Factory is at its best when you're using your own customized")
	print("ciphers. The default ciphers may work for most needs, but in a unique")
	print("exfiltration scenario you may need to build your own.")
	print("")
	print("Creating a Cipher:")
	print("")
	print("- Create a list of at least 66 unique words/phrases/symbols (Unicode accepted)")
	print("- Randomize the list order")
	print("- Remove all duplicate entries and all blank lines")
	print("- Place cipher file in the 'ciphers/' subdirectory")
	print("- Re-run Cloakify Factory to automatically load the new cipher")
	print("- Test cloaking / decloaking with new cipher before using operationally")
	print("")
	
def MainMenu():

	print("  ____ _             _    _  __        ______         _                   ")
	print(" / __ \ |           | |  |_|/ _|       |  ___|       | |                  ")
	print("| /  \/ | ___   __ _| | ___| |_ _   _  | |_ __ _  ___| |_ ___  _ __ _   _ ")
	print("| |   | |/ _ \ / _` | |/ / |  _| | | | |  _/ _` |/ __| __/ _ \| '__| | | |")
	print("| \__/\ | |_| | |_| |   <| | | | |_| | | || |_| | |__| || |_| | |  | |_| |")
	print(" \____/_|\___/ \__,_|_|\_\_|_|  \__, | \_| \__,_|\___|\__\___/|_|   \__, |")
	print("                                 __/ |                               __/ |")
	print("                                |___/                               |___/ ")
	print("")
	print("             \"Hide & Exfiltrate Any Filetype in Plain Sight\"")
	print("")
	print("                         Written by TryCatchHCF")
	print("                     https://github.com/TryCatchHCF")
	print("  (\~---.")
	print("  /   (\-`-/)")
	print(" (      ' '  )         data.xls image.jpg  \\     List of emoji, IP addresses,")
	print("  \ (  \_Y_/\\    ImADolphin.exe backup.zip  -->  sports teams, desserts,")
	print("   \"\"\ \___//         LoadMe.war file.doc  /     beers, anything you imagine")
	print("      `w   \"")   

	selectionErrorMsg = "1-7 are your options. Try again."

	while True: 
		try:
			print("")
			print("====  Cloakify Factory Main Menu  ====")
			print("")
			print("1) Cloakify a File")
			print("2) Decloakify a File")
			print("3) Browse Ciphers")
			print("4) Browse Noise Generators")
			print("5) Help / Basic Usage")
			print("6) About Cloakify Factory")
			print("7) Exit")
			print("")
		
			choice = int(input( "Selection: "))
		
			if choice == 1:
				CloakifyFile()
			elif choice == 2:
				DecloakifyFile()
			elif choice == 3:
				BrowseFiles(gCipherFiles, CIPHER)
			elif choice == 4:
				BrowseFiles(gNoiseScripts, NOISE_GENERATOR)
			elif choice == 5:
				Help()
			elif choice == 6:
				About()
			elif choice == 7:
				break
			else:
				print(selectionErrorMsg)
		except ValueError:
			print(selectionErrorMsg)
	
	byeArray = ("Bye!", "Ciao!", "Adios!", "Aloha!", "Hei hei!", "Bless bless!", "Hej da!", "Tschuss!", "Adieu!", "Cheers!")

	print("")
	print(random.choice( byeArray ))
	print("")


if __name__ == "__main__":
	MainMenu()
