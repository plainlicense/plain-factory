from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from plain_factory.factory._content_interface import FormatType

@dataclass
class LicenseContext:
    """Context object for license rendering."""
    format_type: FormatType
    elements: Dict[str, Any] = field(default_factory=dict)
    footnote_counter: int = 1
    collected_footnotes: List[Any] = field(default_factory=list)
    current_depth: int = 0
    parent_context: Optional[str] = None

    def should_inline_footnotes(self) -> bool:
        """Determine if footnotes should be inlined."""
        return self.format_type == FormatType.READER

    def get_footnote_style(self) -> str:
        """Get the footnote style based on format type."""
        return (
            "markdown"
            if self.format_type in [FormatType.MARKDOWN, FormatType.READER]
            else "plaintext"
        )

    def register_footnote(self, footnote: Any) -> int:
        """Register a footnote and return its index."""
        self.collected_footnotes.append(footnote)
        current = self.footnote_counter
        self.footnote_counter += 1
        return current

