# Cinema

[![tests](https://github.com/martinscooper/cinema/actions/workflows/test.yml/badge.svg)](https://github.com/martinscooper/cinema/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/martinscooper/cinema/graph/badge.svg?token=M1W7GTD4F6)](https://codecov.io/gh/martinscooper/cinema)

## Requirements

### Non-dev environment

- Docker compose

### Dev environment

- Docker compose (if using local Elastic Search cluster)
- Python >= 3.9
- Node > 20

## Set up the app

### Set env variables

Each component has an `.env.example` file with default values. Run the following command to create the `.env` files with those default values.

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### Non-development setup

The following command runs a docker compose file that:

- Sets a local Elastic Search db.
- Builds and runs a FastAPI app. This app serves a React app at the root path `/`.
- Runs a job that calls the `/api/index_movies` endpoint to popupate the index.

```bash
docker compose --profile all up
```

_Note: run `docker compose --profile all down -v` to remove the containers and volumes._

## Development setup

Set up the local Elastic Search database and run the backend and the frontend separatelly.

### Elastic Search

```bash
docker-compose --profile db up
```

_Note: run `docker compose down --profile db -v` to remove the containers and volumes._

### Backend

Run the FastAPI app.

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install pre-commit
pre-commit install
python3 run.py
```

_Note: you will have to manually run a request against `/api/index_movies` endpoint to popupate the Elastic Search index._

### Frontend

Run the React app.

```bash
# from the root directory
cd frontend
npm install
npm run dev
```

## Run the app

Visit [http://localhost:8000](http://localhost:8000)

## OpenAPI documentation

The auto-generated OpenAPI documentation can be found at [http://localhost:8000/docs](http://localhost:8000/docs)

## Tests

FastAPI tests are inside `backend/tests`. Use the following command to run them:

```bash
python3 -m pytest
```
