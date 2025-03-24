from blockchain import Blockchain
from miner import miner
from transaction import Transaction
import account
from signtrx import signTRX
from flask import Flask, request

# menu = """
#     1 -> new trx
#     2 -> mine
#     3 -> see mempool
#     4 -> see full chain
#     5 -> see balance
# """

# bc = Blockchain()
# skm, pkm, addrm = account.loadKeys("./secret_key.pem", "./public_key.pem")
# print(bc.chain)
# print(f"my balance: {bc.balance(addrm)}")
# trx = Transaction(addrm, addrm, 50)
# bc.new_trx(trx, signTRX(trx, skm), pkm)
# bc.new_trx(trx, signTRX(trx, skm), pkm)
# bc.new_trx(trx, signTRX(trx, skm), pkm)
# print(bc.chain)
# print(f"my balance: {bc.balance(addrm)}")
# miner(bc, addrm)
# print(bc.chain)
# print(f"my balance: {bc.balance(addrm)}")
# print([i.data() for i in bc.current_trxs])
app = Flask(__name__)
bc = Blockchain()
sk, pk, addr = account.loadKeys("./w1/secret_key.pem", "./w1/public_key.pem")
# sk, pk, addr = account.generateKey()

print(addr)


@app.route('/wallet', methods=['GET'])
def wallet():
    response = {
        'wallet_address': addr,
    }
    return response, 200


@app.route('/mine', methods=['GET'])
def mine():
    return miner(bc, addr), 200


@app.route('/trxs/new', methods=['POST'])
def newTRX():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return "missing value", 400
    trx = Transaction(values['sender'], values['recipient'], values['amount'])
    bc.new_trx(trx, signTRX(trx, sk), pk)
    response = {'message': 'trx done'}
    return response, 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': bc.chain,
        'length': len(bc.chain)
    }
    return response, 200


@app.route('/mempool', methods=['GET'])
def mempool():
    response = {
        'mempool': [i.data() for i in bc.current_trxs]
    }
    return response, 200


@app.route('/balance', methods=['POST'])
def balance():
    addr = request.get_json()['addr']
    response = {"balance": bc.balance(addr)}
    return response, 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error"
    for node in nodes:
        bc.register_node(node)

    response = {
        'message': 'new node added',
        'total_nodes': list(bc.nodes),
    }
    return response


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = bc.resolve_conflict()
    if replaced:
        response = {
            'message': 'our chain was replaced',
            'new_chain': bc.chain
        }
    else:
        response = {
            'message': 'our chain is longest',
            'chain': bc.chain
        }
    return response, 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000,
                        type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
