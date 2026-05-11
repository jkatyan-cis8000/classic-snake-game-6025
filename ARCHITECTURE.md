# Architecture

## Overview

A layered Snake game implementation following clean architecture principles.

## Module Structure

### src/types/
- `types.py`: Core domain types
  - `Position`: (x, y) coordinates
  - `Direction`: UP, DOWN, LEFT, RIGHT
  - `Snake`: list of Position objects (head is first)
  - `Food`: Position wrapper
  - `GameState`: RUNNING, GAME_OVER, PAUSED
  - `Score`: integer count

### src/config/
- `constants.py`: Game configuration
  - GRID_SIZE = 20
  - INITIAL_SPEED = 150 (ms)
  - SPEED_MULTIPLIERS for difficulties
- `settings.py`: Settings dataclass
  - difficulty: str ("easy", "medium", "hard")
  - grid_size: int
  - base_speed_ms: int

### src/providers/
- `input.py`: InputProvider interface
  - `get_direction() -> Direction | None`
  - `handle_key(key) -> None`
- `time.py`: TimeProvider interface
  - `sleep(ms: int) -> None`
  - `current_time_ms() -> int`
- `random.py`: RandomProvider interface
  - `random_position(exclude: list[Position]) -> Position`

### src/utils/
- `coords.py`: Coordinate utilities
  - `move_position(pos: Position, direction: Direction) -> Position`
  - `positions_equal(a: Position, b: Position) -> bool`
  - `is_within_bounds(pos: Position, size: int) -> bool`

### src/repo/
- `score_repo.py`: ScoreRepository
  - `get_high_score() -> int`
  - `save_score(score: int) -> None`

### src/service/
- `game_engine.py`: GameEngine
  - `__init__(config: Settings, providers) -> None`
  - `start() -> None`
  - `update() -> None`
  - `handle_input(direction: Direction) -> None`
  - `get_state() -> GameState`
  - `get_snake() -> Snake`
  - `get_food() -> Food`
  - `get_score() -> Score`
  - `is_game_over() -> bool`
  - `reset(difficulty: str) -> None`

### src/runtime/
- `game_loop.py`: GameLoop
  - `__init__(engine: GameEngine, providers) -> None`
  - `run() -> None`
  - `stop() -> None`

### src/ui/
- `display.py`: Display
  - `render(game_state, snake, food, score, game_over) -> None`
  - `clear_screen() -> None`
  - `show_game_over(score: int) -> None`
- `input_handler.py`: InputHandler
  - `process_key(key: str) -> Direction | None`
  - `is_exit_key(key: str) -> bool`

### entry point
- `main.py`: `if __name__ == "__main__"` 
  - Wiring all layers together
  - Starting the game loop

## Layer Dependencies

```
types → config → providers → repo → service → runtime → ui
                                    ↑
                                    └── utils (leaf, no internal imports)
```

## Flow

1. `main.py` creates providers, config, and wires the game
2. `GameEngine` handles game logic with providers for I/O
3. `GameLoop` orchestrates the update-render cycle
4. `Display` renders the current state
5. `InputHandler` processes keyboard input
