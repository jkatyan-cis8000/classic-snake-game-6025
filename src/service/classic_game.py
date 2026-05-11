from __future__ import annotations

from src.config.constants import Settings
from src.providers.input import InputProvider
from src.providers.random import RandomProvider
from src.providers.time import TimeProvider
from src.repo.highscore import HighScoreRepository
from src.types.types import Direction, Food, GameState, Position, Score, Snake
from src.service.game import SnakeGame
from src.providers.coords import is_within_bounds, move_position, opposite_directions, positions_equal


class ClassicSnakeGame(SnakeGame):
    """Classic snake game implementation."""
    
    def __init__(
        self,
        settings: Settings,
        input_provider: InputProvider,
        time_provider: TimeProvider,
        random_provider: RandomProvider,
        highscore_repo: HighScoreRepository,
    ) -> None:
        self._settings = settings
        self._input = input_provider
        self._time = time_provider
        self._random = random_provider
        self._highscore_repo = highscore_repo
        
        # Game state
        self._snake: Snake = Snake([Position(10, 10), Position(9, 10), Position(8, 10)])
        self._direction = Direction.RIGHT
        self._next_direction = Direction.RIGHT
        self._food = Food(Position(15, 10))
        self._score = Score(0)
        self._state = GameState.RUNNING
        self._grid_size = settings.grid_size
        self._last_move_time = 0
        self._speed = settings.base_speed_ms
    
    def start(self) -> None:
        """Start the game."""
        self._state = GameState.RUNNING
        self._last_move_time = self._time.current_time_ms()
        self._input.handle_key("")  # Initialize input
    
    def stop(self) -> None:
        """Stop the game and save high score."""
        self._state = GameState.GAME_OVER
        self._highscore_repo.save_high_score(self._score)
    
    def pause(self) -> None:
        """Pause the game."""
        if self._state == GameState.RUNNING:
            self._state = GameState.PAUSED
    
    def resume(self) -> None:
        """Resume the game."""
        if self._state == GameState.PAUSED:
            self._state = GameState.RUNNING
            self._last_move_time = self._time.current_time_ms()
    
    def update(self) -> None:
        """Update game state."""
        if self._state != GameState.RUNNING:
            return
        
        current_time = self._time.current_time_ms()
        if current_time - self._last_move_time < self._speed:
            return
        
        self._last_move_time = current_time
        self._direction = self._next_direction
        
        head = self._snake[0]
        new_head = move_position(head, self._direction)
        
        # Check collision with walls
        if not is_within_bounds(new_head, self._grid_size):
            self.stop()
            return
        
        # Check collision with self
        if new_head in self._snake[1:]:
            self.stop()
            return
        
        # Move snake
        self._snake = Snake([new_head] + self._snake)
        
        # Check if ate food
        if positions_equal(new_head, self._food):
            self._score = Score(self._score + 10)
            # Speed up slightly every 50 points
            if self._score % 50 == 0:
                self._speed = max(50, self._speed - 5)
            self._place_food()
        else:
            # Remove tail
            self._snake = Snake(self._snake[:-1])
        
        # Update input direction
        self._next_direction = self._input.get_direction() or self._direction
    
    def _place_food(self) -> None:
        """Place food in a random position not occupied by snake."""
        exclude = self._snake
        self._food = Food(self._random.random_position(exclude))
    
    def set_direction(self, direction: Direction) -> None:
        """Set snake direction (prevents 180-degree turns)."""
        if not opposite_directions(direction, self._direction):
            self._next_direction = direction
    
    def get_snake(self) -> Snake:
        """Get current snake position."""
        return self._snake
    
    def get_food(self) -> Food:
        """Get current food position."""
        return self._food
    
    def get_score(self) -> Score:
        """Get current score."""
        return self._score
    
    def get_state(self) -> GameState:
        """Get current game state."""
        return self._state
    
    def get_grid_size(self) -> int:
        """Get grid size."""
        return self._grid_size
