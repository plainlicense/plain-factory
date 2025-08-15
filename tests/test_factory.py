"""Tests for the factory module."""

import pytest
from plain_factory.factory import (
    Element,
    FormatType,
    LicenseElement,
    ContentBase,
    TextProcessor,
    Formatter,
)


def test_element_enum():
    """Test the Element enum."""
    assert Element.PAGE.value == 1
    assert Element.TEXT.value == 50
    assert Element.PAGE.is_structure is True
    assert Element.TEXT.is_structure is False
    assert Element.from_str("PAGE") == Element.PAGE
    assert Element.from_int(1) == Element.PAGE
    assert str(Element.PAGE) == "page"


def test_format_type_enum():
    """Test the FormatType enum."""
    assert FormatType.PLAINTEXT.value == 1
    assert FormatType.GITHUB.value == 4
    assert FormatType.from_str("PLAINTEXT") == FormatType.PLAINTEXT
    assert str(FormatType.PLAINTEXT) == "plaintext"
    assert FormatType.PLAINTEXT.implemented is True
