import pytest
from pydantic import ValidationError

from elgyem.core.models import (
    Bench,
    BenchFullError,
    Card,
    CardNotFound,
    EmptyDeckError,
    Game,
    Hand,
    Player,
    PrizeCards,
)


def test_shuffle(dreepy_deck):
    before = dreepy_deck.cards.copy()
    dreepy_deck.shuffle()
    assert before != dreepy_deck.cards


def test_draw_1(dreepy_deck):
    before = len(dreepy_deck)
    assert len(dreepy_deck.draw(1)) == 1
    assert len(dreepy_deck) == before - 1


def test_draw_2(dreepy_deck):
    before = len(dreepy_deck)
    assert len(dreepy_deck.draw(2)) == 2
    assert len(dreepy_deck) == before - 2


def test_draw_dreepy_deckout(dreepy_deck):
    with pytest.raises(EmptyDeckError):
        dreepy_deck.draw(len(dreepy_deck) + 1)


def test_dreepy_deck_stack(dreepy_deck):
    card = Card(name="foo")
    dreepy_deck.stack(card)
    assert dreepy_deck.draw(1).pop() == card


def test_dreepy_deck_push(dreepy_deck):
    card = Card(name="foo")
    dreepy_deck.push(card)
    assert dreepy_deck.draw(len(dreepy_deck)).pop() == card


def test_hand_push():
    hand = Hand()
    assert len(hand) == 0
    hand.push(Card(name="foo"))
    assert len(hand) == 1


def test_prizes_init():
    prizes = PrizeCards()
    assert len(prizes) == 0


def test_prizes_init_with_greater_than_6_cards():
    with pytest.raises(ValidationError):
        PrizeCards(cards=[Card(name="foo")] * 7)


def test_prizes_init_with_greater():
    with pytest.raises(ValidationError):
        PrizeCards(cards=[Card(name="foo")] * 7)


def test_prizes_pop():
    cards = [Card(name="foo")] * 6
    prizes = PrizeCards(cards=cards)

    assert prizes.pop(0) == cards[0]
    assert len(prizes) == 5
    assert prizes.pop(4) == cards[5]
    with pytest.raises(CardNotFound):
        prizes.pop(4)


def test_bench_init():
    bench = Bench()
    assert len(bench) == 0


def test_bench_push():
    bench = Bench()
    bench.push(Card(name="foo"))

    for _ in range(4):
        bench.push(Card(name="foo"))

    with pytest.raises(BenchFullError):
        bench.push(Card(name="foo"))


def test_player_init():
    Player()


def test_game_init():
    Game()
