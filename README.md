# Fitness Tracker API

A comprehensive REST API for tracking fitness goals, workouts, nutrition, water intake, and weight progress. Built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **JWT Authentication**.

> **SDG 3 - Good Health and Well-Being**: This project supports healthy lifestyles in Sierra Leone by empowering individuals to monitor their physical health, nutrition, and fitness through digital tools.

---

## Project Overview

The Fitness Tracker API allows users to:

- **Register** secure accounts with bcrypt-hashed passwords
- **Login** using JWT token-based authentication (OAuth2 Password Flow)
- **Manage Fitness Goals** with target values and deadlines
- **Track Workouts** including duration, type, and calories burned
- **Log Nutrition** with detailed macronutrient tracking
- **Monitor Water Intake** for daily hydration goals
- **Record Weight Progress** over time
- **Generate Progress Reports** with completion statistics

The system implements **Role-Based Access Control (RBAC)** with `admin` and `user` roles, ensuring data privacy and secure endpoint protection.

---

## Features

### Core Features

- ✅ JWT Authentication with OAuth2 Password Flow
- ✅ Password Hashing using Passlib Bcrypt
- ✅ Role-Based Authorization (Admin / User)
- ✅ Dependency Injection with FastAPI `Depends()`
- ✅ Full CRUD for all fitness tracking entities
- ✅ Comprehensive Progress Reports
- ✅ Interactive API Documentation (Swagger & ReDoc)
- ✅ CORS enabled for frontend integration
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Input validation with Pydantic schemas
- ✅ HTTP status code compliance (200, 201, 400, 401, 403, 404)

### Security Features

- 🔐 Bcrypt password hashing (never store plain passwords)
- 🔐 JWT token expiration (30 minutes default)
- 🔐 OAuth2 Bearer token authentication
- 🔐 Protected routes with dependency injection
- 🔐 Admin-only endpoint restrictions (403 Forbidden for non-admins)

---

## Technology Stack

| Technology    | Purpose               | Version |
| ------------- | --------------------- | ------- |
| Python        | Programming Language  | 3.12+   |
| FastAPI       | Web Framework         | 0.111.0 |
| Uvicorn       | ASGI Server           | 0.30.0  |
| SQLAlchemy    | ORM                   | 2.0.30  |
| PostgreSQL    | Database              | 14+     |
| Psycopg2      | PostgreSQL Driver     | 2.9.9   |
| Pydantic      | Data Validation       | 2.7.4   |
| python-jose   | JWT Implementation    | 3.3.0   |
| Passlib       | Password Hashing      | 1.7.4   |
| python-dotenv | Environment Variables | 1.0.1   |

---

## Installation

### Prerequisites

- Python 3.12 or higher
- PostgreSQL 14 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git https://github.com/Bakeer-asc/FICT-SEMESTER-4--OOP-API
cd fitness_tracker_api
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

## Database Setup

### Step 1: Create PostgreSQL Database

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE fitness_tracker;

# Exit
\q
```

### Step 2: Tables Auto-Creation

Tables are automatically created when the application starts via SQLAlchemy's `Base.metadata.create_all()`.

### Manual Table Creation (Optional)

If you prefer manual setup, you can run:

```bash
python -c "from database import engine, Base; Base.metadata.create_all(bind=engine)"
```

---

## Running the Application

### Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Access the API

- **API Base URL**: `http://localhost:8000`
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

---

## Authentication Flow

### 1. Register a New User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### 2. Login to Get JWT Token

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=securepassword123"
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Access Protected Endpoints

Include the token in the Authorization header:

```bash
curl -X GET "http://localhost:8000/workouts/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## API Endpoints

### Authentication

| Method | Endpoint         | Description             | Auth Required |
| ------ | ---------------- | ----------------------- | ------------- |
| POST   | `/auth/register` | Register new user       | No            |
| POST   | `/auth/login`    | Login and get JWT token | No            |

### Fitness Goals

| Method | Endpoint      | Description             | Auth Required |
| ------ | ------------- | ----------------------- | ------------- |
| POST   | `/goals/`     | Create new fitness goal | Yes           |
| GET    | `/goals/`     | List all goals          | Yes           |
| GET    | `/goals/{id}` | Get specific goal       | Yes           |
| PUT    | `/goals/{id}` | Update goal             | Yes           |
| DELETE | `/goals/{id}` | Delete goal             | Yes           |

### Workouts

| Method | Endpoint         | Description          | Auth Required |
| ------ | ---------------- | -------------------- | ------------- |
| POST   | `/workouts/`     | Create workout       | Yes           |
| GET    | `/workouts/`     | List all workouts    | Yes           |
| GET    | `/workouts/{id}` | Get specific workout | Yes           |
| PUT    | `/workouts/{id}` | Update workout       | Yes           |
| DELETE | `/workouts/{id}` | Delete workout       | Yes           |

### Nutrition

| Method | Endpoint          | Description             | Auth Required |
| ------ | ----------------- | ----------------------- | ------------- |
| POST   | `/nutrition/`     | Create nutrition log    | Yes           |
| GET    | `/nutrition/`     | List all nutrition logs | Yes           |
| PUT    | `/nutrition/{id}` | Update nutrition log    | Yes           |
| DELETE | `/nutrition/{id}` | Delete nutrition log    | Yes           |

### Water Tracking

| Method | Endpoint      | Description         | Auth Required |
| ------ | ------------- | ------------------- | ------------- |
| POST   | `/water/`     | Create water log    | Yes           |
| GET    | `/water/`     | List all water logs | Yes           |
| PUT    | `/water/{id}` | Update water log    | Yes           |
| DELETE | `/water/{id}` | Delete water log    | Yes           |

### Progress Reports

| Method | Endpoint                | Description            | Auth Required    |
| ------ | ----------------------- | ---------------------- | ---------------- |
| GET    | `/progress/`            | Get progress report    | Yes              |
| GET    | `/progress/admin/users` | [Admin] List all users | Yes (Admin only) |

---

## Role-Based Access Control

### User Roles

- **user**: Standard user with access to own data only
- **admin**: Full system access including user management

### Admin-Only Endpoints

The following endpoints require `role=admin`:

- `GET /progress/admin/users` - Returns 403 Forbidden for non-admin users

### Creating an Admin User

Currently, admin users must be created directly in the database or by modifying the role after registration:

```sql
UPDATE users SET role = 'admin' WHERE username = 'john_doe';
```

---

## API Documentation

### Swagger UI

Interactive API documentation with try-it-out functionality:

```
http://localhost:8000/docs
```

### ReDoc

Alternative API documentation with clean layout:

```
http://localhost:8000/redoc
```

Both documentations include:

- Request/response schemas with examples
- Authentication requirements
- Endpoint descriptions
- HTTP status codes

---

## SDG Relevance

### SDG 3: Good Health and Well-Being

This Fitness Tracker API directly contributes to **Sustainable Development Goal 3** by:

1. **Promoting Physical Activity**: Users can track workouts and set fitness goals, encouraging regular exercise.

2. **Nutrition Awareness**: Detailed nutrition logging helps users make informed dietary choices.

3. **Hydration Monitoring**: Water tracking is especially critical in tropical climates like Sierra Leone where proper hydration prevents heat-related illnesses.

4. **Health Data Accessibility**: Digital health tracking makes fitness monitoring accessible to university students and communities.

5. **Preventive Health**: By monitoring weight and fitness progress, users can identify health trends early.

6. **Community Health**: Aggregate data can inform public health initiatives in Sierra Leone.

> _"Ensuring healthy lives and promoting well-being for all at all ages is essential to sustainable development."_ — United Nations

---
