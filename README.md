# FastAPI Boilerplate

Production-ready FastAPI skeleton for coding interviews and small projects.

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL 16
- SQLAlchemy 2.x (async)
- Alembic (manual migrations)
- Pipenv
- Ruff (lint + format)
- pytest + GitHub Actions CI

## Project Structure

```
app/
├── api/v1/endpoints/   # Route handlers
├── core/               # Config, logging, exceptions
└── db/                 # SQLAlchemy base + session
alembic/                # Database migrations
tests/                  # pytest suite
```

## Quick Start

### Prerequisites

- Python 3.12
- [Pipenv](https://pipenv.pypa.io/)
- PostgreSQL (local install or remote server — **not** bundled in Docker)
- Docker (optional, for running the API container only)

### Local Development

1. **Clone and configure**

   ```bash
   cp .env.example .env
   pipenv install --dev
   ```

2. **Configure PostgreSQL**

   Install and start PostgreSQL on your machine, or use a remote server. Create a database and set `DATABASE_URL` in `.env`:

   ```
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/app_db
   ```

3. **Run migrations** (none until you add models)

   ```bash
   pipenv run alembic upgrade head
   ```

4. **Start the API**

   ```bash
   pipenv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Verify**

   - Liveness: http://localhost:8000/health
   - Readiness (DB check): http://localhost:8000/api/v1/health
   - Docs: http://localhost:8000/docs

### Run API in Docker

PostgreSQL stays **outside** Docker. Set `DATABASE_URL` in `.env`.

The Docker image name and version live in **`docker-compose.yml`** only:

```yaml
image: your-dockerhub-username/fastapi-boilerplate:1.0.0
build: .
```

CI runs `docker compose build` and `docker compose push` — no extra tagging in the workflow.

**On a server:**

```bash
cp .env.example .env   # set DATABASE_URL
docker compose pull
docker compose up -d
```

**Build and push locally** (same as CI):

```bash
docker login
docker compose build
docker compose push
```

### VS Code Debugging

Use the **API (uvicorn)** launch configuration in `.vscode/launch.json`. It runs on `0.0.0.0:8000` with hot reload.

## Development Workflow

| Task | Command |
|------|---------|
| Lint | `pipenv run ruff check .` |
| Format | `pipenv run ruff format .` |
| Test | `pipenv run pytest -v` |
| New migration | `pipenv run alembic revision -m "description"` |
| Apply migrations | `pipenv run alembic upgrade head` |

CI runs lint, format, and tests on every push/PR. On push to `main`/`master`, it logs into Docker Hub and runs `docker compose build` + `docker compose push`.

### Docker Hub secrets

| Secret | Description |
|--------|-------------|
| `DOCKERHUB_USERNAME` | Must match the username in `image:` inside `docker-compose.yml` |
| `DOCKERHUB_TOKEN` | Docker Hub access token |

Bump the version by editing the `image:` tag in `docker-compose.yml` (e.g. `1.0.0` → `1.0.1`).

## Adding Your First Model

1. Create `app/db/models/item.py`:

   ```python
   from sqlalchemy.orm import Mapped, mapped_column
   from sqlalchemy import String
   from app.db.base import Base

   class Item(Base):
       __tablename__ = "items"
       id: Mapped[int] = mapped_column(primary_key=True)
       name: Mapped[str] = mapped_column(String(255))
   ```

2. Import the model in `app/db/base.py` so Alembic sees it.

3. Create a manual migration:

   ```bash
   pipenv run alembic revision -m "create_items_table"
   ```

4. Edit `alembic/versions/<rev>_create_items_table.py` by hand (no autogenerate).

5. Apply: `pipenv run alembic upgrade head`

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness probe (no DB check) |
| GET | `/api/v1/health` | Readiness probe (checks DB) |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Runtime environment | `development` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `DATABASE_URL` | Async PostgreSQL URL (`postgresql+asyncpg://...`) | **required** |
| `CORS_ORIGINS` | JSON list of allowed origins | `["http://localhost:3000"]` |

## License

MIT
