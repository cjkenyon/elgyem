from elgyem.core.actions import Action, ChooseActiveFromHand
from elgyem.core.models import CardNotFound, Game, Phase, PokemonCard, SetupStep, Stage
from elgyem.core.rules import STARTING_HAND_SIZE


class InvalidAction(Exception):
    pass


class InvalidPhase(Exception):
    pass


class Engine:
    def __init__(self):
        pass

    def setup(self, game: Game) -> Game:
        if game.phase != Phase.SETUP:
            raise InvalidPhase("The game must be in the setup phase to call setup.")

        for player in game.players:
            has_basic = False
            mulligans = 0
            while True:
                player.deck.shuffle()
                for card in player.deck.draw(STARTING_HAND_SIZE):
                    print(card)
                    print(isinstance(card, PokemonCard))
                    if isinstance(card, PokemonCard) and card.stage == Stage.BASIC:
                        has_basic = True
                    player.hand.push(card)

                if has_basic:
                    break
                mulligans += 1

                while len(player.hand) > 0:
                    player.deck.stack(player.hand.pop())

            player.mulligans = mulligans

        game.setup_step = SetupStep.CHOOSE_ACTIVE
        return game

    def execute(self, game: Game, action: Action) -> Game:
        if game.get_current_player().uuid != action.player:
            raise InvalidAction

        match action:
            case ChooseActiveFromHand():
                return self._choose_active_from_hand(game, action)
            case _:
                raise InvalidAction

    def _choose_active_from_hand(
        self, game: Game, action: ChooseActiveFromHand
    ) -> Game:
        player = game.get_player(action.player)
        # if we are setting up the game, the card pokemon must come from the players hand
        if game.turn != 0:
            raise InvalidAction
            # ensure the card exists in the hand
        try:
            pokemon = player.hand.peek(action.pokemon)
        except CardNotFound:
            raise InvalidAction

        # ensure the card is a basic pokemon
        if not isinstance(pokemon, PokemonCard) or pokemon.stage != Stage.BASIC:
            raise InvalidAction

        player.hand.remove(action.pokemon)

        player.active = pokemon

        return game
