import re

from functools import cached_property
from textwrap import dedent
from typing import Literal, NamedTuple, Self

from dataclasses import dataclass

from plain_factory.factory._constants import PATTERNS, SPACE

class Footnote(NamedTuple):
    """
    Represents a full (not inline) footnote (for inline, see [`Citation`]).
    """
    citation: int
    content: str

    def __str__(self) -> str:
        """Returns the string representation of the footnote."""
        return f"[^{self.citation}]:{SPACE}{self.content}"

    @classmethod
    def from_footnote_match(cls, match: re.Match[str]) -> "Footnote":
        """
        Creates a Footnote instance from a regex match object produced by `PATTERNS["footnote"]`.

        Args:
            match (re.Match[str]): The regex match object containing footnote data.

        Returns:
            Footnote: An instance of Footnote with citation and content.
        """
        citation = int(match.group(1))
        content = match.group(2).strip()
        return cls(citation, content)

    @classmethod
    def from_annotation_match(cls, match: re.Match[str]) -> "Footnote":
        """
        Creates a Footnote instance from a regex match object produced by `PATTERNS["annotation"]`.

        Args:
            match (re.Match[str]): The regex match object containing annotation data.

        Returns:
            Footnote: An instance of Footnote with citation and content.
        """
        citation = int(match.group("citation").replace("(", "").replace(")", ""))
        content = match.group("annotation").strip()
        return cls(citation, content)

type Footnotes = tuple[Footnote, ...] | None

class Citation(NamedTuple):
    """Represents an inline footnote or annotation citation."""
    number: int
    kind: Literal["footnote", "annotation"]
    start: int
    end: int
    match: re.Match[str] | None = None

    def __str__(self) -> str:
        """Return a string representation of the citation."""
        return f"[^{self.number}]" if self.kind == "footnote" else f"({self.number})"

    def __eq__(self, other: object) -> bool:
        """Check equality based on number and kind."""
        if not isinstance(other, Citation):
            return NotImplemented
        return self.start == other.start and self.end == other.end and self.number == other.number and self.kind == other.kind

    def __lt__(self, other: object) -> bool:
        """Compare citations based on their start position."""
        return self.start < other.start if isinstance(other, Citation) else NotImplemented

    def __gt__(self, other: object) -> bool:
        """Compare citations based on their end position."""
        return self.end > other.end if isinstance(other, Citation) else NotImplemented

    @property
    def length(self) -> int:
        """Return the length of the citation string."""
        return len(str(self))

    def to_footnote(self, new_number: int | None = None) -> Footnote:
        """Convert the citation to a footnote."""
        if self.kind == "annotation" and self.match:
            return Footnote(
                citation=new_number or self.number,
                content=self.match.group("annotation").strip()
            )
        else:
            raise ValueError("We can only convert annotations with a Match object to footnotes.")

    @classmethod
    def from_match(cls, match: re.Match[str]) -> Self:
        """Create a Citation instance from a regex match."""
        kind = "annotation" if "(" in match.group("citation") else "footnote"
        return cls(
            number=int(match.group("number")),
            kind=kind,
            start=match.start(),
            end=match.end(),
            match=match
        )

type Citations = tuple[Citation, ...]

class Reference(NamedTuple):
    """Represents a Citation and its corresponding Footnote."""
    citation: Citation
    footnote: Footnote

class Paragraph(str):
    """
    A string subclass that tracks footnotes and provides text manipulation.

    NOTE: A Paragraph instance will **only** contain Footnotes if they were created from annotations. This is because of how footnotes are parsed versus annotations. Example:

    ```markdown
    This is a paragraph with an annotation(1) and a footnote[^1].
    { .annotate }

    [^1]: This is the footnote content.
    ```

    """

    __slots__ = ("_original_text", "annotations", "footnote_citations", "footnotes")

    def __new__(cls, text: str = "", *, footnote_citations: Citations = (), annotations: Citations = (), footnotes: "tuple[Footnote, ...]" = ()) -> Self:
        """Create a new Paragraph instance with text and optional footnotes."""
        if not footnote_citations and (footnote_matches := tuple(PATTERNS.footnote["initial"].finditer(text))):
            footnote_citations = tuple(Citation.from_match(m) for m in footnote_matches)
        if not annotations and (annotation_matches := tuple(PATTERNS.annotation["inline"].finditer(text))):
            annotations = tuple(Citation.from_match(m) for m in annotation_matches)

        instance = super().__new__(cls, dedent(text).strip())
        instance.footnote_citations = footnote_citations
        instance.footnotes = footnotes or ()
        instance.annotations = annotations or ()
        instance._original_text = text
        return instance

    @property
    def text(self) -> str:
        """Get the text content (equivalent to str(self))."""
        return str(self)

    @property
    def citation_count(self) -> int:
        """Return the total number of citations (footnotes + annotations)."""
        return len(self.footnote_citations) + len(self.annotations)

    @property
    def _ordered_citations(self) -> list[Citation]:
        """Return a sorted list of citations (footnotes and annotations) by their start position."""
        return sorted(self.footnote_citations + self.annotations, key=lambda c: c.start)

    @cached_property
    def absolute_citation_order(self) -> list[Citation]:
        """Return a sorted list of all citations (footnotes and annotations) by their start position. They will still have their original numbers."""
        all_citations = list(self.footnote_citations) + list(self.annotations)
        return sorted(all_citations, key=lambda c: c.start)

    @cached_property
    def starting_citation_index(self) -> int:
        """Return the index of the first citation in the text."""
        if self.footnote_citations or self.annotations:
            return min(c.number for c in self.footnote_citations) if self.footnote_citations else 1
        return 1

    @cached_property
    def with_all_footnote_citations(self) -> "Paragraph":
        """Return a new Paragraph with all footnotes included in the text."""
        if not self.annotations:
            return self
        if not self.footnote_citations:
            footnotes = [c.to_footnote() for c in self.annotations]
            new_text = self.text
            for annotation in self.annotations:
                # Implementation here
                pass
            return Paragraph(new_text, footnotes=tuple(footnotes))
        return self

    @cached_property
    def with_footnotes_realigned(self) -> "Paragraph":
        """Return a new Paragraph with footnotes realigned to start from 1."""
        if not self.footnotes:
            return Paragraph(self.text, footnotes=self.footnotes)

        import re

        # Create mapping of old to new footnote numbers
        old_nums = sorted([f.citation for f in self.footnotes])
        footnote_mapping = {old_num: i for i, old_num in enumerate(old_nums, 1)}

        def replace_footnote_ref(match):
            old_num = int(match.group(1))
            return f"[{footnote_mapping.get(old_num, old_num)}]"

        # Create new text with updated footnote references
        new_text = re.sub(r"\[(\d+)\]", replace_footnote_ref, self.text)

        # Create new footnotes with updated numbering
        new_footnotes = tuple(
            Footnote(
                citation=footnote_mapping[f.citation],
                content=f.content
            )
            for f in self.footnotes
        )

        return Paragraph(new_text, footnotes=new_footnotes)

    def with_text(self, new_text: str) -> "Paragraph":
        """Return a new Paragraph with different text but same footnotes."""
        return Paragraph(new_text, footnotes=self.footnotes)

    def with_footnotes(self, new_footnotes: tuple[Footnote, ...]) -> "Paragraph":
        """Return a new Paragraph with different footnotes but same text."""
        return Paragraph(self.text, footnotes=new_footnotes)

    def add_footnote(self, number: int, content: str) -> "Paragraph":
        """Return a new Paragraph with an additional footnote."""
        new_footnotes = list(self.footnotes)
        new_footnotes.append(Footnote(citation=number, content=content))
        return Paragraph(self.text, footnotes=tuple(new_footnotes))

    def split_paragraphs(self, delimiter: str = "\n\n") -> list["Paragraph"]:
        """Split into multiple Paragraph instances, distributing footnotes appropriately."""
        text_parts = self.text.split(delimiter)
        paragraphs = []

        import re

        for part in text_parts:
            if not part.strip():
                continue

            # Find footnote references in this part
            footnote_refs = set()
            for match in re.finditer(r"\[(\d+)\]", part):
                footnote_refs.add(int(match.group(1)))

            # Include only relevant footnotes
            part_footnotes = tuple(
                f for f in self.footnotes
                if f.citation in footnote_refs
            )

            paragraphs.append(Paragraph(part.strip(), footnotes=part_footnotes))

        return paragraphs

    def merge_with(self, other: "Paragraph", separator: str = "\n\n") -> "Paragraph":
        """Return a new Paragraph merged with another, handling footnote conflicts."""
        if not isinstance(other, Paragraph):
            # Convert string to Paragraph
            other = Paragraph(str(other))

        # Merge text
        new_text = self.text + separator + other.text

        # Merge footnotes, resolving conflicts by renumbering other's footnotes
        new_footnotes = list(self.footnotes)
        max_footnote = max([f.citation for f in self.footnotes]) if self.footnotes else 0

        import re

        other_text = other.text

        for footnote in other.footnotes:
            if any(f.citation == footnote.citation for f in self.footnotes):
                # Conflict: renumber the footnote from other
                new_num = max_footnote + 1
                max_footnote += 1

                # Update references in other's text
                other_text = re.sub(rf"\[{footnote.citation}\]", f"[{new_num}]", other_text)
                new_footnotes.append(Footnote(citation=new_num, content=footnote.content))
            else:
                new_footnotes.append(footnote)

        # Rebuild the merged text with updated other text
        final_text = self.text + separator + other_text
        return Paragraph(final_text, footnotes=tuple(new_footnotes))

    def __repr__(self) -> str:
        footnote_count = len(self.footnotes)
        return f"Paragraph({str.__repr__(self)}, footnotes={footnote_count})"

