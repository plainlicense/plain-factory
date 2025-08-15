"""Base interface for content types."""
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ContentBase:
    """Base class for all content types."""
    pass

