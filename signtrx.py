from sha256 import hash
from transaction import Transaction
from stringify import stringify
from account import sign


def signTRX(trx: Transaction, sk):
    return sign(stringify(trx.data()), sk)
