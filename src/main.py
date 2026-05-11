#!/usr/bin/env python3
"""
Classic Snake Game - Main Entry Point

Usage:
    python src/main.py [--difficulty easy|medium|hard]

Options:
    --difficulty    Set game difficulty (default: medium)
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add parent directory to path for direct script execution
# This allows imports like `from src.config.constants import ...`
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from src.config.constants import DIFFICULTY_SPEEDS
from src.runtime.game_runtime import GameRuntime


def print_usage() -> None:
    """Print usage information."""
    print("Classic Snake Game")
    print()
    print("Usage:")
    print("    python src/main.py [--difficulty easy|medium|hard]")
    print()
    print("Options:")
    print("    --difficulty    Set game difficulty (default: medium)")
    print()
    print("Difficulty levels:")
    for level, speed in DIFFICULTY_SPEEDS.items():
        print(f"    {level}: {speed}ms per move")


def parse_args() -> str:
    """Parse command line arguments."""
    difficulty = "medium"
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] in ("-h", "--help"):
            print_usage()
            sys.exit(0)
        elif args[i] == "--difficulty":
            if i + 1 >= len(args):
                print("Error: --difficulty requires a value")
                print_usage()
                sys.exit(1)
            difficulty = args[i + 1]
            if difficulty not in DIFFICULTY_SPEEDS:
                print(f"Error: Invalid difficulty '{difficulty}'")
                print(f"Valid options: {', '.join(DIFFICULTY_SPEEDS.keys())}")
                sys.exit(1)
            i += 2
        else:
            print(f"Error: Unknown argument '{args[i]}'")
            print_usage()
            sys.exit(1)
    
    return difficulty


def main() -> None:
    """Main entry point."""
    difficulty = parse_args()
    
    print(f"Starting Snake Game with difficulty: {difficulty}")
    print()
    print("Controls:")
    print("  W / Up Arrow    - Move Up")
    print("  S / Down Arrow  - Move Down")
    print("  A / Left Arrow  - Move Left")
    print("  D / Right Arrow - Move Right")
    print()
    print("Press Enter to start...")
    input()
    
    runtime = GameRuntime(difficulty=difficulty)
    runtime.run()


if __name__ == "__main__":
    main()
