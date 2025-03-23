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
    
# Run this only once 
# rpc_connection.createwallet("mywallet")

try:
    rpc_connection.loadwallet("mywallet")
except:
    Exception("Wallet is already loaded")

legacy_address_A = rpc_connection.getnewaddress("Legacy A", "legacy")
legacy_address_B = rpc_connection.getnewaddress("Legacy B", "legacy")
legacy_address_C = rpc_connection.getnewaddress("Legacy C", "legacy")

print("Legacy Address A:", legacy_address_A)
print("Legacy Address B:", legacy_address_B)
print("Legacy Address C:", legacy_address_C)

rpc_connection.generatetoaddress(201, legacy_address_A)
balance = rpc_connection.getbalance()
print("New balance:", balance)

txid_fund = rpc_connection.sendtoaddress(legacy_address_A, 10)
print("Funding TXID for Legacy Address A:", txid_fund)

utxos = rpc_connection.listunspent(0, 9999999, [legacy_address_A])
utxo = [ut for ut in utxos if ut["txid"] == txid_fund][0]
print("Selected UTXO:", utxo)

send_amount = Decimal("5.0")
fee = Decimal("0.0001")

input_utxo = {
    "txid": utxo["txid"],
    "vout": utxo["vout"]
}

change_amount = Decimal(utxo["amount"]) - send_amount - fee
if change_amount < 0:
    raise Exception("Insufficient funds: UTXO amount is lower than send amount + fee.")

outputs = {
    legacy_address_B: float(send_amount),
    legacy_address_A: float(change_amount)
}

raw_tx = rpc_connection.createrawtransaction([input_utxo], outputs)
print("Raw transaction:", raw_tx)

signed_tx = rpc_connection.signrawtransactionwithwallet(raw_tx)
if not signed_tx["complete"]:
    raise Exception("Transaction signing failed.")
decoded_tx = rpc_connection.decoderawtransaction(signed_tx["hex"])

for vout in decoded_tx["vout"]:
    address = vout["scriptPubKey"].get("address")
    if address == legacy_address_B:
        print(f"scriptPubKey for Address B is {vout['scriptPubKey']['hex']}")

print("Signed transaction:", signed_tx["hex"])

print("Decoded signed transaction ",decoded_tx)

txid = rpc_connection.sendrawtransaction(signed_tx["hex"])
print("Transaction broadcasted successfully. TXID:", txid)

utxos_b = rpc_connection.listunspent(0,9999,[legacy_address_B])
utxo_b = [ut for ut in utxos_b if ut["txid"] == txid][0]

print(utxo_b)

input_utxo_b = {
    "txid":utxo_b["txid"],
    "vout":utxo_b["vout"]
}

send_amount_b = Decimal('2.50')
change_amount_b = Decimal(utxo_b["amount"]) - send_amount_b - fee
change_address_b = legacy_address_B

outputs_b = {
    legacy_address_C: float(send_amount_b),
    change_address_b: float(change_amount_b)
}

raw_tx_b = rpc_connection.createrawtransaction([input_utxo_b], outputs_b)
print("Raw transaction:", raw_tx_b)

signed_tx_b = rpc_connection.signrawtransactionwithwallet(raw_tx_b)
decoded_tx_b = rpc_connection.decoderawtransaction(signed_tx_b["hex"])

print("Decoded signed transaction: ", decoded_tx_b)

for vout in decoded_tx_b["vout"]:
    address = vout["scriptPubKey"].get("address")
    if address == legacy_address_C:
        print(f"scriptPubKey for Address C is {vout['scriptPubKey']['hex']}")




