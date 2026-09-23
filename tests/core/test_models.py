from elgyem.core.models import Deck


def test_deck_load_from_jsonl():
    Deck.from_jsonl("./tests/data/fire_deck.jsonl")
