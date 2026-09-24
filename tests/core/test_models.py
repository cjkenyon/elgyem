import pytest
from pydantic import ValidationError

from elgyem.core.models import (
    Card,
    Deck,
    EmptyDeckError,
    Hand,
    PrizeDoesNotExist,
    Prizes,
)


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


def test_deck_stack(deck):
    card = Card(name="foo")
    deck.stack(card)
    assert deck.draw(1).pop() == card


def test_deck_push(deck):
    card = Card(name="foo")
    deck.push(card)
    assert deck.draw(len(deck)).pop() == card


def test_hand_push():
    hand = Hand()
    assert len(hand) == 0
    hand.push(Card(name="foo"))
    assert len(hand) == 1


def test_prizes_init():
    prizes = Prizes()
    assert len(prizes) == 0


def test_prizes_init_with_greater_than_6_cards():
    with pytest.raises(ValidationError):
        Prizes(cards=[Card(name="foo")] * 7)


def test_prizes_init_with_greater():
    with pytest.raises(ValidationError):
        Prizes(cards=[Card(name="foo")] * 7)


def test_prizes_pop():
    cards = [Card(name="foo")] * 6
    prizes = Prizes(cards=cards)

    assert prizes.pop(0) == cards[0]
    assert len(prizes) == 5
    assert prizes.pop(4) == cards[5]
    with pytest.raises(PrizeDoesNotExist):
        prizes.pop(4)
