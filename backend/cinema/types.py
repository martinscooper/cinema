from typing import List

from pydantic import BaseModel


class Movie(BaseModel):
    """
    Pydantic model representing a movie.

    Attributes:
        title (str): The title of the movie.
        year (int): The release year of the movie.
        imdb_id (str): The IMDb ID of the movie.
    """

    title: str
    year: int
    imdb_id: str


class MoviesResponse(BaseModel):
    """
    Pydantic model representing the response for movie search.

    Attributes:
        movies (List[Movie]): A list of movies matching the search criteria.
        total (int): The total number of movies matching the search criteria.
    """

    movies: List[Movie]
    total: int


class HealthCheck(BaseModel):
    status: str = "OK"


class IndexMoviesResponse(BaseModel):
    indexed_movies_count: int
