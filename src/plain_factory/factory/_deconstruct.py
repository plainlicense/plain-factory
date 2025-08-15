"""
This is where we take everything apart.
"""
from dataclasses import dataclass
from typing import Any, NamedTuple, Dict, List, Optional
from plain_factory.factory._constants import (
    LINEBREAK,
    PARAGRAPH_BREAK,
    PATTERNS,
    SPACE,
)

# Before we actually take anything apart, we need to basically make a map of where everything is so we can put it back together later.

class Part(NamedTuple):
    """
    A generic part of a license of any type.
    """
    parts_index: int
    kind: str
    kind_order: int
    inline: bool
    content: Any
    start_index: int
    end_index: int
    parent: Any
    children: List[Any]

@dataclass(order=True)
class LicenseParts:
    """
    A simple store for license parts with an auto-incrementing index.
    """
    _index = 0
    parts: Dict[Part, Any]
    def __init__(self):
        self.index = LicenseParts._index
        LicenseParts._index += 1
        self.parts = {}

    def add_part(self, part: Part, content):
        """
        Add a part to the license.
        """
        self.parts[part] = content

    def get_part(self, part: Part):
        """
        Get a part from the license.
        """
        return self.parts.get(part)

    def remove_part(self, part: Part):
        """
        Remove a part from the license.
        """
        if part in self.parts:
            del self.parts[part]

    def __getitem__(self, item):
        """
        Get a part by index.
        """
        return self.parts.get(item)

@dataclass
class LicenseStructure:
    """Structure of a license document."""
    title: str
    sections: List[Dict[str, Any]]
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class LicenseDeconstructor:
    """Deconstructs a license document into its component parts."""
    content: str
    
    def deconstruct(self) -> LicenseStructure:
        """Deconstruct the license content into a structured format."""
        # This is a placeholder implementation
        return LicenseStructure(
            title="License",
            sections=[{"title": "Section", "content": self.content}]
        )
    
    def extract_sections(self) -> List[Dict[str, Any]]:
        """Extract sections from the license content."""
        # This is a placeholder implementation
        return [{"title": "Section", "content": self.content}]
    
    def extract_metadata(self) -> Dict[str, Any]:
        """Extract metadata from the license content."""
        # This is a placeholder implementation
        return {"version": "1.0"}

