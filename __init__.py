from shadowlands.sl_dapp import SLDapp
from shadowlands.sl_frame import SLFrame
from shadowlands.sl_contract.erc20 import Erc20
from decimal import Decimal
from shadowlands.tui.debug import debug, end_debug
import pdb

class Dapp(SLDapp):
    def initialize(self):
        self.peasant_contract = Erc20(self.node, address='peasantcoin.eth')
        self.peasants = Decimal(self.peasant_contract.my_balance() / (10 ** 18))
        self.total_peasants =  Decimal( 
            (self.peasant_contract.totalSupply() - self.peasant_contract.functions.balanceOf('deadbeef.burninator.eth').call() ) / (10 ** 18)
        )
        self.add_frame(MyMenuFrame, height=12, width=70, title="Trogdooooor!")

class MyMenuFrame(SLFrame):
    def initialize(self):
        self.add_label("Trogdor the wingaling dragon intends to burninate peasants.")
        self.add_label("There are {} peasants (PSNT) in the world.".format(
            self.peasant_decorator(self.dapp.total_peasants)
        ))
        self.add_label("Trogdor has {} peasants.".format(
            self.peasant_decorator(self.dapp.peasants)
        ))
        self.text_value = self.add_textbox("How many to burninate?", default_value=' ')
        self.add_divider()
        self.add_button_row([
            ("Burninate!", self.burninate, 0),
            ("Get More Peasants", self.get_peasants, 1),
            ("Close", self.close, 2)
        ], layout=[30, 40, 30]
        )

    def get_peasants(self):
        self.dapp.add_uniswap_frame(self.dapp.peasant_contract.address)

    def peasant_decorator(self, peasants):
        return "{:f}".format(peasants)[:15]

    def peasants_validated(self):
        try:
            self.peasants_to_burninate = Decimal(self.text_value())
        except:
            self.dapp.add_message_dialog("That number of peasants doesn't make sense.")
            return False

        if self.peasants_to_burninate > 100000:   
            self.dapp.add_message_dialog("You monster! Leave some for later.")
            return False
        elif self.peasants_to_burninate > self.dapp.peasants:
            self.dapp.add_message_dialog("You don't even *have* that many peasants!")
            return False
        elif self.peasants_to_burninate < 0.5:
            self.dapp.add_message_dialog("This will not satisfy Trogdor.")
            return False

        return True


    def burninate(self):
        if not self.peasants_validated():
            return

        peasantcoins_to_burninate = self.peasants_to_burninate * Decimal(10 ** 18)

        burn_fn = self.dapp.peasant_contract.transfer(
            'deadbeef.burninator.eth',
            int(peasantcoins_to_burninate)
        )

        self.dapp.add_transaction_dialog(
            burn_fn, 
            title="Trogdor burninates the peasantcoins", 
            gas_limit=56000
        )

        self.close()

