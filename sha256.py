from hashlib import sha256


def hash(data: str):
    print(f"[data]{data} and [hash]{sha256(data.encode()).hexdigest()}")
    print("===")
    return sha256(data.encode()).hexdigest()
