from __future__ import annotations

import sys

import typer

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from saarathi.core.lang import validate_lang
from saarathi.panchangam.client import get_panchangam
from saarathi.rituals.sankalpam.rules import build_sankalpam

app = typer.Typer()


@app.command()
def sankalpam(
    date: str = typer.Option(..., help="YYYY-MM-DD"),
    lat: float = typer.Option(..., help="Latitude"),
    lng: float = typer.Option(..., help="Longitude"),
    city: str = typer.Option("", help="City name, for display only"),
    tz: str = typer.Option("Asia/Kolkata"),
    time: str = typer.Option(
        None, help="Ritual time HH:MM (24h). Defaults to the current time in --tz."
    ),
    lang: str = typer.Option(
        "te", help="Output script: 'te' (Telugu) or 'en' (IAST-romanized)."
    ),
):
    try:
        validate_lang(lang)
    except ValueError as e:
        raise typer.BadParameter(str(e)) from e
    panchangam = get_panchangam(date, lat, lng, city=city, tz=tz, lang=lang, ritual_time=time)
    typer.echo(build_sankalpam(panchangam, lang=lang))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
