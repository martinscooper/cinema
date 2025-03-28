from unittest.mock import MagicMock, patch

import pytest
from cinema.app import app, fetch_page
from cinema.consts import BASE_MOVIES_URL, INDEX_NAME
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(app)


def test_fetch_page():
    # Sample movie data to be returned by the mock
    sample_movie_data = {
        "data": [{"imdbID": "tt1234567", "Title": "Sample Movie", "Year": "2025"}]
    }

    with patch("cinema.app.requests.get") as mock_get:
        # Configure the mock to return a response with the sample data
        mock_response = MagicMock()
        mock_response.json.return_value = sample_movie_data
        mock_get.return_value = mock_response

        page = 1
        movies = fetch_page(page, BASE_MOVIES_URL)

        assert len(movies) == 1
        assert movies[0]["imdbID"] == "tt1234567"
        assert movies[0]["Title"] == "Sample Movie"
        assert movies[0]["Year"] == "2025"
        mock_get.assert_called_once_with(f"{BASE_MOVIES_URL}?page={page}")


def test_index_movies(client):
    # Sample response data for the initial request to BASE_MOVIES_URL
    sample_initial_data = {"total_pages": 2}

    # Sample movie data for each page
    sample_movie_data_page_1 = {
        "data": [{"imdbID": "tt1234567", "Title": "Sample Movie 1", "Year": "2025"}]
    }
    sample_movie_data_page_2 = {
        "data": [{"imdbID": "tt7654321", "Title": "Sample Movie 2", "Year": "2024"}]
    }

    with (
        patch("cinema.app.requests.get") as mock_get,
        patch("cinema.app.helpers.bulk") as mock_bulk,
        patch("cinema.app.es_client") as mock_es,
    ):
        mock_es.indices.exists.return_value = True
        mock_es.indices.delete.return_value = None
        mock_es.info.return_value = "Ok"

        # Mock the initial request to BASE_MOVIES_URL
        mock_response_initial = MagicMock()
        mock_response_initial.json.return_value = sample_initial_data
        mock_get.side_effect = [
            mock_response_initial,
            MagicMock(json=MagicMock(return_value=sample_movie_data_page_1)),
            MagicMock(json=MagicMock(return_value=sample_movie_data_page_2)),
        ]

        # Mock the bulk indexing operation
        mock_bulk.return_value = (2, [])

        # Call the endpoint
        response = client.post("/api/index_movies")

        # Assertions
        assert response.status_code == 200
        assert response.json() == {"indexed_movies_count": 2}

        # Verify that the Elasticsearch index was checked and deleted
        mock_es.indices.exists.assert_called_once_with(index=INDEX_NAME)
        mock_es.indices.delete.assert_called_once_with(
            index=INDEX_NAME, ignore_unavailable=True
        )

        # Verify that the bulk indexing was called with the correct number of actions
        actions = [
            {"_index": INDEX_NAME, "_source": movie}
            for movie in [
                {"imdb_id": "tt1234567", "title": "Sample Movie 1", "year": "2025"},
                {"imdb_id": "tt7654321", "title": "Sample Movie 2", "year": "2024"},
            ]
        ]
        mock_bulk.assert_called_once_with(mock_es, actions)


def test_search_movies(client):
    # Sample data returned by the mocked Elasticsearch search method
    sample_search_response = {
        "hits": {
            "total": {"value": 1},
            "hits": [
                {
                    "_source": {
                        "imdb_id": "tt1234567",
                        "title": "Sample Movie",
                        "year": 2025,
                    }
                }
            ],
        }
    }

    with patch("cinema.app.es_client") as mock_es:
        # Mock the indices.exists method to return True, indicating the index exists
        mock_es.indices.exists.return_value = True

        # Mock the search method to return the sample search response
        mock_es.search.return_value = sample_search_response

        # Perform a GET request to the /api/movies endpoint with query parameters
        response = client.get("/api/movies", params={"title": "Sample", "year": 2025})

        # Assertions
        assert response.status_code == 200
        assert response.json() == {
            "movies": [{"imdb_id": "tt1234567", "title": "Sample Movie", "year": 2025}],
            "total": 1,
        }

        # Verify that the Elasticsearch index existence was checked
        mock_es.indices.exists.assert_called_once_with(index=INDEX_NAME)

        # Verify that the search method was called with the correct query
        expected_query = {
            "from": 0,
            "size": 10,
            "query": {
                "bool": {
                    "must": [
                        {"match_phrase": {"title": {"query": "Sample"}}},
                        {"term": {"year": 2025}},
                    ]
                }
            },
        }
        mock_es.search.assert_called_once_with(index=INDEX_NAME, body=expected_query)
