"""This module enumerates all the actions a player could take"""

from uuid import UUID

from pydantic import BaseModel


class Action(BaseModel):
    player: UUID


class ChooseActiveFromHand(Action):
    pokemon: UUID
