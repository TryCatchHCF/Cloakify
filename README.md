# Cloakify
Cloakify Toolset - Data Exfiltration In Plain Sight; Evade DLP/MLS Devices; Social Engineering of Analysts; Evade AV Detection. Text-based steganography usings lists. Convert any file type (e.g. executables, Office, Zip, images) into a list of strings. Very simple tools, powerful concept, limited only by your imagination. 

# Author
Joe Gervais (TryCatchHCF)

# Why

DLP systems, MLS devices, and SecOps analysts know what data to look for: 
<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/payloadExample.png></img>
So transform that data into something they're <b>not</b> looking for: 
<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/cloakedExample.png></img>

# Description
Python scripts to cloak / uncloak payloads using list-based ciphers
(text-based steganography). Allows you to transfer data across a secure
network’s perimeter without triggering alerts, defeating data
whitelisting controls, and derailing analyst’s review via social
engineering attacks against their workflows. As a bonus, cloaked files
defeat signature-based malware detection tools.

Cloakify first Base64-encodes the payload, then applies a cipher to
generate a list of strings that encodes the Base64 payload. Once
exfiltrated, use Decloakify with the same cipher to decode the payload.

Not a secure encryption scheme (vulnerable to frequency analysis
attacks). Encrypt data separately prior to processing to keep secure
(if needed).

Very small, simple, clean, portable - written in Python. Can quickly
type into a target’s local shell session if needed.

Use py2exe if Windows target lacks Python. (http://www.py2exe.org/)

Prepackaged ciphers include lists of:
- Desserts in English, Arabic, Thai, Russian, Hindi, Chinese, Persian,
and Muppet (Swedish Chef)
- IPv4 Addresses of Popular Websites
- GeoCoords World Capitals (Lat/Lon)
- MD5 Password Hashes
- Emoji
- Amphibians (scientific names)
- GeoCaching Coordinates (w/ Site Names)
- Star Trek characters
- evadeAV (smallest cipher space - x3 payload size - purely to evade AV detection)

# To create your own cipher
- Generate a list of at least 66 unique words / phrases / symbols (Unicode accepted)
- Randomize the list order
- Remove all duplicate entries and all blank lines

Pass the new file as the cipher argument to cloakify / decloakify

#Cloakify Example
<pre>
$ cat payload.txt
The FBI just filed a motion to delay Tuesday's hearing in the San
Bernardino iPhone case, claiming that an "outside party" may be able to
help it break into the phone without Apple's help. The motion comes
after weeks of escalation tension in the case with Apple, the FBI, and
other stakeholders arguing the case in public before it reached courts.
It's not clear who is helping the FBI or what the new method entails,
but it may not be coming from the NSA, despite speculation that the
intelligence agency has the ability up its sleeve; today's filing
suggests that the help is coming from "outside the US government."
$ ./cloakify.py payload.txt ciphers/desserts.ciph > cloaked.txt
$ head cloaked.txt
streusel
biscuits
flower
marionberry
puffs
buttermilk
terrine
eggs
muffins
snickerdoodles
$
</pre>

#Decloakify Example
<pre>
$ head cloaked.txt
streusel
biscuits
flower
marionberry
puffs
buttermilk
terrine
eggs
muffins
snickerdoodles
$ ./decloakify.py cloaked.txt ciphers/desserts.ciph
The FBI just filed a motion to delay Tuesday's hearing in the San
Bernardino iPhone case, claiming that an "outside party" may be able to
help it break into the phone without Apple's help. The motion comes
after weeks of escalation tension in the case with Apple, the FBI, and
other stakeholders arguing the case in public before it reached courts.
It's not clear who is helping the FBI or what the new method entails,
but it may not be coming from the NSA, despite speculation that the
intelligence agency has the ability up its sleeve; today's filing
suggests that the help is coming from "outside the US government."
$
</pre>

# Cipher Gallery

<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/Samples1.png></img>
<img src=https://github.com/TryCatchHCF/Cloakify/blob/master/screenshots/Samples2.png></img>
