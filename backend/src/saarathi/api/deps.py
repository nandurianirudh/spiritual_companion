"""Shared request parameters for the ritual routers."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, Query

from saarathi.core.lang import validate_lang


def _lang(
    lang: str = Query(
        "te",
        description="Output script: `te` (Telugu) or `en` (IAST-romanized). Same wording "
        "either way — not a translation, just a different script.",
        examples=["te"],
    ),
) -> str:
    try:
        return validate_lang(lang)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


Lang = Annotated[str, Depends(_lang)]
