"""Fills the fixed Sankalpam template with dynamic Panchangam values."""

from __future__ import annotations

from saarathi.panchangam.schema import Panchangam
from saarathi.core.lang import validate_lang
from saarathi.rituals.sankalpam.template import SANKALPAM_TEMPLATES, SLOT_FIELDS


def build_sankalpam(panchangam: Panchangam, *, lang: str = "te") -> str:
    validate_lang(lang)
    slots = {field: getattr(panchangam, field) for field in SLOT_FIELDS}
    missing = [field for field, value in slots.items() if not value]
    if missing:
        raise ValueError(f"Panchangam missing required field(s) for Sankalpam: {missing}")
    return SANKALPAM_TEMPLATES[lang].format(**slots)
