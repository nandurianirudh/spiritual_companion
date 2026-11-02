"""Fills the fixed Pravara template from a gotra (looked up) plus
sutra/shakha/name (given, defaulting to the PDF's own worked example)."""

from __future__ import annotations

from saarathi.core.lang import validate_lang
from saarathi.rituals.pravara.data import (
    DESCRIPTOR_BY_RISHI_COUNT,
    GOTRA_LABELS,
    GOTRA_NAMES,
    GOTRA_PRAVARAS,
    resolve_gotra,
)
from saarathi.rituals.pravara.template import PRAVARA_TEMPLATES

# Defaults are the PDF's own worked example (Sandhyavandanam.pdf p.24-25),
# per lang — the "en" side is IAST/ASCII romanization, not a translation.
DEFAULT_SUTRA = {"te": "ఆపస్తంభ", "en": "Apastamba"}
DEFAULT_SHAKHA = {"te": "కృష్ణయజుః", "en": "Krishna Yajuh"}
DEFAULT_NAME = {"te": "కృష్ణమాచార్య దాస", "en": "Krishnamacharya Dasa"}


def build_pravara(
    gotra: str,
    *,
    sutra: str | None = None,
    shakha: str | None = None,
    name: str | None = None,
    lang: str = "te",
) -> str:
    validate_lang(lang)

    key = resolve_gotra(gotra)
    if key is None:
        raise ValueError(f"No pravara data for gotra: {gotra!r}. Known: {sorted(GOTRA_NAMES)}")

    rishis = GOTRA_PRAVARAS[key][lang]
    descriptor = DESCRIPTOR_BY_RISHI_COUNT.get(len(rishis), {}).get(lang)
    if descriptor is None:
        raise ValueError(f"No descriptor word for a {len(rishis)}-rishi pravara")

    return PRAVARA_TEMPLATES[lang].format(
        rishis=" ".join(rishis),
        descriptor=descriptor,
        gotra=GOTRA_LABELS[key][lang],
        sutra=sutra if sutra is not None else DEFAULT_SUTRA[lang],
        shakha=shakha if shakha is not None else DEFAULT_SHAKHA[lang],
        name=name if name is not None else DEFAULT_NAME[lang],
    )
