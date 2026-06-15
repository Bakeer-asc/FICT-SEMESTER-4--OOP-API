"""
Water Tracking Router
CRUD operations for daily water intake monitoring.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from auth import get_current_user
from dependencies import get_water_or_404

router = APIRouter(
    prefix="/water",
    tags=["Water Tracking"],
    responses={
        401: {"description": "Unauthorized - Login required"},
        404: {"description": "Not Found - Water log does not exist"}
    }
)


@router.post("/", response_model=schemas.WaterLogResponse, status_code=status.HTTP_201_CREATED)
def create_water_log(
    water: schemas.WaterLogCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new water intake log.

    - **liters**: Amount of water consumed in liters
    - **date**: Date of consumption (YYYY-MM-DD)

    Returns the created water log.
    """
    db_water = models.WaterLog(
        user_id=current_user.id,
        liters=water.liters,
        date=water.date
    )

    db.add(db_water)
    db.commit()
    db.refresh(db_water)

    return db_water


@router.get("/", response_model=List[schemas.WaterLogResponse])
def get_water_logs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve all water intake logs for the current authenticated user.
    """
    water_logs = db.query(models.WaterLog).filter(
        models.WaterLog.user_id == current_user.id
    ).all()

    return water_logs


@router.put("/{water_id}", response_model=schemas.WaterLogResponse)
def update_water_log(
    water_update: schemas.WaterLogUpdate,
    water: models.WaterLog = Depends(get_water_or_404),
    db: Session = Depends(get_db)
):
    """
    Update an existing water log.

    - **water_id**: The ID of the water log to update
    - Provide only fields you want to update
    """
    update_data = water_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(water, field, value)

    db.commit()
    db.refresh(water)

    return water


@router.delete("/{water_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_water_log(
    water: models.WaterLog = Depends(get_water_or_404),
    db: Session = Depends(get_db)
):
    """
    Delete a water log.

    - **water_id**: The ID of the water log to delete

    Returns 204 No Content on success.
    """
    db.delete(water)
    db.commit()

    return None
