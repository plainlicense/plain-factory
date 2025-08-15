"""Tests for the CLI module."""

from pathlib import Path
from typer.testing import CliRunner

import pytest
from plain_factory.cli import app


runner = CliRunner()


def test_version():
    """Test the version command."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "plain-factory version:" in result.stdout


def test_process_nonexistent_file():
    """Test processing a nonexistent file."""
    result = runner.invoke(app, ["process", "nonexistent.yaml"])
    assert result.exit_code == 1
    assert "does not exist" in result.stdout


def test_validate_nonexistent_file():
    """Test validating a nonexistent file."""
    result = runner.invoke(app, ["validate", "nonexistent.yaml"])
    assert result.exit_code == 1
    assert "does not exist" in result.stdout
