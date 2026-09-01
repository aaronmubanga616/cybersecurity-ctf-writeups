# New Caesar

**Platform:** picoCTF 2021  
**Category:** Cryptography  
**Difficulty:** Medium

## Overview

New Caesar is a cryptography challenge involving a custom
Caesar-style transformation combined with a non-standard
Base16 encoding.

## Solution Summary

I analyzed the ciphertext using Python to identify the
Caesar transformation. The resulting ciphertext was split
into character pairs and decoded using a custom `a-p → 0-f`
mapping. The resulting hexadecimal values were then
converted to ASCII to obtain the decoded message.

## Tools & Technologies

Python 3 · Kali Linux · Cryptography · Hexadecimal · ASCII

## Skills Demonstrated

Cryptanalysis, Python scripting, pattern recognition,
encoding/decoding, and Linux command-line analysis.

## Detailed Write-Up

[Read the full technical write-up](writeup.md)