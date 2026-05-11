from __future__ import annotations

import os
from pathlib import Path

from src.repo.highscore import HighScoreRepository
from src.types.types import Score


class FileHighScoreRepository(HighScoreRepository):
    """File-based high score repository using data/scores.txt"""
    
    def __init__(self, data_dir: str = "data", filename: str = "scores.txt") -> None:
        self._filepath = Path(data_dir) / filename
    
    def get_high_score(self) -> Score:
        """Get the current high score from file."""
        if not self._filepath.exists():
            return Score(0)
        try:
            content = self._filepath.read_text().strip()
            return Score(int(content))
        except (ValueError, OSError):
            return Score(0)
    
    def save_high_score(self, score: Score) -> None:
        """Save a new high score if it beats the current one."""
        current = self.get_high_score()
        if score > current:
            self._filepath.parent.mkdir(parents=True, exist_ok=True)
            self._filepath.write_text(str(score))
