from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from sha256 import hash


def sign(data: str, secret_key):
    signature = secret_key.sign(data.encode(), padding.PSS(mgf=padding.MGF1(
        hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
    return signature


def verify(signature, message, public_key):
    try:
        public_key.verify(signature, message.encode(), padding.PSS(mgf=padding.MGF1(
            hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except:
        return False


def generateKey():
    secret_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048)
    public_key = secret_key.public_key()
    with open("secret_key.pem", 'wb') as f:
        f.write(secret_key.private_bytes(encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()))

    with open("public_key.pem", "wb") as f:
        public_key_str = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                 format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()
        f.write(public_key_str.encode())

    return secret_key, public_key, hash(public_key_str)


def loadKeys(sk_addr, pk_addr):
    with open(sk_addr, 'rb') as f:
        secret_key = serialization.load_pem_private_key(
            f.read(), password=None)
    with open(pk_addr, 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read())

    public_key_str = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                             format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()
    return secret_key, public_key, hash(public_key_str)
