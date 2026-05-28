from sqlalchemy.orm import Session
from app.models.pregunta import Pregunta


def crear_pregunta(db: Session, pregunta: Pregunta) -> Pregunta:
    db.add(pregunta)
    return pregunta


def obtener_preguntas_por_examen(db: Session, id_examen: int):
    return db.query(Pregunta).filter(Pregunta.id_examen == id_examen).all()


def actualizar_pregunta(db: Session, pregunta: Pregunta):
    db.merge(pregunta)
    return pregunta


def obtener_preguntas_activas(db, id_examen: int):
    return (
        db.query(Pregunta)
        .filter(Pregunta.id_examen == id_examen, Pregunta.estatus == "activa")
        .all()
    )
