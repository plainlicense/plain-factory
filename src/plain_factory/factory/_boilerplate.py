"""
Boilerplate text and functions for license generation.
"""

from textwrap import dedent
from typing import Any, Dict, Literal, Optional, Tuple


def get_not_advice_text(issues_link: str, edit_link: str) -> tuple[str, str]:
    """Returns the "not advice" disclaimer text for the license."""
    return (
        dedent("We are not lawyers. This is not legal advice. If you need legal advice, talk to a lawyer. You use this license at your own risk."),

        dedent(f"""We are normal people making licenses accessible for everyone. We hope that our plain language helps you and anyone else understand this license  (including lawyers). If you see a mistake or want to suggest a change, please [submit an issue on GitHub]({issues_link} "Submit an issue on GitHub") or [edit this page]({edit_link} "edit on GitHub")."""
        )
    )


def get_not_official_text(plain_license: str, original_license: str | None = None, original_organization: str | None = None, original_url: str | None = None) -> tuple[str] | tuple[str,str]:
    """Returns the "not official" disclaimer text for the license."""
    if not original_license or not original_organization or not original_url:
        return ("",)
    return (
        dedent(
            f"""\
        Plain License is not affiliated with the original {original_license.strip()} authors or {original_organization.strip()}. **Our plain language versions are not official** and are not endorsed by the original authors. Our licenses may also include different terms or additional information. We try to capture the *legal meaning* of the original license, but we can't guarantee our license provides the same legal protections.""".strip()
        ),
        dedent(f"""\
        If you want to use the {plain_license.strip()}, start by reading the official {original_license.strip()} license text. You can find the official {original_license.strip()} [here]({original_url.strip()} "check out the official {original_license.strip()}"). If you have questions about the {original_license.strip()}, you should talk to a lawyer.
        """.strip()),
    )


def get_embed_link(
    embed_url: str,
    title: str,
    page_url: str,
) -> tuple[str, str]:
    """Returns the embed link and instructions for the license."""
    embed_code = f'<iframe src="{embed_url}" title="{title}" width="100%" height="500px" frameborder="0"></iframe>'
    return (
        embed_code,
        f"For more details, visit the [full license page]({page_url})."
    )


def get_boilerplate(meta: Dict[str, Any]) -> str:
    """Returns the boilerplate text for the license."""
    return dedent(f"""
    # {meta.get('plain_name', 'License')}

    {meta.get('license_description', '')}
    """).strip()


def get_disclaimer_block(meta: Dict[str, Any], has_official: bool, not_advice_text: str, not_official_text: str) -> str:
    """Returns the disclaimer block for the license."""
    disclaimer = f"## Disclaimer\n\n{not_advice_text}\n\n"
    if has_official:
        disclaimer += f"{not_official_text}\n\n"
    return disclaimer.strip()


def get_header_block(kind: Literal["reader", "markdown", "plaintext"], meta: Dict[str, Any], plain_name: str, plain_version: str) -> str:
    """Returns the header block for the license."""
    if kind == "plaintext":
        return dedent(f"""
        {plain_name} License v{plain_version}
        ===================================

        Plain License: {meta.get('plain_name', '')}
        Original License: {meta.get('original_name', '')}
        """).strip()
    
    return dedent(f"""
    # {plain_name} License v{plain_version}

    **Plain License**: {meta.get('plain_name', '')}  
    **Original License**: {meta.get('original_name', '')}
    """).strip()


def interpretation_block(kind: Literal["reader", "markdown", "plaintext"], meta: Dict[str, Any], has_official: bool, title: str, interpretation_text: Optional[str] = None) -> str:
    """Returns the interpretation block for the license."""
    if not has_official:
        return ""
    
    if kind == "plaintext":
        if interpretation_text:
            return dedent(f"""
            ## Interpretation

            {interpretation_text}
            """).strip()
        return ""
    
    return dedent(f"""
    ## Interpretation

    {meta.get('interpretation_text', '')}
    """).strip()

