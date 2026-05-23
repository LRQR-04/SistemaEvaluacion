from sqlalchemy.orm import Session
from app.models.estudiante import Estudiante


def crear_estudiante(db: Session, estudiante: Estudiante):
    db.add(estudiante)
