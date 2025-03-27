import { useState } from "react";
import "./App.css";
import { MovieGrid } from "./MovieGrid";
import { MovieForm } from "./MovieForm";
import { Container } from "@mui/material";
import { PaginatedTable } from "./Pagination";
import { useFetchMovies } from "./useFetchMovies";
import { AppToolbar } from "./AppToolbar";
import { usePagination } from "./usePagination";
import { ITEMS_PER_PAGE } from "./const";

function App() {
  const [movies, setMovies] = useState(null);
  const [title, setTitle] = useState("");
  const [year, setYear] = useState("");
  const [totalItems, setTotalItems] = useState(null);
  const { searchMovies } = useFetchMovies({
    title,
    year,
    setMovies,
    setTotalItems,
  });

  const { currentPage, totalPages, setPage } = usePagination(
    ITEMS_PER_PAGE,
    totalItems
  );

  return (
    <>
      <AppToolbar />
      <Container maxWidth="xl">
        <MovieForm
          title={title}
          year={year}
          setTitle={setTitle}
          setYear={setYear}
          searchMovies={searchMovies}
          setPage={setPage}
        />
        <MovieGrid movies={movies} />
        <PaginatedTable
          totalItems={totalItems}
          searchMovies={searchMovies}
          setPage={setPage}
          totalPages={totalPages}
          currentPage={currentPage}
        />
      </Container>
    </>
  );
}

export default App;
