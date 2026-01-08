# FastAPI Task
Simple FastAPI backend with JWT authentication and async bulk
customer upload processing.

## Tech Stack
- FastAPI
- PostgreSQL
- Redis
- TaskIQ
- Docker & Docker Compose

## Features
- User signup, login, logout
- JWT access & refresh tokens
- Protected customer APIs
- Bulk customer upload via CSV/Excel file
- Background processing (non-blocking)
- Upload metrics: total, success, failed
- Retry logic
- Stable and scalable under load

## Main Endpoints
### Auth
- POST /auth/signup
- POST /auth/login
- POST /auth/logout
- POST /auth/refresh

### Customers
- GET  /customers/template
- POST /customers/upload
- GET  /customers/progress
- GET  /customers/metrics

## How to Run
1. Copy environment variables
   cp example.env .env

2. Start the application
   docker compose up --build