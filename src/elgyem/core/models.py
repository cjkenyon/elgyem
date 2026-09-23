from enum import Enum

from pydantic import BaseModel


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
    cost: list[EnergyType]
    type: EnergyType
    text: str


class Deck(BaseModel):
    cards: list[Card]
