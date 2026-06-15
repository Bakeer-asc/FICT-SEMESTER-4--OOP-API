"""
Progress Report Router
Generates comprehensive fitness progress reports for users.
"""
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models
import schemas
from auth import get_current_user
from utils import calculate_goal_completion, get_progress_message

router = APIRouter(
    prefix="/progress",
    tags=["Progress Reports"],
    responses={
        401: {"description": "Unauthorized - Login required"}
    }
)


@router.get("/", response_model=schemas.ProgressReport)
def get_progress_report(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Generate a comprehensive fitness progress report.

    Returns:
    - **total_workouts**: Total number of workouts logged
    - **total_calories_burned**: Sum of all calories burned
    - **current_weight**: Most recent weight entry
    - **total_water_consumed**: Total liters of water consumed
    - **goal_completion_percentage**: Percentage of goals completed
    - **message**: Encouraging message based on progress
    """
    # Total workouts
    total_workouts = db.query(func.count(models.Workout.id)).filter(
        models.Workout.user_id == current_user.id
    ).scalar() or 0

    # Total calories burned
    total_calories = db.query(func.sum(models.Workout.calories_burned)).filter(
        models.Workout.user_id == current_user.id
    ).scalar() or 0.0

    # Current weight (most recent)
    current_weight = db.query(models.WeightLog).filter(
        models.WeightLog.user_id == current_user.id
    ).order_by(models.WeightLog.date.desc()).first()

    # Total water consumed
    total_water = db.query(func.sum(models.WaterLog.liters)).filter(
        models.WaterLog.user_id == current_user.id
    ).scalar() or 0.0

    # Goals and completion percentage
    goals = db.query(models.FitnessGoal).filter(
        models.FitnessGoal.user_id == current_user.id
    ).all()

    completion_percentage = calculate_goal_completion(goals)
    message = get_progress_message(completion_percentage)

    return schemas.ProgressReport(
        total_workouts=total_workouts,
        total_calories_burned=round(total_calories, 2),
        current_weight=current_weight.weight if current_weight else None,
        total_water_consumed=round(total_water, 2),
        goal_completion_percentage=round(completion_percentage, 2),
        message=message
    )


@router.get("/admin/users", response_model=list[schemas.UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    [ADMIN ONLY] Retrieve all registered users.

    This endpoint is restricted to admin users only.
    Non-admin users will receive a 403 Forbidden response.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required. You do not have permission to access this resource."
        )

    users = db.query(models.User).all()
    return users
