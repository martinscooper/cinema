import React, { useState, useEffect, useMemo } from "react";
import {
  Card,
  CardContent,
  Typography,
  Modal,
  Box,
  CircularProgress,
  IconButton,
  Link,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";

const MovieDisplay = ({ title, year, imdb_id }) => {
  const [open, setOpen] = useState(false);
  const [imageUrl, setImageUrl] = useState("");
  const loremText = useMemo(
    () =>
      "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
    []
  );
  const [loading, setLoading] = useState(true);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  useEffect(() => {
    if (open) {
      const randomId = Math.floor(Math.random() * 50);
      const img = new Image();
      img.src = `https://picsum.photos/id/${randomId}/800/400`;
      img.onload = () => setLoading(false);
      img.onerror = () => setLoading(false);
      setImageUrl(img.src);
    }
  }, [open]);

  return (
    <>
      <Card sx={{ height: "100%", cursor: "pointer" }} onClick={handleOpen}>
        <CardContent
          sx={{
            height: "100%",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <Typography mb={4} variant="h5" component="div">
            {title}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Release year: {year}
          </Typography>
        </CardContent>
      </Card>

      <Modal open={open} onClose={handleClose}>
        <Box
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: 600,
            bgcolor: "background.paper",
            boxShadow: 24,
            p: 4,
          }}
        >
          <IconButton
            sx={{ position: "absolute", top: 8, right: 8 }}
            onClick={handleClose}
          >
            <CloseIcon />
          </IconButton>
          <Typography variant="h6" component="h2" gutterBottom>
            {title} ({year})
          </Typography>
          {imageUrl && (
            <Box
              sx={{
                width: "100%",
                height: 400,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                mb: 2,
              }}
            >
              {loading ? (
                <CircularProgress />
              ) : (
                <Box
                  component="img"
                  src={imageUrl}
                  alt="Random"
                  sx={{ width: "100%", height: "100%", objectFit: "cover" }}
                />
              )}
            </Box>
          )}
          <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
            {loremText}
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Visit on{" "}
            <Link
              href={`https://www.imdb.com/title/${imdb_id}`}
              target="_blank"
              rel="noopener"
            >
              IMDB
            </Link>
          </Typography>
        </Box>
      </Modal>
    </>
  );
};

export default MovieDisplay;
