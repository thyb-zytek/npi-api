# Reverse Polish Notation API.

[![Tests](https://github.com/thyb-zytek/npi-api/workflows/Run%20Tests/badge.svg)](https://github.com/thyb-zytek/npi-api/actions/workflows/tests.yml)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/thyb-zytek/npi-api.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirct/thyb-zytek/npi-api)

Provide an API-based RPN calculator with a database model of calcul histories and
the possibility to export histories into CSV.


## Technology Stack and Features

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
    - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database.
- 🐋 [Docker Compose](https://www.docker.com) for development and production.
- ✅ Tests with [Pytest](https://pytest.org).
- 🚢 Deployment instructions using Docker Compose
- 🏭 CI/CD based on GitHub Actions.

## How To Use It

To use this project, you need to clone it and launch it.

Follow the next steps:

- Clone this repository:

```bash
git clone git@github.com:thyb-zytek/npi-api.git
```

- Enter into the new directory:

```bash
cd npi-api
```

- Launch your stack:

```bash
docker compose up -d
```

- Verify API server is up, if it displays `OK`, it means that the server is up:
```bash
curl -X 'GET' 'http://localhost:8000/healthcheck' -H 'accept: application/json'
```

Now you can use the RPN APIs.

### URLs

🌐 Automatic Interactive Docs (Swagger UI): http://localhost:8000/docs

🌐 Automatic Alternative Docs (ReDoc): http://localhost:8000/redoc

🌐 APIs: http://localhost:8000/api/v1/rpn

## RPN available operators and variables

📖 RPN documentation: [rpn.md](./rpn.md)

## License

The RPN API project is licensed under the terms of the MIT license.
