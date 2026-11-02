from fastapi.testclient import TestClient

from saarathi.api import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_fixed_text_routes_are_versioned_and_bilingual():
    for name in ("achamanam", "pranayamam"):
        for lang in ("te", "en"):
            r = client.get(f"/v1/{name}", params={"lang": lang})
            assert r.status_code == 200 and r.json()[name]
        assert client.get(f"/{name}").status_code == 404


def test_bad_lang_is_400():
    for path in ("/v1/achamanam", "/v1/pranayamam", "/v1/pravara?gotra=x", "/v1/sankalpam"):
        sep = "&" if "?" in path else "?"
        assert client.get(f"{path}{sep}lang=fr").status_code == 400


def test_pravara_unknown_gotra_is_400():
    assert client.get("/v1/pravara", params={"gotra": "nope"}).status_code == 400


def test_cors_allows_dev_origin():
    r = client.get("/health", headers={"Origin": "http://localhost:5173"})
    assert r.headers["access-control-allow-origin"] == "http://localhost:5173"
