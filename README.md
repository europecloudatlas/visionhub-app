# VisionHub 🎨

Test application for demonstrating Kubernetes deployments on European cloud providers.

Part of the [Europe Cloud Atlas](https://youtube.com/@europecloudatlas) project - comparing Thalassa Cloud, Hetzner, Scaleway, and OVH infrastructure.

---

## 🎯 What is this?

A simple vision board application that lets users:
- Create multiple vision boards for different goals
- Upload images to their boards
- Manage their vision collection

**Purpose:** Showcase cloud-native deployment patterns with PostgreSQL databases, S3-compatible storage, and REST APIs on European Kubernetes platforms.

---

## 🏗️ Architecture
```
Frontend (HTML/CSS/JS) → Backend (FastAPI/Python) → PostgreSQL + S3 Storage
```

**Backend:**
- FastAPI REST API with JWT authentication
- SQLAlchemy ORM with PostgreSQL
- S3-compatible object storage for images
- JWT token-based auth with bcrypt password hashing

**Frontend:**
- Vanilla JavaScript SPA (no frameworks)
- Responsive CSS with gradient design
- Direct S3 image loading via public URLs

---

## 📡 API Endpoints

### Authentication
```
POST /auth/register          - Create account (returns JWT)
POST /auth/login             - Login (returns JWT)
GET  /auth/me                - Get current user
```

### Vision Boards
```
GET    /boards/              - List all boards
POST   /boards/              - Create board
GET    /boards/{id}          - Get board with images
PATCH  /boards/{id}          - Update board
DELETE /boards/{id}          - Delete board
```

### Images
```
POST   /boards/{id}/images           - Upload image
DELETE /boards/{id}/images/{img_id}  - Delete image
```

### Other
```
GET /health                  - Health check
GET /docs                    - Swagger UI
```

All board/image endpoints require: `Authorization: Bearer <token>`

---

## 🛠️ Tech Stack

**Backend:** Python 3.11, FastAPI, SQLAlchemy, PostgreSQL, boto3 (S3), JWT  
**Frontend:** HTML5, CSS3, Vanilla JavaScript

---

## 📁 Project Structure
```
visionhub-app/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app entry point
│   │   ├── config.py         # Environment configuration
│   │   ├── database.py       # SQLAlchemy setup
│   │   ├── models.py         # Database models
│   │   ├── schemas.py        # Pydantic validation
│   │   ├── auth.py           # JWT authentication
│   │   ├── dependencies.py   # FastAPI dependencies
│   │   ├── storage.py        # S3 client
│   │   └── routers/
│   │       ├── auth.py       # Auth endpoints
│   │       └── boards.py     # Board & image endpoints
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── index.html            # Main HTML
│   ├── app.js                # Frontend logic
│   ├── style.css             # Styling
│   ├── config.js             # Environment config
│   ├── nginx.conf            # Nginx configuration
│   └── Dockerfile
└── docker-compose.yml        # Local development
```

---

## 🖼️ Image Storage Flow

**Upload:**
1. Frontend → `POST /boards/{id}/images` with file
2. Backend uploads to S3 bucket
3. Backend saves public URL to PostgreSQL
4. Returns image metadata to frontend

**Display:**
1. Frontend → `GET /boards/{id}` 
2. Backend returns board with image URLs
3. Frontend loads images **directly from S3** (not via backend)
4. Browser: `GET https://objects.thalassa.cloud/bucket/image.jpg`

⚠️ **Note:** S3 bucket must be publicly accessible for direct image loading.

---

## 🚀 Deployment

This app is deployed across multiple European Kubernetes providers as part of comparison videos on the Europe Cloud Atlas YouTube channel.

**Infrastructure code:** [visionhub-infrastructure](https://github.com/europecloudatlas/visionhub-infrastructure)

**Deployment:**
- Backend: FastAPI on Kubernetes with PostgreSQL + S3
- Frontend: Nginx serving static files
- Ingress: cert-manager for SSL, nginx-ingress for routing

---

## 📧 Contact

**Europe Cloud Atlas**  
📺 YouTube: [@europecloudatlas](https://youtube.com/@europecloudatlas)  
💻 GitHub: [@europecloudatlas](https://github.com/europecloudatlas)  
📧 Email: hello@europecloudatlas.com