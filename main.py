"""
Fitness Tracker API - Main Application

A comprehensive REST API for tracking fitness, nutrition, and health goals.
Built with FastAPI, SQLAlchemy, and PostgreSQL.

Supports healthy lifestyles in Sierra Leone and aligns with SDG 3
(Good Health and Well-Being).
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import engine, Base
from auth import get_current_admin_user
import models
from routers import (
    auth_router,
    goals_router,
    workout_router,
    nutrition_router,
    water_router,
    progress_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Creates database tables on startup if they don't exist.
    """
    # Startup: Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: Cleanup if needed


# Initialize FastAPI application with metadata
app = FastAPI(
    title="Fitness Tracker API",
    description="""
    A comprehensive REST API for tracking fitness goals, workouts, nutrition, 
    water intake, and weight progress. 

    ## Features

    - **User Authentication**: JWT-based secure login and registration
    - **Fitness Goals**: Set and track personal fitness objectives
    - **Workout Tracking**: Log exercise sessions with calorie burn
    - **Nutrition Logging**: Monitor meals and macronutrients
    - **Water Intake**: Track daily hydration levels
    - **Weight Progress**: Monitor body weight changes over time
    - **Progress Reports**: Generate comprehensive fitness summaries
    - **Role-Based Access**: Admin and user roles with protected endpoints

    ## Authentication

    This API uses OAuth2 Password Flow with JWT tokens. 
    1. Register an account at `/auth/register`
    2. Login at `/auth/login` to receive a token
    3. Include the token in the Authorization header: `Bearer <token>`

    ## SDG 3 - Good Health and Well-Being

    This API supports healthy lifestyles in Sierra Leone by providing tools
    for individuals to monitor their physical health, nutrition, and fitness.
    """,
    version="1.0.0",
    contact={
        "name": "Fitness Tracker API Team",
        "email": "support@fitnesstracker.sl"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    lifespan=lifespan
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers with their prefixes
app.include_router(auth_router.router)
app.include_router(goals_router.router)
app.include_router(workout_router.router)
app.include_router(nutrition_router.router)
app.include_router(water_router.router)
app.include_router(progress_router.router)


@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint providing API information and navigation links.
    """
    return {
        "message": "Welcome to Fitness Tracker API",
        "version": "1.0.0",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "sdg": "SDG 3 - Good Health and Well-Being",
        "region": "Sierra Leone"
    }


@app.get("/health", tags=["Health Check"])
def health_check():
    """
    Health check endpoint for monitoring API status.
    """
    return {"status": "healthy", "service": "fitness-tracker-api"}


@app.get("/admin/users", tags=["Admin"], status_code=status.HTTP_200_OK)
def admin_get_all_users(
    admin_user=Depends(get_current_admin_user)
):
    """
    [ADMIN ONLY] Admin endpoint to list all users.

    This endpoint requires admin privileges. Regular users will receive a 403 Forbidden response.
    """
    # This is a duplicate endpoint for admin-only access demonstration
    # The actual implementation is in progress_router.py
    return {"message": "Admin endpoint accessible", "admin": admin_user.username}
