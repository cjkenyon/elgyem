import pytest

from elgyem.core.actions import ChooseActiveFromHand
from elgyem.core.engine import InvalidPhase
from elgyem.core.models import Game, Phase


def test_engine_choose_active_at_start_of_game(engine, dreepy_asc_158):
    new_game = Game()
    active_player = new_game.get_current_player()
    active_player.hand.push(dreepy_asc_158)
    new_game_state = engine.execute(
        new_game,
        ChooseActiveFromHand(player=active_player.uuid, pokemon=dreepy_asc_158.uuid),
    )

    assert new_game_state.get_current_player().active == dreepy_asc_158


def test_engine_setup_invalid_phase(engine, new_game):
    new_game.phase = Phase.MAIN
    with pytest.raises(InvalidPhase):
        engine.setup(new_game)


def test_engine_setup(engine, new_game):
    engine.setup(new_game)
