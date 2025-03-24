from time import time
from transaction import Transaction
import account
from stringify import stringify
from sha256 import hash
from urllib.parse import urlparse
import requests
from broadcast import broadcast

addr = "5661ab781623bdbdf4a045b5c695cb1880baff78619a62b19b16a7f45fe6e84e"


class Blockchain:
    REWARD = 100
    MIN_TRXS_COUNT = 1

    def __init__(self):
        self.chain = []
        self.current_trxs = []
        self.nodes = set()
        genesis_trx = Transaction("0", addr, 1000)
        self.new_trx(genesis_trx, "0", "0")
        self.new_block(0, 0)

    def register_node(self, address):
        parsed_url = urlparse(address)

        if parsed_url.netloc and parsed_url.scheme:
            self.nodes.add(parsed_url.scheme+'://'+parsed_url.netloc)
        else:
            raise Exception("invalid url")

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            last_block_hash = hash(stringify(last_block))
            if block['prev_hash'] != last_block_hash:
                return False
            if not self.valid_POW(last_block['proof'], last_block_hash, block['proof']):
                return False
            last_block = block
            current_index += 1
        return True

    def resolve_conflict(self):
        neighbors = self.nodes
        print("[neighbor nodes]:", neighbors)
        new_chain = None
        max_length = len(self.chain)

        for node in neighbors:
            response = requests.get(node+"/chain")
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                print("[length]:", length)
                print("[chain]:", chain)
                print("[chain validation]:", self.valid_chain(chain))
                if length > max_length:
                    if self.valid_chain(chain):
                        max_length = length
                        new_chain = chain
                        broadcast(self.nodes, "nodes/resolve")
                    else:
                        print("validation method returns false")
                else:
                    print("length check did not passed")
            else:
                print('failed to connect')
        if new_chain:
            self.chain = new_chain
            return True
        return False

    def new_block(self, proof, prev_hash):
        if self.last_block == -1 or hash(stringify(self.last_block)) == prev_hash:
            block = {
                "index": len(self.chain),
                "timestamp": time(),
                "proof": proof,
                "trxs": [trx.data() for trx in self.current_trxs],
                "prev_hash": prev_hash,
            }
            self.current_trxs = []
            self.chain.append(block)
            broadcast(self.nodes, "nodes/resolve")
            return block
        else:
            raise Exception('invalid proof')

    def new_trx(self, trx: Transaction, signed_trx, sender_publickey):
        if len(self.current_trxs) == 0 and signed_trx == '0' and sender_publickey == "0" and trx.amount == self.REWARD:
            self.current_trxs.append(trx)
        elif account.verify(signed_trx, stringify(trx.data()), sender_publickey):
            if self.balance(trx.sender) >= trx.amount:
                self.current_trxs.append(trx)
            else:
                raise Exception("not enough coin")
        else:
            raise Exception("trx is invalid")

    def proofOfWork(self, last_block, addr):
        if len(self.current_trxs) > self.MIN_TRXS_COUNT:
            last_proof = last_block["proof"]
            last_block_hash = hash(stringify(last_block))

            proof = 0
            while not self.valid_POW(last_proof, last_block_hash, proof):
                proof += 1
            return proof
        else:
            raise Exception("not enough trx in mempool.")

    def valid_POW(self, last_proof, last_hash, new_proof):
        guess = f"{last_proof}{last_hash}{new_proof}"
        guess_hash = hash(guess)
        return guess_hash[:4] == "0000"

    def balance(self, address):
        total = 0
        for block in self.chain:
            for trx in block['trxs']:
                if address == trx['recipient']:
                    total += trx['amount']
                if address == trx['sender']:
                    total -= trx['amount']
        return total

    @property
    def last_block(self):
        if len(self.chain) != 0:
            return self.chain[-1]
        else:
            return -1
