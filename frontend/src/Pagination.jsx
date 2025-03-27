import React, { useCallback } from "react";
import Pagination from "@mui/material/Pagination";
import { Box } from "@mui/material";
import { ITEMS_PER_PAGE } from "./const";

export const PaginatedTable = ({
  totalItems,
  searchMovies,
  setPage,
  totalPages,
  currentPage,
}) => {
  const onPageChange = useCallback(
    (e, newPage) => {
      setPage(newPage);
      searchMovies({
        from: (newPage - 1) * ITEMS_PER_PAGE,
        size: ITEMS_PER_PAGE,
      });
    },
    [searchMovies, setPage]
  );

  if (!totalItems) {
    return null;
  }

  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: 2,
      }}
    >
      <Pagination
        count={totalPages}
        page={currentPage}
        onChange={onPageChange}
        shape="rounded"
        color="primary"
      />
    </Box>
  );
};
