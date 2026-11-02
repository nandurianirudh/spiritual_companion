"""Canonical Panchangam schema. Internal contract — LangGraph/rules nodes
depend on this, never on a provider's raw JSON shape."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Location(BaseModel):
    city: str = Field(description="Display label only, e.g. 'Hyderabad'.")
    latitude: float
    longitude: float
    timezone: str = Field(description="IANA timezone, e.g. 'Asia/Kolkata'.")


class Transition(BaseModel):
    name: str = Field(description="The anga's name as used in the Sankalpam (resolved for ritual_time).")
    end_time: str = Field(
        default="",
        description="ISO datetime this anga's value ends, per the provider. Empty if unknown "
        "(e.g. after resolving to a previous-day value, whose own endsAt isn't tracked here).",
    )
    next_name: str | None = Field(
        default=None, description="The anga's next value after end_time, if known."
    )


class Panchangam(BaseModel):
    date: str = Field(description="Requested ritual date, ISO format.")
    location: Location
    ritual_time: str = Field(
        default="", description="'HH:MM' the tithi/nakshatra/yoga/karana below were resolved for."
    )

    samvatsara: str = Field(description="Telugu year name, e.g. 'పరాభవ' (Parabhava).")
    masa: str = Field(description="Telugu lunar month.")
    is_adhika_masa: bool = Field(description="Whether this masa is an intercalary (adhika) month.")
    paksha: str = Field(description="Lunar fortnight: Shukla or Krishna paksha.")
    tithi: str = Field(description="Current tithi, resolved for ritual_time.")
    nakshatra: str = Field(description="Current nakshatra, resolved for ritual_time.")
    nakshatra_pada: int | None = Field(default=None, description="Nakshatra pada (quarter), 1-4.")
    yoga: str = Field(description="Current yoga, resolved for ritual_time.")
    karana: str = Field(description="Current karana, resolved for ritual_time.")
    vara: str = Field(description="Weekday.")
    ayana: str = Field(description="Uttarayana or Dakshinayana.")
    ritu: str = Field(description="Season.")

    sunrise: str = Field(description="ISO datetime of sunrise at the given location/date.")
    sunset: str = Field(description="ISO datetime of sunset at the given location/date.")

    transitions: dict[str, Transition] = Field(
        default={},
        description="Per-anga transition detail (tithi/nakshatra/yoga/karana), keyed by anga name.",
    )
