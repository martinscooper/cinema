import React from "react";
import { TextField, FormControl, Box, IconButton } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import { ITEMS_PER_PAGE } from "./const";

export const MovieForm = ({
  title,
  setTitle,
  year,
  setYear,
  searchMovies,
  setPage,
}) => {
  return (
    <Box
      component="form"
      sx={{
        "& .MuiTextField-root": { m: 1, width: "25ch" },
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexGrow: 1,
        padding: 2,
      }}
      noValidate
      onSubmit={(e) => {
        e.preventDefault();
        searchMovies({ from: null, size: ITEMS_PER_PAGE });
        setPage(1);
      }}
    >
      <FormControl>
        <TextField
          label="Movie Title"
          variant="outlined"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
      </FormControl>
      <FormControl>
        <TextField
          label="Release year"
          variant="outlined"
          value={year}
          onChange={(e) => setYear(e.target.value)}
        />
      </FormControl>
      <IconButton type="submit" aria-label="search" sx={{ m: 1 }}>
        <SearchIcon />
      </IconButton>
    </Box>
  );
};
