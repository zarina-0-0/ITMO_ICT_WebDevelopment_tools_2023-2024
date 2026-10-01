from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


class WorkoutCategory(str, Enum):
    strength = "силовая"
    cardio = "кардио"
    stretching = "растяжка"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    weight: float
    height: float
    level: Optional[int] = None

    workouts: List["Workout"] = Relationship(back_populates="user")
    

class ExerciseMuscleGroupLink(SQLModel, table=True):
    exercise_id: Optional[int] = Field(
        default=None,
        foreign_key="exercise.id",
        primary_key=True
    )

    muscle_group_id: Optional[int] = Field(
        default=None,
        foreign_key="musclegroup.id",
        primary_key=True
    )

    level: Optional[int] = Field(default=None)


class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: WorkoutCategory
    title: str
    date: str
    duration: int
    notes: Optional[str] = None

    user_id: int = Field(foreign_key="user.id")

    user: Optional[User] = Relationship(back_populates="workouts")
    exercises: List["Exercise"] = Relationship(back_populates="workout")


class Exercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    sets: int
    reps: Optional[int] = None
    duration: Optional[int] = None
    weight: Optional[float] = None
    description: str

    workout_id: int = Field(foreign_key="workout.id")

    workout: Optional[Workout] = Relationship(back_populates="exercises")

    muscle_groups: List["MuscleGroup"] = Relationship(
        back_populates="exercises",
        link_model=ExerciseMuscleGroupLink
    )


class MuscleGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

    exercises: List[Exercise] = Relationship(
        back_populates="muscle_groups",
        link_model=ExerciseMuscleGroupLink
    )

class MuscleGroupRead(SQLModel):
    id: int
    name: str
    description: Optional[str] = None


class ExerciseRead(SQLModel):
    id: int
    name: str
    sets: int
    reps: Optional[int] = None
    duration: Optional[int] = None
    weight: Optional[float] = None
    description: str
    workout_id: int
    muscle_groups: List[MuscleGroupRead] = []


class UserCreate(SQLModel):
    name: str
    age: int
    weight: float
    height: float
    level: Optional[int] = None


class WorkoutCreate(SQLModel):
    category: WorkoutCategory
    title: str
    date: str
    duration: int
    notes: Optional[str] = None
    user_id: int


class ExerciseCreate(SQLModel):
    name: str
    sets: int
    reps: Optional[int] = None
    duration: Optional[int] = None
    weight: Optional[float] = None
    description: str
    workout_id: int


class MuscleGroupCreate(SQLModel):
    name: str
    description: Optional[str] = None


class UserUpdate(SQLModel):
    name: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    level: Optional[int] = None


class WorkoutUpdate(SQLModel):
    category: Optional[WorkoutCategory] = None
    title: Optional[str] = None
    date: Optional[str] = None
    duration: Optional[int] = None
    notes: Optional[str] = None
    user_id: Optional[int] = None


class ExerciseUpdate(SQLModel):
    name: Optional[str] = None
    sets: Optional[int] = None
    reps: Optional[int] = None
    duration: Optional[int] = None
    weight: Optional[float] = None
    description: Optional[str] = None
    workout_id: Optional[int] = None