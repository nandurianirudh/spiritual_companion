from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from saarathi.api.deps import Lang
from saarathi.rituals.pranayamam.rules import build_pranayamam

router = APIRouter()


class PranayamamResponse(BaseModel):
    pranayamam: str = Field(description="Fixed Pranayamam text, in the language requested via `lang`.")


@router.get(
    "/pranayamam",
    response_model=PranayamamResponse,
    summary="Get the fixed Pranayamam text",
    description=(
        "Returns the fixed Pranayamam wording (source: "
        "book_Books_sandhyavandhanam.pdf pp.6-7) — no dynamic slots, "
        "nothing varies by request other than `lang`. `en` has mantra lines "
        "IAST-romanized and instruction lines translated to English."
    ),
)
def pranayamam(lang: Lang) -> dict:
    return {"pranayamam": build_pranayamam(lang=lang)}
