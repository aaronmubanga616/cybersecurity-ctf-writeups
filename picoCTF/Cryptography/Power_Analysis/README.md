# PowerAnalysis: Warmup

**picoCTF 2023 — Cryptography — Hard**

## Description

PowerAnalysis: Warmup is a cryptography challenge from picoCTF 2023 that introduces **power analysis and side-channel attacks**.

The encryption algorithm leaks a single bit of information during its computations. By interacting with the encryption oracle and analyzing the leakage, the encryption key can be recovered.

## Challenge

> This encryption algorithm leaks a "bit" of data every time it does a computation. Use this to figure out the encryption key.

The challenge can be solved by modeling the relationship between the plaintext, the secret key, and the leaked bit.

## Approach

The solution uses a chosen-plaintext attack against the encryption oracle.

For each key byte:

1. Keep the plaintext at 16 bytes.
2. Change one plaintext byte through all `0x00`–`0xff` values.
3. Record the leakage returned by the oracle.
4. Compare the observed leakage pattern against every possible key-byte value.
5. Identify the matching key byte.
6. Repeat for all 16 bytes.

The complete technical analysis and implementation details are documented in [`WRITEUP.md`](WRITEUP.md).

## Files

```text
.
├── README.md
├── WRITEUP.md
└── run.py
```

### `run.py`

Python implementation of the power-analysis attack using Pwntools.

### `WRITEUP.md`

Detailed explanation of the vulnerability, leakage model, attack methodology, implementation, and key recovery process.

## Requirements

* Python 3
* Pwntools
* Kali Linux or another Linux environment
* Active picoCTF challenge instance

Install Pwntools on Kali Linux:

```bash
sudo apt update
sudo apt install python3-pwntools
```

## Running

Start the challenge instance on picoCTF and update the host/port in `run.py` with the values provided by the challenge.

Then run:

```bash
python3 run.py
```

## Skills Demonstrated

* Cryptography
* Power analysis
* Side-channel analysis
* Chosen-plaintext attacks
* Oracle interaction
* Python scripting
* Pwntools
* AES S-box analysis

## Platform

**picoCTF 2023**

**Category:** Cryptography

**Difficulty:** Hard

## Disclaimer

This repository contains a solution developed for the authorized picoCTF challenge environment and is intended for educational and cybersecurity learning purposes.


