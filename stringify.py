def stringify(data: dict):
    string = ""
    if data.get('trxs'):
        data['trxs'] = [sort_dict(trx) for trx in data['trxs']]
    data = sort_dict(data)
    for key in data:
        string += f"{key}:{data[key]},"
    return string


def sort_dict(data: dict):
    new_dict = dict()
    for key in sorted(data):
        new_dict[key] = data[key]
    return new_dict
