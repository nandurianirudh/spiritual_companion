"""Gotra -> pravara rishi names, and the gotra's display form in the
"___ గోత్రః" slot. Every value below is keyed by `lang` ("te"/"en") — the
"en" side is an IAST/ASCII romanization of the identical "te" wording, never
a semantic translation, mirroring saarathi.rituals.sankalpam.template's te/en split.

Koushika: transcribed verbatim from Sandhyavandanam.pdf p.24-25 (the
book's own worked example) — including "కౌశికస గోత్రః" (not "కౌశిక
గోత్రః"). Whether that "-స" is a real convention or an OCR artifact is
unconfirmed; not extending it to other gotras without a source.

Bharadwaja: NOT in that PDF. Sourced from web references (Vanshmool,
Familypedia) rather than a verified printed source the way Koushika was —
same "verify with a priest before ritual use" caveat as the Sankalpam
template applies here, doubly so.
"""

GOTRA_PRAVARAS: dict[str, dict[str, list[str]]] = {
    "కౌశిక": {
        "te": ["విశ్వామిత్ర", "అఘమర్షణ", "కౌశిక"],
        "en": ["Vishwamitra", "Aghamarshana", "Kaushika"],
    },
    "భరద్వాజ": {
        "te": ["అంగీరస", "బార్హస్పత్య", "భరద్వాజ"],
        "en": ["Angirasa", "Barhaspatya", "Bharadwaja"],
    },
}

GOTRA_LABELS: dict[str, dict[str, str]] = {
    "కౌశిక": {"te": "కౌశికస", "en": "Kaushikasa"},  # as transcribed, see module docstring
    "భరద్వాజ": {"te": "భరద్వాజ", "en": "Bharadwaja"},
}

# The gotra's own name per lang — distinct from GOTRA_LABELS, which carries
# the "-స"/"-sa" display suffix and would be the wrong string to key
# GOTRA_ALIASES off of.
GOTRA_NAMES: dict[str, dict[str, str]] = {
    "కౌశిక": {"te": "కౌశిక", "en": "Kaushika"},
    "భరద్వాజ": {"te": "భరద్వాజ", "en": "Bharadwaja"},
}

# Word preceding "ప్రవరాన్విత", chosen by how many rishis the pravara has
# (త్రయ = three, పంచ = five). Both seeded gotras are 3-rishi; extend this
# if a 5-rishi (pancharshi) gotra is added later.
DESCRIPTOR_BY_RISHI_COUNT: dict[int, dict[str, str]] = {
    3: {"te": "త్రయార్షేయ", "en": "Trayarsheya"},
    5: {"te": "పంచార్షేయ", "en": "Pancharsheya"},
}

# Case-folded name (either script) -> canonical (Telugu) gotra key. Derived
# from GOTRA_NAMES so it can't drift out of sync when a gotra is added.
GOTRA_ALIASES: dict[str, str] = {
    name.casefold(): key for key, names in GOTRA_NAMES.items() for name in names.values()
}


def resolve_gotra(gotra: str) -> str | None:
    """Look up `gotra` (Telugu or English spelling, case-insensitive) and
    return its canonical Telugu key, or None if unrecognized."""
    return GOTRA_ALIASES.get(gotra.strip().casefold())
