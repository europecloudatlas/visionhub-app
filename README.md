# VisionHub 🎨

A simple, cloud-native vision board application for creating and managing personal goal visualization boards with image uploads.

Built as a demonstration project for deploying applications on European cloud providers' Kubernetes services.

---

## 📌 Purpose

**VisionHub** is a reference implementation designed to:

- **Test Kubernetes Deployments** across multiple European cloud providers (Thalassa Cloud, Hetzner, Scaleway, OVH)
- **Demonstrate Modern Architecture** using containerized microservices
- **Showcase Cloud-Native Patterns** with PostgreSQL, S3-compatible storage, and REST APIs

This project serves as practical content for the [**Europe Cloud Atlas**](https://youtube.com/@europecloudatlas) YouTube channel, where we explore and compare European cloud infrastructure.

---

## 🏗️ Architecture
```
┌──────────────────────────────────────────────────────────────┐
│                        VisionHub                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐           ┌──────────────┐                  │
│  │  Frontend   │    HTTP   │   Backend    │                  │
│  │ HTML/CSS/JS │ ────────> │   FastAPI    │                  │
│  └─────────────┘           │   Python     │                  │
│                             └───────┬──────┘                 │
│                                     │                        │
│                    ┌────────────────┼──────────────┐         │
│                    ▼                ▼              ▼         │
│              ┌──────────┐    ┌──────────┐   ┌──────────┐     │
│              │PostgreSQL│    │ Storage  │   │ Frontend │     │
│              │  Server  │    │ (S3 API) │   │  Server  │     │
│              └──────────┘    └──────────┘   └──────────┘     │
│              User Data       Images          Static Files    │
│              Board Metadata  Object Storage                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘

Data Flow:
1. User → Frontend → Static HTML/CSS/JS
2. Frontend → Backend API → JWT Auth
3. Backend → PostgreSQL (User data, Board metadata, Image refs)
4. Backend → Storage (Image uploads via S3 protocol)
5. Frontend → Storage (Direct image access via public URLs)
```
---

## 📡 API Routes

### Authentication
```
POST   /auth/register          Register new user (returns JWT token)
POST   /auth/login             Authenticate user (returns JWT token)
GET    /auth/me                Get current user info (protected)
```

### Vision Boards
```
GET    /boards/                List all user's boards
POST   /boards/                Create new board
GET    /boards/{id}            Get board with images
PATCH  /boards/{id}            Update board name/description
DELETE /boards/{id}            Delete board (cascade deletes images)
```

### Images
```
POST   /boards/{id}/images           Upload image to board
DELETE /boards/{id}/images/{img_id}  Delete image from board
```

### Health & Documentation
```
GET    /health                 Health check endpoint
GET    /docs                   Interactive API documentation (Swagger UI)
GET    /redoc                  API documentation (ReDoc)
```

**Authentication:** All board and image endpoints require `Authorization: Bearer <token>` header.

---

## ⚡ Features

- **🔐 JWT Authentication** - Secure token-based auth with auto-login on registration
- **📋 Vision Boards** - Create multiple boards for different life goals
- **🖼️ Image Upload** - S3-compatible object storage for vision images
- **👤 User Isolation** - Complete data separation between users
- **🎨 Modern UI** - Responsive design with gradient styling
- **🐳 Containerized** - Docker-ready for Kubernetes deployment
- **☁️ Cloud-Agnostic** - Works on any Kubernetes cluster (AWS, GCP, Hetzner, Scaleway, etc.)

---

## 🛠️ Technology Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.11** | Runtime environment |
| **FastAPI** | Modern async web framework |
| **SQLAlchemy** | ORM for database operations |
| **PostgreSQL** | Relational database (users, boards, metadata) |
| **S3-Compatible Storage** | Object storage for images |
| **JWT (python-jose)** | Token-based authentication |
| **bcrypt** | Password hashing |
| **boto3** | S3 client library |
| **Pydantic** | Data validation and serialization |
| **Uvicorn** | ASGI server |

### Frontend
| Technology | Purpose |
|------------|---------|
| **HTML5** | Semantic markup |
| **CSS3** | Styling & animations |
| **Vanilla JavaScript** | UI logic (no framework dependencies) |

---

## 📁 Project Structure
```
visionhub-app/
│
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── main.py            # Application entry point
│   │   ├── config.py          # Configuration management
│   │   ├── database.py        # Database connection & ORM
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── schemas.py         # Pydantic validation schemas
│   │   ├── auth.py            # JWT authentication logic
│   │   ├── dependencies.py    # FastAPI dependencies
│   │   ├── storage.py         # S3/MinIO client
│   │   └── routers/           # API route handlers
│   │       ├── auth.py        # Auth endpoints
│   │       └── boards.py      # Board & image endpoints
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                   # Static web application
│   ├── index.html             # Main HTML
│   ├── style.css              # Styling
│   ├── app.js                 # Frontend logic
│   └── Dockerfile
│
├── docker-compose.yml         # Local development setup
├── README.md
└── LICENSE
```

---

## 🤝 Contributing

Contributions are welcome! This project serves as educational content for comparing cloud providers.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

---

## 📧 Contact

**Europe Cloud Atlas**
- 📺 YouTube: [@europecloudatlas](https://youtube.com/@europecloudatlas)
- 📧 Email: [hello@europecloudatlas.com](mailto:hello@europecloudatlas.com)
- 💻 GitHub: [@europecloudatlas](https://github.com/europecloudatlas)

---
