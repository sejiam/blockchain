import requests
from account import generateKey, loadKeys
from json import dumps
url = "https://4300-5-181-235-74.ngrok-free.app/"
headers = {'Content-Type': 'application/json'}

menu = """
    1 -> new trx
    2 -> mine
    3 -> see mempool
    4 -> see full chain
    5 -> see balance
    6 -> add node
    7 -> update chain
"""
skm, pkm, addrm = loadKeys("./secret_key.pem", "./public_key.pem")
# skm, pkm, addrm = loadKeys("./w1/secret_key.pem", "./w1/public_key.pem")
print(f"your secret key: [{skm}]")
print(f"your public key: [{pkm}]")
print(f"your wallet address: [{addrm}]")

while 1:
    choice = input(menu)
    if choice == '1':
        sender = addrm
        recipient = input('recipient')
        amount = int(input('amount'))
        payload = {'sender': sender, 'recipient': recipient, 'amount': amount}
        res = requests.post(
            url+'trxs/new', dumps(payload), headers=headers)
        if res.ok:
            print('done')
        else:
            print('trx failed')

    elif choice == '2':
        print('started to mine')
        res = requests.get(url+'mine')
        print('a new block mined')

    elif choice == '3':
        res = requests.get(url+'mempool')
        print(res.text)

    elif choice == '4':
        res = requests.get(url+'chain')
        print(res.text)

    elif choice == '5':
        payload = {'addr': addrm}

        res = requests.post(url+'balance', dumps(payload), headers=headers)
        print(res.text)

    elif choice == '6':
        nodeid = input('node identifier')
        payload = {'nodes': [nodeid]}
        res = requests.post(url+'nodes/register',
                            dumps(payload), headers=headers)
        print(res.text)

    elif choice == '7':
        res = requests.get(url+'nodes/resolve')
        print(res.text)
    else:
        pass
