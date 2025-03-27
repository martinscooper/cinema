import { useCallback } from "react";

export const useFetchMovies = ({ title, year, setMovies, setTotalItems }) => {
  const searchMovies = useCallback(
    ({ from, size }) => {
      let url = `${import.meta.env.VITE_BACKEND_URL}/api/movies?`;
      if (title) {
        url += `title=${title}`;
      }
      if (year) {
        url += `&year=${year}`;
      }
      if (from) {
        url += `&from_item=${from}`;
      }
      if (size) {
        url += `&size=${size}`;
      }
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          setMovies(data["movies"]);
          setTotalItems(data["total"]);
        });
    },
    [setMovies, setTotalItems, title, year]
  );

  return { searchMovies };
};
