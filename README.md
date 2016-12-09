# Cloakify Factory
Cloakify Factory & Cloakify Toolset - Data Exfiltration In Plain Sight; Evade DLP/MLS Devices; Social Engineering of Analysts; Defeat Data Whitelisting Controls; Evade AV Detection. Text-based steganography usings lists. Convert any file type (e.g. executables, Office, Zip, images) into a list of everyday strings. Very simple tools, powerful concept, limited only by your imagination. 

# Author
Joe Gervais (TryCatchHCF)

# Why

DLP systems, MLS devices, and SecOps analysts know what data to look for: 
<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/payloadAcctSpreadsheet.png></img>
So transform that data into something they're <b>not</b> looking for: 
<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/CloakifyFactoryWorkflow.png></img>

#Tutorial
See my DEF CON 24 slides (included in project) from Crypto & Privacy Village workshop and DemoLabs session. Complete tutorial on what Cloakify can do, specific use cases, and more.

For a quick start, see the cleverly titled file "README_GETTING_STARTED.txt" in the project for a walkthrough of Cloakify Factory.

# Overview
Cloakify Factory transforms any filetype (e.g. .zip, .exe, .xls, etc.) into a list of harmless-looking strings. This lets you hide the file in plain sight, and transfer the file without triggering alerts. The fancy term for this is "text-based steganography", hiding data by making it look like other data. For example, you can transform a .zip file into a list of Pokemon creatures or Top 100 Websites. You then transfer the cloaked file however you choose, and then decloak the exfiltrated file back into its original form. 

This allows you to transfer data across a secure network’s perimeter without triggering alerts. You can also defeat data whitelisting controls - is there a security device that only allows IP addresses to leave a network? Turn your payload into IP addresses, problem solved. Additionaly, you can derail the security analyst’s review via social engineering attacks against their workflows. And as a final bonus, cloaked files defeat signature-based malware detection tools.

The pre-packaged ciphers are designed to appear like harmless / ignorable lists, though some (like MD5 password hashes) are specifically meant as distracting bait.

# Requires
Python 2.7.x

# Run Cloakify Factory: 
% ./cloakifyFactory.py

# Description
CloakifyFactory is a menu-driven tool that leverages Cloakify Toolset scripts. When you choose to Cloakify a file, the scripts  first Base64-encodes the payload, then apply a cipher to generate a list of strings that encodes the Base64 payload. You then transfer the file however you wish to its desired destination. Once exfiltrated, choose Decloakify with the same cipher to decode the payload.

NOTE: Cloakify is not a secure encryption scheme. It's vulnerable to frequency analysis attacks. Use the 'Add Noise' option to add entropy when cloaking a payload to help degrade frequency analysis attacks. Be sure to encrypt the file prior to cloaking if secrecy is needed.

The supporting scripts (cloakify.py and decloakify.py) can be use as standalone scripts. Very small, simple, clean, portable. For scenarios where infiltrating the full toolset is impractical, you can quickly type the standalone into a target’s local shell, generate a cipher in place, and cloakify -> exfiltrate.

Use py2exe if Windows target lacks Python. (http://www.py2exe.org/)

Prepackaged ciphers include lists of:
- Amphibians (scientific names)
- Belgian Beers
- Desserts in English, Arabic, Thai, Russian, Hindi, Chinese, Persian, and Muppet (Swedish Chef)
- Emoji
- evadeAV (smallest cipher space, x3 payload size)
- GeoCoords World Capitals (Lat/Lon)
- GeoCaching Coordinates (w/ Site Names)
- IPv4 Addresses of Popular Websites
- MD5 Password Hashes
- PokemonGo Monsters
- Ski Resorts
- Status Codes (generic)
- Star Trek characters
- Top 100 Websites
- World Beaches
- World Cup Teams

Prepackaged scripts for adding noise / entropy to your cloaked payloads:
- prependEmoji.py: Adds a randomize emoji to each line
- prependID.py: Adds a randomized ID tag to each line 
- prependLatLonCoords.py: Adds randomized LatLong coordinates to each line
- prependTimestamps.py: Adds timestamps (log file style) to each line

See comments script file for details on how to tailor the Noise Generators for your own needs

# Create Your Own Cipers

Cloakify Factory is at its best when you're using your own customized ciphers. The default ciphers may work for most needs, but in a unique exfiltration scenario you may need to build your own.

Creating a Cipher:
- Generate a list of at least 66 unique words / phrases / symbols (Unicode accepted)
- Remove all duplicate entries and all blank lines
- Randomize the list order
- Place in the "ciphers/" subdirectory
- Re-run CloakifyFactory and it will automatically load your new cipher as an option
- Test cloaking / decloaking with new cipher before using operationally

#Cloakify Example
<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/cloak.png></img>

#Decloakify Example
<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/decloak.png></img>

#Adding Entropy
Add noise to degrade frequency analysis attacks against your cloaked payloads. Here we use the 'pokemonGo' cipher, then use the 'prependLatLonCoords.py' script to generate random geocoords in a 10x10 mile grid. (Strip noise from file before decloaking.)
<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/pokemonGoExample.png></img>

#Sample Cipher Gallery

<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/Samples1.png></img>
<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/Samples2.png></img>
