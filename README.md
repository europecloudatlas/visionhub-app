# VisionHub 🎨

Personal vision board platform for creating and managing inspirational image boards.

## Features

- 🔐 User Authentication (JWT)
- 📋 Create & Manage Vision Boards
- 🖼️ Upload Images to Boards
- 🗑️ Delete Boards & Images
- 👤 User-Specific Content (only see your own boards)

## Tech Stack

**Backend:**
- Python 3.11 + FastAPI
- PostgreSQL
- Redis (caching)
- MinIO/S3 (image storage)

**Frontend:**
- HTML/CSS/JavaScript
- Responsive design

## Quick Start
```bash
# Clone repo
git clone https://github.com/europecloudatlas/visionhub-app.git
cd visionhub-app

# Start all services
docker-compose up -d

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

## Project Structure
```
backend/          # FastAPI backend
frontend/         # HTML/CSS/JS frontend
docker-compose.yml # Local development setup
```

## License

MIT

---

**Europe Cloud Atlas** - https://youtube.com/@europecloudatlas
