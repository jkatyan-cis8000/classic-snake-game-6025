from __future__ import annotations

import random
from abc import ABC, abstractmethod

from src.types.types import Position


class RandomProvider(ABC):
    """Base class for random number generation."""
    
    @abstractmethod
    def random_position(self, exclude: list[Position]) -> Position:
        """Generate a random position not in the exclude list."""
        pass


class StandardRandomProvider(RandomProvider):
    """Standard random provider using random module."""
    
    def __init__(self, grid_size: int = 20) -> None:
        self._grid_size = grid_size
    
    def random_position(self, exclude: list[Position]) -> Position:
        """Generate a random position not in the exclude list."""
        while True:
            pos = Position(x=random.randint(0, self._grid_size - 1), 
                          y=random.randint(0, self._grid_size - 1))
            if pos not in exclude:
                return pos
