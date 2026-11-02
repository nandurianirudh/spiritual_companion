# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Personal spiritual companion app. MVP is a **Sankalpam generator** driven by
accurate Telugu Panchangam data. Full product direction, data requirements,
and API evaluation are in `documents/Personal_Spiritual_App_Agreements.docx` — read
it before making architectural changes. `Sandhyavandanam.pdf` is the source
ritual text the Sankalpam wording/slots are transcribed from.

All code lives under `backend/` (and later `frontend/`). The repo root holds only these source docs
plus this file — keep it that way; don't scatter code at the root.

`documents/` holds the other source PDFs, including
`book_Books_sandhyavandhanam.pdf` — a separate print edition (Jeeyar
Educational Trust, 2001) that backs Achamanam/Pranayamam (see below).
`documents/book_Books_sandhyavandhanam.md` is a faithful, verbatim Telugu
transcription of that entire 107-page scanned book (no text layer in the
PDF, so it was vision-transcribed page by page) — a document conversion,
not a ritual-template feature; regenerate it by re-rendering the PDF's
pages and re-transcribing if it ever needs updating.

## Commands

Run everything from `backend/` (uv-managed, Python 3.13):

```
uv sync                              # install/update deps from pyproject.toml + uv.lock
uv add <package>                     # add a runtime dependency
uv add --dev <package>               # add a dev-only dependency
uv run pytest -q                     # run tests
uv run pytest tests/test_sankalpam.py::test_build_sankalpam_fills_all_slots  # single test
uv run saarathi --date 2026-08-29 --lat 17.385 --lng 78.486 --city Hyderabad --time 06:00  # run CLI
uv run uvicorn saarathi.api:app --reload  # run the FastAPI service locally
docker compose up --build            # run it in Docker (localhost:8000)
```

Live-API regression tests (hit the real TeluguPanchangam.app endpoint, skipped by default):
```
SAARATHI_RUN_LIVE_API_TESTS=1 uv run pytest -q
```

Never run `pip install` or manage a venv by hand — `uv` owns
`pyproject.toml`/`uv.lock`/`.venv` for this project.

## Architecture

Pipeline (see agreement doc section 7 for the full diagram):

```
saarathi.panchangam.client.fetch_with_transitions -> 3 cached calls to TeluguPanchangam.app
saarathi.panchangam.client.normalize -> raw JSON, resolved for ritual_dt -> saarathi.panchangam.schema.Panchangam
saarathi.rituals.sankalpam.rules.build_sankalpam -> Panchangam -> filled Sankalpam text
saarathi.rituals.sankalpam.template  -> fixed Telugu wording + slot list (transcribed from PDF p.8)
saarathi.cli / saarathi.api  -> Typer CLI and FastAPI entry points, both call the same two functions above
```

Key rule: nothing outside `panchangam/client.py` should touch the provider's
raw JSON shape. Everything downstream (rules engine, template filler, future
FastAPI layer, future LangGraph nodes) depends only on the canonical
`Panchangam` pydantic model in `panchangam/schema.py`. If the provider's
actual response shape differs from what `normalize()` assumes, fix the
mapping in `normalize()` only — the schema and everything downstream should
not need to change.

### Provider caveat

`client.normalize()`'s field mapping is confirmed against a real captured
payload (2026-08-29, Hyderabad — `client.py`'s module docstring has the full
shape). If the provider changes its response shape, hit the live API again
and fix the mapping in `normalize()` only.

Regression check: `samvatsara == "Parabhava"` for 2026-08-29/Hyderabad — this
is the specific case that got VedicOrbit rejected as a provider (it returned
the wrong value, "Raudra", for that date/location).

### Ritual-time transitions and caching

Tithi/nakshatra/yoga/karana can change mid-day, and a date's own values in
the API are anchored to something like sunrise, not midnight — confirmed by
testing against live data: 2026-08-29's nakshatra doesn't end until
2026-08-30T03:42, yet 2026-08-30's own payload already shows the *next*
nakshatra, even for a ritual time of 02:00 that date. So resolving "what's
correct at this ritual time" requires checking the **previous**, **current**,
and **next** day's payload — not just current vs. next. See `client.py`'s
module docstring for the full reasoning and the upstream GitHub doc this is
based on (`suhasatluri/telugu-panchangam-app`, `API.md`).

`_fetch_day()` is `@lru_cache`'d on `(date, lat, lng, tz, lang)` — a given
combination is deterministic and never changes, so the cache never expires
for the life of the process. `fetch_with_transitions()` always fetches 3 days
per call, but repeat calls for the same day reuse the cache instead of
re-hitting the API. Cached payloads are shared dicts — never mutate one in
place; build new dicts instead (see how `fetch_with_transitions` merges
prev/next data without touching the cached originals).

### Sankalpam template

`rituals/sankalpam/template.py` separates fixed wording from the 8 dynamic slots
(samvatsara, ayana, ritu, masa, paksha, tithi, vara, nakshatra) per the
agreement doc's canonical schema — these field names are shared 1:1 between
`Panchangam` and the template slots. The wording itself is OCR-transcribed
from the source PDF and not yet verified against a priest/authoritative
source — flag this if editing ritual text.

`build_sankalpam(panchangam, lang="te")` picks between `SANKALPAM_TEMPLATE`
(Telugu) and `SANKALPAM_TEMPLATE_EN` (IAST-romanized) — the `en` side is a
transliteration of the identical wording, never a semantic translation.
Slot values come out in the matching script for free: `client.get_panchangam`
already accepts `lang` and picks `section[lang]` per anga (`client.py:173`),
so passing `lang="en"` end to end needs no extra plumbing there.

### Pravara

`rituals/pravara/rules.py`'s `build_pravara(gotra, *, sutra=None, shakha=None,
name=None, lang="te")` fills `rituals/pravara/template.py`'s fixed template from
gotra data looked up in `rituals/pravara/data.py`. Unlike Sankalpam, Pravara's slot
values (rishi names, gotra label, descriptor) are hardcoded local data, not
provider data — so `rituals/pravara/data.py` keys every one of those by `lang` too
(`GOTRA_PRAVARAS`, `GOTRA_LABELS`, `DESCRIPTOR_BY_RISHI_COUNT`), the same
te/en split as the Sankalpam template.

`gotra` itself is looked up by either script via `resolve_gotra()`, which
resolves through `GOTRA_ALIASES` — an index *derived* from `GOTRA_NAMES`
(casefolded name -> canonical Telugu key), not hand-maintained, so it can't
drift when a gotra is added. The canonical key stored everywhere else
(`GOTRA_PRAVARAS`, `GOTRA_LABELS`) stays Telugu-script regardless of `lang`.

Same "OCR-transcribed, not priest-verified" caveat as the Sankalpam template
applies to both the `te` and `en` Pravara wording — doubly so for the
Bharadwaja gotra data, which (per `rituals/pravara/data.py`'s docstring) came from
web references rather than the source PDF.

### Achamanam / Pranayamam

`rituals/achamanam/` and `rituals/pranayamam/` (mirroring `rituals/pravara/`'s three-file shape)
hold two more fixed ritual texts, sourced from a *different* print edition
— `documents/book_Books_sandhyavandhanam.pdf` (pp.4-6 and pp.6-7
respectively), not the `Sandhyavandanam.pdf` that backs Sankalpam/Pravara.
Unlike Sankalpam/Pravara, these have **zero dynamic slots** — `build_achamanam(lang="te")`/
`build_pranayamam(lang="te")` just return the matching fixed
`*_TEMPLATES[lang]` string, no slot-filling.

Both texts mix spoken mantra lines (ఓం...నమః) with physical gesture
instructions for the practitioner ("- చూపుడు వ్రేలు, బ్రొటన వ్రేలితో పెదవి
కుడివైపు" = touch the right side of the lips with index+thumb) — the
output includes both, by design; this is a step-by-step ritual guide, not
a slot-filled sentence.

**Deliberate exception to the te/en convention below:** in these two
modules' `en` templates, mantra lines stay IAST transliteration but
instruction lines are actual English translation (not transliterated
Telugu prose) — an English reader needs the stage directions to mean
something, not just sound like something. Every other feature in this
project follows the transliteration-only rule; don't extend this
exception without a reason as deliberate as this one.

### Bilingual (te/en) convention — applies to every future ritual-text feature

Every ritual-text feature ships bilingual from the start, following the
Sankalpam/Pravara pattern above:
- Fixed wording lives in a `*_TEMPLATES = {"te": ..., "en": ...}` dict.
- Any hardcoded lookup data that reaches the output (names, labels,
  descriptors, defaults) is lang-keyed the same way.
- The `build_*()` function takes `lang: str = "te"` and raises `ValueError`
  on anything else.
- The API exposes `lang` as a query param, 400 on a bad value; the CLI gets
  a `--lang` option.
- The `en` side is always transliteration of the identical wording — never
  a semantic translation.
- Lookup keys (like `gotra`) stay canonical Telugu; add a derived alias
  index (see `GOTRA_ALIASES`) if the feature should also accept the English
  spelling as input.

### Layout

```
backend/src/saarathi/
  core/        shared helpers (lang.py: te/en validation — use validate_lang, don't re-check)
  panchangam/  provider client + canonical schema
  rituals/     one folder per ritual: template.py, rules.py (+ data.py)
  api/         main.py (app, CORS, /health), deps.py (Lang param), routers/<ritual>.py
  cli.py
backend/tests/
```
New ritual = new `rituals/<name>/` + new `api/routers/<name>.py` + one line in `api/main.py`.

### API / Docker

`api/` is a thin FastAPI wrapper — routes live at `/v1/<ritual>` (plus unversioned
`/health`) and call the same `get_panchangam`/`build_*` functions `cli.py` uses.
Don't duplicate pipeline logic into `api/`; add it to `panchangam`/`rituals`
and both entry points pick it up. CORS allows the Vite dev origin by default;
set `SAARATHI_CORS_ORIGINS` (comma-separated) for deployed web origins.
`Dockerfile` builds the image with `uv` (two-stage `uv sync` so dependency
layers cache independently of source changes) and runs
`uvicorn saarathi.api:app`; `docker-compose.yml` exposes port 8000.

### Frontend (`frontend/`)

Not started — only `frontend/README.md` (the plan) exists. When built, it
consumes `/v1/*` only and never reimplements Panchangam/ritual logic.
