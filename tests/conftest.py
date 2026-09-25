import pytest

from elgyem.core.engine import Engine
from elgyem.core.models import (
    Attack,
    Deck,
    Energy,
    Hand,
    PokemonCard,
    Stage,
    build_game,
)


@pytest.fixture(scope="session")
def full_deck():
    return Deck.from_jsonl("./tests/data/fire_deck.jsonl")


@pytest.fixture(scope="session")
def dreepy_deck():
    return Deck.from_jsonl("./tests/data/dreepy_deck.jsonl")


@pytest.fixture(scope="function")
def empty_hand():
    return Hand()


@pytest.fixture(scope="function")
def new_game(dreepy_deck):
    return build_game(dreepy_deck, dreepy_deck.model_copy(deep=True))


@pytest.fixture(scope="session")
def dreepy_asc_158():
    return PokemonCard(
        name="Dreepy",
        type=Energy.DRAGON,
        hp=70,
        stage=Stage.BASIC,
        attacks=[
            Attack(name="Petty Grudge", cost=[Energy.PSYCHIC], damage=40),
            Attack(name="Bite", cost=[Energy.FIRE, Energy.PSYCHIC], damage=40),
        ],
        retreat_cost=[Energy.COLORLESS],
    )


@pytest.fixture(scope="session")
def engine():
    return Engine()
