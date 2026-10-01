from fastapi import FastAPI
from models import temp_bd, users_bd, Workout, User
from typing_extensions import TypedDict


app = FastAPI()


@app.get("/workouts")
def workouts_list() -> list[Workout]:
    return temp_bd


@app.get("/users")
def users_list() -> list[User]:
    return users_bd


@app.get("/workout/{workout_id}")
def workout_list(workout_id: int) -> list[Workout]:
    return [workout for workout in temp_bd if workout.get("id") == workout_id]


@app.get("/user/{user_id}")
def users_get(user_id: int) -> list[User]:
    return [user for user in users_bd if user.get("id") == user_id]


@app.post("/workout")
def workout_add(workout: Workout) -> TypedDict('Response', {"status": int, "data": Workout}):
    temp_bd.append(workout.model_dump())
    return {"status": 200, "data": workout}


@app.post("/user")
def user_add(user: User) -> TypedDict('Response', {"status": int, "data": User}):
    users_bd.append(user.model_dump())
    return {"status": 200, "data": user}


@app.delete("/workout/delete/{workout_id}")
def workout_delete(workout_id: int):
    for i, workout in enumerate(temp_bd):
        if workout.get("id") == workout_id:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}


@app.put("/workout/{workout_id}")
def workout_update(workout_id: int, workout: Workout) -> list[Workout]:
    for i, work in enumerate(temp_bd):
        if work.get("id") == workout_id:
            temp_bd[i] = workout.model_dump()
    return temp_bd
