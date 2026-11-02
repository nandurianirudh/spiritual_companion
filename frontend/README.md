# Frontend (planned, not started)

Web app, responsive for phone and laptop. Consumes the backend's `/v1/*`
API only — no Panchangam or ritual logic here.

## Plan

- **Stack:** React + Vite + TypeScript SPA.
- **API access:** one client module for all `/v1` calls; dev server proxies
  `/v1` to `localhost:8000`. Prod: `VITE_API_URL` + add the origin to the
  backend's `SAARATHI_CORS_ORIGINS`.
- **Types:** generate from the backend's OpenAPI schema (`/openapi.json`)
  so UI and API can't drift.
- **Layout:** mobile-first CSS, tap-sized controls, a font that renders
  Telugu script well.
- **Screens, in order:**
  1. Sankalpam — date, place, time, language toggle (MVP).
  2. Pravara — gotra picker, sutra/shakha/name.
  3. Achamanam / Pranayamam — fixed text, step-by-step view.
- **Language:** te/en toggle on every screen, matching the API's `lang`.

## Start

From this folder:

```
npm create vite@latest . -- --template react-ts
```

then follow the plan above.
