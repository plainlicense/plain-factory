"""
Factory module for Plain License.

This module contains the core components for license construction and processing.
It provides a flexible system for deconstructing and reconstructing licenses in various formats.
"""

from plain_factory.factory._boilerplate import (
    get_boilerplate,
    get_disclaimer_block,
    get_header_block,
    interpretation_block,
)
from plain_factory.factory._constants import (
    BLOCK_END_PATTERN,
    BLOCK_SEP_PATTERN,
    BLOCK_START_PATTERN,
    CRITIC_BLOCK_PATTERN,
    CRITIC_PATTERN,
    CRITIC_PLACEHOLDER_PATTERN,
    CRITIC_SUB_PLACEHOLDER_PATTERN,
    FENCED_BLOCK_PATTERN,
    INDENT_YAML_LINE_PATTERN,
    MARK_PATTERN,
    PAGE_DIVIDER,
    PATTERNS,
    SPACE,
    YAML_END_PATTERN,
    YAML_START_PATTERN,
    YEAR,
)
from plain_factory.factory._content_interface import (
    ContentBase,
    Element,
    FormatType,
    LicenseElement,
)
from plain_factory.factory._content_types import (
    Block,
    CodeBlock,
    DefinitionList,
    DefinitionListItem,
    Heading,
    License,
    List,
    ListItem,
    Page,
    Paragraph,
    Section,
    Tab,
    Text,
    Title,
)
from plain_factory.factory._context import LicenseContext
from plain_factory.factory._deconstruct import (
    LicenseDeconstructor,
    LicenseStructure,
)
from plain_factory.factory._formatter import Formatter
from plain_factory.factory._license_metadata import LicenseMetadata
from plain_factory.factory._paragraph import (
    InlineCode,
    InlineFormatting,
    InlineImage,
    InlineLink,
    ParagraphDeconstructor,
    ParagraphStructure,
)
from plain_factory.factory._tab_generators import (
    ChangelogTabGenerator,
    EmbedTabGenerator,
    MarkdownTabGenerator,
    OfficialTabGenerator,
    PlaintextTabGenerator,
    ReaderTabGenerator,
    TabGenerator,
    TabGeneratorFactory,
)
from plain_factory.factory._text_processor import TextProcessor
from plain_factory.factory._types import (
    BaseStrEnum,
    ConditionsTags,
    LicenseCategory,
    LicenseFrontMatter,
    LimitationsTags,
    PermissionsTags,
    PlainLicenseTags,
    ReferenceLink,
)

__all__ = [
    # _boilerplate
    "get_boilerplate",
    "get_disclaimer_block",
    "get_header_block",
    "interpretation_block",
    
    # _constants
    "BLOCK_END_PATTERN",
    "BLOCK_SEP_PATTERN",
    "BLOCK_START_PATTERN",
    "CRITIC_BLOCK_PATTERN",
    "CRITIC_PATTERN",
    "CRITIC_PLACEHOLDER_PATTERN",
    "CRITIC_SUB_PLACEHOLDER_PATTERN",
    "FENCED_BLOCK_PATTERN",
    "INDENT_YAML_LINE_PATTERN",
    "MARK_PATTERN",
    "PAGE_DIVIDER",
    "PATTERNS",
    "SPACE",
    "YAML_END_PATTERN",
    "YAML_START_PATTERN",
    "YEAR",
    
    # _content_interface
    "ContentBase",
    "Element",
    "FormatType",
    "LicenseElement",
    
    # _content_types
    "Block",
    "CodeBlock",
    "DefinitionList",
    "DefinitionListItem",
    "Heading",
    "License",
    "List",
    "ListItem",
    "Page",
    "Paragraph",
    "Section",
    "Tab",
    "Text",
    "Title",
    
    # _context
    "LicenseContext",
    
    # _deconstruct
    "LicenseDeconstructor",
    "LicenseStructure",
    
    # _formatter
    "Formatter",
    
    # _license_metadata
    "LicenseMetadata",
    
    # _paragraph
    "InlineCode",
    "InlineFormatting",
    "InlineImage",
    "InlineLink",
    "ParagraphDeconstructor",
    "ParagraphStructure",
    
    # _tab_generators
    "ChangelogTabGenerator",
    "EmbedTabGenerator",
    "MarkdownTabGenerator",
    "OfficialTabGenerator",
    "PlaintextTabGenerator",
    "ReaderTabGenerator",
    "TabGenerator",
    "TabGeneratorFactory",
    
    # _text_processor
    "TextProcessor",
    
    # _types
    "BaseStrEnum",
    "ConditionsTags",
    "LicenseCategory",
    "LicenseFrontMatter",
    "LimitationsTags",
    "PermissionsTags",
    "PlainLicenseTags",
    "ReferenceLink",
]
