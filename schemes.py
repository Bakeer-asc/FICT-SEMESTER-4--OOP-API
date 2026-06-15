"""
Pydantic Schemas Module
Defines data validation and serialization models for all API endpoints.
Separates request/response models for clean API contracts.
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date as date_type


# ==========================================
# USER SCHEMAS
# ==========================================

class UserBase(BaseModel):
    """Base user schema with shared attributes."""
    username: str = Field(..., min_length=3, max_length=50, example="john_doe")
    email: EmailStr = Field(..., example="john@example.com")


class UserCreate(UserBase):
    """Schema for user registration requests."""
    password: str = Field(..., min_length=6, max_length=100, example="securepassword123")


class UserResponse(UserBase):
    """Schema for user data in responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str = Field(default="user", example="user")
    created_at: datetime


class UserInDB(UserBase):
    """Internal schema including hashed password."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    hashed_password: str
    role: str
    created_at: datetime


class Token(BaseModel):
    """JWT token response schema."""
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(default="bearer", example="bearer")


class TokenData(BaseModel):
    """Schema for decoded JWT token payload."""
    username: Optional[str] = None
    role: Optional[str] = None


# ==========================================
# FITNESS GOAL SCHEMAS
# ==========================================

class FitnessGoalBase(BaseModel):
    """Base fitness goal schema."""
    goal_type: str = Field(..., max_length=100, example="Weight Loss")
    target_value: float = Field(..., gt=0, example=10.0)
    start_date: date_type = Field(..., example="2024-01-01")
    end_date: date_type = Field(..., example="2024-06-01")


class FitnessGoalCreate(FitnessGoalBase):
    """Schema for creating a new fitness goal."""
    pass


class FitnessGoalUpdate(BaseModel):
    """Schema for updating an existing fitness goal."""
    goal_type: Optional[str] = Field(None, max_length=100, example="Muscle Gain")
    target_value: Optional[float] = Field(None, gt=0, example=5.0)
    start_date: Optional[date_type] = Field(None, example="2024-02-01")
    end_date: Optional[date_type] = Field(None, example="2024-07-01")


class FitnessGoalResponse(FitnessGoalBase):
    """Schema for fitness goal responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime


# ==========================================
# WORKOUT SCHEMAS
# ==========================================

class WorkoutBase(BaseModel):
    """Base workout schema."""
    workout_name: str = Field(..., max_length=100, example="Morning Run")
    workout_type: str = Field(..., max_length=50, example="Cardio")
    duration_minutes: int = Field(..., gt=0, example=45)
    calories_burned: float = Field(..., ge=0, example=350.5)
    workout_date: date_type = Field(..., example="2024-01-15")


class WorkoutCreate(WorkoutBase):
    """Schema for creating a new workout."""
    pass


class WorkoutUpdate(BaseModel):
    """Schema for updating an existing workout."""
    workout_name: Optional[str] = Field(None, max_length=100, example="Evening Jog")
    workout_type: Optional[str] = Field(None, max_length=50, example="Cardio")
    duration_minutes: Optional[int] = Field(None, gt=0, example=30)
    calories_burned: Optional[float] = Field(None, ge=0, example=250.0)
    workout_date: Optional[date_type] = Field(None, example="2024-01-16")


class WorkoutResponse(WorkoutBase):
    """Schema for workout responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime


# ==========================================
# NUTRITION LOG SCHEMAS
# ==========================================

class NutritionLogBase(BaseModel):
    """Base nutrition log schema."""
    meal_name: str = Field(..., max_length=100, example="Grilled Chicken Salad")
    calories: float = Field(..., ge=0, example=450.0)
    protein: float = Field(default=0.0, ge=0, example=35.5)
    carbohydrates: float = Field(default=0.0, ge=0, example=20.0)
    fat: float = Field(default=0.0, ge=0, example=15.0)
    date: date_type = Field(..., example="2024-01-15")


class NutritionLogCreate(NutritionLogBase):
    """Schema for creating a new nutrition log."""
    pass


class NutritionLogUpdate(BaseModel):
    """Schema for updating an existing nutrition log."""
    meal_name: Optional[str] = Field(None, max_length=100, example="Salmon with Rice")
    calories: Optional[float] = Field(None, ge=0, example=600.0)
    protein: Optional[float] = Field(None, ge=0, example=40.0)
    carbohydrates: Optional[float] = Field(None, ge=0, example=50.0)
    fat: Optional[float] = Field(None, ge=0, example=20.0)
    date: Optional[date_type] = Field(None, example="2024-01-16")


class NutritionLogResponse(NutritionLogBase):
    """Schema for nutrition log responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime


# ==========================================
# WATER LOG SCHEMAS
# ==========================================

class WaterLogBase(BaseModel):
    """Base water log schema."""
    liters: float = Field(..., gt=0, example=2.5)
    date: date_type = Field(..., example="2024-01-15")


class WaterLogCreate(WaterLogBase):
    """Schema for creating a new water log."""
    pass


class WaterLogUpdate(BaseModel):
    """Schema for updating an existing water log."""
    liters: Optional[float] = Field(None, gt=0, example=3.0)
    date: Optional[date_type] = Field(None, example="2024-01-16")


class WaterLogResponse(WaterLogBase):
    """Schema for water log responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime


# ==========================================
# WEIGHT LOG SCHEMAS
# ==========================================

class WeightLogBase(BaseModel):
    """Base weight log schema."""
    weight: float = Field(..., gt=0, example=75.5)
    date: date_type = Field(..., example="2024-01-15")


class WeightLogCreate(WeightLogBase):
    """Schema for creating a new weight log."""
    pass


class WeightLogUpdate(BaseModel):
    """Schema for updating an existing weight log."""
    weight: Optional[float] = Field(None, gt=0, example=74.0)
    date: Optional[date_type] = Field(None, example="2024-01-22")


class WeightLogResponse(WeightLogBase):
    """Schema for weight log responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime


# ==========================================
# PROGRESS REPORT SCHEMA
# ==========================================

class ProgressReport(BaseModel):
    """Schema for comprehensive progress reports."""
    total_workouts: int = Field(..., example=25)
    total_calories_burned: float = Field(..., example=8750.5)
    current_weight: Optional[float] = Field(None, example=74.0)
    total_water_consumed: float = Field(..., example=150.5)
    goal_completion_percentage: float = Field(..., ge=0, le=100, example=65.5)
    message: str = Field(..., example="Keep pushing! You are 65.5% towards your goal.")