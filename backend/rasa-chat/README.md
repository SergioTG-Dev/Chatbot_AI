# Rasa chat (action server & training)

This folder contains the Rasa assistant: NLU, Core rules/stories and
custom actions. The project intentionally removed Twilio/WhatsApp integration
— the connector was deprecated and disabled.

Quick dev checklist

- Install Rasa (compatible with the project's `config.yml`) and dependencies.
- Configure `FASTAPI_URL` environment variable so actions can call the backend API.
- Remove or clean old models before retraining: `rm -rf models/*.tar.gz models/*`.

Training and running (local)

1. Train the model (from this directory):

```powershell
rasa train
```

2. Run the action server (custom actions):

```powershell
setx FASTAPI_URL "http://localhost:8000"
rasa run actions --port 5055
```

3. Run Rasa server (in another shell):

```powershell
rasa run -m models --enable-api --cors "*" --debug
```

Notes for Docker/Compose

- Use `ACTION_ENDPOINT_URL` env var in your compose file to point Rasa to the
	action server (example: `http://action-server:5055/webhook`).
- Ensure FastAPI is reachable from the action server (set `FASTAPI_URL` to
	the internal Docker service address, e.g. `http://backend-api:8000`).
- Prometheus metrics are emitted by the FastAPI app on `/metrics` (see
	`backend/api/src/api/main.py`). Do not remove the Instrumentator call.

FAQ & seeds

- FAQs are sourced from `backend/rasa-chat/src/rasa-chat/actions/gcba_faqs_db.py`.
- To seed FAQs into Supabase, use `backend/api/src/api/seed_faqs.py` which
	imports the `gcba_faqs_db.py` module.

If you want, I can add example `docker-compose` snippets and a CI job to
retrain models automatically on changes to `data/` files.

Additional utilities

- Example Docker Compose (for local integration): `docker-compose.example.yml` (in this folder).
- Generate NLU FAQ examples from the internal knowledge base:

```powershell
cd src\rasa-chat
python scripts\generate_faq_nlu.py --out ../data/faq_nlu_examples.yml
```

The previous command will produce a small YAML file with `faq_gcba` examples
which you can merge into `data/nlu.yml` before training to improve FAQ
classification. Review examples (they come from `gcba_faqs_db.py`) and
filter/augment as needed.

