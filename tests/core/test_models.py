import pytest

from elgyem.core.models import Deck, EmptyDeckError


@pytest.fixture(scope="session")
def deck():
    return Deck.from_jsonl("./tests/data/fire_deck.jsonl")


def test_shuffle(deck):
    before = deck.cards.copy()
    deck.shuffle()
    assert before != deck.cards


def test_draw_1(deck):
    before = len(deck)
    assert len(deck.draw(1)) == 1
    assert len(deck) == before - 1


def test_draw_2(deck):
    before = len(deck)
    assert len(deck.draw(2)) == 2
    assert len(deck) == before - 2


def test_draw_deckout(deck):
    with pytest.raises(EmptyDeckError):
        deck.draw(len(deck) + 1)
