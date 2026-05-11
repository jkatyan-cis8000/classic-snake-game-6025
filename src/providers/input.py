from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

from src.types.types import Direction, Position


class InputProvider(ABC):
    """Base class for input handling."""
    
    @abstractmethod
    def get_direction(self) -> Direction | None:
        """Get current direction input, or None if no input."""
        pass
    
    @abstractmethod
    def handle_key(self, key: str) -> Direction | None:
        """Process a key press and return direction if valid."""
        pass


class StandardInputProvider(InputProvider):
    """Standard keyboard input provider using input()"""
    
    def __init__(self) -> None:
        self._pending_direction: Direction | None = None
    
    def get_direction(self) -> Direction | None:
        """Get current direction input."""
        return self._pending_direction
    
    def handle_key(self, key: str) -> Direction | None:
        """Process a key press and return direction if valid."""
        key = key.lower().strip()
        if key in ("w", "arrow_up", "\x1b[A"):
            self._pending_direction = Direction.UP
        elif key in ("s", "arrow_down", "\x1b[B"):
            self._pending_direction = Direction.DOWN
        elif key in ("a", "arrow_left", "\x1b[D"):
            self._pending_direction = Direction.LEFT
        elif key in ("d", "arrow_right", "\x1b[C"):
            self._pending_direction = Direction.RIGHT
        else:
            self._pending_direction = None
        return self._pending_direction
