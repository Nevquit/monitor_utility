from iWAN import iWAN #pip install iWAN
from iWAN_Request import iWAN_Request

def get_evm_coin_balance(iwan:iWAN,account,chain):
    '''
    :param account:
    :param chain:
    :return:
    {"jsonrpc": "2.0", "id": 1, "result": "63063269117771397923"} #wei
    '''
    result = iwan.sendRequest(iWAN_Request.getBalance(account, chain))['result']
    return int(result)

def get_evm_erc20_balance(iwan:iWAN,chainType,account,tokenScAddr):
    '''

    :param chainType:
    :param account:
    :param tokenScAddr:
    :return:
    {"jsonrpc": "2.0", "id": 1, "result": "44390"} #wei
    '''
    result = iwan.sendRequest(iWAN_Request.getTokenBalance(chainType, account, tokenScAddr))['result']
    return int(result)
def get_evm_erc20_total_supply(iwan:iWAN,chainType, tokenScAddr):
    '''

    :param chainType:
    :param tokenScAddr:
    :return: {"jsonrpc": "2.0", "id": 1, "result": "31924999999999995"} #wei
    '''
    totalSupply = iwan.sendRequest(iWAN_Request.getTokenSupply(chainType, tokenScAddr))['result']
    return int(totalSupply)
def get_btc_type_balance(iwan:iWAN,chainType, Addr):
    '''

    :param BTC/LTC/DOGE:
    :param Addr:
    :return: amount staoshi/wei
    '''

    amount = 0
    totalSupply = iwan.sendRequest(iWAN_Request.getBTCUTXO(chainType, Addr))
    for tx in totalSupply['result']:
        amount += float(tx['amount'])
    return int(amount*100000000)

def get_xrp_coin_balance(iwan:iWAN,account):
    '''
    :param account:
    :return:
    {"jsonrpc": "2.0", "id": 1, "result": "63063269117771397923"} #wei
    '''
    result = iwan.sendRequest(iWAN_Request.getBalance(account, 'XRP'))['result']
    return int(result)


if __name__ == '__main__':
    pass