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
- Docker & Docker Compose (optional)

### Local Development

1. **Clone and configure**

   ```bash
   cp .env.example .env
   pipenv install --dev
   ```

2. **Start PostgreSQL**

   ```bash
   docker compose up -d db
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

### Full Stack with Docker

Update `.env` so `DATABASE_URL` uses the `db` service hostname:

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/app_db
```

Then:

```bash
docker compose up --build
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

CI runs the same lint, format, and test steps on every push/PR to `main`.

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
