
import random
from handeval import evalhand


class PokerGame:
    def __init__(self, player_chips=1000, bot_chips=1000, min_raise=20, sb=10, bb=20):
        self.starting_player_chips = player_chips
        self.starting_bot_chips = bot_chips

        self.player_chips = player_chips
        self.bot_chips = bot_chips

        self.min_raise = min_raise
        self.sb = sb
        self.bb = bb
        self.deck = []
        self.player_cards = []
        self.bot_cards = []
        self.community_cards = []

        self.pot = 0
        self.current_bet = 0
        self.player_round_bet = 0
        self.bot_round_bet = 0

        self.stage = "preflop"
        self.finished = False
        self.winner = None
        self._pot_awarded = False
        self.message = "Your turn."

        # Betting-round state
        self.player_acted = False
        self.bot_acted = False
        self.hand_started = False
        self.hand_recorded = False

    def start_hand(self, card_names):
        """Start a fresh hand using the available card names."""

        # Check whether the game is over BEFORE posting blinds.
        if self.player_chips <= 0 or self.bot_chips <= 0:
            self.finished = True
            self.stage = "game_over"
            self.winner = (
                "bot" if self.player_chips <= 0 else "player"
            )
            self.message = (
                "Game over! "
                + ("Bot wins!" if self.winner == "bot" else "You win!")
            )
            return

        self.deck = list(card_names)
        random.shuffle(self.deck)

        if len(self.deck) < 9:
            raise ValueError("The deck must contain at least 9 unique cards.")

        self.player_cards = [self.deck.pop(), self.deck.pop()]
        self.bot_cards = [self.deck.pop(), self.deck.pop()]
        self.community_cards = []

        self.pot = 0
        self._pot_awarded = False
        self.current_bet = 0
        self.player_round_bet = 0
        self.bot_round_bet = 0

        # Post the small blind.
        player_blind = min(self.sb, self.player_chips)
        self.player_chips -= player_blind
        self.player_round_bet = player_blind
        self.pot += player_blind

        # Post the big blind.
        bot_blind = min(self.bb, self.bot_chips)
        self.bot_chips -= bot_blind
        self.bot_round_bet = bot_blind
        self.pot += bot_blind

        self.current_bet = max(
            self.player_round_bet,
            self.bot_round_bet
        )

        self.stage = "preflop"
        self.finished = False
        self.winner = None

        self.player_acted = False
        self.bot_acted = False
        self.hand_started = True
        self.hand_recorded  = False

        self.message = "Preflop: your turn."

    def amount_to_call(self):
        return max(0, self.current_bet - self.player_round_bet)

    def fold(self):
        if self.finished:
            return

        self.award_pot("bot")
        self.message = "You folded. The bot wins the pot."

    def checkcall(self):
        if self.finished:
            return

        amount = self.amount_to_call()
        paid = min(amount, self.player_chips)

        self.player_chips -= paid
        self.player_round_bet += paid
        self.pot += paid

        self.player_acted = True

        if amount == 0:
            self.message = "You checked."
        elif paid < amount:
            self.message = "You called all-in."
        else:
            self.message = f"You called {paid} chips."
        self._advance_if_ready()

    def raise_bet(self, multiplier):
        if self.finished:
            return

        if multiplier <= 0:
            self.message = "Invalid raise size."
            return

        call_amount = self.amount_to_call()

        # Must be able to cover the call before raising
        if self.player_chips <= call_amount:
            self.message = "Not enough chips to raise."
            return

        raise_size = max(
            self.min_raise,
            round((self.pot + call_amount) * multiplier)
        )

        available_for_raise = self.player_chips - call_amount
        raise_size = min(raise_size, available_for_raise)

        total_payment = call_amount + raise_size

        self.player_chips -= total_payment
        self.player_round_bet += total_payment
        self.pot += total_payment

        self.current_bet = self.player_round_bet

        self.player_acted = True
        self.bot_acted = False

        if raise_size < self.min_raise:
            self.message = "You raised all-in for less than the minimum."
        else:
            self.message = f"You raised by {raise_size} chips."

    def all_in(self):
        if self.finished or self.player_chips <= 0:
            return

        paid = self.player_chips
        self.player_chips = 0

        self.player_round_bet += paid
        self.pot += paid

        if self.player_round_bet > self.current_bet:
            self.current_bet = self.player_round_bet
            self.bot_acted = False

        self.player_acted = True
        self.message = f"You went all-in for {paid} chips."

    def reveal_next_stage(self):
        """Reveal community cards and reset round betting."""
        if self.finished:
            return

        if self.stage == "preflop":
            self.community_cards.extend(
                [self.deck.pop(), self.deck.pop(), self.deck.pop()])
            self.stage = "flop"

        elif self.stage == "flop":
            self.community_cards.append(self.deck.pop())
            self.stage = "turn"

        elif self.stage == "turn":
            self.community_cards.append(self.deck.pop())
            self.stage = "river"

        elif self.stage == "river":
            self._runout_to_showdown()
            return

        self.player_round_bet = 0
        self.bot_round_bet = 0
        self.current_bet = 0

        self.player_acted = False
        self.bot_acted = False

        self.message = f"{self.stage.capitalize()}: your turn."

    def award_pot(self, winner):
        """Award the pot to 'player' or 'bot'."""
        if self.finished and self.stage != "showdown":
            return

        if winner == "player":
            self.player_chips += self.pot
        else:
            self.bot_chips += self.pot

        self.winner = winner
        self.pot = 0
        self._pot_awarded = True
        self.finished = True
        self.message = f"{winner.capitalize()} wins the hand."

    def bot_response(self):
        if self.finished or self.bot_acted:
            return

        amount_to_call = max(0, self.current_bet - self.bot_round_bet)

        if amount_to_call == 0:
            # Usually check; occasionally raise.
            if self.bot_chips > self.min_raise and random.random() < 0.20:
                raise_size = min(
                    max(self.min_raise, round((self.pot or self.min_raise) * 0.5)),
                    self.bot_chips
                )

                self.bot_chips -= raise_size
                self.bot_round_bet += raise_size
                self.pot += raise_size
                self.current_bet = self.bot_round_bet
                self.player_acted = False
                self.bot_acted = True
                self.message = f"Bot raises by {raise_size} chips."
                return

            self.bot_acted = True
            self.message = "Bot checks."

        else:
            # Define the threshold before using it.
            fold_threshold = max(100, self.pot * 0.75)

            if amount_to_call > fold_threshold and random.random() < 0.35:
                self.award_pot("player")
                self.message = "Bot folds. You win the pot."
                return

            # Call as much as the bot can afford.
            paid = min(amount_to_call, self.bot_chips)

            self.bot_chips -= paid
            self.bot_round_bet += paid
            self.pot += paid
            self.bot_acted = True

            if paid < amount_to_call:
                self.message = "Bot calls all-in."
            else:
                self.message = f"Bot calls {paid} chips."
        self._advance_if_ready()

    def _runout_to_showdown(self):
        """Reveal remaining cards, evaluate hands and settle the pot."""
        if self.finished or self.stage == "showdown":
            return

        while len(self.community_cards) < 5:
            self.community_cards.append(self.deck.pop())

        self.stage = "showdown"

        player_hand = self.player_cards + self.community_cards
        bot_hand = self.bot_cards + self.community_cards

        player_score = evalhand(player_hand)
        bot_score = evalhand(bot_hand)

        if player_score > bot_score:
            self.award_pot("player")

        elif bot_score > player_score:
            self.award_pot("bot")

        else:
            split_amount = self.pot // 2
            remainder = self.pot % 2

            self.player_chips += split_amount + remainder
            self.bot_chips += split_amount

            self.pot = 0
            self.winner = "tie"
            self._pot_awarded = True
            self.finished = True
            self.message = "Tie! The pot is split."

        print("Player hand score:", player_score)
        print("Bot hand score:", bot_score)
        print("Player chips:", self.player_chips)
        print("Bot chips:", self.bot_chips)

    def _advance_if_ready(self):
        """Advance only when betting is settled."""
        if self.finished:
            return

        if not (self.player_acted and self.bot_acted):
            return

        if self.player_chips == 0 or self.bot_chips == 0:
            self._runout_to_showdown()
            return
        if self.player_round_bet != self.bot_round_bet:
            return

        # Otherwise, advance automatically to the next street.
        self.reveal_next_stage()
