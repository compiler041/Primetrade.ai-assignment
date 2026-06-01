# Primetrade.ai Backend & Frontend Assignment

This repository contains a full-stack web application built to fulfill the assignment requirements. It provides a secure backend API built with FastAPI and a modern frontend UI built with React.

## Features

### 🚀 Backend (FastAPI)
- **Authentication & Security:**
  - JWT-based authentication using `jose.jwt`.
  - Password hashing via `bcrypt`.
  - SQLite for local development (can be switched to PostgreSQL via `.env`).
- **Role-Based Access Control:**
  - Distinct permissions for users and superusers (admins).
  - Admin-only routes for user management.
- **RESTful API:**
  - API versioning (`/api/v1`).
  - Full CRUD endpoints for Tasks and Projects.
  - Interactive Swagger documentation at `/api/docs`.
- **Database & Architecture:**
  - SQLAlchemy ORM models.
  - Alembic for database migrations.
  - Pydantic models for request validation and response serialization.

### 🎨 Frontend (React + TypeScript)
- **Modern UI Framework:** Built using Material-UI (MUI) components.
- **Authentication Flow:**
  - Secure Login and Registration pages with modern gradient designs.
  - Protected Dashboard routing (redirects unauthenticated users).
  - JWT token stored in `localStorage`.
- **Project & Task Management:**
  - Create, view, edit, and delete projects.
  - Drill down into projects to manage associated tasks.
  - Form validation with `react-hook-form` and `yup`.
- **User Feedback:**
  - Toast notifications for errors.
  - Confirmation modals for destructive actions (e.g., deleting a project).
  - Loading states during API calls.

## Project Structure

```text
Primetradassignment/
├── backend/
│   ├── app/
│   │   ├── core/           # Configs, Security, Celery App
│   │   ├── db/             # SQLAlchemy Session, Engine
│   │   ├── domains/        # Business Logic (auth, tasks, users)
│   │   ├── alembic/        # Migrations
│   │   └── main.py         # FastAPI Entry Point
│   ├── requirements.txt
│   └── start.sh            # Docker Entrypoint Script
├── frontend/
│   ├── src/
│   │   ├── apis/           # Fetch wrappers (Projects, Tasks)
│   │   ├── components/     # UI Components (Forms, Tables, Layouts)
│   │   ├── context/        # AuthContext (JWT management)
│   │   ├── pages/          # Login, Register, Dashboards
│   │   ├── types/          # TypeScript Interfaces
│   │   ├── App.tsx         # Root Component
│   │   └── index.tsx       # React Router Setup
│   ├── package.json
│   └── tsconfig.json
└── docker-compose.yml      # Orchestrates Frontend, Backend, Postgres, Redis, Nginx
```

## Quick Start (Docker)

The easiest way to run the entire stack is via Docker Compose.

1. **Build and start the containers:**
   ```bash
   docker compose up --build -d
   ```
2. **Access the application:**
   - **Frontend UI:** `http://localhost:3000`
   - **Backend API Docs:** `http://localhost:8888/api/docs`
   - **Flower (Celery Monitor):** `http://localhost:5555`

## Local Development (Without Docker)

### Backend
1. Create a virtual environment and activate it (Python 3.10+ recommended).
2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Start the FastAPI server (it will automatically create the SQLite tables on startup):
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend
1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the React development server:
   ```bash
   npm start
   ```
3. Open `http://localhost:3000` in your browser. (Ensure your `.env` points to the correct API base URL, typically `http://localhost:8000/api`).

## Technologies Used
- **Backend:** Python, FastAPI, SQLAlchemy, Alembic, Pydantic, Passlib, python-jose.
- **Frontend:** React, TypeScript, React Router DOM, Material UI (MUI), React Hook Form.
- **Infrastructure:** Docker, Docker Compose, Nginx, PostgreSQL, Redis, Celery.
