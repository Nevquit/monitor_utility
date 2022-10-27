from substrateinterface import SubstrateInterface # for DOT RPC
def get_dot_balance(url, dot_address):
    '''
    return unit:wei
    '''
    substrate = SubstrateInterface(url=url)
    result = substrate.query(
        module='System',
        storage_function='Account',
        params=[dot_address]
    )
    return int(result.value['data']['free'])  # unit wei

if __name__ == '__main__':
    pass


