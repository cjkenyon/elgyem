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


def test_shuffle(full_deck):
    before = full_deck.cards.copy()
    full_deck.shuffle()
    assert before != full_deck.cards


def test_draw_1(full_deck):
    before = len(full_deck)
    assert len(full_deck.draw(1)) == 1
    assert len(full_deck) == before - 1


def test_draw_2(full_deck):
    before = len(full_deck)
    assert len(full_deck.draw(2)) == 2
    assert len(full_deck) == before - 2


def test_draw_full_deckout(full_deck):
    with pytest.raises(EmptyDeckError):
        full_deck.draw(len(full_deck) + 1)


def test_full_deck_stack(full_deck):
    card = Card(name="foo")
    full_deck.stack(card)
    assert full_deck.draw(1).pop() == card


def test_full_deck_push(full_deck):
    card = Card(name="foo")
    full_deck.push(card)
    assert full_deck.draw(len(full_deck)).pop() == card


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
