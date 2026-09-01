RSA Oracle — Cryptography CTF Write-Up

Platform: picoCTF
Challenge: RSA Oracle
Category: Cryptography
Difficulty: Medium
Environment: Kali Linux
Primary Language: Python 3
Key Technologies: RSA, modular arithmetic, chosen-ciphertext attack, Pwntools, OpenSSL, hexadecimal encoding

Overview

The RSA Oracle challenge is a cryptography-based Capture The Flag problem that demonstrates a practical weakness in the use of textbook RSA encryption without appropriate padding. The challenge provides access to a remote RSA oracle that allows users to encrypt and decrypt selected values. The objective is to abuse this functionality to recover information about an encrypted secret without directly knowing the RSA private key.

The challenge instance was accessed remotely through titan.picoctf.net on port 59353. The service presented two operations: encrypt and decrypt. By interacting with the service and observing how RSA encryption and decryption behaved, I identified that the oracle could be exploited using RSA's multiplicative property.

The key idea was to submit the encryption of the value 2, combine that ciphertext with the encrypted secret, and then send the resulting ciphertext to the decryption oracle. Because textbook RSA is multiplicatively homomorphic, decrypting the manipulated ciphertext produces 2 × m, where m is the original plaintext. Dividing the resulting value by 2 therefore recovers the original encrypted secret value.

Initial Reconnaissance

I first connected directly to the challenge instance using Netcat:

nc titan.picoctf.net 59353

The remote service displayed an interface asking what operation should be performed:

what should we do for you?
E → encrypt D → decrypt.

I initially interacted with the encryption functionality manually to understand how the oracle operated. I supplied a test value and observed that the service returned both the hexadecimal representation of the plaintext and the RSA ciphertext.

For example, encrypting:

12345678900987

produced the hexadecimal representation:

3132333435363738393030393837

and the service subsequently returned a large RSA ciphertext.

This confirmed that the service was performing standard RSA operations on an integer representation of the supplied plaintext.

Understanding the RSA Operation

The oracle was effectively performing the standard RSA operations:

Encryption:

c = m^e mod n

and:

Decryption:

m = c^d mod n

where m is the plaintext represented as an integer, c is the ciphertext, e is the public exponent, d is the private exponent, and n is the RSA modulus.

The important property for this challenge is that textbook RSA is multiplicatively homomorphic.

If:

c1 = m1^e mod n

and:

c2 = m2^e mod n

then multiplying the ciphertexts gives:

c1 × c2 mod n

which decrypts to:

m1 × m2 mod n

This property provided the vulnerability needed to attack the oracle.

Identifying the Oracle Vulnerability

The encrypted secret was stored in password.enc as a large integer. Instead of attempting to factor the RSA modulus or recover the private key, I looked for a way to manipulate the ciphertext using the encryption and decryption functionality provided by the server.

The approach was to ask the oracle to encrypt the value:

2

The server returned the RSA encryption of 2:

2^e mod n

I then multiplied this value by the ciphertext contained in password.enc.

If the original encrypted password is:

c = m^e mod n

and the oracle gives us:

c2 = 2^e mod n

we can calculate:

c' = c × c2 mod n

which is equivalent to:

c' = m^e × 2^e mod n

Using the properties of exponents:

c' = (2m)^e mod n

Therefore, when the modified ciphertext is submitted to the decryption oracle:

D(c') = 2m

The original plaintext can then be recovered simply by dividing the result by 2.

Automating the Attack with Python

After confirming the behavior manually, I created a Python script using Pwntools to automate communication with the remote service.

The script established a connection to:

titan.picoctf.net:59353

and interacted with the oracle programmatically.

The important part of the script was obtaining the encryption of 2:

payload = b'E' + b'\n'
connection.send(payload)

response = connection.recvuntil(b'keysize:')

After determining the required input format, I supplied 2 to the encryption service and received its RSA ciphertext.

The script then read the encrypted value from password.enc and multiplied it by the ciphertext corresponding to 2, as shown in the analysis:

num = int(response.decode()) * 2336150584734702647514724021470643922433811330098144930425570297739084758922591855204953033

The resulting value was then sent to the decryption functionality of the oracle. The script was specifically designed around the mathematical relationship:

Decrypt(Encrypt(2) × Encrypt(m))
    =
Decrypt(Encrypt(2m))
    =
2m

The script and terminal output demonstrate the complete interaction with the remote oracle.

Recovering the Secret

After sending the manipulated ciphertext to the oracle, the service returned the decrypted value.

The important output was:

decrypted ciphertext as hex (c ^ d mod n):
6c60cc6a60

The manipulated plaintext represented 2 × m, so the next step was to divide the value by 2 before interpreting the original message.

The resulting hexadecimal representation was:

3630663530

This hexadecimal value represents an ASCII string.

Converting the hexadecimal bytes:

36 → 6
30 → 0
66 → f
35 → 5
30 → 0

produced:

60f50

This value was the recovered password/key needed to decrypt the final secret.enc file. The terminal evidence shows the recovered value being used as the OpenSSL decryption key.

Decrypting the Final Secret

After recovering the key:

60f50

I used OpenSSL to decrypt the AES-encrypted secret.enc file.

The command used was:

openssl enc -aes-256-cbc -d -in secret.enc -k 60f50

OpenSSL successfully decrypted the file and returned the final picoCTF flag:

picoCTF{su((3ss_(r0ck1ng_r3a_60f50766}

The successful decryption and recovered flag are shown in the final terminal output.

Check md Attack Chain 


Why the Attack Worked

The fundamental vulnerability was the use of raw textbook RSA in an environment where an attacker could submit arbitrary ciphertexts to a decryption oracle.

RSA encryption has the multiplicative property:

E(m1) × E(m2) mod n = E(m1 × m2)

Therefore, an attacker does not need to know the private key to manipulate an encrypted message in a mathematically predictable way.

In this challenge, encrypting 2 gave me a valid RSA ciphertext corresponding to 2. Multiplying that ciphertext with the encrypted password produced a ciphertext representing 2m. The decryption oracle then unknowingly revealed 2m, allowing the original plaintext to be recovered.

This is why the attack is commonly described as a chosen-ciphertext attack against a vulnerable RSA implementation.

Tools and Technologies

The primary operating environment for the challenge was Kali Linux, which provided the command-line environment used for networking, scripting, file analysis, and cryptographic operations.

Python 3 was used to automate the interaction with the remote oracle. Pwntools provided the networking functionality required to establish the connection and communicate with the challenge service programmatically. The remote service was accessed using Netcat during the initial manual investigation.

OpenSSL was used during the final stage to decrypt the AES-256-CBC encrypted secret.enc file after the RSA oracle attack recovered the required key.

The cryptographic concepts involved were RSA encryption/decryption, modular arithmetic, RSA's multiplicative homomorphism, chosen-ciphertext attacks, hexadecimal encoding, ASCII conversion, and AES-256-CBC decryption.

Skills Demonstrated

This challenge demonstrated practical skills in cryptographic vulnerability analysis, RSA mathematics, chosen-ciphertext exploitation, Python scripting, network communication, Linux command-line usage, hexadecimal analysis, and file decryption.

A particularly important skill demonstrated was the ability to move beyond simply identifying the encryption algorithm and instead analyze how the implementation could be abused. Rather than attempting to break RSA through factorization, I recognized that the exposed encryption/decryption oracle itself provided the attack primitive required to manipulate the ciphertext.

The challenge also demonstrated the ability to combine multiple tools and techniques into a complete attack chain: Netcat for reconnaissance, Python and Pwntools for automation, mathematical analysis for the RSA attack, and OpenSSL for the final decryption stage.

Lessons Learned

The main lesson from this challenge was that the security of a cryptographic algorithm depends heavily on how it is implemented and exposed, not simply on the strength of the underlying mathematics.

RSA itself was not "broken" during the challenge. Instead, the vulnerability came from allowing an attacker to submit chosen ciphertexts to a decryption oracle while using textbook RSA without appropriate protections. The mathematical properties of raw RSA allowed the ciphertext to be manipulated in a predictable way.

This challenge reinforced the importance of understanding mathematical properties of cryptographic algorithms and recognizing when those properties become vulnerabilities in real-world implementations.

It also demonstrated why modern RSA encryption should use secure padding schemes such as RSA-OAEP, rather than directly applying RSA mathematics to plaintext values.

Final Flag
picoCTF{su((3ss_(r0ck1ng_r3a_60f50766}

