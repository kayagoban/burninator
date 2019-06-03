from shadowlands.sl_contract.erc20 import Erc20
from shadowlands.tui.debug import debug, end_debug
from decimal import Decimal
import pdb


class PeasantCoin(Erc20):

    # Similar to balanceOf, but keeps track of burninated peasants
    def burninatedBy(self, address):
        return self.functions.burninatedBy(address).call()
    
    # I should have returned the entire array, but I don't want to redeploy the contract.
    # it's only 10 iterations.  I hope you have a local node.
    def top_burninators(self): 
        ''' 
        Returns a sorted list of lists of integers and addresses, representing the top
        burninators in peasantcoin. Maximum 10 results.
        '''
        burninators = set(self.functions.topBurninators().call())
        burninators.remove('0x0000000000000000000000000000000000000000')
        if len(burninators) == 0:
            return []

        burninators = [[x, Decimal(self.functions.burninatedBy(x).call()) / (10 ** self.functions.decimals().call())] for x in list(burninators)]
        burninators = list(burninators.sort(key=lambda x: x[1], reverse=True))
        debug(); pdb.set_trace()
        return burninators

    #TXs
    def burninate(self, peasants):
        return self.functions.burn(peasants)


    def claimVictory(self):
        return self.functions.claimVictory()


    MAINNET='token.burninator.eth'
    ABI='''
    [{"name":"Transfer","inputs":[{"type":"address","name":"_from","indexed":true},{"type":"address","name":"_to","indexed":true},{"type":"uint256","name":"_value","indexed":false}],"anonymous":false,"type":"event"},{"name":"Approval","inputs":[{"type":"address","name":"_owner","indexed":true},{"type":"address","name":"_spender","indexed":true},{"type":"uint256","name":"_value","indexed":false}],"anonymous":false,"type":"event"},{"outputs":[],"inputs":[{"type":"string","name":"_name"},{"type":"string","name":"_symbol"},{"type":"uint256","name":"_decimals"},{"type":"uint256","name":"_supply"}],"constant":false,"payable":false,"type":"constructor"},{"name":"topBurninators","outputs":[{"type":"address[10]","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":3937},{"name":"totalSupply","outputs":[{"type":"uint256","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":513},{"name":"allowance","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"address","name":"_owner"},{"type":"address","name":"_spender"}],"constant":true,"payable":false,"type":"function","gas":875},{"name":"transfer","outputs":[{"type":"bool","name":"out"}],"inputs":[{"type":"address","name":"_to"},{"type":"uint256","name":"_value"}],"constant":false,"payable":false,"type":"function","gas":74104},{"name":"transferFrom","outputs":[{"type":"bool","name":"out"}],"inputs":[{"type":"address","name":"_from"},{"type":"address","name":"_to"},{"type":"uint256","name":"_value"}],"constant":false,"payable":false,"type":"function","gas":109977},{"name":"approve","outputs":[{"type":"bool","name":"out"}],"inputs":[{"type":"address","name":"_spender"},{"type":"uint256","name":"_value"}],"constant":false,"payable":false,"type":"function","gas":37839},{"name":"mint","outputs":[],"inputs":[{"type":"address","name":"_to"},{"type":"uint256","name":"_value"}],"constant":false,"payable":false,"type":"function","gas":74668},{"name":"burn","outputs":[],"inputs":[{"type":"uint256","name":"_value"}],"constant":false,"payable":false,"type":"function","gas":110620},{"name":"burnFrom","outputs":[],"inputs":[{"type":"address","name":"_to"},{"type":"uint256","name":"_value"}],"constant":false,"payable":false,"type":"function","gas":146501},{"name":"claimVictory","outputs":[{"type":"bool","name":"out"}],"inputs":[],"constant":false,"payable":false,"type":"function","gas":54489},{"name":"name","outputs":[{"type":"string","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":11757},{"name":"symbol","outputs":[{"type":"string","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":6642},{"name":"decimals","outputs":[{"type":"uint256","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":873},{"name":"balanceOf","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"address","name":"arg0"}],"constant":true,"payable":false,"type":"function","gas":1075},{"name":"burninatedBy","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"address","name":"arg0"}],"constant":true,"payable":false,"type":"function","gas":1105}]
    '''
