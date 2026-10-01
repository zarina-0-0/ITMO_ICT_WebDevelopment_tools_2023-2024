from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from connections import init_db, get_session
from models import (
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
)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/user")
def user_create(
    user: UserCreate,
    session: Session = Depends(get_session)
):
    db_user = User.model_validate(user)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get("/users")
def users_list(
    session: Session = Depends(get_session)
) -> List[User]:
    return session.exec(select(User)).all()


@app.get("/user/{user_id}")
def user_get(
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


@app.post("/workout")
def workout_create(
    workout: WorkoutCreate,
    session: Session = Depends(get_session)
):
    db_workout = Workout.model_validate(workout)

    session.add(db_workout)
    session.commit()
    session.refresh(db_workout)

    return db_workout


@app.get("/workouts")
def workouts_list(
    session: Session = Depends(get_session)
) -> List[Workout]:
    return session.exec(select(Workout)).all()


@app.get("/workout/{workout_id}")
def workout_get(
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


@app.post("/exercise")
def exercise_create(
    exercise: ExerciseCreate,
    session: Session = Depends(get_session)
):
    db_exercise = Exercise.model_validate(exercise)

    session.add(db_exercise)
    session.commit()
    session.refresh(db_exercise)

    return db_exercise


@app.get("/exercises")
def exercises_list(
    session: Session = Depends(get_session)
) -> List[Exercise]:
    return session.exec(select(Exercise)).all()


@app.get("/exercise/{exercise_id}", response_model=ExerciseRead)
def exercise_get(
    exercise_id: int,
    session: Session = Depends(get_session)
):
    exercise = session.get(Exercise, exercise_id)

    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found"
        )

    return exercise


@app.post("/muscle-group")
def muscle_group_create(
    muscle_group: MuscleGroupCreate,
    session: Session = Depends(get_session)
):
    db_muscle_group = MuscleGroup.model_validate(muscle_group)

    session.add(db_muscle_group)
    session.commit()
    session.refresh(db_muscle_group)

    return db_muscle_group


@app.get("/muscle-groups")
def muscle_groups_list(
    session: Session = Depends(get_session)
) -> List[MuscleGroup]:
    return session.exec(select(MuscleGroup)).all()


@app.get("/muscle-group/{muscle_group_id}")
def muscle_group_get(
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

@app.patch("/user/{user_id}")
def user_update(
    user_id: int,
    user: UserUpdate,
    session: Session = Depends(get_session)
):
    db_user = session.get(User, user_id)

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user_data = user.model_dump(exclude_unset=True)

    for key, value in user_data.items():
        setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@app.patch("/workout/{workout_id}")
def workout_update(
    workout_id: int,
    workout: WorkoutUpdate,
    session: Session = Depends(get_session)
):
    db_workout = session.get(Workout, workout_id)

    if not db_workout:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )

    workout_data = workout.model_dump(exclude_unset=True)

    for key, value in workout_data.items():
        setattr(db_workout, key, value)

    session.add(db_workout)
    session.commit()
    session.refresh(db_workout)

    return db_workout

@app.patch("/exercise/{exercise_id}")
def exercise_update(
    exercise_id: int,
    exercise: ExerciseUpdate,
    session: Session = Depends(get_session)
):
    db_exercise = session.get(Exercise, exercise_id)

    if not db_exercise:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found"
        )

    exercise_data = exercise.model_dump(exclude_unset=True)

    for key, value in exercise_data.items():
        setattr(db_exercise, key, value)

    session.add(db_exercise)
    session.commit()
    session.refresh(db_exercise)

    return db_exercise


@app.post("/exercise/{exercise_id}/muscle-group/{muscle_group_id}")
def add_muscle_group_to_exercise(
    exercise_id: int,
    muscle_group_id: int,
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

    existing_link = session.get(
        ExerciseMuscleGroupLink,
        (exercise_id, muscle_group_id)
    )

    if existing_link:
        raise HTTPException(
            status_code=400,
            detail="Muscle group is already linked to this exercise"
        )

    link = ExerciseMuscleGroupLink(
        exercise_id=exercise_id,
        muscle_group_id=muscle_group_id
    )

    session.add(link)
    session.commit()

    return {
        "message": "Muscle group added to exercise",
        "exercise_id": exercise_id,
        "muscle_group_id": muscle_group_id
    }


@app.delete("/user/{user_id}")
def user_delete(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()

    return {"message": "User deleted"}


@app.delete("/workout/{workout_id}")
def workout_delete(workout_id: int, session: Session = Depends(get_session)):
    workout = session.get(Workout, workout_id)

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    session.delete(workout)
    session.commit()

    return {"message": "Workout deleted"}


@app.delete("/exercise/{exercise_id}")
def exercise_delete(exercise_id: int, session: Session = Depends(get_session)):
    exercise = session.get(Exercise, exercise_id)

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    session.delete(exercise)
    session.commit()

    return {"message": "Exercise deleted"}


@app.delete("/muscle-group/{muscle_group_id}")
def muscle_group_delete(
    muscle_group_id: int,
    session: Session = Depends(get_session)
):
    muscle_group = session.get(MuscleGroup, muscle_group_id)

    if not muscle_group:
        raise HTTPException(status_code=404, detail="Muscle group not found")

    session.delete(muscle_group)
    session.commit()

    return {"message": "Muscle group deleted"}
