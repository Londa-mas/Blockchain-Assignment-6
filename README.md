# BLCH9X2 — Assignment 6: Mining & Proof-of-Work Lab

**Student Name:** Olonda Thoba Holizwi Masuku  
**Course:** Master of Financial Engineering (MFE), University of Johannesburg  
**Module:** BLCH9X2 Blockchain  

---

## Overview
This repository contains the core Proof-of-Work (PoW) mining module, simplified block reward (coinbase) implementation, empirical timing study scripts, and automated test suites for Assignment 6.

## Project Structure
- `mining.py`: Core PoW miner implementing nonce searches with leading hexadecimal zeros, coinbase transaction generation, and difficulty evaluation loops.
- `tests.py`: Automated test suite verifying mining difficulty compliance, coinbase structure, chain integration, and difficulty studies.
- `blockchain.py`: Underlying chain verification and block integrity modules.

## Installation & Setup
Clone the repository:
   ```bash
   git clone [https://github.com/Londa-mas/SimpleBlockchain.git](https://github.com/Londa-mas/SimpleBlockchain.git)
   cd SimpleBlockchain
   ```
Verify that your environment uses Python 3.10+ (no third-party package dependencies required).

## Running the Test Suite and Mining Module
To run the automated test suite and ensure all components pass:
```bash
python tests.py
```
To execute the mining and difficulty study workflow:
```bash
python mining.py
```
