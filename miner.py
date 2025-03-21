from blockchain import Blockchain
from sha256 import hash
from signtrx import signTRX
from account import verify
from stringify import stringify
from transaction import Transaction
REWARD = 100


def miner(bc: Blockchain, addr):
    last_block = bc.last_block
    proof = bc.proofOfWork(last_block)
    reward_trx = Transaction("0", addr, REWARD)
    prev_hash = hash(stringify(last_block))
    block = bc.new_block(proof, prev_hash)
    bc.new_trx(reward_trx, "0", "0")
    bc.resolve_conflict()
    response = {
        'message': 'a new block mined',
        'index': block['index'],
        'trxs': block['trxs'],
        'proof': block['proof'],
        'prev_hash': block['prev_hash'],
    }
    return response
