"""Pytest configuration for plain-factory tests."""

import pytest
from pathlib import Path


@pytest.fixture
def sample_license_data() -> dict:
    """Return sample license data for testing."""
    return {
        "plain_name": "Test License",
        "spdx_id": "TEST-1.0",
        "original_name": "Original Test License",
        "original_url": "https://example.com/license",
        "original_organization": "Test Organization",
        "original_version": "1.0",
        "plain_version": "1.0.0",
        "category": "permissive",
        "license_description": "A test license for testing purposes.",
        "reader_license_text": "This is a test license text.",
        "original_license_text": "This is the original test license text.",
        "link_in_original": False,
    }


@pytest.fixture
def fixtures_dir() -> Path:
    """Return the path to the test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def temp_output_dir(tmp_path) -> Path:
    """Return a temporary directory for test outputs."""
    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir
