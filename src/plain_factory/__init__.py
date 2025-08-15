"""
Plain Factory - A flexible license construction system for Plain License.

This package provides tools for deconstructing and reconstructing licenses in various formats.
It is designed to be flexible and extensible, allowing for custom license formats and processing.
"""

__version__ = "0.1.0"

from plain_factory.license_factory import (
    LicenseContent,
    assemble_license_page,
    clean_content,
    create_page_content,
    get_changelog_text,
    get_category,
    get_extra_meta,
    render_mapping,
    save_license,
)

__all__ = [
    "LicenseContent",
    "assemble_license_page",
    "clean_content",
    "create_page_content",
    "get_changelog_text",
    "get_category",
    "get_extra_meta",
    "render_mapping",
    "save_license",
]
