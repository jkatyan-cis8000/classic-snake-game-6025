from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Settings:
    """Game configuration settings."""
    difficulty: str
    grid_size: int
    base_speed_ms: int


# Difficulty multipliers for speed adjustment
DIFFICULTY_SPEEDS = {
    "easy": 200,    # Slower
    "medium": 150,  # Normal
    "hard": 100,    # Faster
}
