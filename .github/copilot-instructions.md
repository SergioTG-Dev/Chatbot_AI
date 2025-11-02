## Repo snapshot for AI coding agents

This project contains a Next.js frontend (in `front/`), a FastAPI backend/service (in `backend/api/src/api/`) and a Rasa action/chat component (in `backend/rasa-chat/`). The app uses Supabase as the primary data backend and Prometheus instrumentation is enabled for the API.

Keep changes small and local-first. When in doubt, run and validate locally before editing cross-cutting files (database schema, infra, or CI).

Key entry points and examples
- Backend FastAPI app: `backend/api/src/api/main.py` (includes CORS, Prometheus `/metrics`, and a debug `/debug/routes`).
- Backend dependencies: `backend/api/pyproject.toml` (Poetry-managed; dev deps include `pytest`, `httpx`).
- Seeds & DB helpers: `backend/api/src/api/seed_data.py`, `seed_faqs.py` (use Supabase client at `backend/api/src/api/db/supabase_client.py`).
- FAQs knowledge DB (source of truth for FAQ seeds and SQL): `backend/rasa-chat/src/rasa-chat/actions/gcba_faqs_db.py` (contains CREATE_TABLE_SQL and `faqs_database`). If table missing, run that SQL in Supabase or use `backend/api/codigo.sql`.
- Frontend: `front/` (Next.js). Key scripts in `front/package.json` — use `npm run dev` / `npm run build` / `npm run start` from `front/`.

Common developer workflows (concrete)
- Run frontend (from repo root):
  - cd into `front/` then `npm run dev` (PowerShell: `cd front; npm run dev`).
- Run backend API locally:
  - From `backend/api/src/api/` run: `uvicorn main:app --reload` (this starts the FastAPI app on default port). Alternatively, use your Python/Poetry workflow if available.
- Run backend tests: from `backend/api/` run `pytest` (or `poetry run pytest` if using Poetry).
- Seed FAQs into Supabase:
  - `python backend/api/src/api/seed_faqs.py` (requires SUPABASE credentials and that `faqs_gcba` exists — see `gcba_faqs_db.py` for CREATE_TABLE_SQL).
- Populate sample data:
  - `python backend/api/src/api/seed_data.py` (requires Supabase SERVICE_ROLE_KEY with sufficient privileges; this script clears/inserts several tables).

Project-specific patterns and conventions
- Supabase is used directly via a Supabase client wrapper under `backend/api/src/api/db/`. Seeds use `upsert` semantics for idempotency.
- Seed files compute repo-relative paths (see `seed_faqs.py`) — maintain directory structure when moving files.
- The FastAPI app prints routes on startup and exposes a `/debug/routes` endpoint — use this for discovering endpoints during development.
- FAQ knowledge is kept inside the Rasa actions module (large python list + CREATE_TABLE_SQL). Changes to FAQs should be done by editing that file and re-seeding via `seed_faqs.py`.

Integration points to watch
- Supabase: env vars required (backend and frontend). Frontend expects `NEXT_PUBLIC_SUPABASE_URL` & `NEXT_PUBLIC_SUPABASE_ANON_KEY` in `.env.local`. Backend seeding/clear needs SERVICE_ROLE key.
- Rasa: action code lives under `backend/rasa-chat/src/rasa-chat/actions/` — actions are invoked by Rasa and must be reachable by the Rasa action server. If you change function/class names here, update Rasa config accordingly.
- Prometheus: the API is instrumented (endpoint `/metrics`) — do not remove the Instrumentator call in `main.py` unless you also update monitoring configs.

Quick troubleshooting notes (discovered patterns)
- If `seed_faqs.py` fails with table-not-found: either run the SQL in `backend/api/codigo.sql` or execute the `CREATE_TABLE_SQL` constant in `gcba_faqs_db.py` against your Supabase DB.
- Seeds that clear tables use a SERVICE_ROLE key; a typical failure is permission-denied — check that the key is the service role, not an anon key.
- When debugging routes, use the built-in `/debug/routes` endpoint or read the console output on FastAPI startup (the app prints registered routes).

What an AI agent should do by default
- Prefer modifying feature files under `front/` or `backend/api/src/api/` and run the local dev server to validate behavior.
- When changing DB schema, update `gcba_faqs_db.py` (if FAQ-related) and include migration instructions: update SQL in `backend/api/codigo.sql` and mention the need to re-run seeds.
- Create small, focused tests under `backend/api/tests/` (pytest) when changing backend logic.

If anything here is unclear or you'd like more detail (CI steps, Docker compose usage, or Rasa run instructions), tell me which area to expand and I'll update this file.
