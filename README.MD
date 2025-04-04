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

### Clone the repo

Start by cloning the repository to your local machine using Git:

```bash
git clone https://github.com/martinscooper/cinema.git
# or via ssh: git@github.com:martinscooper/cinema.git
cd cinema
```

### Set env variables

Each component has an `.env.example` file with default values. Run the following command to create the `.env` files with those default values.

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### Setup, intallation, and running the app

You may choose one of the following subsections in order to run the app.

#### Non-development setup (just run the app)

The following command runs a docker compose file that:

- Sets a local Elastic Search db.
- Builds and runs a FastAPI app. This app serves a React app at the root path `/`.
- Runs a job that calls the `/api/index_movies` endpoint to popupate the index.

```bash
docker compose --profile all up
```

_Note: run `docker compose --profile all down -v` to remove the containers and volumes._

#### Development setup

Set up the local Elastic Search database and run the backend and the frontend separatelly.

1. Elastic Search

    ```bash
    docker-compose --profile db up
    ```

    _Note: run `docker compose down --profile db -v` to remove the containers and volumes._

2. Backend

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

3. Frontend

    Run the React app.

    ```bash
    # from the root directory
    cd frontend
    npm install
    npm run dev
    ```

## Open the app

Visit [http://localhost:8000](http://localhost:8000)

## OpenAPI documentation

The auto-generated OpenAPI documentation can be found at [http://localhost:8000/docs](http://localhost:8000/docs)

## Tests

FastAPI tests are inside `backend/tests`. Use the following command to run them:

```bash
cd backend
source venv/bin/activate
python3 -m pytest
```

## Improvements/TODO

- Rethink `index-movies` endpoint. Should it be just a script?
- In the backend, implement a layered architecture.
- Complete parametrization of docker compose and docker.
- Take a more defensive approach for the API and tests.
- Search: explore treating search by title as a keyword.
- In the frontend, bind title and year values to the query params to allow refreshing the page without losing the results.
