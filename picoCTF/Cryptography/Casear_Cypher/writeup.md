New Caesar — Cryptography CTF Write-Up

Platform: picoCTF 2021
Challenge: New Caesar
Category: Cryptography
Difficulty: Medium
Environment: Kali Linux
Primary Language: Python 3

Overview

The New Caesar challenge is a cryptography problem from picoCTF 2021 that involves breaking a custom encryption scheme based on the principles of a Caesar cipher. The challenge presents an encrypted string and provides hints indicating that the cipher does not operate using the conventional 26-letter alphabet. The objective was to analyze the encryption mechanism, determine the appropriate transformation, reverse the encoding process, and ultimately recover the hidden message.

The challenge description states that a new type of encryption has been discovered and asks the player to break the secret code. The provided hints were particularly important because they indicated that the alphabet size was different from the standard 26-character English alphabet and that, despite the letters being split apart, the same underlying paradigms still applied.

Challenge Analysis

The initial ciphertext provided by the challenge was:

cbdabldadbzlblzdzdzezczcczzczx

Rather than attempting to decode the entire string manually, I first analyzed the encryption as a variation of the Caesar cipher. A traditional Caesar cipher shifts characters through the alphabet by a fixed number of positions. However, the first hint suggested that the alphabet used by this challenge was not the standard 26-character alphabet, which indicated that the encryption process was likely using a modified character mapping.

To identify the transformation, I used Python to iterate through the possible Caesar shifts. Instead of manually testing each shift, I wrote a short Python command that applied every possible shift to the ciphertext and printed the resulting strings. This allowed me to quickly compare the outputs and identify the transformation that produced a meaningful intermediate value.

The Python analysis produced a series of possible transformations. The relevant transformation appeared at shift 23, producing:

gfhefphehfdpfpdhdhdidgdggddgdb

This was an important breakthrough because the resulting text was clearly structured differently from the original ciphertext and provided the next stage of the decoding process.

Understanding the Custom Encoding

At this point, the output was not yet readable plaintext. Instead, I analyzed the structure of the resulting string:

gfhefphehfdpfpdhdhdidgdggddgdb

The second challenge hint indicated that although the characters were split up, the same paradigms still applied. This suggested that the characters should be processed in groups rather than treated as one continuous string.

I therefore divided the transformed ciphertext into two-character groups:

gf he fp he hf dp fp dh dh id gd gg dd gd db

This revealed that the encrypted data was effectively representing a sequence of two-character values.

The next step was to determine how these character pairs represented hexadecimal data.

Custom Base16 Mapping

The key observation was that the challenge uses a custom Base16 alphabet rather than the normal hexadecimal characters 0–9 and a–f.

The mapping identified during the analysis was:

a → 0
b → 1
c → 2
d → 3
e → 4
f → 5
g → 6
h → 7
i → 8
j → 9
k → a
l → b
m → c
n → d
o → e
p → f

In other words, the characters from a through p represent the hexadecimal values 0 through f.

Applying this mapping to the two-character groups transformed the encoded data into hexadecimal values:

65 74 5f 74 75 3f 5f 37 37 83 63 66 33 63 31

This was another major step in the solution because the data now had the structure of hexadecimal byte values.

Hexadecimal to ASCII

The final decoding stage involved interpreting the hexadecimal values as ASCII characters.

For example, the first values demonstrate the conversion:

65 → e
74 → t
5f → _
74 → t
75 → u

This confirmed that the hexadecimal interpretation was correct because the values corresponded to recognizable ASCII characters.

The complete transformation can therefore be represented as:

Original Ciphertext
        ↓
Caesar Cipher Analysis
        ↓
Determine Shift
        ↓
Shifted Ciphertext
        ↓
Split Characters into Pairs
        ↓
Custom Base16 Mapping
        ↓
Hexadecimal Values
        ↓
Hex → ASCII
        ↓
Decoded Message

This decoding architecture was also documented separately during the investigation.

Python Automation

To make the Caesar cipher analysis faster and more reliable, I used Python to automate the process of testing the possible shifts. The script iterated through the alphabet and calculated the shifted character for each position rather than requiring every possible transformation to be performed manually.

A simplified version of the analysis script is:

import string

ciphertext = "cbdabldadbzlblzdzdzezczcczzczx"
alphabet = string.ascii_lowercase

for shift in range(26):
    decoded = ""

    for character in ciphertext:
        index = alphabet.index(character)
        decoded += alphabet[(index - shift) % 26]

    print(shift, decoded)

This approach allowed all possible Caesar transformations to be examined efficiently. The output was then analyzed to identify the transformation that produced the meaningful intermediate ciphertext.

Technical Approach

The solution relied primarily on cryptographic analysis, pattern recognition, encoding identification, and scripting. The first stage involved recognizing that the challenge was based on the Caesar cipher concept. The second stage involved identifying the correct transformation through automated testing. Once the intermediate ciphertext was obtained, the repeated two-character structure provided an indication that the characters represented encoded hexadecimal values.

The unusual alphabet was then identified as a custom Base16 representation in which the letters a through p correspond to hexadecimal values 0 through f. Converting these character pairs into hexadecimal bytes exposed the final layer of the challenge, which could then be interpreted using ASCII encoding.

This made the challenge less about brute-forcing a conventional Caesar cipher and more about understanding how multiple encoding layers were combined.

Tools and Technologies

The primary operating environment used during the investigation was Kali Linux, which provided the terminal environment and security-focused tooling used to perform the analysis. Python 3 was used to automate the Caesar cipher transformations and reduce the amount of manual testing required.

The challenge itself was hosted on picoCTF, and the analysis relied on fundamental cryptographic concepts including Caesar substitution, custom Base16 encoding, hexadecimal representation, and ASCII decoding.

The main technologies and concepts demonstrated in this challenge were Python 3, Kali Linux, command-line analysis, cryptography, Caesar cipher analysis, hexadecimal encoding, ASCII encoding, character mapping, pattern recognition, and CTF problem solving.

Key Findings

The most significant discovery was that the challenge was not using a standard Caesar cipher workflow. The encryption contained multiple stages, requiring the ciphertext to be transformed before it could be interpreted as hexadecimal data.

The important sequence was the identification of the Caesar transformation, followed by the discovery that the transformed output needed to be split into pairs. Those pairs could then be interpreted using the custom mapping from a-p to hexadecimal 0-f. The resulting hexadecimal values could finally be converted into ASCII characters.

This demonstrated the importance of not assuming that a ciphertext uses a standard encoding simply because it resembles a familiar cipher. Understanding the hints and examining the structure of the output were essential to identifying the additional encoding layer.

Skills Demonstrated

This challenge provided practical experience in cryptographic analysis and reverse-engineering of custom encoding schemes. It also demonstrated the use of Python for automating repetitive cryptographic operations and Kali Linux for conducting command-line security investigations.

The challenge specifically strengthened my ability to analyze substitution ciphers, identify patterns in encoded data, work with hexadecimal and ASCII representations, interpret custom character mappings, automate analysis with Python, and approach unfamiliar encryption mechanisms systematically.

Evidence and Documentation

The solution process was documented using terminal output and analysis screenshots. These provide evidence of the transformation from the original ciphertext through the Caesar analysis, character-pair separation, custom Base16 conversion, and hexadecimal-to-ASCII interpretation.

The accompanying architecture diagram documents the complete decoding pipeline from the original encrypted data to the final decoded text.

Conclusion

The New Caesar challenge demonstrated how a seemingly simple Caesar cipher can be combined with additional encoding techniques to create a more complex cryptographic puzzle. The solution required identifying the Caesar transformation, analyzing the resulting character structure, recognizing the custom Base16 alphabet, converting the encoded pairs into hexadecimal, and finally interpreting the hexadecimal representation as ASCII.

The main lesson from the challenge was that effective cryptographic analysis requires examining the data at every stage rather than assuming that the first recognizable cipher is the only layer involved. Automating the initial Caesar analysis with Python significantly reduced the amount of manual work and made it possible to systematically investigate the available transformations.

Overall, this challenge provided practical experience with cryptography, encoding analysis, Python scripting, Linux command-line tools, pattern recognition, and structured CTF methodology.

