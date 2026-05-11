from __future__ import annotations

from abc import ABC, abstractmethod

from src.types.types import Direction, Food, GameState, Position, Score, Snake


class SnakeGame(ABC):
    """Core game logic interface."""
    
    @abstractmethod
    def start(self) -> None:
        """Start the game."""
        pass
    
    @abstractmethod
    def stop(self) -> None:
        """Stop the game."""
        pass
    
    @abstractmethod
    def pause(self) -> None:
        """Pause the game."""
        pass
    
    @abstractmethod
    def resume(self) -> None:
        """Resume the game."""
        pass
    
    @abstractmethod
    def update(self) -> None:
        """Update game state."""
        pass
    
    @abstractmethod
    def set_direction(self, direction: Direction) -> None:
        """Set snake direction."""
        pass
    
    @abstractmethod
    def get_snake(self) -> Snake:
        """Get current snake position."""
        pass
    
    @abstractmethod
    def get_food(self) -> Food:
        """Get current food position."""
        pass
    
    @abstractmethod
    def get_score(self) -> Score:
        """Get current score."""
        pass
    
    @abstractmethod
    def get_state(self) -> GameState:
        """Get current game state."""
        pass
    
    @abstractmethod
    def get_grid_size(self) -> int:
        """Get grid size."""
        pass
