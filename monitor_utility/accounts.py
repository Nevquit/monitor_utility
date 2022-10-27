from iWAN import iWAN #pip install iWAN
import json
from pubkey2address import Gpk2BtcAddr,Gpk2DotAddr,Gpk2XrpAddr #pip install pubkey2address
from iWAN_Request import iWAN_Request
class LockedAccountUtility:
    '''
    LockedAccounts;
    TokenPairs related infomations
    '''
    def __init__(self,net,iWAN_Config,chainInfo:dict,evmChainCrossSc:dict,print_flag=False):
        '''
        :param net: 'main'/'test'
        :param chainInfo : 'https://raw.githubusercontent.com/Nevquit/configW/main/chainInfos.json'
        :param iWAN_Config: path: ".iWAN_config.json"
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
        self.chainInfo = chainInfo[net]
        self.evmLockedAccounts = evmChainCrossSc[net]
    def pprint(self,*args,**kwargs):
        if self.print_flag :
            print(*args,**kwargs)
    def get_evm_locked_accounts(self):
        return self.evmLockedAccounts
    def get_noevm_locked_accounts(self,grInfo):
        '''
        Need update this function when add new noEvm chains
        :param grInfo:
        :return:
        '''
        BTCAddr = Gpk2BtcAddr.GPK2BTCADDRESS(grInfo,net=self.net)
        btcAddress = BTCAddr.Public_key_to_address('BTC')
        ltcAddress = BTCAddr.Public_key_to_address('LTC')
        dogeAddress = BTCAddr.Public_key_to_address('DOGE')
        xrpAddress = Gpk2XrpAddr.GPK2XRPADDRESS().getSmXrpAddr(grInfo)
        dotAddress = Gpk2DotAddr.GPK2DOTADDRESS().getSmDotAddr(grInfo,self.net)
        noEVMLockedAccout = {'LTC':ltcAddress,'XRP':xrpAddress,'BTC':btcAddress,'DOGE':dogeAddress,'DOT':dotAddress}
        return noEVMLockedAccout
    def get_locked_account(self,grInfo):
        LockedAccounts = {}
        evmLockedAccounts = self.get_evm_locked_accounts()
        noEVMLockedAccout = self.get_noevm_locked_accounts(grInfo)
        LockedAccounts.update(evmLockedAccounts)
        LockedAccounts.update(noEVMLockedAccout)
        return LockedAccounts
    def get_locked_account_for_multi_grps(self,working_groups:list):
        '''
        :param working_groups: [group1ID,group2ID]
        :return:
        '''
        LockedAccs_allGroups = {}
        for wk_grp in working_groups:
            grInfo = self.iwan.sendRequest(iWAN_Request.getStoremanGrpInfo(wk_grp))
            self.pprint(grInfo)
            LockedAccs = self.get_locked_account(grInfo)
            for chain, locked_account in LockedAccs.items():
                if not LockedAccs_allGroups.get(chain):
                    LockedAccs_allGroups[chain] = [locked_account]
                else:
                    if locked_account not in LockedAccs_allGroups[chain]:
                        LockedAccs_allGroups[chain].append(locked_account)
        return LockedAccs_allGroups

if __name__ == '__main__':
    pass



