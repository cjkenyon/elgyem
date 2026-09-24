from elgyem.core.actions import ChooseActiveFromHand


def test_engine_choose_active_at_start_of_game(engine, new_game, dreepy_asc_158):
    active_player = new_game.get_current_player()
    active_player.hand.push(dreepy_asc_158)
    new_game_state = engine.execute(
        new_game,
        ChooseActiveFromHand(player=active_player.uuid, pokemon=dreepy_asc_158.uuid),
    )

    assert new_game_state.get_current_player().active == dreepy_asc_158
