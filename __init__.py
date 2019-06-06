from shadowlands.sl_dapp import SLDapp
from shadowlands.sl_frame import SLFrame
from burninator.peasant_coin import PeasantCoin
from decimal import Decimal
from shadowlands.tui.debug import debug, end_debug
import pdb

class Dapp(SLDapp):
    def initialize(self):
        self.token = PeasantCoin(self.node)
        self.peasants = Decimal(self.token.my_balance() / (10 ** 18))
        self.total_peasants =  self.token.totalSupply() / (10 ** 18)
        self.my_burninated_peasants = self.token.burninatedBy(self.node.credstick.address) / (10 ** 18)
        self.add_sl_frame(MyMenuFrame(self, height=24, width=74 ))

        if self.token.victorious():
            self.add_sl_frame(VictoryFrame(self, height=9, width=62, title="Victory!!!"))


class MyMenuFrame(SLFrame):
    def initialize(self):
        self.add_label("The Hall Of Maximum Burnination", add_divider=False)
        self.add_divider(draw_line=True)
        self.add_label("Rank    Peasants           Hero", add_divider=False)

        for heroes in self.top_burninators_decorator():
            self.add_label(heroes, add_divider=False)
        self.add_divider(draw_line=True)

        self.add_label("Trogdor the wingaling dragon intends to burninate peasants.", add_divider=False)
        self.add_label("There are {} peasants (BRNT) in the world.".format(self.peasant_decorator(self.dapp.total_peasants)))
        self.add_label("Trogdor has {} peasants, and has burninated {}".format(self.peasant_decorator(self.dapp.peasants), self.peasant_decorator(self.dapp.my_burninated_peasants)))
        self.text_value = self.add_textbox("How many to burninate?", default_value=' ')
        self.add_button_row([
            ("Burninate!", self.burninate, 0),
            ("Get More Peasants", self.get_peasants, 1),
            ("Close", self.close, 2)
        ], layout=[30, 40, 30]
        )

        
    def top_burninators_decorator(self):
        burninators = self.dapp.token.top_burninators()
        i = 0 
        heroes = []

        #debug(); pdb.set_trace()
        for hero in burninators:
            hero_name = self.dapp.node._ns.name(hero[0])
            if hero_name is None:
                hero_name = hero[0]
            heroes.append("{}       {:14s}     {}".format(i, self.peasant_decorator(hero[1]), hero_name))
            i += 1 

        if len(heroes) < 10:
            for x in range(len(heroes), 10):
                heroes.append(
                    "{}       Unclaimed".format(str(x)))

        return heroes

    def peasant_decorator(self, peasants):
        return "{:f}".format(peasants)[:14]


    def get_peasants(self):
        self.dapp.add_uniswap_frame(self.dapp.token.address)

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

class VictoryFrame(SLFrame):
    def initialize(self):
        self.add_label("Congratulations!  You have racked up a truly impressive", add_divider=False)
        self.add_label("count of {} burninated peasants, as well".format(self.peasant_decorator(self.dapp.my_burninated_peasants)), add_divider=False)
        self.add_label("as several incinerated thatched roof cottages and various", add_divider=False)
        self.add_label("counts of petty theft and vandalism.  Your throne in the", add_divider=False)
        self.add_label("Hall of Maximum Burnination awaits your Dragonly Personage!")
        self.add_button_row(
            [("Claim Victoriousness", self.claim_victory, 0),
            ("Back", self.close, 1)],
            layout=[50, 50],
        )

    def claim_victory(self):
        self.dapp.add_transaction_dialog(
            self.dapp.token.claimVictory(), 
            title="Claiming victory", 
            gas_limit=100000
        )
        self.close()

    def peasant_decorator(self, peasants):
        return "{:f}".format(peasants)[:14]

