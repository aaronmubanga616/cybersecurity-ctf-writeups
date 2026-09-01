Encrypted password
       │
       ▼
password.enc
       │
       ▼
Connect to RSA Oracle
       │
       ▼
Request encryption of 2
       │
       ▼
Obtain 2^e mod n
       │
       ▼
Multiply with encrypted password
       │
       ▼
(2m)^e mod n
       │
       ▼
Send manipulated ciphertext
to decryption oracle
       │
       ▼
Receive 2m
       │
       ▼
Divide by 2
       │
       ▼
Recover original plaintext
       │
       ▼
Hexadecimal → ASCII
       │
       ▼
60f50
       │
       ▼
Use key with OpenSSL
       │
       ▼
Recover final flag

