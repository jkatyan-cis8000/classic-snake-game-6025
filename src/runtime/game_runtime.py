from __future__ import annotations

from src.config.constants import DIFFICULTY_SPEEDS, Settings
from src.config.settings import Score
from src.types.types import GameState
from src.providers.input import StandardInputProvider
from src.providers.random import StandardRandomProvider
from src.providers.time import StandardTimeProvider
from src.repo.file_highscore import FileHighScoreRepository
from src.service.classic_game import ClassicSnakeGame
from src.ui.terminal_renderer import TerminalRenderer


class GameRuntime:
    """Runtime controller for the snake game."""
    
    def __init__(self, difficulty: str = "medium") -> None:
        grid_size = 20
        base_speed = DIFFICULTY_SPEEDS.get(difficulty, 150)
        
        self._settings = Settings(
            difficulty=difficulty,
            grid_size=grid_size,
            base_speed_ms=base_speed,
        )
        
        self._input = StandardInputProvider()
        self._time = StandardTimeProvider()
        self._random = StandardRandomProvider(grid_size=grid_size)
        self._highscore_repo = FileHighScoreRepository()
        
        self._game = ClassicSnakeGame(
            settings=self._settings,
            input_provider=self._input,
            time_provider=self._time,
            random_provider=self._random,
            highscore_repo=self._highscore_repo,
        )
        
        self._renderer = TerminalRenderer(grid_size=grid_size)
    
    def run(self) -> None:
        """Run the game loop."""
        self._game.start()
        
        while True:
            if self._game.get_state() == GameState.GAME_OVER:
                high_score = self._highscore_repo.get_high_score()
                self._renderer.show_game_over(self._game.get_score(), high_score)
                # Restart
                self._game = ClassicSnakeGame(
                    settings=self._settings,
                    input_provider=self._input,
                    time_provider=self._time,
                    random_provider=self._random,
                    highscore_repo=self._highscore_repo,
                )
                self._game.start()
                continue
            
            # Update game
            self._game.update()
            
            # Render
            self._renderer.render(
                snake=self._game.get_snake(),
                food=self._game.get_food(),
                score=self._game.get_score(),
                state=self._game.get_state(),
            )
            
            # Sleep
            self._time.sleep(100)
            
            # Handle input
            try:
                key = input("\nEnter direction (w/a/s/d or arrow keys): ")
                if key:
                    direction = self._input.handle_key(key)
                    if direction:
                        self._game.set_direction(direction)
            except EOFError:
                break
