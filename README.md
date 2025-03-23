# BitcoinScripting

### Team Members:
- Tanvi Agarwal: 230001075
- Suryansh Nagar: 230003077
- Manan Nigam: 230051009
- Manan Jiwnani: 230001049

## Overview

This project demonstrates how to create, sign, and broadcast Bitcoin transactions on a regtest network using Python and Bitcoin Core’s RPC interface. Two examples are provided:

- **Segwit Transactions:**  
  Shows how to fund a legacy address, create a transaction from Address A to Address B using Segwit inputs (with witness data), and then create another transaction spending from Address B to Address C.

- **Legacy Transactions:**  
  Demonstrates the same process using legacy (non-Segwit) addresses and transactions.

Both examples illustrate:
- Connecting to a Bitcoin Core node via RPC.
- Generating new addresses.
- Funding addresses by generating blocks.
- Creating raw transactions.
- Signing transactions using the wallet.
- Decoding and printing transaction details.
- Broadcasting transactions to the regtest network.

## Prerequisites

- **Bitcoin Core Node:**  
  A Bitcoin Core node running in regtest mode with RPC enabled. Ensure that the wallet (e.g., named `mywallet`) is loaded.
  
- **Python 3:**  
  Make sure Python 3 is installed on your system.
  
- **Python Bitcoin RPC Library:**  
  Install the `python-bitcoinrpc` package. You can install it using pip:
  ```bash
  pip install python-bitcoinrpc
