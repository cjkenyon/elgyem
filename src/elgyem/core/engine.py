from elgyem.core.actions import Action, ChooseActiveFromHand
from elgyem.core.models import CardNotFound, Game, PokemonCard, Stage


class InvalidAction(Exception):
    pass


class Engine:
    def __init__(self):
        pass

    def execute(self, game: Game, action: Action) -> Game:
        new_game_state = game.model_copy(deep=True)

        if game.get_current_player().uuid != action.player:
            raise InvalidAction

        match action:
            case ChooseActiveFromHand():
                return self._choose_active_from_hand(new_game_state, action)
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
