from __future__ import annotations

from abc import ABC, abstractmethod

from src.types.types import Score


class HighScoreRepository(ABC):
    """Repository interface for high score persistence."""
    
    @abstractmethod
    def get_high_score(self) -> Score:
        """Get the current high score."""
        pass
    
    @abstractmethod
    def save_high_score(self, score: Score) -> None:
        """Save a new high score if it beats the current one."""
        pass
