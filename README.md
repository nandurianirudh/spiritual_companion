# personal_companion

Personal spiritual companion app. MVP: Sankalpam generator driven by
Telugu Panchangam data. See `CLAUDE.md` for commands and architecture.

## Running it

All commands run from `backend/`. Requires [uv](https://docs.astral.sh/uv/)
and Python 3.13 (uv installs the interpreter itself if missing).

### 1. Install dependencies

```
cd backend
uv sync
```
Output:
```
Resolved 25 packages in 1ms
Checked 25 packages in 3ms
```
(First run downloads/builds packages instead of just checking them.)

### 2. Run the test suite

```
uv run pytest -q
```
Output:
```
...................................ss                                    [100%]
35 passed, 2 skipped in 9.10s
```
The skipped test is a live-API regression check. Run it too with:
```
SAARATHI_RUN_LIVE_API_TESTS=1 uv run pytest -q
```
Output:
```
...                                                                      [100%]
3 passed in 1.57s
```
That third test hits the real TeluguPanchangam.app API and asserts
Hyderabad/2026-08-29 comes back as samvatsara "Parabhava" — the exact case
that got VedicOrbit rejected as a provider (see the agreement doc, section 4).

### 3. Generate a Sankalpam

```
uv run saarathi --date 2026-08-29 --lat 17.385 --lng 78.486 --city Hyderabad
```

**Inputs:**

| flag | required | meaning | example |
|---|---|---|---|
| `--date` | yes | ritual date, `YYYY-MM-DD` | `2026-08-29` |
| `--lat` | yes | latitude of the ritual location | `17.385` |
| `--lng` | yes | longitude of the ritual location | `78.486` |
| `--city` | no | display label only, not used in the API call | `Hyderabad` |
| `--tz` | no, default `Asia/Kolkata` | IANA timezone for the location | `Asia/Kolkata` |
| `--time` | no, defaults to current time in `--tz` | ritual time `HH:MM` (24h) — picks which tithi/nakshatra/yoga/karana is actually valid at that moment, see below | `06:00` |
| `--lang` | no, default `te` | output script: `te` (Telugu) or `en` (IAST-romanized) — same wording either way, not a translation | `en` |

### Ritual-time transitions

Tithi/nakshatra/yoga/karana can change *during* a day, and — a subtlety found by
testing against live data — a date's own values in the API are anchored to
something like sunrise, not midnight. So the same date can resolve to different
values depending on `--time`. Confirmed live, straddling a real boundary
(nakshatra transitions 2026-08-30T03:42):

```
uv run saarathi --date 2026-08-30 --lat 17.385 --lng 78.486 --city Hyderabad --time 02:00
# ...నక్షత్రే... shows పూర్వభాద్ర (Purva Bhadrapada) — before the transition

uv run saarathi --date 2026-08-30 --lat 17.385 --lng 78.486 --city Hyderabad --time 06:00
# ...నక్షత్రే... shows ఉత్తరభాద్ర (Uttara Bhadrapada) — after it
```
Same date, two different nakshatras — proves the resolution works end-to-end.
This requires fetching the previous, requested, and next day (3 API calls);
see `CLAUDE.md` for why. Results are cached in-process, so repeat calls for
the same day don't re-hit the API.

**Output** (actual run, real API data):
```
శ్రీ గోవింద! గోవింద! గోవింద! శ్రీ మహావిష్ణోరాజ్ఞయా ప్రవర్తమానస్య అద్య బ్రహ్మణః ద్వితీయ పరార్ధే శ్రీ శ్వేతవరాహ కల్పే వైవస్వత మన్వంతరే, కలియుగే, ప్రథమపాదే, జంబూద్వీపే, భరతవర్షే, భరతఖండే, మేరోర్దక్షిణ దిగ్భాగే, శ్రీరంగస్య ఉత్తర దిక్పార్శ్వదేశే, గంగాకావేర్యోర్మధ్యదేశే, భగవత్ భాగవతాచార్య సన్నిధౌ, అస్మిన్ వర్తమాన వ్యావహారిక చాంద్రమాన ప్రభవాది షష్టి సంవత్సరాణాం మధ్యే పరాభవ సంవత్సరే దక్షిణాయనం అయనే శరద్ ఋతువు ఋతౌ శ్రావణం మాసే కృష్ణ పక్షం పక్షే పాడ్యమి తిథౌ శనివారం వాసరే పూర్వభాద్ర నక్షత్రే శుభయోగే శుభకరణే ఏవంగుణ విశేషణ విశిష్టాయాం అస్యాం శుభ తిథౌ భగవదాజ్ఞయా భాగవతాచార్య కైంకర్యరూపేణ ప్రాతః సంధ్యావందనం కరిష్యే.
```
The dynamic slots filled in this run: samvatsara=పరాభవ (Parabhava), ayana=దక్షిణాయనం,
ritu=శరద్ ఋతువు, masa=శ్రావణం, paksha=కృష్ణ పక్షం, tithi=పాడ్యమి, vara=శనివారం,
nakshatra=పూర్వభాద్ర. Everything else in the output is fixed wording from the template.

### CLI help

```
uv run saarathi --help
```
```
 Usage: saarathi [OPTIONS]

┌─ Options ───────────────────────────────────────────────────────────────────┐
│ *  --date                      <str>    YYYY-MM-DD [required]               │
│ *  --lat                       <float>  Latitude [required]                 │
│ *  --lng                       <float>  Longitude [required]                │
│    --city                      <str>    City name, for display only         │
│    --tz                        <str>    [default: Asia/Kolkata]             │
│    --install-completion                 Install completion for the current  │
│                                         shell.                              │
│    --show-completion                    Show completion for the current     │
│                                         shell, to copy it or customize the  │
│                                         installation.                       │
│    --help                               Show this message and exit.         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4. Run the API (FastAPI)

```
uv run uvicorn saarathi.api:app --reload
```
Then:
```
curl "http://localhost:8000/v1/sankalpam?date=2026-08-30&lat=17.385&lng=78.486&city=Hyderabad&time=06:00"
```
Output (actual run):
```json
{"sankalpam":"శ్రీ గోవింద! ... ఉత్తరభాద్ర నక్షత్రే ... సంధ్యావందనం కరిష్యే.","panchangam":{"date":"2026-08-30","location":{"city":"Hyderabad","latitude":17.385,"longitude":78.486,"timezone":"Asia/Kolkata"},"ritual_time":"06:00","samvatsara":"పరాభవ","masa":"శ్రావణం","is_adhika_masa":false,"paksha":"కృష్ణ పక్షం","tithi":"విదియ","nakshatra":"ఉత్తరభాద్ర","nakshatra_pada":2,"yoga":"శూల","karana":"గరజ","vara":"ఆదివారం","ayana":"దక్షిణాయనం","ritu":"శరద్ ఋతువు","sunrise":"2026-08-30T06:03:16+05:30","sunset":"2026-08-30T18:33:27+05:30","transitions":{...}}}
```
`/v1/sankalpam` params mirror the CLI flags (`date`, `lat`, `lng`, `city`, `tz`, `time`, `lang`).
`/health` returns `{"status": "ok"}` for container liveness checks.

There's also `/pravara` — fills the fixed Pravara/Abhivadana template for a
gotra:
```
curl "http://localhost:8000/v1/pravara?gotra=కౌశిక"
# or, English spelling and script both work:
curl "http://localhost:8000/v1/pravara?gotra=Kaushika&lang=en"
```
Params: `gotra` (required — Telugu or English spelling, e.g. `కౌశిక`/`Kaushika`),
`sutra`, `shakha`, `name` (all optional, default to the source PDF's own
worked example, in `lang`), `lang` (`te`/`en`, default `te`). Unlike
`/sankalpam`, Pravara has no CLI command yet — API only.

`/v1/achamanam` and `/v1/pranayamam` return two more fixed ritual texts, sourced
from a different print edition (`documents/book_Books_sandhyavandhanam.pdf`,
pp.4-6 and pp.6-7). Unlike Sankalpam/Pravara, these have no dynamic
slots — just a `lang` param:
```
curl "http://localhost:8000/v1/achamanam"
curl "http://localhost:8000/v1/pranayamam?lang=en"
```
In `lang=en`, the ఓం-mantra lines stay IAST-romanized but the physical
gesture instructions ("touch the right side of the lips with the index
and thumb") are actual English translation, not transliteration — the
one deliberate exception to the te/en convention every other endpoint
follows (see `CLAUDE.md`).

### 5. Run with Docker

```
docker compose up --build
```
Output (actual run): image builds, then `Container backend-saarathi-1  Started`.
Same `curl` command as above works against `http://localhost:8000` once it's up.
Stop with `docker compose down`.

## Files

```
documents/Personal_Spiritual_App_Agreements.docx
                                         Product direction, Panchangam data
                                          requirements, API evaluation
                                          (why VedicOrbit was rejected,
                                          why TeluguPanchangam.app was
                                          chosen), canonical schema spec,
                                          MVP decisions, naming ideas.

Sandhyavandanam.pdf                      Source ritual text (Krishna
                                          Yajurveda, Telugu+English) the
                                          Sankalpam wording and dynamic
                                          slots are transcribed from
                                          (see p.8 for the Sankalpam
                                          mantra with blank slots).

documents/                               Other source PDFs, incl.
                                          book_Books_sandhyavandhanam.pdf
                                          (a separate print edition backing
                                          Achamanam/Pranayamam) and its
                                          full verbatim Telugu transcription,
                                          book_Books_sandhyavandhanam.md
                                          (vision-transcribed page by page —
                                          the PDF has no text layer).

CLAUDE.md                                Guidance for Claude Code:
                                          commands, architecture, gotchas.

backend/                                 uv-managed Python 3.13 package
                                          ("saarathi") implementing the
                                          pipeline. See below.
```

### backend/

```
pyproject.toml                           Package config + dependencies
                                          (managed via `uv`, not pip).
uv.lock                                  Locked dependency versions.
Dockerfile                               uv-based image; runs uvicorn.
docker-compose.yml                       `docker compose up` -> localhost:8000.
.dockerignore                            Keeps .venv/tests out of the image.

src/saarathi/
  cli.py                                 Typer CLI entry point
                                          (`uv run saarathi --date ...`).
                                          Wires panchangam + sankalpam
                                          together and prints the result.
  api/                                   FastAPI app (main.py: CORS, /health,
                                          mounts routers at /v1) + one router
                                          per ritual in routers/. No logic
                                          duplicated from cli.py.
  core/lang.py                           Shared te/en validation.
  rituals/                               One folder per ritual (below).

  panchangam/
    schema.py                            Canonical Panchangam data model
                                          (pydantic). Everything downstream
                                          depends only on this, never on
                                          the provider's raw JSON.
    client.py                            Adapter for TeluguPanchangam.app:
                                          fetch_with_transitions() calls the
                                          API (lru_cache'd), normalize() maps
                                          the real JSON
                                          shape (confirmed live) into the
                                          canonical schema, resolved for
                                          a given ritual time.

  rituals/sankalpam/
    template.py                          Fixed Sankalpam wording +
                                          dynamic slot list, transcribed
                                          from Sandhyavandanam.pdf p.8.
                                          te/en templates (en = IAST
                                          transliteration).
    rules.py                             Fills the template's slots from
                                          a Panchangam object.

  rituals/pravara/
    data.py                              Gotra -> pravara rishi names,
                                          gotra labels, per lang. Derived
                                          te/en alias lookup (GOTRA_ALIASES).
    template.py                          Fixed Pravara template, te/en.
    rules.py                             build_pravara(gotra, ..., lang=).

  rituals/achamanam, rituals/pranayamam                Two more fixed ritual texts
                                          (source: a different print
                                          edition, book_Books_sandhyavandhanam.pdf).
                                          No dynamic slots. In lang="en",
                                          mantra lines are IAST but gesture
                                          instructions are actual English
                                          translation — the one deliberate
                                          exception to the te/en convention.

tests/
  test_sankalpam.py                      Mocked-API pipeline + transition +
                                          caching + API-endpoint tests, plus
                                          live-API regression tests for the
                                          Parabhava/Hyderabad case and the
                                          nakshatra transition boundary
                                          (opt-in via
                                          SAARATHI_RUN_LIVE_API_TESTS=1).
  test_pravara.py                        Pravara build/API tests, te + en,
                                          incl. English-gotra-alias lookup.
  test_achamanam.py, test_pranayamam.py  Fixed-text build/API tests, te + en.
```
