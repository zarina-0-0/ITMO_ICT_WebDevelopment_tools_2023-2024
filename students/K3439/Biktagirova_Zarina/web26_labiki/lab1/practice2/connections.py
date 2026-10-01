from sqlmodel import SQLModel, Session, create_engine

from models import User, Workout, Exercise, MuscleGroup, ExerciseMuscleGroupLink


DATABASE_URL = "postgresql://a1111@localhost:5432/workout_db"

engine = create_engine(
    DATABASE_URL,
    echo=True
)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session