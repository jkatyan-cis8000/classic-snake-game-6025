from __future__ import annotations


def move_position(pos: tuple[int, int], direction: str) -> tuple[int, int]:
    """Move position in given direction by one unit."""
    x, y = pos
    if direction == "UP":
        return (x, y - 1)
    elif direction == "DOWN":
        return (x, y + 1)
    elif direction == "LEFT":
        return (x - 1, y)
    elif direction == "RIGHT":
        return (x + 1, y)
    return (x, y)


def positions_equal(a: tuple[int, int], b: tuple[int, int]) -> bool:
    """Check if two positions are equal."""
    return a[0] == b[0] and a[1] == b[1]


def is_within_bounds(pos: tuple[int, int], size: int) -> bool:
    """Check if position is within grid bounds [0, size)."""
    return 0 <= pos[0] < size and 0 <= pos[1] < size


def opposite_directions(a: str, b: str) -> bool:
    """Check if two directions are opposite."""
    return (
        (a == "UP" and b == "DOWN") or
        (a == "DOWN" and b == "UP") or
        (a == "LEFT" and b == "RIGHT") or
        (a == "RIGHT" and b == "LEFT")
    )
