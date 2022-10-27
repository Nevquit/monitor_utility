from websocket import create_connection
import json
import requests
def get_xrp_balance(url, xrp_address):
    '''
    https://web.postman.co/workspace/My-Workspace~91bae4f2-24a4-4b11-8d51-6f5c00ef3ccf/request/create?requestId=b2babce0-7635-4df8-a6d7-52e4a778d200
    return unit:wei
    '''
    data = {
            "method": "account_info",
            "params": [
                {
                    "account": xrp_address,
                    "strict": True,
                    "ledger_index": "current",
                    "queue": True
                }
            ]
        }
    headers = {'content-type': 'application/json'}
    balance = requests.get(url, data=json.dumps(data), headers=headers).json()['account_data']['Balance']
    return int(balance)
def get_xrp_token_balance(url,xrp_address, tokensympol):
    '''
    parameter tokensympol:token code
    return balance unit wei
    '''
    data = {
        "method": "account_lines",
        "params": [
            {
                "account": xrp_address
            }
        ]
    }
    headers = {'content-type': 'application/json'}
    lines = requests.get(url, data=json.dumps(data), headers=headers).json()['result']['lines']
    '''
    {
    "result": {
        "account": "r3iMrTH6y1DBkQpLidW3ZDRRRdS3tGZvFc",
        "ledger_hash": "04DC7D3392EA7B9F513E1E0EB2F63E62835CC1FECF31A434B672CB0ABDFB5289",
        "ledger_index": 74983627,
        "lines": [
            {
                "account": "rNy8hFXoXEaJwkiT6U6ED5CWsfZHELNcnr",
                "balance": "9.001122437",
                "currency": "584C495354000000000000000000000000000000",
                "limit": "1000000000000000e4",
                "limit_peer": "0",
                "no_ripple": true,
                "no_ripple_peer": false,
                "quality_in": 0,
                "quality_out": 0
            }]
    '''
    print(lines)
    for line in lines:
        if line['currency'] == tokensympol:
            return float(line['balance']) * 10 ** 15
if __name__ == '__main__':
    pass


