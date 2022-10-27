import requests
import json

def get_btc_balance(node, user, password, address,decimal=8):
    '''
    param: node: RPC for BTC/LTC/DOGE
    return: int: wei
    '''
    url = node
    balance = 0
    headers = {"Content-Type": "application/json"}
    method = json.dumps({"jsonrpc": "1.0", "id": "curltest", "method": "listunspent", "params": [1, 99999999, [address]]})
    rsp = requests.post(url=url, auth=(user, password), headers=headers, data=method).json()
    for utxo in rsp['result']:
        balance += utxo['amount']
    return int(balance * 10**decimal)



if __name__ == '__main__':
    pass


