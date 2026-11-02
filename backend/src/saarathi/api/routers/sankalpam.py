from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from saarathi.api.deps import Lang
from saarathi.panchangam.client import get_panchangam
from saarathi.panchangam.schema import Panchangam
from saarathi.rituals.sankalpam.rules import build_sankalpam

router = APIRouter()


class SankalpamResponse(BaseModel):
    sankalpam: str = Field(description="Filled Sankalpam text, in the language requested via `lang`.")
    panchangam: Panchangam = Field(
        description="Canonical Panchangam values the Sankalpam was resolved against, "
        "including each anga's transition time and next value."
    )


@router.get(
    "/sankalpam",
    response_model=SankalpamResponse,
    summary="Generate a Sankalpam for a date, location, and ritual time",
    description=(
        "Resolves the Panchangam (samvatsara/masa/tithi/nakshatra/yoga/karana/...) for the "
        "given date and location, at the given ritual time, and fills the fixed Sankalpam "
        "template with those values. Tithi/nakshatra/yoga/karana are each independently "
        "checked against the ritual time — see the field docs on `time` for details."
    ),
)
def sankalpam(
    lang: Lang,
    date: str | None = Query(
        None,
        description="Ritual date, ISO format (YYYY-MM-DD). Defaults to today's date in `tz` if omitted.",
        examples=["2026-08-29"],
    ),
    lat: float = Query(
        17.385,
        description="Latitude of the ritual location, decimal degrees. Defaults to Hyderabad.",
        examples=[17.385],
    ),
    lng: float = Query(
        78.486,
        description="Longitude of the ritual location, decimal degrees. Defaults to Hyderabad.",
        examples=[78.486],
    ),
    city: str = Query(
        "Hyderabad",
        description="Display label only — not sent to the Panchangam provider, "
        "has no effect on the computed values.",
        examples=["Hyderabad"],
    ),
    tz: str = Query(
        "Asia/Kolkata",
        description="IANA timezone of the ritual location. Also used to compute the "
        "default `time` (current clock time) when `time` is omitted.",
        examples=["Asia/Kolkata"],
    ),
    time: str | None = Query(
        None,
        description="Ritual time, 24h `HH:MM`. Determines which side of each anga's "
        "transition (tithi/nakshatra/yoga/karana) is used — e.g. a nakshatra that changes "
        "mid-morning shows differently before vs. after that instant. "
        "Defaults to the current time in `tz` if omitted.",
        examples=["06:00"],
    ),
) -> dict:
    if date is None:
        date = datetime.now(ZoneInfo(tz)).date().isoformat()
    try:
        panchangam = get_panchangam(date, lat, lng, city=city, tz=tz, lang=lang, ritual_time=time)
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid date/time: {e}. `date` must be ISO YYYY-MM-DD, `time` must be HH:MM."
        ) from e
    return {
        "sankalpam": build_sankalpam(panchangam, lang=lang),
        "panchangam": panchangam,
    }
