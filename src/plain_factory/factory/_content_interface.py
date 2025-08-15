"""Base interface for content types."""
from dataclasses import dataclass
from enum import IntEnum, StrEnum
from typing import Protocol, Literal, Any, Dict, ClassVar


@dataclass(frozen=True)
class ContentBase:
    """Base class for all content types."""
    pass


class FormatType(IntEnum):
    """Enum for format types."""
    PLAINTEXT = 1
    MARKDOWN = 2
    READER = 3
    GITHUB = 4
    EMBED = 5
    
    @classmethod
    def from_str(cls, s: str) -> "FormatType":
        """Convert string to FormatType."""
        return getattr(cls, s.upper())
    
    @property
    def implemented(self) -> bool:
        """Check if format type is implemented."""
        return True
    
    def __str__(self) -> str:
        """Convert to string."""
        return self.name.lower()


class Element(IntEnum):
    """Enum for element types."""
    PAGE = 1
    SECTION = 2
    PARAGRAPH = 3
    LIST = 4
    LIST_ITEM = 5
    DEFINITION_LIST = 6
    DEFINITION_LIST_ITEM = 7
    HEADING = 8
    BLOCK = 9
    CODE_BLOCK = 10
    TEXT = 50
    
    @property
    def is_structure(self) -> bool:
        """Check if element is a structure element."""
        return self.value < 50
    
    @classmethod
    def from_str(cls, s: str) -> "Element":
        """Convert string to Element."""
        return getattr(cls, s.upper())
    
    @classmethod
    def from_int(cls, i: int) -> "Element":
        """Convert int to Element."""
        return cls(i)
    
    def __str__(self) -> str:
        """Convert to string."""
        return self.name.lower()


class ElementProtocol(Protocol):
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

