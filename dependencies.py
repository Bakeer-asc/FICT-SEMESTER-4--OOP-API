"""
Custom Dependencies Module
Provides reusable dependency injection functions for the API.
"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models


def get_user_or_404(
    user_id: int,
    db: Session = Depends(get_db)
) -> models.User:
    """
    Retrieve a user by ID or raise 404.

    Args:
        user_id: The ID of the user to retrieve
        db: Database session

    Returns:
        User model if found

    Raises:
        HTTPException: 404 if user not found
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user


def get_goal_or_404(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> models.FitnessGoal:
    """
    Retrieve a fitness goal by ID or raise 404.
    Ensures users can only access their own goals.

    Args:
        goal_id: The ID of the goal to retrieve
        db: Database session
        current_user: The authenticated user

    Returns:
        FitnessGoal model if found and authorized

    Raises:
        HTTPException: 404 if goal not found or not owned by user
    """
    goal = db.query(models.FitnessGoal).filter(
        models.FitnessGoal.id == goal_id,
        models.FitnessGoal.user_id == current_user.id
    ).first()

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fitness goal with id {goal_id} not found"
        )
    return goal


def get_workout_or_404(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> models.Workout:
    """
    Retrieve a workout by ID or raise 404.
    Ensures users can only access their own workouts.
    """
    workout = db.query(models.Workout).filter(
        models.Workout.id == workout_id,
        models.Workout.user_id == current_user.id
    ).first()

    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workout with id {workout_id} not found"
        )
    return workout


def get_nutrition_or_404(
    nutrition_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> models.NutritionLog:
    """
    Retrieve a nutrition log by ID or raise 404.
    Ensures users can only access their own nutrition logs.
    """
    nutrition = db.query(models.NutritionLog).filter(
        models.NutritionLog.id == nutrition_id,
        models.NutritionLog.user_id == current_user.id
    ).first()

    if not nutrition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nutrition log with id {nutrition_id} not found"
        )
    return nutrition


def get_water_or_404(
    water_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> models.WaterLog:
    """
    Retrieve a water log by ID or raise 404.
    Ensures users can only access their own water logs.
    """
    water = db.query(models.WaterLog).filter(
        models.WaterLog.id == water_id,
        models.WaterLog.user_id == current_user.id
    ).first()

    if not water:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Water log with id {water_id} not found"
        )
    return water
