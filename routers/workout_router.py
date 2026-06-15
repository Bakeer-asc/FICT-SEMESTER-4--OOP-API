"""
Workout Router
CRUD operations for tracking exercise sessions.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from auth import get_current_user
from dependencies import get_workout_or_404

router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"],
    responses={
        401: {"description": "Unauthorized - Login required"},
        404: {"description": "Not Found - Workout does not exist"}
    }
)


@router.post("/", response_model=schemas.WorkoutResponse, status_code=status.HTTP_201_CREATED)
def create_workout(
    workout: schemas.WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new workout record.

    - **workout_name**: Name of the workout (e.g., "Morning Run")
    - **workout_type**: Type of exercise (e.g., "Cardio", "Strength")
    - **duration_minutes**: Duration in minutes
    - **calories_burned**: Calories burned during workout
    - **workout_date**: Date of the workout (YYYY-MM-DD)

    Returns the created workout record.
    """
    db_workout = models.Workout(
        user_id=current_user.id,
        workout_name=workout.workout_name,
        workout_type=workout.workout_type,
        duration_minutes=workout.duration_minutes,
        calories_burned=workout.calories_burned,
        workout_date=workout.workout_date
    )

    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)

    return db_workout


@router.get("/", response_model=List[schemas.WorkoutResponse])
def get_workouts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve all workouts for the current authenticated user.
    """
    workouts = db.query(models.Workout).filter(
        models.Workout.user_id == current_user.id
    ).all()

    return workouts


@router.get("/{workout_id}", response_model=schemas.WorkoutResponse)
def get_workout(
    workout: models.Workout = Depends(get_workout_or_404)
):
    """
    Retrieve a specific workout by ID.

    - **workout_id**: The ID of the workout to retrieve
    """
    return workout


@router.put("/{workout_id}", response_model=schemas.WorkoutResponse)
def update_workout(
    workout_update: schemas.WorkoutUpdate,
    workout: models.Workout = Depends(get_workout_or_404),
    db: Session = Depends(get_db)
):
    """
    Update an existing workout record.

    - **workout_id**: The ID of the workout to update
    - Provide only fields you want to update
    """
    update_data = workout_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(workout, field, value)

    db.commit()
    db.refresh(workout)

    return workout


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(
    workout: models.Workout = Depends(get_workout_or_404),
    db: Session = Depends(get_db)
):
    """
    Delete a workout record.

    - **workout_id**: The ID of the workout to delete

    Returns 204 No Content on success.
    """
    db.delete(workout)
    db.commit()

    return None
