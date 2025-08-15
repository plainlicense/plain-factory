# Plain Factory

Plain Factory is a flexible license construction system for [Plain License](https://plainlicense.org). It provides tools for deconstructing and reconstructing licenses in various formats.

## Features

- Flexible license construction from YAML metadata
- Multiple output formats (Markdown, plaintext, reader-friendly)
- Customizable license templates
- Command-line interface for easy integration

## Installation

```bash
pip install plain-factory
```

## Usage

### Command Line

Process a license file:

```bash
plain-factory process input.yaml --output ./output --format all
```

Validate a license file:

```bash
plain-factory validate license.yaml
```

### Python API

```python
from plain_factory import LicenseContent, assemble_license_page

# Create a license content object
license_content = LicenseContent.from_yaml("path/to/license.yaml")

# Assemble a license page
page = assemble_license_page(license_content)

# Save the license in different formats
page.save_markdown("output/license.md")
page.save_plaintext("output/license.txt")
```

## Development

### Setup

Clone the repository with submodules:

```bash
git clone --recursive https://github.com/plainlicense/plain-factory.git
cd plain-factory
```

Install development dependencies:

```bash
pip install -e ".[dev]"
```

### Testing

Run tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=plain_factory
```

### Linting and Formatting

```bash
# Lint
ruff check .

# Format
ruff format .

# Type check
mypy src
```

## License

MIT License
