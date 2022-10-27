import requests
import json

def get_coin_balance(accout,rpc):
    '''
    :parameters:
    return: unit wei
    '''
    headers = {"Content-Type": "application/json"}
    rsp = requests.post(url = rpc,headers=headers,data = json.dumps({"jsonrpc":"2.0","method":"eth_getBalance","params":[accout, "latest"],"id":1}))
    return int(rsp.json()['result'],16)
def get_erc20_token_balance(token_address,account,rpc):
    '''
    eth_call data can get by utility_evm_web3.get_eth_call_data
    :parameters:
    return: unit wei
    '''
    headers = {"Content-Type": "application/json"}
    get_token_balance = {"jsonrpc":"2.0","method":"eth_call","params":[{"to": token_address, "data":"0x70a08231"+"000000000000000000000000"+account.lstrip('0x')}, "latest"],"id":1}
    rsp = requests.post(url = rpc,headers=headers,data = json.dumps(get_token_balance))
    return int(rsp.json()['result'],16)
def get_erc20_token_total_supply(token_address,rpc):
    headers = {"Content-Type": "application/json"}
    get_token_balance = {"jsonrpc": "2.0", "method": "eth_call", "params": [{"to": token_address, "data": "0x18160ddd"}, "latest"],"id": 1}
    rsp = requests.post(url=rpc, headers=headers, data=json.dumps(get_token_balance))
    return int(rsp.json()['result'], 16)
def get_erc721_token_balance(token_address,account,rpc):
    headers = {"Content-Type": "application/json"}
    get_token_balance = {"jsonrpc": "2.0", "method": "eth_call", "params": [{"to": token_address, "data": "0x70a08231" + "000000000000000000000000" + account.lstrip('0x')}, "latest"],"id": 1}
    rsp = requests.post(url=rpc, headers=headers, data=json.dumps(get_token_balance))
    return int(rsp.json()['result'], 16)
def get_erc1155_token_balance(token_address,tokenID:int,account,rpc):
    headers = {"Content-Type": "application/json"}
    get_token_balance = {"jsonrpc": "2.0", "method": "eth_call", "params": [{"to": token_address, "data": "0x00fdd58e" + "000000000000000000000000" + account.lstrip('0x')+"{0:0{1}x}".format(tokenID,64)}, "latest"],"id": 1}
    rsp = requests.post(url=rpc, headers=headers, data=json.dumps(get_token_balance))
    if rsp.status_code == 200:
        json_raw = rsp.json()
        if json_raw.get('result'):
            return int(rsp.json()['result'], 16)
        else:
            raise Exception('Get erc1155 token balance failed and response is  {}'.format(json_raw))
    else:
        raise Exception('Get erc1155 token balance failed status code is {}'.format(rsp.status_code))
def get_nft_total_supply(url:str,nft_sc_address):
    '''
    :paramater: url: 'https://api.thegraph.com/subgraphs/name/orelliao/testnet-eth-nft'
    '''
    query = '''
        {{
          tokenTotalSupplies(first: 5,where: {{id: {nft_sc_address}}}) {{
            id
            amount
          }}
        }}
    '''.format(nft_sc_address = nft_sc_address)
    rsp = requests.post(url, '',json={'query': query}) #{'data': {'tokenTotalSupplies': [{'id': '0x9b43a09368486699acd3baad3779a6bde4d62ca8', 'amount': '1'}]}}
    if rsp.status_code == 200:
        json_raw = rsp.json()
        if json_raw.get('data'):
            tokenTotalSupplies = json_raw['data']['tokenTotalSupplies']
            if tokenTotalSupplies:
                totalsupply = tokenTotalSupplies[0]['amount']
                return int(totalsupply)
            else:
                return 0
        else:
            raise Exception('Query failed response is  {}'.format(json_raw))
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(rsp.status_code, query))

if __name__ == '__main__':
    rpc = "https://rpc.ankr.com/eth"
    # token_address = '0x83e2BE8d114F9661221384B3a50d24B96a5653F5'
    # account = '0x8b157B3fFEAD48C8a4CDC6bddBE1C1D170049Da4'
    # print(get_erc20_token_balance(token_address,account,rpc))
    # print(get_erc20_token_total_supply(token_address,rpc))
    # erc721Sc = '0xB4feDc003053C22ac8b808Bb424f3e1787f30cF2'
    # account = '0xd62a5ba868e9f43216db1818ea5953af0b68a2fe'
    # # print(get_erc721_token_balance(erc721Sc,account,rpc))
    # print(get_erc721_token_total_supply(erc721Sc,rpc))
    erc1155Sc = '0x9b43A09368486699acD3baAd3779a6BdE4D62Ca8'.lower()
    account = '0x8b15***Da4'
    tokenID = 62909440381532276439567648116598540129728352131046336549933134526848664862721
    # print(get_erc1155_token_balance(erc1155Sc, tokenID,account,rpc))
    get_nft_total_supply('https://api.thegraph.com/subgraphs/name/orelliao/testnet-eth-nft', erc1155Sc)


