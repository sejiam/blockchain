from sha256 import hash


class Transaction:
    def __init__(self, sender, recipient, amount: int):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def data(self):
        trx = {"sender": self.sender,
               "recipient": self.recipient,
               "amount": self.amount}
        return trx
