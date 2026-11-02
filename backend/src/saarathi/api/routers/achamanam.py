from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from saarathi.api.deps import Lang
from saarathi.rituals.achamanam.rules import build_achamanam

router = APIRouter()


class AchamanamResponse(BaseModel):
    achamanam: str = Field(description="Fixed Achamanam text, in the language requested via `lang`.")


@router.get(
    "/achamanam",
    response_model=AchamanamResponse,
    summary="Get the fixed Achamanam text",
    description=(
        "Returns the fixed Achamanam wording (source: "
        "book_Books_sandhyavandhanam.pdf pp.4-6) — no dynamic slots, "
        "nothing varies by request other than `lang`. `en` has mantra lines "
        "IAST-romanized and instruction lines translated to English."
    ),
)
def achamanam(lang: Lang) -> dict:
    return {"achamanam": build_achamanam(lang=lang)}
