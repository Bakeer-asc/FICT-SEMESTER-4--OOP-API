"""
Utility Functions Module
Provides helper functions for calculations and data processing.
"""
from datetime import date, timedelta
from typing import List, Optional
import models


def calculate_goal_completion(goals: List[models.FitnessGoal]) -> float:
    """
    Calculate the overall goal completion percentage.

    Args:
        goals: List of fitness goals

    Returns:
        float: Completion percentage (0-100)
    """
    if not goals:
        return 0.0

    total_goals = len(goals)
    today = date.today()

    completed = 0
    for goal in goals:
        if goal.end_date <= today:
            completed += 1

    return (completed / total_goals) * 100 if total_goals > 0 else 0.0


def get_progress_message(percentage: float) -> str:
    """
    Generate an encouraging message based on progress percentage.

    Args:
        percentage: Goal completion percentage

    Returns:
        str: Encouraging message
    """
    if percentage >= 100:
        return "Congratulations! You have achieved all your fitness goals! 🎉"
    elif percentage >= 75:
        return f"Amazing progress! You are {percentage:.1f}% towards your goals. Keep it up! 💪"
    elif percentage >= 50:
        return f"Great work! You are {percentage:.1f}% towards your goals. Stay consistent! 🌟"
    elif percentage >= 25:
        return f"Good start! You are {percentage:.1f}% towards your goals. Keep pushing! 🚀"
    else:
        return f"Every journey begins with a single step! You are {percentage:.1f}% towards your goals. 🌱"
