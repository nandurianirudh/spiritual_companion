"""Adapter for TeluguPanchangam.app.

TeluguPanchangam.app is the primary provider (see
Personal_Spiritual_App_Agreements.docx section 5-6). No API key required.

Field mapping below is confirmed against a live response captured
2026-08-29 for Hyderabad (17.385, 78.486) — samvatsara came back
"Parabhava", matching the agreement doc and NOT the "Raudra" VedicOrbit
returned. Real payload shape (verified):

    {"data": {
        "date": "...", "samvatsaram": {"te","en","number"},
        "masa": {"te","en","number","isAdhika"},
        "paksha": {"te","en","value"}, "ritu": {"te","en"}, "ayana": {"te","en"},
        "tithi": {"te","en","number","endsAt","nextTithi":{"te","en","number"}},
        "nakshatra": {"te","en","number","pada","endsAt"},
        "yoga": {"te","en","number","isAuspicious","endsAt"},
        "karana": {"te","en","number","endsAt"},
        "vara": {"te","en","number"},
        "sunrise", "sunset" (top-level ISO datetimes),
        "moonrise","moonset","moonPhase","rahukalam","gulikaKalam",
        "yamagandam","festivals",
      }, "source", "computedAt"}

lat/lng/tz are not echoed back in the response, so they're carried over
from the request rather than read from the payload.

TRANSITIONS (see Personal_Spiritual_App_Agreements.docx section 3 —
"Sankalpam must use the Panchangam state at the actual ritual time"):

tithi/nakshatra/yoga/karana each carry an `endsAt`. If the ritual time is
past `endsAt`, the value in this date's payload is stale. Per the
provider's own transition-timing guide
(github.com/suhasatluri/telugu-panchangam-app, API.md — "Handling Multiple
Transitions"): tithi is self-contained (payload includes `nextTithi`);
nakshatra/yoga/karana have no such field, so the documented workaround is
to query `/api/panchangam` for an adjacent calendar date and take that
day's value instead.

A subtlety upstream doesn't spell out, found by testing against live data:
a date's own anga values are anchored to something like sunrise, not
midnight. Confirmed live: 2026-08-29's nakshatra (Purva Bhadrapada) doesn't
end until 2026-08-30T03:42 — but the 2026-08-30 payload's OWN nakshatra
field already reports the next one, Uttara Bhadrapada, even for a ritual
time of 02:00 that same date. So a ritual performed before that pre-dawn
cutoff needs the *previous* date's value, not the current date's — a
same-date-only comparison (today vs. tomorrow) gets this wrong for any
ritual time before that anga's early-morning rollover.

`fetch_with_transitions()` therefore fetches yesterday/today/tomorrow (3
calls, each independently cached by `_fetch_day`) and stitches
prev/next-day values onto today's payload for nakshatra/yoga/karana
(`prevNakshatra`/`nextNakshatra`, etc. — tithi keeps the provider's own
`nextTithi` and gets a matching `prevTithi`). `normalize()` then picks
whichever of prev/today/next is valid for the requested ritual time.

Caveat (upstream's own limitation, not ours): this assumes at most one
transition per anga per calendar day each direction. Doesn't hold in
general, but there is no endpoint that exposes a full transition list.
"""

from __future__ import annotations

from datetime import date as date_cls
from datetime import datetime, timedelta
from functools import lru_cache
from zoneinfo import ZoneInfo

import httpx

from saarathi.panchangam.schema import Location, Panchangam, Transition

BASE_URL = "https://telugupanchangam.app/api/panchangam"


@lru_cache(maxsize=512)
def _fetch_day(date: str, lat: float, lng: float, tz: str, lang: str) -> dict:
    """Cached single-day fetch. A given (date, lat, lng, tz, lang) is
    deterministic and never changes, so caching for the life of the
    process is safe. Callers must treat the returned dict as read-only —
    it's the same cached object handed to every caller."""
    params = {"date": date, "lat": lat, "lng": lng, "tz": tz, "lang": lang}
    response = httpx.get(BASE_URL, params=params, timeout=10.0)
    response.raise_for_status()
    return response.json()


def fetch_with_transitions(
    date: str, lat: float, lng: float, tz: str = "Asia/Kolkata", lang: str = "te"
) -> dict:
    """Fetch `date` plus the adjacent dates, and merge each anga's
    predecessor/successor onto `date`'s payload (prevNakshatra/
    nextNakshatra, etc. — tithi's nextTithi already comes from the
    provider, so it only gains a matching prevTithi). Returns a new dict;
    the cached originals from `_fetch_day` are never mutated."""
    d = date_cls.fromisoformat(date)
    yesterday_raw = _fetch_day((d - timedelta(days=1)).isoformat(), lat, lng, tz, lang)
    today_raw = _fetch_day(date, lat, lng, tz, lang)
    tomorrow_raw = _fetch_day((d + timedelta(days=1)).isoformat(), lat, lng, tz, lang)

    today_data = today_raw["data"]
    yesterday_data = yesterday_raw["data"]
    tomorrow_data = tomorrow_raw["data"]
    data = {
        **today_data,
        "tithi": {**today_data["tithi"], "prevTithi": yesterday_data.get("tithi")},
        "nakshatra": {
            **today_data["nakshatra"],
            "prevNakshatra": yesterday_data.get("nakshatra"),
            "nextNakshatra": tomorrow_data.get("nakshatra"),
        },
        "yoga": {
            **today_data["yoga"],
            "prevYoga": yesterday_data.get("yoga"),
            "nextYoga": tomorrow_data.get("yoga"),
        },
        "karana": {
            **today_data["karana"],
            "prevKarana": yesterday_data.get("karana"),
            "nextKarana": tomorrow_data.get("karana"),
        },
    }
    return {**today_raw, "data": data}


def _effective(section: dict, prev_key: str, next_key: str, ritual_dt: datetime | None) -> dict:
    """Return whichever of section/prev/next is valid at `ritual_dt`:
    prev if ritual_dt is before prev's own endsAt (ritual is early enough
    that the previous transition hasn't happened yet), next if ritual_dt
    is past this section's endsAt, else section itself."""
    if ritual_dt is None:
        return section

    prev_section = section.get(prev_key)
    prev_ends_at = prev_section.get("endsAt") if prev_section else None
    if prev_ends_at and ritual_dt < datetime.fromisoformat(prev_ends_at):
        return prev_section

    ends_at = section.get("endsAt")
    next_section = section.get(next_key)
    if ends_at and next_section and datetime.fromisoformat(ends_at) < ritual_dt:
        return next_section

    return section


def _resolve_ritual_dt(raw: dict, *, date: str, tz: str, ritual_time: str | None) -> datetime:
    """`ritual_time` ("HH:MM") applied to `date`, in the response's UTC
    offset. Defaults to the current time-of-day in `tz`, applied to
    `date` — i.e. "what would this Sankalpam be if performed at this
    moment, on this date"."""
    offset = raw["data"]["sunrise"][-6:]  # e.g. "+05:30" — matches endsAt's offset
    if ritual_time is None:
        ritual_time = datetime.now(ZoneInfo(tz)).strftime("%H:%M")
    return datetime.fromisoformat(f"{date}T{ritual_time}:00{offset}")


def normalize(
    raw: dict,
    *,
    city: str,
    lat: float,
    lng: float,
    tz: str,
    lang: str = "te",
    ritual_dt: datetime | None = None,
) -> Panchangam:
    """Map the provider's raw JSON into the canonical Panchangam schema,
    resolved for `ritual_dt` if given (see module docstring)."""
    data = raw["data"]

    def _name(section: dict) -> str:
        return section.get(lang, section.get("en", ""))

    def _transition(section: dict, next_key: str | None = None) -> Transition:
        next_name = None
        if next_key and section.get(next_key):
            next_name = _name(section[next_key])
        return Transition(
            name=_name(section),
            end_time=section.get("endsAt") or "",
            next_name=next_name,
        )

    tithi = _effective(data.get("tithi", {}), "prevTithi", "nextTithi", ritual_dt)
    nakshatra = _effective(data.get("nakshatra", {}), "prevNakshatra", "nextNakshatra", ritual_dt)
    yoga = _effective(data.get("yoga", {}), "prevYoga", "nextYoga", ritual_dt)
    karana = _effective(data.get("karana", {}), "prevKarana", "nextKarana", ritual_dt)
    masa = data.get("masa", {})

    return Panchangam(
        date=data.get("date", ""),
        location=Location(city=city, latitude=lat, longitude=lng, timezone=tz),
        ritual_time=ritual_dt.strftime("%H:%M") if ritual_dt else "",
        samvatsara=_name(data.get("samvatsaram", {})),
        masa=_name(masa),
        is_adhika_masa=bool(masa.get("isAdhika")),
        paksha=_name(data.get("paksha", {})),
        tithi=_name(tithi),
        nakshatra=_name(nakshatra),
        nakshatra_pada=nakshatra.get("pada"),
        yoga=_name(yoga),
        karana=_name(karana),
        vara=_name(data.get("vara", {})),
        ayana=_name(data.get("ayana", {})),
        ritu=_name(data.get("ritu", {})),
        sunrise=data.get("sunrise", ""),
        sunset=data.get("sunset", ""),
        transitions={
            "tithi": _transition(tithi, "nextTithi"),
            "nakshatra": _transition(nakshatra, "nextNakshatra"),
            "yoga": _transition(yoga, "nextYoga"),
            "karana": _transition(karana, "nextKarana"),
        },
    )


def get_panchangam(
    date: str,
    lat: float,
    lng: float,
    *,
    city: str,
    tz: str = "Asia/Kolkata",
    lang: str = "te",
    ritual_time: str | None = None,
) -> Panchangam:
    """Fetch and normalize Panchangam for `date`, resolved for the anga
    valid at `ritual_time` ("HH:MM", 24h; defaults to the current time in
    `tz`). See module docstring for the transition-resolution rules."""
    raw = fetch_with_transitions(date, lat, lng, tz=tz, lang=lang)
    ritual_dt = _resolve_ritual_dt(raw, date=date, tz=tz, ritual_time=ritual_time)
    return normalize(raw, city=city, lat=lat, lng=lng, tz=tz, lang=lang, ritual_dt=ritual_dt)
