from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.examen import Examen
from app.models.pregunta import Pregunta


def crear_examen(db: Session, examen: Examen) -> Examen:
    db.add(examen)
    db.flush()

    return examen


def obtener_examenes_docente(
    db: Session,
    id_docente: int,
):
    """
    Obtiene los exámenes
    asociados a un docente.
    """

    return db.query(Examen).filter(Examen.id_docente == id_docente).all()


def obtener_examenes_activos_docente(
    db: Session,
    id_docente: int,
):

    examenes = (
        db.query(Examen)
        .join(Pregunta, Pregunta.id_examen == Examen.id_examen)
        .filter(
            Examen.id_docente == id_docente,
            Examen.estatus == "activo",
            Pregunta.estatus == "activa",
        )
        .group_by(Examen.id_examen)
        .having(func.count(Pregunta.id_pregunta) >= 3)
        .all()
    )

    return examenes


def guardar_examen(db: Session, examen: Examen) -> Examen:
    db.commit()
    db.refresh(examen)

    return examen
