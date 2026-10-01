from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class WorkoutCategory(Enum):
    strength = "силовая"
    cardio = "кардио"
    stretching = "растяжка"


class User(BaseModel):
    id: int
    name: str
    age: int
    weight: float
    height: float
    level: Optional[int] = None


class Exercise(BaseModel):
    id: int
    name: str
    sets: int
    reps: Optional[int] = None
    duration: Optional[int] = None
    weight: Optional[float] = None
    description: str


class Workout(BaseModel):
    id: int
    category: WorkoutCategory
    title: str
    date: str
    duration: int
    user: User
    notes: Optional[str] = None
    exercises: List[Exercise]


temp_bd = [{
    "id": 1,
    "category": "силовая",
    "title": "пресс + руки",
    "date": "2026-04-22",
    "duration": 25,
    "user": {
        "id": 1,
        "name": "Аня Смирнова",
        "age": 22,
        "weight": 57.5,
        "height": 158,
        "level": 3
    },
    "notes": "тренировка прошла легко но сильно вспотела)",
    "exercises":
        [{
            "id": 1,
            "name": "планка",
            "sets": 3,
            "reps": None,
            "duration": 40,
            "weight": None,
            "description": "четыре опоры на руках и ногах, руки под плечами, поясница не проваливается и не поднимается высоко"

        },
        {
            "id": 2,
            "name": "отжимания",
            "sets": 3,
            "reps": 8,
            "duration": None,
            "weight": None,
            "description": ""

        }]
},
    {
    "id": 2,
    "category": "силовая",
    "title": "ноги",
    "date": "2026-05-22",
    "duration": 25,
    "user": {
        "id": 2,
        "name": "Даша",
        "age": 29,
        "weight": 58.8,
        "height": 162,
        "level": 2
    },
    "notes": "устала, но не сильно",
    "exercises":
        [{
            "id": 1,
            "name": "выпады с гантелями",
            "sets": 3,
            "reps": 15,
            "duration": None,
            "weight": 6,
            "description": "спина прямая, угол в коленях 90 градусов"

        }]
},
]


users_bd = [
    {
        "id": 1,
        "name": "Аня Смирнова",
        "age": 22,
        "weight": 57.5,
        "height": 158,
        "level": 3
    },
    {
        "id": 2,
        "name": "Даша",
        "age": 29,
        "weight": 58.8,
        "height": 162,
        "level": 2
    }
]
