from lab3.worker.main import parse_url_task
from typing import List
import requests

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from .connections import init_db, get_session
from .models import (
    User,
    UserCreate,
    Workout,
    WorkoutCreate,
    Exercise,
    ExerciseCreate,
    MuscleGroup,
    MuscleGroupCreate,
    ExerciseMuscleGroupLink,
    ExerciseRead,
    UserUpdate,
    WorkoutUpdate,
    ExerciseUpdate,
    ExerciseMuscleGroupRead,
)


app = FastAPI(
    title="Workout API",
    description="API для управления тренировками, упражнениями и мышечными группами"
)


@app.on_event("startup")
def on_startup():
    init_db()



@app.post("/user", response_model=User)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    user = User.model_validate(user_data)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@app.get("/users", response_model=List[User])
def get_users(
    session: Session = Depends(get_session)
):
    return session.exec(select(User)).all()


@app.get("/user/{user_id}", response_model=User)
def get_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@app.patch("/user/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    session: Session = Depends(get_session)
):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    data = user_data.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@app.delete("/user/{user_id}")
def delete_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Находим тренировки пользователя
    workouts = session.exec(
        select(Workout).where(Workout.user_id == user_id)
    ).all()

    for workout in workouts:
        # Находим упражнения тренировки
        exercises = session.exec(
            select(Exercise).where(Exercise.workout_id == workout.id)
        ).all()

        for exercise in exercises:
            # Удаляем связи упражнения с мышечными группами
            links = session.exec(
                select(ExerciseMuscleGroupLink).where(
                    ExerciseMuscleGroupLink.exercise_id == exercise.id
                )
            ).all()

            for link in links:
                session.delete(link)
            session.delete(exercise)
        session.delete(workout)

    session.delete(user)

    session.commit()

    return {"ok": True}




@app.post("/workout", response_model=Workout)
def create_workout(
    workout_data: WorkoutCreate,
    session: Session = Depends(get_session)
):
    user = session.get(User, workout_data.user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    workout = Workout.model_validate(workout_data)

    session.add(workout)
    session.commit()
    session.refresh(workout)

    return workout


@app.get("/workouts", response_model=List[Workout])
def get_workouts(
    session: Session = Depends(get_session)
):
    return session.exec(select(Workout)).all()


@app.get("/workout/{workout_id}", response_model=Workout)
def get_workout(
    workout_id: int,
    session: Session = Depends(get_session)
):
    workout = session.get(Workout, workout_id)

    if not workout:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )

    return workout


@app.patch("/workout/{workout_id}", response_model=Workout)
def update_workout(
    workout_id: int,
    workout_data: WorkoutUpdate,
    session: Session = Depends(get_session)
):
    workout = session.get(Workout, workout_id)

    if not workout:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )

    data = workout_data.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(workout, key, value)

    session.add(workout)
    session.commit()
    session.refresh(workout)

    return workout


@app.delete("/workout/{workout_id}")
def delete_workout(
    workout_id: int,
    session: Session = Depends(get_session)
):
    workout = session.get(Workout, workout_id)

    if not workout:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )

    session.delete(workout)
    session.commit()

    return {"ok": True}



@app.post("/exercise", response_model=Exercise)
def create_exercise(
    exercise_data: ExerciseCreate,
    session: Session = Depends(get_session)
):
    workout = session.get(Workout, exercise_data.workout_id)

    if not workout:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )

    exercise = Exercise.model_validate(exercise_data)

    session.add(exercise)
    session.commit()
    session.refresh(exercise)

    return exercise


@app.get("/exercises", response_model=List[Exercise])
def get_exercises(
    session: Session = Depends(get_session)
):
    return session.exec(select(Exercise)).all()


@app.get("/exercise/{exercise_id}", response_model=ExerciseRead)
def get_exercise(
    exercise_id: int,
    session: Session = Depends(get_session)
):
    exercise = session.get(Exercise, exercise_id)

    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found"
        )

    links = session.exec(
        select(ExerciseMuscleGroupLink).where(
            ExerciseMuscleGroupLink.exercise_id == exercise_id
        )
    ).all()

    muscle_groups = []

    for link in links:
        muscle_group = session.get(
            MuscleGroup,
            link.muscle_group_id
        )

        if muscle_group:
            muscle_groups.append(
                ExerciseMuscleGroupRead(
                    id=muscle_group.id,
                    name=muscle_group.name,
                    description=muscle_group.description,
                    level=link.level
                )
            )

    return ExerciseRead(
        id=exercise.id,
        name=exercise.name,
        sets=exercise.sets,
        reps=exercise.reps,
        duration=exercise.duration,
        weight=exercise.weight,
        description=exercise.description,
        workout_id=exercise.workout_id,
        muscle_groups=muscle_groups
    )


@app.patch("/exercise/{exercise_id}", response_model=Exercise)
def update_exercise(
    exercise_id: int,
    exercise_data: ExerciseUpdate,
    session: Session = Depends(get_session)
):
    exercise = session.get(Exercise, exercise_id)

    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found"
        )

    data = exercise_data.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(exercise, key, value)

    session.add(exercise)
    session.commit()
    session.refresh(exercise)

    return exercise


@app.delete("/exercise/{exercise_id}")
def delete_exercise(
    exercise_id: int,
    session: Session = Depends(get_session)
):
    exercise = session.get(Exercise, exercise_id)

    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found"
        )

    session.delete(exercise)
    session.commit()

    return {"ok": True}


# =========================
# MUSCLE GROUP
# =========================

@app.post("/muscle-group", response_model=MuscleGroup)
def create_muscle_group(
    muscle_group_data: MuscleGroupCreate,
    session: Session = Depends(get_session)
):
    muscle_group = MuscleGroup.model_validate(muscle_group_data)

    session.add(muscle_group)
    session.commit()
    session.refresh(muscle_group)

    return muscle_group


@app.get("/muscle-groups", response_model=List[MuscleGroup])
def get_muscle_groups(
    session: Session = Depends(get_session)
):
    return session.exec(select(MuscleGroup)).all()


@app.get("/muscle-group/{muscle_group_id}", response_model=MuscleGroup)
def get_muscle_group(
    muscle_group_id: int,
    session: Session = Depends(get_session)
):
    muscle_group = session.get(MuscleGroup, muscle_group_id)

    if not muscle_group:
        raise HTTPException(
            status_code=404,
            detail="Muscle group not found"
        )

    return muscle_group


@app.delete("/muscle-group/{muscle_group_id}")
def delete_muscle_group(
    muscle_group_id: int,
    session: Session = Depends(get_session)
):
    muscle_group = session.get(MuscleGroup, muscle_group_id)

    if not muscle_group:
        raise HTTPException(
            status_code=404,
            detail="Muscle group not found"
        )

    session.delete(muscle_group)
    session.commit()

    return {"ok": True}





@app.post(
    "/exercise/{exercise_id}/muscle-group/{muscle_group_id}"
)
def add_muscle_group_to_exercise(
    exercise_id: int,
    muscle_group_id: int,
    level: int | None = None,
    session: Session = Depends(get_session)
):
    exercise = session.get(Exercise, exercise_id)

    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found"
        )

    muscle_group = session.get(MuscleGroup, muscle_group_id)

    if not muscle_group:
        raise HTTPException(
            status_code=404,
            detail="Muscle group not found"
        )

    link = ExerciseMuscleGroupLink(
        exercise_id=exercise_id,
        muscle_group_id=muscle_group_id,
        level=level
    )

    session.add(link)
    session.commit()

    return {
        "message": "Muscle group added to exercise",
        "exercise_id": exercise_id,
        "muscle_group_id": muscle_group_id,
        "level": level
    }


@app.post("/parse-url")
def parse_url(url: str):
    try:
        response = requests.post(
            "http://parser:8001/parse",
            params={"url": url},
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Parser service error: {e}"
        )


@app.post("/parse-url-async")
async def parse_url_async(url: str):
    task = parse_url_task.delay(url)

    return {
        "message": "Parsing task started",
        "task_id": task.id
    }