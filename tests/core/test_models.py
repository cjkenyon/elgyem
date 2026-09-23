import pytest

from elgyem.core.models import Card, Deck, EmptyDeckError


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


def test_stack(deck):
    card = Card(name="foo")
    deck.stack(card)
    assert deck.draw(1).pop() == card


def test_push(deck):
    card = Card(name="foo")
    deck.push(card)
    assert deck.draw(len(deck)).pop() == card
