"""
Fitness Goals Router
CRUD operations for managing user fitness goals.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from auth import get_current_user
from dependencies import get_goal_or_404

router = APIRouter(
    prefix="/goals",
    tags=["Fitness Goals"],
    responses={
        401: {"description": "Unauthorized - Login required"},
        403: {"description": "Forbidden - Access denied"},
        404: {"description": "Not Found - Goal does not exist"}
    }
)


@router.post("/", response_model=schemas.FitnessGoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(
    goal: schemas.FitnessGoalCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new fitness goal.

    - **goal_type**: Type of goal (e.g., "Weight Loss", "Muscle Gain")
    - **target_value**: Numeric target value
    - **start_date**: Goal start date (YYYY-MM-DD)
    - **end_date**: Goal end date (YYYY-MM-DD)

    Returns the created goal.
    """
    db_goal = models.FitnessGoal(
        user_id=current_user.id,
        goal_type=goal.goal_type,
        target_value=goal.target_value,
        start_date=goal.start_date,
        end_date=goal.end_date
    )

    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)

    return db_goal


@router.get("/", response_model=List[schemas.FitnessGoalResponse])
def get_goals(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve all fitness goals for the current authenticated user.
    """
    goals = db.query(models.FitnessGoal).filter(
        models.FitnessGoal.user_id == current_user.id
    ).all()

    return goals


@router.get("/{goal_id}", response_model=schemas.FitnessGoalResponse)
def get_goal(
    goal: models.FitnessGoal = Depends(get_goal_or_404)
):
    """
    Retrieve a specific fitness goal by ID.

    - **goal_id**: The ID of the goal to retrieve
    """
    return goal


@router.put("/{goal_id}", response_model=schemas.FitnessGoalResponse)
def update_goal(
    goal_update: schemas.FitnessGoalUpdate,
    goal: models.FitnessGoal = Depends(get_goal_or_404),
    db: Session = Depends(get_db)
):
    """
    Update an existing fitness goal.

    - **goal_id**: The ID of the goal to update
    - Provide only fields you want to update
    """
    update_data = goal_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(goal, field, value)

    db.commit()
    db.refresh(goal)

    return goal


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(
    goal: models.FitnessGoal = Depends(get_goal_or_404),
    db: Session = Depends(get_db)
):
    """
    Delete a fitness goal.

    - **goal_id**: The ID of the goal to delete

    Returns 204 No Content on success.
    """
    db.delete(goal)
    db.commit()

    return None
