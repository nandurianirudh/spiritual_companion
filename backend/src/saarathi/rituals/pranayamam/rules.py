"""Returns the fixed Pranayamam text for the requested lang. No dynamic
slots — unlike Sankalpam/Pravara, nothing here varies per request."""

from __future__ import annotations

from saarathi.core.lang import validate_lang
from saarathi.rituals.pranayamam.template import PRANAYAMAM_TEMPLATES


def build_pranayamam(*, lang: str = "te") -> str:
    validate_lang(lang)
    return PRANAYAMAM_TEMPLATES[lang]
