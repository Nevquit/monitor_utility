from iWAN import iWAN #pip install iWAN
import json
from BalanceSpider import BtcBalanceSpider,XrpBalanceSpider
import traceback
import monitor_utility.get_balance_via_iwan as iwan_balance
import monitor_utility.get_balance_via_rpc_evm as evm_balance
import monitor_utility.get_balance_via_rpc_btc as btc_balance
import monitor_utility.get_balance_via_rpc_dot as dot_balance
import monitor_utility.get_balance_via_rpc_xrp as xrp_balance

class BalanceUtility:
    def __init__(self,net,iWAN_Config,print_flag=False):
        '''
        :param net: 'main'/'test'
        :param iWAN_Config: ".iWAN_config.json"
                {
                    "secretkey": "your secretkey",
                    "Apikey": "your apikey",
                    "url_test": "wss://apitest.wanchain.org:8443/ws/v3/",
                    "url_main": "wss://api.wanchain.org:8443/ws/v3/"
                }

        '''
        with open(iWAN_Config,'r') as f:
            config = json.load(f)
        self.net = net
        self.iwan = iWAN.iWAN(config["url_{}".format(net)],config['secretkey'],config['Apikey'])
        self.print_flag = print_flag
    def pprint(self,*args,**kwargs):
        if self.print_flag :
            print(*args,**kwargs)
    def get_btc_balance(self, spider = False, **kwargs):# def getBTCsBalance(self,chain,node,user,password,address):

        '''
        get the balance from node,iwan,third part data
        :param chain:
        :param address:
        :param kwargs['nodes']:[url1,url2.....]
        :return:
        '''
        balancePool = []
        # get from iwan
        try:
            balance_iWAN = iwan_balance.get_btc_type_balance(self.iwan,kwargs['chain'],kwargs['address'])
        except:
            print('get {} balance from iwan  failed due to : {} '.format(kwargs['chain'], traceback.format_exc()))
            balance_iWAN = 'failed'
        if balance_iWAN != 'failed':
            balancePool.append(balance_iWAN)

        # get by spider
        if self.net == 'main' and spider:
            try:
                balance_spider = BtcBalanceSpider.BtcBalanceSpider().getBTCBalance(kwargs['chain'], kwargs['address'])
            except:
                balance_spider = 'failed'
            if balance_spider != 'failed':
                balancePool.append(balance_spider)

        #get from node
        for node in kwargs['nodes']:
            try:
                balance_Node = btc_balance.get_btc_balance(node,kwargs['user'],kwargs['password'],kwargs['address'])
            except Exception:
                print('get {} balance from {} failed due to : {} '.format(node,kwargs['chain'], traceback.format_exc()))
                balance_Node = 'failed'
            if balance_Node != 'failed':
                balancePool.append(balance_Node)
        # summay balance
        if balancePool:
            amt = max(balancePool,key=balancePool.count)
            self.pprint(balancePool)
            return amt
        self.pprint(balancePool)
    def get_dot_balance(self,spider = False,**kwargs):
        '''
        :param nodes: [node1,node2,node3,...]
        :param address:
        :return:
        '''
        balancePool = []
        urls = kwargs['nodes']
        for url in urls:
            try:
                balance_node = dot_balance.get_dot_balance(url,kwargs['address'])
            except:
                print('get DOT balance from rpc {} failed due to : {} '.format(url, traceback.format_exc()))
                balance_node = 'failed'
            if balance_node != 'failed':
                balancePool.append(int(balance_node))
        if balancePool:
            return max(balancePool, key=balancePool.count)
    def get_xrp_balance(self,spider = False,**kwargs):
        '''
        curl - H
        'Content-Type: application/json' - d
        '{"method":"account_info","params":[{"account":"rf1BiGeXwwQoi8Z2ueFYTEXSwuJYfV2Jpn","strict":true,"ledger_index":"current","queue":true}]}'
        :param: nodes
        '''

        balance_pool = []
        # get balance from iwan
        try:
            balance_iwan = iwan_balance.get_xrp_coin_balance(self.iwan,kwargs['address'])
        except:
            print('get XRP balance from iwan due to {}'.format(traceback.format_exc()))
            balance_iwan = 'failed'
        if balance_iwan != 'failed':
            balance_pool.append(balance_iwan)
        self.pprint('Get Balnce From iWAN Done')

        # get balance from rpc
        for url in kwargs['nodes']:
            try:
                balance_rpc = xrp_balance.get_xrp_balance(url,kwargs['address'])
            except:
                print('get XRP balance from {} due to {}'.format(url,traceback.format_exc()))
                balance_rpc = 'failed'
            if balance_rpc != 'failed':
                balance_pool.append(balance_rpc)
        self.pprint('Get Balnce From RPC Done')
        #get balance from spider
        if self.net =='main' and spider:
            try:
                xrpbalance_spider = XrpBalanceSpider.XrpBalanceSpider().getXRPBalance(kwargs['address'])
            except:
                print('get xrp balance from spider failed due to {}'.format(traceback.format_exc()))
                xrpbalance_spider = None
            if xrpbalance_spider:
                balance_pool.append(xrpbalance_spider)
        self.pprint('Get Balnce From Spider Done')

        # summary balance
        if balance_pool:
            self.pprint(balance_pool)
            return max(balance_pool,key=balance_pool.count) #to avoid get 0 balance
    def get_xrp_token_balance(self,spider = False,**kwargs):
        balance_pool = []
        for url in kwargs['nodes']:
            try:
                balance_rpc = xrp_balance.get_xrp_token_balance(url,kwargs['address'],kwargs['tokensympol'])
            except:
                print('get xrp token {} balance from {} failed due to {}'.format(kwargs['tokensympol'],url,traceback.format_exc()))
                balance_rpc = 'failed'
            if balance_rpc != 'failed':
                balance_pool.append(balance_rpc)
        if balance_pool:
            self.pprint(balance_pool)
            return max(balance_pool,key=balance_pool.count)
    def get_evm_coin_balance(self,spider = False,**kwargs):
        balance_pool = []
        #get balance from iwan
        try:
            balance_iwan = iwan_balance.get_evm_coin_balance(self.iwan,kwargs['address'],kwargs['chain'])
        except:
            print('get {} balance from iwan failed due to {}: '.format(kwargs['chain'], traceback.format_exc()))
            balance_iwan = 'failed'
        if balance_iwan != 'failed':
            balance_pool.append(balance_iwan)
        #get balance from rpcs
        for rpc in kwargs['nodes']:
            try:
                balance_rpc = evm_balance.get_coin_balance(kwargs['address'],rpc)
            except:
                print('get {} balance from rpc {} failed due to {}: '.format(kwargs['chain'],rpc,traceback.format_exc()))
                balance_rpc = 'failed'
            if balance_rpc != 'failed':
                balance_pool.append(balance_rpc)
        #summay balance
        if balance_pool:
            self.pprint(balance_pool)
            return max(balance_pool,key=balance_pool.count)
    def get_evm_token_balance(self,spider = False,**kwargs):
        balance_pool = []
        #get balance from iwan
        try:
            balance_iwan = iwan_balance.get_evm_erc20_balance(self.iwan,kwargs['chain'],kwargs['address'],kwargs['token_address'])
        except:
            print('get {} balance from iwan failed due to {}: '.format(kwargs['token_address'], traceback.format_exc()))
            balance_iwan = 'failed'
        if balance_iwan != 'failed':
            balance_pool.append(balance_iwan)
        #get balance from rpcs
        for rpc in kwargs['nodes']:
            try:
                balance_rpc = evm_balance.get_erc20_token_balance(kwargs['token_address'],kwargs['address'],rpc)
            except:
                print('get {} balance from rpc {} failed due to {}: '.format(kwargs['token_address'],rpc,traceback.format_exc()))
                balance_rpc = 'failed'
            if balance_rpc != 'failed':
                balance_pool.append(balance_rpc)
        #summay balance
        if balance_pool:
            self.pprint(balance_pool)
            return max(balance_pool,key=balance_pool.count)
    def get_evm_token_totalsupply(self,spider = False,**kwargs):
        balance_pool = []
        #get balance from iwan
        try:
            balance_iwan = iwan_balance.get_evm_erc20_total_supply(self.iwan,kwargs['chain'],kwargs['token_address'])
        except:
            print('get {} totall supply from iwan failed due to {}: '.format(kwargs['token_address'], traceback.format_exc()))
            balance_iwan = 'failed'
        if balance_iwan != 'failed':
            balance_pool.append(balance_iwan)
        #get balance from rpcs
        for rpc in kwargs['nodes']:
            try:
                balance_rpc = evm_balance.get_erc20_token_total_supply(kwargs['token_address'],rpc)
            except:
                print('get {} total supply from rpc {} failed due to {}: '.format(kwargs['token_address'],rpc,traceback.format_exc()))
                balance_rpc = 'failed'
            if balance_rpc != 'failed':
                balance_pool.append(balance_rpc)
        #summay balance
        if balance_pool:
            self.pprint(balance_pool)
            return max(balance_pool,key=balance_pool.count)

if __name__ == '__main__':
    utl = BalanceUtility('main','E:\Automation\wanchain_monitor\config\.iWAN_config.json',print_flag=False)
    # dotkwargs = {'nodes':[''],'address':'15FbT22gc9aqT1DFyfxUyPerbhyY36F4ATXFmKRVBBRvqLYF'}
    # print(utl.get_dot_balance(**dotkwargs))
    # btckwargs = {'chain':'BTC','nodes':[""],'user':'',"password": "","address":'171BgtCMUiCQfXSBDX66R8jFW29z4kcnJC'}
    # print(utl.get_btc_balance(**btckwargs))
    # xrpkwargs = {'nodes':["https://s1.ripple.com:51234/"],"address":'rQnk4Wksyy3FiTuM5xKnE78fkwYXRVs48R',"tokensympol":"DKS"}
    # print(utl.get_xrp_token_balance(**xrpkwargs))
    # ethkwargs = {'chain':'WAN','nodes':[""],"address":'0xe85b0D89CbC670733D6a40A9450D8788bE13da47'}
    # print(utl.get_evm_coin_balance(**ethkwargs))
    ethkwargs = {'chain':'WAN','nodes':["https://gwan-ssl.wandevs.org:56891","https://gwan-ssl.wandevs.org:56891"],"address":'0xe85b0D89CbC670733D6a40A9450D8788bE13da47',"token_address":"0x6e11655d6aB3781C6613db8CB1Bc3deE9a7e111F"}
    print(utl.get_evm_token_balance(**ethkwargs))
    print(utl.get_evm_token_totalsupply(**ethkwargs))


