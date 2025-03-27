import { useState } from "react";

export const usePagination = (itemsPerPage, totalItems) => {
  const [currentPage, setCurrentPage] = useState(1);

  const totalPages = Math.ceil(totalItems / itemsPerPage);

  const setPage = (page) => {
    setCurrentPage(page);
  };

  return { currentPage, totalPages, setPage };
};
