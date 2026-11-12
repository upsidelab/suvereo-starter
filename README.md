# suvereo-starter

Starter pack for building on Suvereo. It runs the Suvereo server and frontend with Docker Compose and gives you a place for your own code: domains, agents, integrations and anything else you want to wire into Suvereo.

## What is included

The starter ships with the **diet advice domain** (`server/src/diet_advice_domain/`) as a working example: models and migrations, recipe and user sources, a nutrition agent and a weekly meal plan agentic execution.

### Your code lives in `server/src/`

`server/src/` is part of this codebase, so it is yours to change. Define your own domain definitions (entities and migrations), agents, agentic executions and integrations there, then wire them into Suvereo in `server/config/settings_override.py` (`INSTALLED_DOMAIN_DEFINITIONS`, `AVAILABLE_AGENTS`, `AVAILABLE_AGENTIC_EXECUTION_DEFINITIONS`, `CATALOG_INTEGRATION_PLUGINS` and so on).

### Packages from PyPI

`server/src/pyproject.toml` describes your code as a Python package. Add packages from PyPI to its dependencies, such as domain definitions, agents and integrations published by others, and they are installed into the image together with your code. Then register them in `settings_override.py` the same way as your own.

### How the image is built

`server/Dockerfile` starts from the Suvereo server image, builds `server/src/` into a wheel and installs it (with its dependencies), then replaces `pecl/settings_override.py` with `server/config/settings_override.py`.

## Getting started

```shell
cp server/config/sample.env server/config/.env
cp frontend/config/sample.env frontend/config/.env
docker compose build && docker compose up
```

The frontend is at http://localhost:10001 and the API at http://localhost:10000. Set your API keys (for example `OPENAI_API_KEY`) in `server/config/.env`.

### Logging in

Open the frontend and log in as the initial admin user. Its credentials are set in `server/config/.env`:

```
ECL_ADMIN_EMAIL=admin@example.com
ECL_ADMIN_PASSWORD=changeme
```

The user is only created when the database has no users, which is the first start. Set the values you want in `server/config/.env` before then. Changing them later has no effect on an existing database; change the password in the app, or reset with `docker compose down -v`. Never keep the defaults outside a local setup.

Env files are read when a container is created, not when an image is built. After editing one, run `docker compose up -d --force-recreate`.

## Local testing against unreleased Suvereo images

From the Suvereo repo root:

```shell
docker build -f server/Dockerfile.development -t suvereo-server:dev .
docker build -t suvereo-frontend:dev frontend/
```

Then, here:

```shell
cp server/config/sample.env server/config/.env
cp frontend/config/sample.env frontend/config/.env
export SUVEREO_VERSION=dev
docker compose build && docker compose up
```

## Layout

```
server/    Dockerfile, config/ (sample.env, settings_override.py), src/ (your code and pyproject.toml)
frontend/  config/sample.env (copy to config/.env)
```
