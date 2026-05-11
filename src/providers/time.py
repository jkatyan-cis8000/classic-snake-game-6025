from __future__ import annotations

import time
from abc import ABC, abstractmethod


class TimeProvider(ABC):
    """Base class for time handling."""
    
    @abstractmethod
    def sleep(self, ms: int) -> None:
        """Sleep for given milliseconds."""
        pass
    
    @abstractmethod
    def current_time_ms(self) -> int:
        """Get current time in milliseconds."""
        pass


class StandardTimeProvider(TimeProvider):
    """Standard time provider using time module."""
    
    def sleep(self, ms: int) -> None:
        """Sleep for given milliseconds."""
        time.sleep(ms / 1000.0)
    
    def current_time_ms(self) -> int:
        """Get current time in milliseconds."""
        return int(time.time() * 1000)
