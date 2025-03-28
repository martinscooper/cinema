from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from time import time
from typing import Optional

import requests
from elasticsearch import helpers
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .app_logger import logger
from .consts import BASE_MOVIES_URL, INDEX_NAME
from .elastic_search import es_client
from .types import HealthCheck, IndexMoviesResponse, Movie, MoviesResponse
from .utils import verify_es_connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)


@app.get(
    "/health",
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    return HealthCheck(status="OK")


def fetch_page(page, base_url):
    """
    Fetch a specific page of movie data from the remote service.

    Args:
        page (int): The page number to fetch.
        base_url (str): The base URL of the remote service.

    Returns:
        List[dict]: A list of movies on the specified page.
    """
    response = requests.get(f"{base_url}?page={page}")
    data = response.json()
    return data.get("data", [])


@app.post(
    "/api/index_movies",
    summary=("Fetch movie data from a remote service and index it into Elasticsearch."),
    response_description=(
        "An object whose indexed_movies_count indicates the number of movies indexed."
    ),
    status_code=status.HTTP_200_OK,
    response_model=IndexMoviesResponse,
)
async def index_movies():
    verify_es_connection(es_client)

    init = time()
    response = requests.get(BASE_MOVIES_URL)
    total_pages = response.json().get("total_pages", 0)

    movies = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(fetch_page, page, BASE_MOVIES_URL)
            for page in range(1, total_pages + 1)
        ]

        for future in as_completed(futures):
            movies_on_page = future.result()
            movies_on_page = [
                {
                    "imdb_id": movie["imdbID"],
                    "title": movie["Title"],
                    "year": movie["Year"],
                }
                for movie in movies_on_page
            ]

            if movies_on_page:
                movies.extend(movies_on_page)

    if es_client.indices.exists(index=INDEX_NAME):
        es_client.indices.delete(index=INDEX_NAME, ignore_unavailable=True)
        logger.info(f"Index '{INDEX_NAME}' already exists, deleting it.")

    actions = [{"_index": INDEX_NAME, "_source": movie} for movie in movies]

    # Bulk index the movies into Elasticsearch
    helpers.bulk(es_client, actions)
    logger.info(f"Indexed {len(movies)} movies in {time() - init} seconds.")
    return {"indexed_movies_count": len(movies)}


@app.get(
    "/api/movies",
    summary=(
        "Search for movies in the Elasticsearch index based on title and/or year."
    ),
    response_description=(
        "A response object containing the list of movies "
        "matching the search criteria and the total number of matches."
    ),
    status_code=status.HTTP_200_OK,
    response_model=MoviesResponse,
)
async def search_movies(
    title: Optional[str] = None,
    year: Optional[int] = None,
    from_item: Optional[int] = 0,
    size: Optional[int] = 10,
) -> MoviesResponse:
    verify_es_connection(es_client)

    if not es_client.indices.exists(index=INDEX_NAME):
        return HTTPException("The movies weren't loaded yet")

    and_conditions = []

    if title:
        and_conditions.append(
            {
                "match_phrase": {
                    "title": {
                        "query": title,
                    }
                }
            },
        )

    if year:
        and_conditions.append({"term": {"year": year}})

    query = {
        "from": from_item,
        "size": size,
        "query": {"bool": {"must": and_conditions}},
    }

    response = es_client.search(index=INDEX_NAME, body=query)
    hits = response["hits"]["hits"]
    total = response["hits"]["total"]["value"]
    return MoviesResponse(movies=[Movie(**hit["_source"]) for hit in hits], total=total)


# Define the path to the static directory
static_directory = Path(__file__).parent.parent / "static"
if Path.exists(static_directory):
    logger.info("Serving static files.")
    app.mount("/", StaticFiles(directory=static_directory, html=True), name="static")
else:
    logger.info("Static files were not found.")
