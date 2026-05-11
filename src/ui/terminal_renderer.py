from __future__ import annotations

import os
import sys
import time

from src.types.types import GameState, Score

from src.ui.renderer import Renderer


class TerminalRenderer(Renderer):
    """Terminal-based renderer for the snake game."""
    
    def __init__(self, grid_size: int = 20) -> None:
        self._grid_size = grid_size
        self._buffer: list[str] = []
    
    def render(self, snake: list, food: tuple, score: Score, state: GameState) -> None:
        """Render the game state to terminal."""
        self.clear()
        
        # Create grid
        grid = [["." for _ in range(self._grid_size)] for _ in range(self._grid_size)]
        
        # Place food
        grid[food[1]][food[0]] = "F"
        
        # Place snake
        for i, segment in enumerate(snake):
            if i == 0:
                grid[segment.y][segment.x] = "O"  # Head
            else:
                grid[segment.y][segment.x] = "o"  # Body
        
        # Draw top border
        self._buffer.append("+" + "-" * (self._grid_size * 2) + "+")
        
        # Draw grid
        for row in grid:
            self._buffer.append("| " + " ".join(row) + " |")
        
        # Draw bottom border
        self._buffer.append("+" + "-" * (self._grid_size * 2) + "+")
        
        # Draw score
        self._buffer.append(f"Score: {score}")
        
        if state == GameState.PAUSED:
            self._buffer.append("PAUSED - Press any key to resume")
        
        # Print all at once
        print("\n".join(self._buffer))
    
    def clear(self) -> None:
        """Clear the screen."""
        os.system("cls" if os.name == "nt" else "clear")
        self._buffer = []
    
    def show_game_over(self, score: Score, high_score: Score) -> None:
        """Show game over screen."""
        self.clear()
        print("\n" + "=" * 40)
        print("         GAME OVER!")
        print("=" * 40)
        print(f"  Final Score:  {score}")
        print(f"  High Score:   {high_score}")
        print("=" * 40)
        print("\n  Press any key to restart...")
        time.sleep(0.5)
        self.clear()
