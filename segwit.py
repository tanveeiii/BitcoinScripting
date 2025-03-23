from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal

rpc_user = "tanveeiii"
rpc_password = "tanvi.agarwal"
rpc_port = "18443"
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}")

try:
    info = rpc_connection.getblockchaininfo()
    print("Connected. Blockchain info:", info)
except JSONRPCException as e:
    print("Error connecting to bitcoind:", e)

try:
    rpc_connection.loadwallet("mywallet")
except:
    Exception("Wallet is already loaded")

address_A = rpc_connection.getnewaddress("A")
address_B = rpc_connection.getnewaddress("B")
address_C = rpc_connection.getnewaddress("C")

print("Address A:", address_A)
print("Address B:", address_B)
print("Address C:", address_C)

rpc_connection.generatetoaddress(201, address_A)
balance = rpc_connection.getbalance()
print("New balance:", balance)

txid_fund = rpc_connection.sendtoaddress(address_A, 10) 
print("Funding txid for address A:", txid_fund)

# tx_id = rpc_connection.gettransaction(txid_fund)
# print(tx_id)

# mempool = rpc_connection.getrawmempool()
# print(txid_fund in mempool)


# raw_tx = rpc_connection.getrawtransaction(txid_fund, True)
# print(raw_tx["vout"])

utxos = rpc_connection.listunspent(0, 9999999, [address_A])
utxo = [ut for ut in utxos if ut["txid"] == txid_fund]
print(utxo)

send_amount = Decimal("5.0")
change_address = address_A  

fee = Decimal("0.0001")
input_utxo = {
    "txid": utxo[0]["txid"],
    "vout": utxo[0]["vout"]
}

change_amount = Decimal(utxo[0]["amount"]) - send_amount - fee
print(utxo[0]["amount"])
print(change_amount)
if change_amount < 0:
    raise Exception("Insufficient funds: the UTXO amount is lower than the send amount plus fee.")

outputs = {
    address_B: float(send_amount),
    change_address: float(change_amount)
}

raw_tx = rpc_connection.createrawtransaction([input_utxo], outputs)
print("Raw transaction:", raw_tx)

signed_tx = rpc_connection.signrawtransactionwithwallet(raw_tx)
if not signed_tx["complete"]:
    raise Exception("Transaction signing failed.")
decoded_tx = rpc_connection.decoderawtransaction(signed_tx["hex"])

for vout in decoded_tx["vout"]:
    address = vout["scriptPubKey"].get("address")
    if address == address_B:
        print(f"scriptPubKey for Address B is {vout['scriptPubKey']['hex']}")

print("Signed transaction:", signed_tx["hex"])

print("Decoded signed transaction ",decoded_tx)

txid = rpc_connection.sendrawtransaction(signed_tx["hex"])
print("Transaction broadcasted successfully. TXID:", txid)

utxos_b = rpc_connection.listunspent(0,9999,[address_B])
utxo_b = [ut for ut in utxos_b if ut["txid"] == txid][0]

print(utxo_b)

input_utxo_b = {
    "txid":utxo_b["txid"],
    "vout":utxo_b["vout"]
}

send_amount_b = Decimal('2.50')
change_amount_b = Decimal(utxo_b["amount"]) - send_amount_b - fee
change_address_b = address_B

outputs_b = {
    address_C: float(send_amount_b),
    change_address_b: float(change_amount_b)
}

raw_tx_b = rpc_connection.createrawtransaction([input_utxo_b], outputs_b)
print("Raw transaction:", raw_tx_b)

signed_tx_b = rpc_connection.signrawtransactionwithwallet(raw_tx_b)
print(signed_tx_b)
decoded_tx_b = rpc_connection.decoderawtransaction(signed_tx_b["hex"])

print("Decoded signed transaction: ", decoded_tx_b)

for vout in decoded_tx_b["vout"]:
    address = vout["scriptPubKey"].get("address")
    if address == address_C:
        print(f"scriptPubKey for Address C is {vout['scriptPubKey']['hex']}")

