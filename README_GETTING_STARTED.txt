=======================  Using Cloakify Factory  =======================

            "Hide & Exfiltrate Any Filetype in Plain Sight"

                        Written by TryCatchHCF
                https://github.com/TryCatchHCF/Cloakify

Data Exfiltration In Plain Sight; Evade DLP/MLS Devices; Social Engineering
of Analysts; Defeat Data Whitelisting Controls; Evade AV Detection. Text-based
steganography usings lists. Convert any file type (e.g. executables, Office,
Zip, images) into a list of everyday strings. Very simple tools, powerful
concept, limited only by your imagination.

For background and full tutorial, see the presentation slides at Github
repository (above).

WHAT IT DOES:

Cloakify Factory transforms any filetype (e.g. .zip, .exe, .xls, etc.) into
a list of harmless-looking strings. This lets you hide the file in plain sight,
and transfer the file without triggering alerts. The fancy term for this is 
"text-based steganography", hiding data by making it look like other data.

For example, you can transform a .zip file into a list made of Pokemon creatures
or Top 100 Websites. You then transfer the cloaked file however you choose, 
and then decloak the exfiltrated file back into its original form. The ciphers 
are designed to appear like harmless / ignorable lists, though some (like MD5 
password hashes) are specifically meant as distracting bait.

REQUIRES:

- Python 2.7.x

BASIC USE:

Cloakify Factory will guide you through each step. Run the script, follow the 
prompts, and it will show you the way.

Run Cloakify Factory: 

% ./cloakifyFactory.py

Cloakify a Payload:
- Select 'Cloakify a File' (any filetype will work - zip, binaries, etc.)
- Enter filename that you want to Cloakify (can be filename or filepath)
- Enter filename that you want to save the cloaked file as
- Select the cipher you want to use
- Select a Noise Generator if desired
- Preview cloaked file if you want to check the results
- Transfer cloaked file via whatever method you prefer

Decloakify a Payload:
- Receive cloaked file via whatever method you prefer
- Select 'Decloakify a File'
- Enter filename of cloaked file (can be filename or filepath)
- Enter filename to save decloaked file to
- Preview cloaked file to review which Noise Generator and Cipher you used
- If Noise Generator was used, select matching Generator to remove noise
- Select the cipher used to cloak the file
- Your decloaked file is ready to go!

You can browse the ciphers and outputs of the Noise Generators to get an 
idea of how to cloak files for your own needs.

Anyone using the same cipher can decloak your cloaked file, but you can 
randomize (scramble) the preinstalled ciphers. See "randomizeCipherExample.txt"
in the Cloakify directory for an example.

NOTE: Cloakify is not a secure encryption scheme. It's vulnerable to 
frequency analysis attacks. Use the 'Add Noise' option to add entropy when 
cloaking a payload to help degrade frequency analysis attacks. Be sure to 
encrypt the file prior to cloaking if secrecy is needed.

=================  About Cloakify Exfiltration Toolset  =================

The Cloakify Exfiltration Toolset is a collection of Python scripts to 
cloak / uncloak any file type using list-based ciphers (text-based 
steganography). Allows you to transfer data across a secure network's 
perimeter without triggering alerts, defeating data whitelisting
controls, and derailing analyst's review via social engineering attacks
against their workflows. As a bonus, cloaked files defeat signature-based
malware detection tools.

NOTE: Cloakify is not a secure encryption scheme. It's vulnerable to 
frequency analysis attacks. Use the 'Add Noise' option to add entropy when 
cloaking a payload to help degrade frequency analysis attacks. Be sure to 
encrypt the file prior to cloaking if secrecy is needed.

DETAILS:

Cloakify first Base64-encodes the payload, then applies a cipher to generate
a list of strings that encodes the Base64 payload. Once exfiltrated, use
Decloakify with the same cipher to decode the payload. The ciphers are
designed to appear like harmless / ignorable lists, though some (like MD5
password hashes) are specifically meant as distracting bait.

Prepackaged ciphers include lists of:

- Amphibians (scientific names)
- Belgian Beers
- Desserts in English, Arabic, Thai, Russian, Hindi, Chinese, Persian, and
  Muppet (Swedish Chef)
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

- prependEmoji.py: Adds a randomized emoji to each line
- prependID.py: Adds a randomized ID tag to each line
- prependLatLonCoords.py: Adds random LatLong coordinates to each line
- prependTimestamps.py: Adds timestamps (log file style) to each line

CREATE YOUR OWN CIPHERS:

Cloakify Factory is at its best when you're using your own customized
ciphers. The default ciphers may work for most needs, but in a unique
exfiltration scenario you may need to build your own.

Creating a Cipher:

- Create a list of at least 66 unique words/phrases/symbols (Unicode accepted)
- Randomize the list order
- Remove all duplicate entries and all blank lines
- Place cipher file in the 'ciphers/' subdirectory
- Re-run Cloakify Factory to automatically load the new cipher 
- Test cloaking / decloaking with new cipher before using operationally

