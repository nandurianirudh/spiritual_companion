"""Single source of truth for supported output scripts (te/en convention)."""

from __future__ import annotations

SUPPORTED_LANGS = ("te", "en")


def validate_lang(lang: str) -> str:
    if lang not in SUPPORTED_LANGS:
        raise ValueError(f"Unsupported lang {lang!r}; must be one of {sorted(SUPPORTED_LANGS)}")
    return lang
