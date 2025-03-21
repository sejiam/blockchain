from blockchain import Blockchain
from transaction import Transaction
from account import loadKeys
from signtrx import signTRX
from miner import miner
from stringify import stringify
from sha256 import hash
bc = Blockchain()
sk, pk, addr = loadKeys("./secret_key.pem", "./public_key.pem")
sk1, pk1, addr1 = loadKeys("./w1/secret_key.pem", "./w1/public_key.pem")
sk2, pk2, addr2 = loadKeys("./w2/secret_key.pem", "./w2/public_key.pem")
chain = [{'index': 0, 'prev_hash': 0, 'proof': 0, 'timestamp': 1742570179.9924562, 'trxs': [{'amount': 1000, 'recipient': '6f9d536661baa43659145aaf7f9715f197f74c530a8b913c7ae8797396de0a5b', 'sender': '0'}]}, {'index': 1, 'prev_hash': 'da6f4d8da394766c6a7fff1e8418c7fa15e404812fd3a80324f90097b34e912b', 'proof': 92589, 'timestamp': 1742570207.0884306, 'trxs': [
    {'amount': 100, 'recipient': 'c1c04a6e8043d029ebf2853677cdc44dd2961f6c01a629f5443d42b2924336c7', 'sender': '6f9d536661baa43659145aaf7f9715f197f74c530a8b913c7ae8797396de0a5b'}, {'amount': 100, 'recipient': 'c1c04a6e8043d029ebf2853677cdc44dd2961f6c01a629f5443d42b2924336c7', 'sender': '6f9d536661baa43659145aaf7f9715f197f74c530a8b913c7ae8797396de0a5b'}]}]
fb = chain[0]
cb = chain[1]
data = "index:0,prev_hash:0,proof:0,timestamp:1742570179.9924562,trxs:[{'amount': 1000, 'recipient': '6f9d536661baa43659145aaf7f9715f197f74c530a8b913c7ae8797396de0a5b', 'sender': '0'}],"
# print(hash('0'+hash((data))+'72923'))
print(hash(stringify(fb)))
