# GraftNode

A backend for **plant care & genetics** — the plants module of the **Rhizome** platform
(Rhizome → **GraftNode** (plants) · Cookie Jar (notes)).

Users register, log in, and manage their own plants. Plants are organised by a shared
taxonomy of **types** and **categories**. Authentication is JWT-based, and every plant is
owned by the user who created it — you can only see and change your own.

## Setup

**Prerequisites:** Python 3.10+ and a running PostgreSQL database.

1. Enter the project and create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Copy the environment template and fill in real values:
   ```bash
   copy .env.example .env          # macOS/Linux: cp .env.example .env
   ```
   Set `DATABASE_URL` to your Postgres database and `SECRET_KEY` to a long random string.
3. Run the app — interactive docs at http://localhost:8000/docs :
   ```bash
   uvicorn main:app --reload
   ```

On startup the tables are created automatically (`Base.metadata.create_all`), so there is
no migration step to run. (See "What I'd improve" for moving to Alembic.)

## How to use it (auth flow)

1. `POST /register` — create a user (email + password).
2. `POST /token` — log in with those credentials; you get back a JWT access token.
3. Send that token as `Authorization: Bearer <token>` on every other request. In the
   `/docs` UI, click **Authorize** and paste it once.
4. Now `POST /plants`, `GET /plants`, etc. work — and only ever touch *your* plants.

## Stack (with reasoning)

- **FastAPI** — fast to build, automatic validation and interactive docs; the framework I
  know best and can defend line by line.
- **SQLAlchemy 2.0** — the standard Python ORM; keeps database logic in the app and is
  database-agnostic.
- **Pydantic v2** — validates incoming JSON against the schemas and serialises ORM objects
  back to JSON (`from_attributes`).
- **pydantic-settings** — typed, validated config loaded from `.env` (fails fast on missing
  config) instead of reading raw strings with python-dotenv.
- **PostgreSQL** — robust relational database.
- **JWT (python-jose) + passlib/bcrypt** — token auth with hashed passwords (never stored
  in plain text).

## Project structure

```
main.py            # app entry point: creates the app, includes the routers
database.py        # Settings (.env), engine, SessionLocal, Base, get_db
models/            # SQLAlchemy tables: user, plant, plant_type, plant_category
schemas/           # Pydantic request/response models
routers/           # endpoints: auth, user, plants, plant_categories, plant_types
auth/              # security.py (hashing + JWT) and dependencies.py (get_current_user)
```

## Security model (important)

- **Passwords** are hashed with bcrypt; only the hash is stored.
- **get_current_user** decodes the JWT, loads the user, and is a dependency on every
  protected route — no valid token means the request is rejected with 401 before any
  handler runs.
- **Ownership comes from the token, never the request body.** When you create a plant, the
  owner is set from the logged-in user (`current_user.user_id`), so a client can't create
  or read plants under someone else's account. Listing and reading are filtered to the
  owner; a plant that isn't yours returns 404 (we don't even reveal it exists).

## What I'd improve with more time

- **Alembic migrations** instead of `create_all`, and a **docker-compose** for Postgres
  (the way library_backend does it) for reproducible setup.
- **Tests** (pytest + FastAPI TestClient) for the auth flow and ownership rules.
- A `/return`-style richer domain and validation on the taxonomy.

## AI/LLM tools

Claude used as a coaching pair-programmer — explaining concepts, reviewing the security
model, and helping structure the code. The design decisions and code are mine and I can
defend each one.
