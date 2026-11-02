"""Fixed Sankalpam wording, transcribed from Sandhyavandanam.pdf p.8
(Krishna Yajurveda prathaha-sandhyavandanam). Dynamic slots are the
Panchangam fields identified in Personal_Spiritual_App_Agreements.docx
section 2 — everything else is fixed.

NOTE: transcribed from an OCR'd scan; verify against the source PDF /
a priest before using this for an actual ritual.
"""

SANKALPAM_TEMPLATE = (
    "శ్రీ గోవింద! గోవింద! గోవింద! శ్రీ మహావిష్ణోరాజ్ఞయా "
    "ప్రవర్తమానస్య అద్య బ్రహ్మణః ద్వితీయ పరార్ధే "
    "శ్రీ శ్వేతవరాహ కల్పే వైవస్వత మన్వంతరే, కలియుగే, "
    "ప్రథమపాదే, జంబూద్వీపే, భరతవర్షే, భరతఖండే, మేరోర్దక్షిణ "
    "దిగ్భాగే, శ్రీరంగస్య ఉత్తర దిక్పార్శ్వదేశే, "
    "గంగాకావేర్యోర్మధ్యదేశే, భగవత్ భాగవతాచార్య "
    "సన్నిధౌ, అస్మిన్ వర్తమాన వ్యావహారిక చాంద్రమాన "
    "ప్రభవాది షష్టి సంవత్సరాణాం మధ్యే {samvatsara} సంవత్సరే "
    "{ayana} అయనే {ritu} ఋతౌ {masa} మాసే {paksha} పక్షే {tithi} తిథౌ "
    "{vara} వాసరే {nakshatra} నక్షత్రే శుభయోగే శుభకరణే ఏవంగుణ "
    "విశేషణ విశిష్టాయాం అస్యాం శుభ తిథౌ "
    "భగవదాజ్ఞయా భాగవతాచార్య కైంకర్యరూపేణ ప్రాతః "
    "సంధ్యావందనం కరిష్యే."
)

# Same wording as SANKALPAM_TEMPLATE above, IAST-romanized — not a translation,
# just the identical Sanskrit/Telugu text in Latin script. Transcribed by hand
# from the Telugu template; like SANKALPAM_TEMPLATE, not yet verified against
# a priest/authoritative source — flag if editing ritual text.
SANKALPAM_TEMPLATE_EN = (
    "śrī govinda! govinda! govinda! śrī mahāviṣṇōrājñayā "
    "pravartamānasya adya brahmaṇaḥ dvitīya parārdhe "
    "śrī śvētavarāha kalpē vaivasvata manvantarē, kaliyugē, "
    "prathamapādē, jambūdvīpē, bharatavarṣē, bharatakhaṇḍē, mērōrdakṣiṇa "
    "digbhāgē, śrīraṅgasya uttara dikpārśvadēśē, "
    "gaṅgākāvēryōrmadhyadēśē, bhagavat bhāgavatācārya "
    "sannidhau, asmin vartamāna vyāvahārika cāndramāna "
    "prabhavādi ṣaṣṭi saṁvatsarāṇāṁ madhyē {samvatsara} saṁvatsarē "
    "{ayana} ayanē {ritu} ṛtau {masa} māsē {paksha} pakṣē {tithi} tithau "
    "{vara} vāsarē {nakshatra} nakṣatrē śubhayōgē śubhakaraṇē ēvaṁguṇa "
    "viśēṣaṇa viśiṣṭāyāṁ asyāṁ śubha tithau "
    "bhagavadājñayā bhāgavatācārya kaiṅkaryarūpēṇa prātaḥ "
    "sandhyāvandanaṁ kariṣyē."
)

# One template per supported `lang` value. Both share the same slot names —
# the Panchangam field values themselves come out in `lang`'s script too,
# via saarathi.panchangam.client.get_panchangam(lang=...).
SANKALPAM_TEMPLATES = {
    "te": SANKALPAM_TEMPLATE,
    "en": SANKALPAM_TEMPLATE_EN,
}

# Slot names, in template order — matches the canonical Panchangam schema
# field names 1:1 (Personal_Spiritual_App_Agreements.docx section 2/8).
SLOT_FIELDS = (
    "samvatsara",
    "ayana",
    "ritu",
    "masa",
    "paksha",
    "tithi",
    "vara",
    "nakshatra",
)
