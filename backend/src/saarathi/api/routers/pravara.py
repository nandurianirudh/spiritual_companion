from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from saarathi.api.deps import Lang
from saarathi.rituals.pravara.data import GOTRA_NAMES
from saarathi.rituals.pravara.rules import DEFAULT_NAME, DEFAULT_SHAKHA, DEFAULT_SUTRA, build_pravara

router = APIRouter()


class PravaraResponse(BaseModel):
    pravara: str = Field(description="Filled Pravara/Abhivadana text.")


@router.get(
    "/pravara",
    response_model=PravaraResponse,
    summary="Generate a Pravara/Abhivadana for a gotra",
    description=(
        "Looks up the pravara rishis for the given gotra and fills the fixed "
        "Pravara/Abhivadana template with them plus sutra/shakha/name. "
        f"Known gotras (Telugu or English spelling accepted): {sorted(GOTRA_NAMES)}."
    ),
)
def pravara(
    lang: Lang,
    gotra: str = Query(
        ...,
        description=f"Gotra name, Telugu or English spelling. One of: {sorted(GOTRA_NAMES)}.",
        examples=["కౌశిక"],
    ),
    sutra: str | None = Query(
        None,
        description="Sutra (e.g. Apastamba). Defaults to the source example's, in `lang`.",
        examples=[DEFAULT_SUTRA["te"]],
    ),
    shakha: str | None = Query(
        None,
        description="Vedic shakha (e.g. Krishna Yajus). Defaults to the source example's, in `lang`.",
        examples=[DEFAULT_SHAKHA["te"]],
    ),
    name: str | None = Query(
        None,
        description="Person's name, as it appears before 'శర్మాహం'/'śarmāhaṁ'. "
        "Defaults to the source example's, in `lang`.",
        examples=[DEFAULT_NAME["te"]],
    ),
) -> dict:
    try:
        return {"pravara": build_pravara(gotra, sutra=sutra, shakha=shakha, name=name, lang=lang)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
