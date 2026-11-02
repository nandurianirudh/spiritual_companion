"""Fixed Pravara/Abhivadana wording, transcribed from Sandhyavandanam.pdf
p.20/22 (blank template) and p.24-25 (the Koushika worked example).
Dynamic slots: rishis, descriptor (త్రయార్షేయ/పంచార్షేయ), gotra, sutra,
shakha, name.

NOTE: transcribed from an OCR'd scan; verify against the source PDF /
a priest before using this for an actual ritual — see pravara/data.py's
docstring for the Bharadwaja-specific caveat.
"""

PRAVARA_TEMPLATE = (
    "చతుస్సాగర పర్యంతం గోబ్రాహ్మణేభ్యః శుభం భవతు "
    "{rishis} {descriptor} ప్రవరాన్విత "
    "{gotra} గోత్రః "
    "{sutra} సూత్రః {shakha} శాఖాధ్యయీ "
    "{name} శర్మాహం అస్మి భో అభివాదయే॥"
)

# Same wording as PRAVARA_TEMPLATE above, IAST-romanized — not a translation,
# just the identical text in Latin script. Like PRAVARA_TEMPLATE, not yet
# verified against a priest/authoritative source — flag if editing.
PRAVARA_TEMPLATE_EN = (
    "catussāgara paryantaṁ gōbrāhmaṇēbhyaḥ śubhaṁ bhavatu "
    "{rishis} {descriptor} pravarānvita "
    "{gotra} gōtraḥ "
    "{sutra} sūtraḥ {shakha} śākhādhyayī "
    "{name} śarmāhaṁ asmi bhō abhivādayē॥"
)

# One template per supported `lang` value — mirrors
# saarathi.rituals.sankalpam.template.SANKALPAM_TEMPLATES.
PRAVARA_TEMPLATES = {
    "te": PRAVARA_TEMPLATE,
    "en": PRAVARA_TEMPLATE_EN,
}
