FROM node:22 AS build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install --legacy-peer-deps
COPY frontend/ ./
RUN npm run build

FROM python:3.9-alpine AS backend
WORKDIR /app/backend
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./
EXPOSE 8000

FROM backend AS production
COPY --from=build /app/frontend/dist /app/backend/static
CMD ["uvicorn", "cinema.app:app",  "--workers", "4", "--host", "0.0.0.0", "--port", "8000"]
