# RSA Oracle — picoCTF

A cryptography challenge from **picoCTF** involving a vulnerable RSA implementation and a decryption oracle. The objective was to exploit the mathematical properties of textbook RSA to recover a secret value and use it to decrypt the final encrypted file.

## Challenge Information

**Platform:** picoCTF  
**Challenge:** RSA Oracle  
**Category:** Cryptography  
**Difficulty:** Medium  
**Environment:** Kali Linux  
**Language:** Python 3

## Overview

The challenge provided access to a remote RSA oracle capable of encrypting and decrypting values. During the investigation, I identified that the service was vulnerable to a **chosen-ciphertext attack** because it exposed raw RSA encryption and decryption operations without appropriate padding protection.

Rather than attempting to factor the RSA modulus or recover the private key, I exploited the multiplicative property of textbook RSA. I requested the encryption of the value `2`, combined the resulting ciphertext with the encrypted secret, and submitted the manipulated ciphertext to the decryption oracle.

Because RSA is multiplicatively homomorphic:

```text
E(m) × E(2) mod n = E(2m)

