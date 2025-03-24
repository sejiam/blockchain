import requests


def broadcast(nodes, path, data: list = None):
    results = dict()
    for node in nodes:
        url = node+'/'+path
        if data:
            res = requests.post(url, data)
        else:
            res = requests.get(url)
        results[url] = res
    return results
