from shadowlands.sl_dapp import SLDapp
from shadowlands.sl_frame import SLFrame
from burninator.peasant_coin import PeasantCoin
from decimal import Decimal
from shadowlands.tui.debug import debug, end_debug
import pdb

class Dapp(SLDapp):
    def initialize(self):
        #self.top_burninators = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.token = PeasantCoin(self.node)
        self.peasants = Decimal(self.token.my_balance() / (10 ** 18))
        self.total_peasants =  self.token.totalSupply() / (10 ** 18)
        self.my_burninated_peasants = self.token.burninatedBy(self.node.credstick.address) / (10 ** 18)
        self.add_frame(MyMenuFrame, height=19, width=74, title="Trogdooooor!")


class MyMenuFrame(SLFrame):
    def initialize(self):
        #self.claimVictory(9)
        #debug(); pdb.set_trace()
        self.add_label("The Hall Of Maximum Burnination", add_divider=False)
        self.add_divider(draw_line=True)
        for heroes in self.top_burninators_decorator():
            self.add_label(heroes)
        self.add_divider(draw_line=True)

        self.add_label("Trogdor the wingaling dragon intends to burninate peasants.", add_divider=False)
        self.add_label("There are {} peasants in the world.".format(self.peasant_decorator(self.dapp.total_peasants)))
        self.add_label("Trogdor has {} peasants, and has burninated {}".format(self.peasant_decorator(self.dapp.peasants), self.peasant_decorator(self.dapp.my_burninated_peasants)))
        self.text_value = self.add_textbox("How many to burninate?", default_value=' ')
        self.add_divider()
        self.add_button_row([
            ("Burninate!", self.burninate, 0),
            ("Get More Peasants", self.get_peasants, 1),
            ("Close", self.close, 2)
        ], layout=[30, 40, 30]
        )

        self.add_button(self.claim_victory, "Claim Victory!",)
        
    #def claimVictory(self, number):
    #    debug(); pdb.set_trace()
    #    weakest_burninator = 0
    #    for i in range(10):
    #        if number == self.dapp.top_burninators[i]:
    #            return True
    #        if self.dapp.top_burninators[weakest_burninator] > self.dapp.top_burninators[i]:
    #           weakest_burninator = i
    #    assert self.dapp.top_burninators[weakest_burninator] < number
    #    self.dapp.top_burninators[weakest_burninator] = number
    #    return True

    def top_burninators_decorator(self):
        burninators = self.dapp.token.top_burninators()
        i = 1 
        heroes = []

        debug(); pdb.set_trace()
        for hero in burninators:
            heroes.append("{}. {}\t{}".format(i, hero[0], self.peasant_decorator(self.hero[1])))
            i += 1

        return heroes
         

    def claim_victory(self):
        self.dapp.add_transaction_dialog(
            self.dapp.token.claimVictory(), 
            title="Trogdor burninates the tokens", 
            gas_limit=100000
        )


    def get_peasants(self):
        self.dapp.add_uniswap_frame(self.dapp.token.address)

    def peasant_decorator(self, peasants):
        return "{:f}".format(peasants)[:12]

    def peasants_validated(self):
        try:
            self.peasants_to_burninate = Decimal(self.text_value())
        except:
            self.dapp.add_message_dialog("That number of peasants doesn't make sense.")
            return False

        if self.peasants_to_burninate > self.dapp.peasants:
            self.dapp.add_message_dialog("You don't even *have* that many peasants!")
            return False
        elif self.peasants_to_burninate < 0.5:
            self.dapp.add_message_dialog("This will not satisfy Trogdor.")
            return False

        return True



    def burninate(self):
        if not self.peasants_validated():
            return

        tokens_to_burninate = self.peasants_to_burninate * Decimal(10 ** 18)

        burn_fn = self.dapp.token.burninate(
            int(tokens_to_burninate)
        )

        self.dapp.add_transaction_dialog(
            burn_fn, 
            title="Trogdor burninates the tokens", 
            gas_limit=56000
        )

        self.close()

