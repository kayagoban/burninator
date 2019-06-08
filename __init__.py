from shadowlands.sl_dapp import SLDapp
from shadowlands.sl_frame import SLFrame
from burninator.peasant_coin import PeasantCoin
from decimal import Decimal
from cached_property import cached_property
from shadowlands.tui.debug import debug, end_debug
import logging
import pdb

class Dapp(SLDapp):
    def initialize(self):
        self.token = PeasantCoin(self.node)
        self.current_position = self.my_position
        self.victory_notification_has_been_seen = False
        self.add_sl_frame(MyMenuFrame(self, height=22, width=74, title="The Hall of Maximum Burnination" ))

    def new_block_callback(self):
        self.victory_check()
        self.check_for_rank_change()

    def victory_check(self):
        if self.victory_notification_has_been_seen:
            return

        if self.token.victorious():
            self.victory_notification_has_been_seen = True
            self.add_sl_frame(VictoryFrame(self, height=9, width=62, title="Victory!!!"))

    def check_for_rank_change(self):
        if self.current_position == self.my_position:
            # no change
            return
        elif self.current_position is None and self.my_position is not None:
            logging.info("Burninator rank change: {} to {}",format(str(self.current_position), str(self.my_position)))
            message = "Huzzah!  You have ascended to rank {}!".format(self.my_position)
            self.add_message_dialog(message)
            self.current_position = self.my_position
            return

        if self.current_position is not None and self.my_position is None:
            message = "D: You lost your seat in the Hall of Max.Burn!"
        else:
            change = self.current_position - self.my_position
            if change > 0:
                message = "Huzzah!  You have ascended to rank {}!".format(self.my_position)
            elif change < 0:
                message = "Sworded!  You have been cast down to rank {}.".format(self.my_position)

        self.add_message_dialog(message)
        self.current_position = self.my_position

    @cached_property
    def my_position(self):
        my_seat = [self.top_burninators.index(x) for x in self.top_burninators if x[0] == self.node.credstick.address]
        if len(my_seat) > 0:
            return my_seat[0]
        return None

    @cached_property
    def top_burninators(self):
        return self.token.top_burninators()

    @cached_property
    def total_peasants(self):
        return self.token.totalSupply() / (10 ** 18)

    @cached_property
    def my_burninated_peasants(self):
        return self.token.burninatedBy(self.node.credstick.address) / (10 ** 18)

    @cached_property
    def peasants(self):
        return Decimal(self.token.my_balance() / (10 ** 18))

    def peasant_decorator(self, peasants):
        return "{:f}".format(peasants)[:14]



class MyMenuFrame(SLFrame):
    def initialize(self):
        self.add_label("Rank    Peasants           Hero", add_divider=False)

        for i in range(10):
            self.add_label(self.burninator_hero(i), add_divider=False)
        self.add_divider(draw_line=True)

        self.add_label("Trogdor the wingaling dragon intends to burninate peasants.", add_divider=False)
        self.add_label(lambda: self.total_peasants_string)
        self.add_label(lambda: self.my_peasant_status_string)
        self.text_value = self.add_textbox("How many to burninate?", default_value=' ')
        self.add_button_row([
            ("Burninate!", self.burninate, 0),
            ("Get More Peasants", self.get_peasants, 1),
            ("Close", self.close, 2)
        ], layout=[30, 40, 30]
        )

    @cached_property
    def total_peasants_string(self):
        return "There are {} peasants (BRNT) in the world.".format(self.dapp.peasant_decorator(self.dapp.total_peasants))

    @cached_property
    def my_peasant_status_string(self):
        return "Trogdor has {} peasants, and has burninated {}".format(self.dapp.peasant_decorator(self.dapp.peasants), self.dapp.peasant_decorator(self.dapp.my_burninated_peasants))

    def burninator_hero(self, index):
        return lambda: self.top_burninators_decorator[index]
    
    @cached_property
    def top_burninators_decorator(self):
        i = 0 
        heroes = []

        for hero in self.dapp.top_burninators:
            hero_name = self.dapp.node._ns.name(hero[0]) or hero[0]
            heroes.append("{}       {:14s}     {}".format(i, self.dapp.peasant_decorator(hero[1]), hero_name))
            i += 1 

        if len(heroes) < 10:
            for x in range(len(heroes), 10):
                heroes.append(
                    "{}       Unclaimed".format(str(x)))

        return heroes


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


class VictoryFrame(SLFrame):
    def initialize(self):
        self.add_label("Huzzah!  You have racked up a truly impressive", add_divider=False)
        self.add_label("count of {} burninated peasants, as well".format(self.dapp.peasant_decorator(self.dapp.my_burninated_peasants)), add_divider=False)
        self.add_label("as several incinerated thatched roof cottages and various", add_divider=False)
        self.add_label("counts of petty theft and vandalism.  Your throne in the", add_divider=False)
        self.add_label("Hall of Maximum Burnination awaits your Dragonly Personage!")
        self.add_button_row(
            [("Claim your victory", self.claim_victory, 0),
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



