"""Base interface for content types."""
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, Literal, Any, Dict


@dataclass(frozen=True)
class ContentBase:
    """Base class for all content types."""
    pass


class FormatType(StrEnum):
    """Enum for format types."""
    MARKDOWN = "markdown"
    PLAINTEXT = "plaintext"
    READER = "reader"
    EMBED = "embed"


class Element(Protocol):
    """Protocol for elements."""
    def to_markdown(self) -> str:
        """Convert to markdown."""
        ...

    def to_plaintext(self) -> str:
        """Convert to plaintext."""
        ...


class LicenseElement(Protocol):
    """Protocol for license elements."""
    def to_format(self, format_type: FormatType) -> str:
        """Convert to specified format."""
        ...

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        ...

