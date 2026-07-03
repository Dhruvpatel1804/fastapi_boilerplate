# Alembic Migrations

This project uses **manual migrations only**. Do not use `--autogenerate`.

## Commands

```bash
# Create an empty migration (edit the file by hand)
pipenv run alembic revision -m "create_items_table"

# Apply all pending migrations
pipenv run alembic upgrade head

# View history
pipenv run alembic history

# Current version
pipenv run alembic current

# Roll back one step
pipenv run alembic downgrade -1
```

## Workflow

1. Define or update SQLAlchemy models in `app/db/models/`
2. Import models in `app/db/base.py` so metadata is registered
3. Create a revision: `pipenv run alembic revision -m "description"`
4. Write `upgrade()` and `downgrade()` by hand in `alembic/versions/`
5. Apply: `pipenv run alembic upgrade head`

Alembic uses a synchronous `psycopg2` connection. The sync URL is derived from `DATABASE_URL` in `alembic/env.py`.
