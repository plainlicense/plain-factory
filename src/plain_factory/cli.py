"""
Command-line interface for plain-factory.
"""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from plain_factory import __version__
from plain_factory.license_factory import LicenseContent

console = Console()
app = typer.Typer(
    name="plain-factory",
    help="Plain License's modular license factory. Produces license versions from a single yaml input.",
    add_completion=False,
)


def version_callback(value: bool) -> None:
    """Print the version of the package."""
    if value:
        console.print(f"[bold]plain-factory[/bold] version: [bold green]{__version__}[/bold green]")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-v", help="Show the version and exit.", callback=version_callback
    ),
) -> None:
    """Plain License's modular license factory."""
    pass


@app.command()
def process(
    input_file: Path = typer.Argument(
        ..., help="Path to the input YAML file containing license metadata."
    ),
    output_dir: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Directory to output the processed license files."
    ),
    format: str = typer.Option(
        "all", "--format", "-f", help="Format to output (markdown, plaintext, reader, all)."
    ),
) -> None:
    """Process a license file and output in the specified format."""
    if not input_file.exists():
        console.print(f"[bold red]Error:[/bold red] Input file {input_file} does not exist.")
        raise typer.Exit(1)

    if output_dir is None:
        output_dir = Path.cwd() / "output"

    output_dir.mkdir(parents=True, exist_ok=True)

    console.print(
        Panel(
            f"Processing license file: [bold]{input_file}[/bold]\n"
            f"Output directory: [bold]{output_dir}[/bold]\n"
            f"Format: [bold]{format}[/bold]",
            title="Plain Factory",
            subtitle="License Processing",
        )
    )

    # TODO: Implement actual license processing
    console.print("[yellow]Note:[/yellow] License processing not yet implemented.")
    console.print("[green]Success:[/green] Placeholder processing completed.")


@app.command()
def validate(
    input_file: Path = typer.Argument(..., help="Path to the license file to validate.")
) -> None:
    """Validate a license file for correctness."""
    if not input_file.exists():
        console.print(f"[bold red]Error:[/bold red] Input file {input_file} does not exist.")
        raise typer.Exit(1)

    console.print(
        Panel(
            f"Validating license file: [bold]{input_file}[/bold]",
            title="Plain Factory",
            subtitle="License Validation",
        )
    )

    # TODO: Implement actual license validation
    console.print("[yellow]Note:[/yellow] License validation not yet implemented.")
    console.print("[green]Success:[/green] Placeholder validation completed.")


if __name__ == "__main__":
    app()
