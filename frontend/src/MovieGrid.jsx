import React from "react";
import { Grid2 as Grid, Box } from "@mui/material";
import MovieDisplay from "./MovieDisplay";

export const MovieGrid = ({ movies }) => {
  return (
    <Box sx={{ flexGrow: 1, padding: 2 }}>
      <Grid container spacing={2}>
        {movies === null ? (
          <Grid>Fill title and year to find movies</Grid>
        ) : movies.length > 0 ? (
          movies.map((movie, index) => (
            <Grid size={{ xs: 12, sm: 6, md: 4, lg: 3 }} key={index}>
              <MovieDisplay
                title={movie.title}
                year={movie.year}
                imdb_id={movie.imdb_id}
              />
            </Grid>
          ))
        ) : (
          <Grid>No movies found</Grid>
        )}
      </Grid>
    </Box>
  );
};
