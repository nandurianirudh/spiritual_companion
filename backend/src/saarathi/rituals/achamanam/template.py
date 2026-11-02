"""Fixed Achamanam wording, transcribed from book_Books_sandhyavandhanam.pdf
pp.4-6 (a separate print edition from Sandhyavandanam.pdf, which backs
Sankalpam/Pravara). No dynamic slots — this text never varies.

NOTE: transcribed from an OCR'd scan; verify against the source PDF /
a priest before using this for an actual ritual.

Unlike every other te/en template pair in this project, ACHAMANAM_TEMPLATE_EN
is NOT a pure transliteration. The text mixes spoken mantra lines (ఓం...నమః)
with physical gesture instructions for the practitioner ("- చూపుడు వ్రేలు,
బ్రొటన వ్రేలితో పెదవి కుడివైపు"). In the "en" version: mantra lines stay
IAST-romanized (still sacred text in the original language), but instruction
lines are actual English translation, not transliterated Telugu prose —
confirmed with the user, since an English reader needs the instructions to
mean something, not just sound like something. Do not "fix" one to match
the other's style.
"""

ACHAMANAM_TEMPLATE = (
    "ఆచమనము\n"
    "అరచేతిని గోర్కర్తాకృతిలో పెట్టి జలమును చేతిలో పోసి ఒక్కొక్క నామము చెబుతూ త్రాగవలెను.\n"
    "ఒకటవసారి\n"
    '"ఓం అచ్యుతాయ నమః" నీటిని త్రాగవలెను.\n'
    "రెండవసారి\n"
    '"ఓం అనంతాయ నమః" నీటిని త్రాగవలెను.\n'
    "మూడవసారి\n"
    '"ఓం గోవిందాయ నమః" నీటిని త్రాగవలెను.\n'
    "ఓం కేశవాయ నమః - చూపుడు వ్రేలు, బ్రొటన వ్రేలితో పెదవి కుడివైపు.\n"
    "ఓం నారాయణాయ నమః - అలాగే ఎడమ వైపు.\n"
    "ఓం మాధవాయ నమః - బ్రొటన ఉంగరం వ్రేళ్ళతో కుడి నేత్రమును.\n"
    "ఓం గోవిందాయ నమః - అలాగే ఎడమ వైపు.\n"
    "ఓం విష్ణవే నమః - చూపుడు వేలు బ్రొటన వేలితో కలిపి కుడి నాసికను.\n"
    "ఓం మధుసూదనాయ నమః - అలాగే ఎడమ వైపు.\n"
    "ఓం త్రివిక్రమాయ నమః - చిటికెన వ్రేలు బ్రొటన వ్రేలు కలిపి కుడి చెవిని.\n"
    "ఓం వామనాయ నమః - అలాగే ఎడమ వైపు.\n"
    "ఓం శ్రీధరాయ నమః - ఐదు వ్రేళ్ళను కలిపి కుడి భుజమును.\n"
    "ఓం హృషీకేశాయ నమః - అలాగే ఎడమ వైపు.\n"
    "ఓం పద్మనాభాయ నమః - అరచేతితో నాభియందు.\n"
    "ఓం దామోదరాయ నమః - అలాగే హృదయము నందు.\n"
    "ఓం శ్రీ వాసుదేవాయ నమః - శిరస్సు నందు స్పృశించాలి."
)

ACHAMANAM_TEMPLATE_EN = (
    "Achamanam\n"
    "Take water in the right palm cupped like a cow's ear, and drink it while chanting each name.\n"
    "First time:\n"
    '"ōṁ acyutāya namaḥ" — drink the water.\n'
    "Second time:\n"
    '"ōṁ anantāya namaḥ" — drink the water.\n'
    "Third time:\n"
    '"ōṁ gōvindāya namaḥ" — drink the water.\n'
    "ōṁ kēśavāya namaḥ - touch the right side of the lips with the index and thumb.\n"
    "ōṁ nārāyaṇāya namaḥ - the same, on the left side.\n"
    "ōṁ mādhavāya namaḥ - touch the right eye with the thumb and ring finger.\n"
    "ōṁ gōvindāya namaḥ - the same, on the left side.\n"
    "ōṁ viṣṇavē namaḥ - touch the right nostril with the index and thumb together.\n"
    "ōṁ madhusūdanāya namaḥ - the same, on the left side.\n"
    "ōṁ trivikramāya namaḥ - touch the right ear with the little finger and thumb together.\n"
    "ōṁ vāmanāya namaḥ - the same, on the left side.\n"
    "ōṁ śrīdharāya namaḥ - touch the right shoulder with all five fingers together.\n"
    "ōṁ hṛṣīkēśāya namaḥ - the same, on the left side.\n"
    "ōṁ padmanābhāya namaḥ - touch the navel with the palm.\n"
    "ōṁ dāmōdarāya namaḥ - the same, at the heart.\n"
    "ōṁ śrī vāsudēvāya namaḥ - touch the top of the head."
)

# One template per supported `lang` value — mirrors
# saarathi.rituals.sankalpam.template.SANKALPAM_TEMPLATES.
ACHAMANAM_TEMPLATES = {
    "te": ACHAMANAM_TEMPLATE,
    "en": ACHAMANAM_TEMPLATE_EN,
}
