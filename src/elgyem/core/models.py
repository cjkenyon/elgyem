import random
from enum import Enum
from pathlib import Path
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Energy(Enum):
    FIRE = "FIRE"
    WATER = "WATER"
    GRASS = "GRASS"
    COLORLESS = "COLORLESS"


class Stage(Enum):
    BASIC = "BASIC"
    STAGE_1 = "STAGE_1"
    STAGE_2 = "STAGE_2"


class Attack(BaseModel):
    name: str
    cost: list[Energy]
    text: str
    damage: int


class Card(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    name: str


class PokemonCard(Card):
    hp: int
    type: Energy
    stage: Stage
    attacks: list[Attack]
    retreat_cost: list[Energy]


class TrainerType(Enum):
    SUPPORTER = "SUPPORTER"
    ITEM = "ITEM"
    STADIUM = "STADIUM"


class TrainerCard(Card):
    text: str
    type: TrainerType


class EnergyType(Enum):
    BASIC = "BASIC"
    SPECIAL = "SPECIAL"


class EnergyCard(Card):
    cost: list[Energy]
    type: EnergyType
    text: str


class EmptyDeckError(Exception):
    pass


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
                cards.append(Card.model_validate_json(line))
        return cls(cards=cards)

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


class CardDoesNotExist(Exception):
    pass


class PrizeCards(BaseModel):
    cards: list[Card] = Field(default_factory=list, max_length=6)

    def __len__(self) -> int:
        return len(self.cards)

    def pop(self, position: int) -> Card:
        try:
            return self.cards.pop(position)
        except IndexError:
            raise CardDoesNotExist


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
            raise CardDoesNotExist


class Player(BaseModel):
    deck: Deck = Field(default_factory=Deck)
    hand: Hand = Field(default_factory=Hand)
    prize_cards: PrizeCards = Field(default_factory=PrizeCards)
    bench: Bench = Field(default_factory=Bench)
    active: PokemonCard | None = None
