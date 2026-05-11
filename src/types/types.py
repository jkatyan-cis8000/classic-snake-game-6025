from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import NewType, Protocol


@dataclass(frozen=True)
class Position:
    x: int
    y: int


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


Snake = NewType("Snake", list[Position])
Food = NewType("Food", Position)


class GameState(Enum):
    RUNNING = "RUNNING"
    GAME_OVER = "GAME_OVER"
    PAUSED = "PAUSED"


Score = NewType("Score", int)


class InputProvider(Protocol):
    def get_direction(self) -> Direction | None:
        ...

    def handle_key(self, key: str) -> Direction | None:
        ...


class TimeProvider(Protocol):
    def sleep(self, ms: int) -> None:
        ...

    def current_time_ms(self) -> int:
        ...


class RandomProvider(Protocol):
    def random_position(self, exclude: list[Position]) -> Position:
        ...
