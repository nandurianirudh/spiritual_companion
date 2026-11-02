"""Fixed Pranayamam wording, transcribed from book_Books_sandhyavandhanam.pdf
pp.6-7 (a separate print edition from Sandhyavandanam.pdf, which backs
Sankalpam/Pravara). No dynamic slots — this text never varies.

NOTE: transcribed from an OCR'd scan; verify against the source PDF /
a priest before using this for an actual ritual.

Same departure from the usual te/en convention as saarathi.rituals.achamanam.template:
PRANAYAMAM_TEMPLATE_EN is NOT a pure transliteration. The rishi/chandas/
devata/viniyoga attribution lines and the physical-action lines are
instructional prose, so they get actual English translation; the ōṁ-mantra
lines stay IAST-romanized. Do not "fix" one to match the other's style.
"""

PRANAYAMAM_TEMPLATE = (
    "ప్రాణాయామము\n"
    "పృథివ్యాః మేరుః పృష్ఠ ఋషిః - శిరస్సును స్పృశిస్తూ\n"
    "సుతలం ఛందః - నాసికను స్పృశిస్తూ\n"
    "కూర్మోదేవతా, ఆసనే వినియోగః - హృదయమును\n"
    "ఓం అనంతాసనాయ నమః - ఆసనమును\n"
    "ప్రాణస్య పరబ్రహ్మ ఋషిః - శిరస్సును\n"
    "దైవీ గాయత్రీ ఛందః - నాసికను\n"
    "పరమాత్మా దేవతా - హృదయమును\n"
    "ప్రాణాయామే వినియోగః\n"
    "కుడి బ్రొటన వ్రేలితోను ఉంగరపు వ్రేలితోను ముక్కును పట్టుకొని, "
    "మధ్య వ్రేలును లోనికి మడిచి ఉంచవలెను.\n"
    "కుడి ముక్కుతో గాలిని వదలి ఎడమ ముక్కుతో గాలిని పీలుస్తూ\n"
    "పూరకం - ఓం భూః ఓం భువః ఓగం సువః ఓం మహః ఓం జనః ఓం తపః ఓగం సత్యం\n"
    "(రెండు ముక్కులను మూసి)\n"
    "కుంభకం- ఓం తత్సవితుర్వరేణ్యం భర్గో దేవస్య ధీమహి ధియో యోనః ప్రచోదయాత్ |\n"
    "ఓమాపో జ్యోతీ రసోఽమృతం బ్రహ్మ భూర్భువస్సువరోమ్ ||\n"
    "(కుడి ముక్కుతో గాలిని వదలుతూ) భూర్భువస్సువరోమ్||"
)

PRANAYAMAM_TEMPLATE_EN = (
    "Pranayamam\n"
    "Rishi of the earth is Meru, of the crown of the head - touching the head\n"
    "Meter is Sutala - touching the nose\n"
    "Deity is the tortoise; used for the seat - touching the heart\n"
    "ōṁ anantāsanāya namaḥ - touching the seat\n"
    "Rishi of the breath is the Supreme Brahman - touching the head\n"
    "Meter is the divine Gayatri - touching the nose\n"
    "Deity is the Supreme Self - touching the heart\n"
    "Used for pranayama\n"
    "Hold the nose with the right thumb and ring finger, folding the middle finger inward.\n"
    "Release the breath through the right nostril and draw it in through the left, while reciting:\n"
    "Puraka (inhalation) - ōṁ bhūḥ ōṁ bhuvaḥ ōgaṁ suvaḥ ōṁ mahaḥ ōṁ janaḥ ōṁ tapaḥ ōgaṁ satyaṁ\n"
    "(closing both nostrils)\n"
    "Kumbhaka (retention) - ōṁ tatsaviturvarēṇyaṁ bhargō dēvasya dhīmahi dhiyō yōnaḥ pracōdayāt |\n"
    "ōmāpō jyōtī rasō'mṛtaṁ brahma bhūrbhuvassuvarōm ||\n"
    "(releasing the breath through the right nostril) bhūrbhuvassuvarōm ||"
)

# One template per supported `lang` value — mirrors
# saarathi.rituals.sankalpam.template.SANKALPAM_TEMPLATES.
PRANAYAMAM_TEMPLATES = {
    "te": PRANAYAMAM_TEMPLATE,
    "en": PRANAYAMAM_TEMPLATE_EN,
}
