"""
Nutrition Router
CRUD operations for tracking meals and macronutrients.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from auth import get_current_user
from dependencies import get_nutrition_or_404

router = APIRouter(
    prefix="/nutrition",
    tags=["Nutrition"],
    responses={
        401: {"description": "Unauthorized - Login required"},
        404: {"description": "Not Found - Nutrition log does not exist"}
    }
)


@router.post("/", response_model=schemas.NutritionLogResponse, status_code=status.HTTP_201_CREATED)
def create_nutrition(
    nutrition: schemas.NutritionLogCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new nutrition log entry.

    - **meal_name**: Name of the meal (e.g., "Grilled Chicken Salad")
    - **calories**: Total calories
    - **protein**: Protein in grams (optional)
    - **carbohydrates**: Carbohydrates in grams (optional)
    - **fat**: Fat in grams (optional)
    - **date**: Date of the meal (YYYY-MM-DD)

    Returns the created nutrition log.
    """
    db_nutrition = models.NutritionLog(
        user_id=current_user.id,
        meal_name=nutrition.meal_name,
        calories=nutrition.calories,
        protein=nutrition.protein,
        carbohydrates=nutrition.carbohydrates,
        fat=nutrition.fat,
        date=nutrition.date
    )

    db.add(db_nutrition)
    db.commit()
    db.refresh(db_nutrition)

    return db_nutrition


@router.get("/", response_model=List[schemas.NutritionLogResponse])
def get_nutrition_logs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve all nutrition logs for the current authenticated user.
    """
    nutrition_logs = db.query(models.NutritionLog).filter(
        models.NutritionLog.user_id == current_user.id
    ).all()

    return nutrition_logs


@router.put("/{nutrition_id}", response_model=schemas.NutritionLogResponse)
def update_nutrition(
    nutrition_update: schemas.NutritionLogUpdate,
    nutrition: models.NutritionLog = Depends(get_nutrition_or_404),
    db: Session = Depends(get_db)
):
    """
    Update an existing nutrition log.

    - **nutrition_id**: The ID of the nutrition log to update
    - Provide only fields you want to update
    """
    update_data = nutrition_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(nutrition, field, value)

    db.commit()
    db.refresh(nutrition)

    return nutrition


@router.delete("/{nutrition_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_nutrition(
    nutrition: models.NutritionLog = Depends(get_nutrition_or_404),
    db: Session = Depends(get_db)
):
    """
    Delete a nutrition log.

    - **nutrition_id**: The ID of the nutrition log to delete

    Returns 204 No Content on success.
    """
    db.delete(nutrition)
    db.commit()

    return None
