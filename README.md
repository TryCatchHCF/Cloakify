# Cloakify
Cloakify Toolset - Data Exfiltration In Plain Sight; Evade DLP/MLS Devices; Social Engineering of Analysts; Evade AV Detection. Text-based steganography usings lists. Convert any file type (e.g. executables, Office, Zip, images) into a list of everyday strings. Very simple tools, powerful concept, limited only by your imagination. 

# Author
Joe Gervais (TryCatchHCF)

# Why

DLP systems, MLS devices, and SecOps analysts know what data to look for: 
<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/payloadAcctSpreadsheet.png></img>
So transform that data into something they're <b>not</b> looking for: 
<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/cloakedAcctSpreadsheet.png></img>

#Tutorial
See my DEF CON 24 slides (included in project) from Crypto & Privacy Village workshop and DemoLabs session. Complete tutorial on what Cloakify can do, specific use cases, and more.

# Description
Python scripts to cloak / uncloak any file type using list-based ciphers
(text-based steganography). Allows you to transfer data across a secure
network’s perimeter without triggering alerts, defeating data
whitelisting controls, and derailing analyst’s review via social
engineering attacks against their workflows. As a bonus, cloaked files
defeat signature-based malware detection tools.

Cloakify first Base64-encodes the payload, then applies a cipher to
generate a list of strings that encodes the Base64 payload. Once
exfiltrated, use Decloakify with the same cipher to decode the payload.

Not a secure encryption scheme (vulnerable to frequency analysis
attacks, use 'noiseTools' scripts to add entropy). Encrypt data separately 
prior to processing to keep secure (if needed).

Very small, simple, clean, portable - written in Python. Can quickly
type into a target’s local shell session if needed.

Use py2exe if Windows target lacks Python. (http://www.py2exe.org/)

Prepackaged ciphers include lists of:
- Desserts in English, Arabic, Thai, Russian, Hindi, Chinese, Persian,
and Muppet (Swedish Chef)
- IPv4 Addresses of Popular Websites
- GeoCoords World Capitals (Lat/Lon)
- PokemonGo Monsters
- MD5 Password Hashes
- Emoji
- World Cup Teams
- Belgian Beers
- Ski Resorts
- World Beaches
- Amphibians (scientific names)
- GeoCaching Coordinates (w/ Site Names)
- Star Trek characters
- evadeAV (smallest cipher space - x3 payload size - purely to evade AV detection)

Prepackaged scripts for adding noise / entropy to your cloaked payloads:
- prependID.py: Adds a randomized ID tag to front of each line 
- prependLatLonCoords.py: Adds randomized LatLong coordinates to front of each line
- prependTimestamps.py: Adds timestamps (log file style) to front of each line

See script comments for details on how to tailor the output for your own needs

# To create your own cipher
- Generate a list of at least 66 unique words / phrases / symbols (Unicode accepted)
- Randomize the list order
- Remove all duplicate entries and all blank lines

Pass the new file as the cipher argument to cloakify / decloakify

#Cloakify Example
<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/cloak.png></img>

#Decloakify Example
<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/decloak.png></img>

#Adding Entropy
Add noise to degrade frequency analysis attacks against your cloaked payloads. Here we use the 'pokemonGo' cipher, then use the 'prependLatLonCoords.py' script to generate random geocoords in a 10x10 mile grid. (Strip noise from file before decloaking.)
<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/pokemonGoNoise.png></img>

#Sample Cipher Gallery

<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/Samples1.png></img>
<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/Samples2.png></img>
