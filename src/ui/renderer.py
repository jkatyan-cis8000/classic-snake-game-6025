from __future__ import annotations

from src.types.types import GameState, Score

from abc import ABC, abstractmethod


class Renderer(ABC):
    """Renderer interface for UI output."""
    
    @abstractmethod
    def render(self, snake: list, food: tuple, score: Score, state: GameState) -> None:
        """Render the game state."""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear the screen."""
        pass
    
    @abstractmethod
    def show_game_over(self, score: Score, high_score: Score) -> None:
        """Show game over screen."""
        pass
