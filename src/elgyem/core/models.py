import json
import random
from enum import StrEnum
from pathlib import Path
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Energy(StrEnum):
    FIRE = "FIRE"
    PSYCHIC = "PSYCHIC"
    WATER = "WATER"
    GRASS = "GRASS"
    DRAGON = "DRAGON"
    COLORLESS = "COLORLESS"


class Stage(StrEnum):
    BASIC = "BASIC"
    STAGE_1 = "STAGE_1"
    STAGE_2 = "STAGE_2"


class Attack(BaseModel):
    name: str
    cost: list[Energy]
    text: str | None = None
    damage: int


class Card(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    name: str


class PokemonCard(Card):
    card_type: Literal["pokemon"] = "pokemon"

    hp: int
    type: Energy
    stage: Stage
    attacks: list[Attack]
    retreat_cost: list[Energy]
    weakness: Energy | None = None
    resistance: Energy | None = None


class TrainerType(StrEnum):
    SUPPORTER = "SUPPORTER"
    ITEM = "ITEM"
    STADIUM = "STADIUM"


class TrainerCard(Card):
    card_type: Literal["trainer"] = "trainer"

    text: str
    type: TrainerType


class EnergyType(StrEnum):
    BASIC = "BASIC"
    SPECIAL = "SPECIAL"


class EnergyCard(Card):
    card_type: Literal["energy"] = "energy"
    cost: list[Energy]
    type: EnergyType
    text: str | None = None


class EmptyDeckError(Exception):
    pass


CARD_TYPE = {
    "pokemon": PokemonCard,
    "trainer": TrainerCard,
    "energy": EnergyCard,
}


class Deck(BaseModel):
    cards: list[Card] = Field(default_factory=list)

    def __len__(self) -> int:
        return len(self.cards)

    @classmethod
    def from_jsonl(cls, path: str | Path) -> "Deck":
        cards = []
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                data = json.loads(line)
                card_type = data.pop("card_type")
                cards.append(CARD_TYPE[card_type].model_validate_json(line))
        return cls(cards=cards)

    def to_jsonl(self, path: str | Path):
        with open(path, "w") as f:
            f.writelines(card.model_dump_json() + "\n" for card in self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, count: int) -> list[Card]:

        if count > len(self):
            raise EmptyDeckError

        cards_drawn = self.cards[0:count]
        self.cards = self.cards[count:]
        return cards_drawn

    def stack(self, card: Card):
        self.cards.insert(0, card)

    def push(self, card: Card):
        self.cards.append(card)


class Hand(BaseModel):
    cards: list[Card] = Field(default_factory=list)

    def __len__(self) -> int:
        return len(self.cards)

    def push(self, card: Card):
        self.cards.append(card)

    def pop(self, index: int = 0):
        return self.cards.pop(index)

    def peek(self, uuid: UUID) -> Card:
        for card in self.cards:
            if card.uuid == uuid:
                return card
        raise CardNotFound

    def remove(self, uuid: UUID) -> Card:
        for i, card in enumerate(self.cards):
            if card.uuid == uuid:
                return self.cards.pop(i)
        raise CardNotFound


class CardNotFound(Exception):
    pass


class PrizeCards(BaseModel):
    cards: list[Card] = Field(default_factory=list, max_length=6)

    def __len__(self) -> int:
        return len(self.cards)

    def pop(self, position: int) -> Card:
        try:
            return self.cards.pop(position)
        except IndexError:
            raise CardNotFound


class BenchFullError(Exception):
    pass


DEFAULT_BENCH_SIZE: int = 5


class Bench(BaseModel):
    cards: list[Card] = Field(default_factory=list, max_length=DEFAULT_BENCH_SIZE)

    def __len__(self) -> int:
        return len(self.cards)

    def push(self, card: Card):
        if len(self) >= DEFAULT_BENCH_SIZE:
            raise BenchFullError

        self.cards.append(card)

    def pop(self, position: int) -> Card:
        try:
            return self.cards.pop(position)
        except IndexError:
            raise CardNotFound


class Player(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    deck: Deck = Field(default_factory=Deck)
    hand: Hand = Field(default_factory=Hand)
    prize_cards: PrizeCards = Field(default_factory=PrizeCards)
    bench: Bench = Field(default_factory=Bench)
    active: PokemonCard | None = None
    mulligans: int = 0


def _pair_of_players_factory() -> tuple[Player, Player]:
    return (Player(), Player())


class Phase(StrEnum):
    SETUP = "SETUP"
    DRAW = "DRAW"
    MAIN = "MAIN"
    ATTACK = "ATTACK"
    CHECKUP = "CHECKUP"
    GAME_OVER = "GAME_OVER"


class SetupStep(StrEnum):
    DRAW_HAND = "DRAW_HAND"
    CHOOSE_ACTIVE = "CHOOSE_ACTIVE"
    CHOOSE_BENCH = "CHOOSE_BENCH"
    COMPLETE = "COMPLETE"


class PlayerNotFound(Exception):
    pass


class Game(BaseModel):
    players: tuple[Player, Player] = Field(default_factory=_pair_of_players_factory)
    active_player: int = 0
    turn: int = 0
    phase: Phase = Phase.SETUP
    setup_step: SetupStep = SetupStep.DRAW_HAND

    def get_current_player(self) -> Player:
        return self.players[self.active_player]

    def get_player(self, uuid: UUID) -> Player:
        for player in self.players:
            if uuid == player.uuid:
                return player

        raise PlayerNotFound


def build_game(deck_a, deck_b) -> Game:
    game = Game()
    game.players[0].deck = deck_a
    game.players[1].deck = deck_b
    return game
