"""Defines content types for markdown, including admonitions and code blocks."""
import re

from dataclasses import dataclass, field
from enum import StrEnum
from functools import cached_property
from os import PathLike
from pathlib import Path
from textwrap import dedent, indent
from typing import Annotated, ClassVar, Literal, LiteralString, NamedTuple, Self, cast, List as TypeList, Dict, Any, Optional, Union
from unittest import mock

from plain_factory.factory._constants import (
    LINEBREAK,
    PARAGRAPH_BREAK,
    TAB,
    PATTERNS,
    SPACE,
)
from plain_factory.factory._content_interface import ContentBase, Element, FormatType, LicenseElement
from plain_factory.factory._paragraph import (
    Citation,
    Citations,
    Footnote,
    Footnotes,
    Paragraph as ParaClass,
)


type EmptyString = Literal[""]
type StrPath = str | PathLike[str]

class SelfEnum(StrEnum):
    """
    Base class for self-referential enums.
    """
    def __str__(self) -> str:
        """
        Returns the string representation of the enum value.
        """
        return self.value

class AdmonitionStyle(SelfEnum):
    """Enum representing the style of admonition blocks in markdown."""
    OPEN = "!!!"
    COLLAPSED = "???"
    EXPANDED = "???+"

class Admonition(SelfEnum):
    """
    Enum representing different types of admonitions used in markdown.
    """
    ABSTRACT = "abstract"
    BUG = "bug"
    CAUTION = "caution"
    DANGER = "danger"
    EXAMPLE = "example"
    FAILURE = "failure"
    INFO = "info"
    NOTE = "note"
    QUESTION = "question"
    QUOTE = "quote"
    SUCCESS = "success"
    TIP = "tip"
    WARNING = "warning"

class GithubAlertName(SelfEnum):
    """
    Enum representing different types of GitHub alerts.
    """
    CAUTION = "[!CAUTION]"
    IMPORTANT = "[!IMPORTANT]"
    NOTE = "[!NOTE]"
    TIP = "[!TIP]"
    WARNING = "[!WARNING]"

    @classmethod
    def from_admonition(cls, admonition: Admonition) -> "GithubAlertName":
        """
        Converts an Admonition to a GithubAlertName.
        """
        match admonition:
            case Admonition.ABSTRACT | Admonition.INFO | Admonition.NOTE | Admonition.QUOTE | Admonition.QUESTION | Admonition.SUCCESS:
                return cls.NOTE
            case Admonition.TIP | Admonition.EXAMPLE:
                return cls.TIP
            case Admonition.CAUTION | Admonition.DANGER | Admonition.FAILURE:
                return cls.CAUTION
            case Admonition.BUG | Admonition.WARNING:
                return cls.WARNING

    @property
    def alert_line(self) -> str:
        """
        Returns the alert line for the GitHub alert.
        """
        return f">{SPACE}{self}"

    @classmethod
    def to_full_string(cls, admonition: Admonition, content: str) -> str:
        """
        Converts an Admonition to its full string representation.
        """
        return f">{SPACE}{cls.from_admonition(admonition)}{LINEBREAK}>{SPACE}{dedent(content.strip())}"


class Paragraphs(tuple):
    """
    Represents a collection of paragraphs, ensuring they are non-empty and stripped of leading/trailing whitespace. Added text should be in rich markdown (i.e. mkdocs markdown), as it will be deconstructed into other content types.
    """
    __slots__ = ()

    br: ClassVar[LiteralString] = PARAGRAPH_BREAK

    def __new__(cls, s: str) -> "Paragraphs":
        """Makes a new instance of Paragraphs from a string."""
        if not s:
            raise ValueError("At least one paragraph must be provided.")
        if paragraphs := tuple(
            dedent(paragraph.strip()) for paragraph in s.split("\n\n") if paragraph.strip()
        ):
            return super().__new__(cls, paragraphs)
        raise ValueError("Paragraphs cannot be empty.")

    def rich_markdown(self) -> str:
        """Returns the rich markdown representation of the paragraphs."""
        return type(self).br.join(self)

    def markdown(self) -> str:
        """Returns the markdown representation of the paragraphs."""
        return self.rich_markdown()


@dataclass(frozen=True, order=True, kw_only=True, slots=True)
class AdmonitionBlock(ContentBase):
    """
    Represents a markdown admonition block with a specific type and content.
    """
    type: Annotated[Admonition, field(hash=True)]
    content: Annotated[Paragraphs, field(hash=True)]
    style: Annotated[AdmonitionStyle, field(default=AdmonitionStyle.OPEN, hash=True)]
    admonition: Annotated[Admonition, field(default=Admonition.INFO, hash=True)]
    title: Annotated[str, field(default="", hash=True)]
    inline: Annotated[Literal["left", "right"] | EmptyString, field(hash=True)] = ""

    @property
    def inline_statement(self) -> EmptyString | Literal['inline', 'inline end']:
        """Returns the inline statement for the admonition block if applicable.
        """
        if self.inline:
            statement = "inline"
            return statement if self.inline == "left" else f"{statement}{SPACE}end" # type: ignore  # plain as day to me pylance...
        return self.inline

    @property
    def rich_markdown_header(self) -> str:
        """
        Returns the header for the admonition block.
        """
        inline_block = f"{self.inline_statement}{SPACE}" if self.inline else ""
        return f"""{self.style}{SPACE}{self.admonition}{SPACE}{inline_block}"{self.title}" """.strip()

    @property
    def plaintext_header(self) -> str:
        """
        Returns the plaintext header for the admonition block.
        """
        return f"{self.admonition.name}: {self.title.title()}" if self.title else f"{self.admonition.name}:"

@dataclass(frozen=True, order=True, kw_only=True, slots=True)
class CodeBlock(ContentBase):
    """
    Represents a markdown code block with a specific language.
    """
    language: Annotated[str, field(default="plaintext", hash=True)]
    content: Annotated[Paragraphs | None, field(hash=True)]
    title: Annotated[str, field(hash=True)] = ""
    snippet: Annotated[StrPath | None, field(hash=True)] = None
    _delimiter: str = field(default="```", init=False, repr=False)
    plaintext_delimiter: ClassVar[str] = "==="

    def __post_init__(self) -> None:
        """
        Post-initialization to ensure content is a Paragraphs instance.
        """
        if self.content is None and self.snippet is None:
            raise ValueError("Content or snippet must be provided for a code block.")
        if self.snippet:
            file = Path(self.snippet)
            if not file.exists():
                raise FileNotFoundError(f"Snippet file '{self.snippet}' does not exist.")
            snippet_content = file.read_text(encoding="utf-8")
            # Ensure the content is a Paragraphs instance
            # we also have to cheat a little around the frozen=True dataclass
            object.__setattr__(self, "content", Paragraphs(snippet_content))

    @property
    def rich_markdown_header(self) -> str:
        """
        Returns the header for the code block.
        """
        return f"""{self._delimiter}{self.language}{SPACE}"title={self.title}" """.strip()

    @property
    def markdown(self) -> str:
        """
        Returns the markdown representation of the code block.
        """
        content = self.content.rich_markdown() if isinstance(self.content, Paragraphs) else self.content
        return f"{self.rich_markdown_header}{LINEBREAK}{content}{LINEBREAK}{self._delimiter}"

    @property
    def plaintext_header(self) -> str:
        """
        Returns the plaintext header for the code block.
        """
        if self.language in ["md", "markdown", "plaintext", "text"]:
            if self.title:
                return f"{type(self).plaintext_delimiter}{SPACE}{self.title.title()}:"
            return type(self).plaintext_delimiter
        return f"{type(self).plaintext_delimiter}{SPACE}{self.language.title()}" if self.language else "Code Block"

    @property
    def plaintext(self) -> str:
        """
        Returns the plaintext representation of the code block.
        """
        content = self.content.split('\n') # type: ignore  # string subclass
        lines = [f"> {line}" for line in content]
        return f"{self.plaintext_header}{LINEBREAK}{LINEBREAK.join(lines)}{LINEBREAK}{type(self).plaintext_delimiter}"

@dataclass(frozen=True, order=True, kw_only=True, slots=True)
class Definition(ContentBase):
    """
    Represents a markdown definition.
    """
    term: Annotated[str, field(hash=True)]
    definition: Annotated[str, field(hash=True)]

    def __post_init__(self) -> None:
        """
        Post-initialization to ensure term and definition are stripped of leading/trailing whitespace.
        """
        object.__setattr__(self, "term", dedent(self.term.strip()))
        object.__setattr__(self, "definition", dedent(self.definition.strip()))

    @property
    def header(self) -> str:
        """
        Returns the header for the definition.
        """
        return dedent(f"`{self.term.strip()}`")

    @property
    def body(self) -> str:
        """
        Returns the body for the definition.
        """
        start_prefix = f":{SPACE}{SPACE}{SPACE}"
        prefix = SPACE * 4
        return dedent(f"{self.definition.strip()}")

# Add missing classes needed by __init__.py
@dataclass(frozen=True)
class Block(ContentBase, Element):
    """Block element in a document."""
    content: str

    def to_markdown(self) -> str:
        """Convert to markdown."""
        return self.content

    def to_plaintext(self) -> str:
        """Convert to plaintext."""
        return self.content

@dataclass(frozen=True)
class DefinitionList(ContentBase, Element):
    """Definition list element."""
    items: TypeList["DefinitionListItem"]

    def to_markdown(self) -> str:
        """Convert to markdown."""
        return "\n".join(item.to_markdown() for item in self.items)

    def to_plaintext(self) -> str:
        """Convert to plaintext."""
        return "\n".join(item.to_plaintext() for item in self.items)

@dataclass(frozen=True)
class DefinitionListItem(ContentBase, Element):
    """Definition list item."""
    term: str
    definition: str

    def to_markdown(self) -> str:
        """Convert to markdown."""
        return f"{self.term}\n: {self.definition}"

    def to_plaintext(self) -> str:
        """Convert to plaintext."""
        return f"{self.term}: {self.definition}"

@dataclass(frozen=True)
class Heading(ContentBase, Element):
    """Heading element."""
    level: int
    text: str

    def to_markdown(self) -> str:
        """Convert to markdown."""
        return f"{'#' * self.level} {self.text}"

    def to_plaintext(self) -> str:
        """Convert to plaintext."""
        return f"{self.text.upper()}"

@dataclass(frozen=True)
class License(ContentBase, LicenseElement):
    """License element."""
    name: str
    content: str

    def to_format(self, format_type: FormatType) -> str:
        """Convert to specified format."""
        if format_type == FormatType.MARKDOWN:
            return f"# {self.name}\n\n{self.content}"
        elif format_type == FormatType.PLAINTEXT:
            return f"{self.name.upper()}\n\n{self.content}"
        elif format_type == FormatType.READER:
            return f"# {self.name}\n\n{self.content}"
        else:
            return self.content

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {"name": self.name, "content": self.content}

@dataclass(frozen=True)
class List(ContentBase, Element):
    """List element."""
    items: TypeList["ListItem"]
    ordered: bool = False

    def to_markdown(self) -> str:
        """Convert to markdown."""
        result = []
        for i, item in enumerate(self.items, 1):
            prefix = f"{i}." if self.ordered else "-"
            result.append(f"{prefix} {item.to_markdown()}")
        return "\n".join(result)

    def to_plaintext(self) -> str:
        """Convert to plaintext."""
        result = []
        for i, item in enumerate(self.items, 1):
            prefix = f"{i}." if self.ordered else "*"
            result.append(f"{prefix} {item.to_plaintext()}")
        return "\n".join(result)

@dataclass(frozen=True)
class ListItem(ContentBase, Element):
    """List item element."""
    content: str

    def to_markdown(self) -> str:
        """Convert to markdown."""
        return self.content

    def to_plaintext(self) -> str:
        """Convert to plaintext."""
        return self.content

@dataclass(frozen=True)
class Page(ContentBase, LicenseElement):
    """Page element."""
    title: str
    sections: TypeList["Section"]

    def to_format(self, format_type: FormatType) -> str:
        """Convert to specified format."""
        if format_type == FormatType.MARKDOWN:
            return f"# {self.title}\n\n" + "\n\n".join(s.to_markdown() for s in self.sections)
        elif format_type == FormatType.PLAINTEXT:
            return f"{self.title.upper()}\n\n" + "\n\n".join(s.to_plaintext() for s in self.sections)
        elif format_type == FormatType.READER:
            return f"# {self.title}\n\n" + "\n\n".join(s.to_markdown() for s in self.sections)
        else:
            return self.title + "\n\n" + "\n\n".join(s.to_markdown() for s in self.sections)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "title": self.title,
            "sections": [s.to_dict() for s in self.sections]
        }

@dataclass(frozen=True)
class Paragraph(ContentBase, Element):
    """Paragraph element."""
    text: str

    def to_markdown(self) -> str:
        """Convert to markdown."""
        return self.text

    def to_plaintext(self) -> str:
        """Convert to plaintext."""
        return self.text

@dataclass(frozen=True)
class Section(ContentBase, Element):
    """Section element."""
    title: Optional[str]
    content: TypeList[Element]

    def to_markdown(self) -> str:
        """Convert to markdown."""
        result = []
        if self.title:
            result.append(f"## {self.title}")
        result.extend(item.to_markdown() for item in self.content)
        return "\n\n".join(result)

    def to_plaintext(self) -> str:
        """Convert to plaintext."""
        result = []
        if self.title:
            result.append(f"{self.title.upper()}")
        result.extend(item.to_plaintext() for item in self.content)
        return "\n\n".join(result)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "title": self.title,
            "content": [{"type": type(item).__name__, "content": item.to_markdown()} for item in self.content]
        }

@dataclass(frozen=True)
class Tab(ContentBase, LicenseElement):
    """Tab element."""
    title: str
    content: str
    format_type: FormatType

    def to_format(self, format_type: FormatType) -> str:
        """Convert to specified format."""
        if format_type == self.format_type:
            return self.content
        return ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "title": self.title,
            "content": self.content,
            "format_type": self.format_type
        }

@dataclass(frozen=True)
class Text(ContentBase, Element):
    """Text element."""
    content: str
    
    def to_markdown(self) -> str:
        """Convert to markdown."""
        return self.content
    
    def to_plaintext(self) -> str:
        """Convert to plaintext."""
        return self.content

@dataclass(frozen=True)
class Title(ContentBase, Element):
    """Title element."""
    text: str
    level: int = 1
    
    def to_markdown(self) -> str:
        """Convert to markdown."""
        return f"{'#' * self.level} {self.text}"
    
    def to_plaintext(self) -> str:
        """Convert to plaintext."""
        return f"{self.text.upper()}"

