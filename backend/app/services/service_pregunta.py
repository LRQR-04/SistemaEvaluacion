from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.pregunta import Pregunta
from app.models.examen import Examen
from app.models.docente import Docente
from app.models.usuario import Usuario

from app.schemas.schema_pregunta import (
    PreguntaCreate,
    PreguntaUpdate,
)

from app.repositories.pregunta_repository import (
    crear_pregunta,
    obtener_preguntas_por_examen,
)


def registrar_pregunta(
    db: Session,
    data: PreguntaCreate,
    current_user: Usuario,
):
    try:
        examen = db.query(Examen).filter(Examen.id_examen == data.id_examen).first()

        if not examen:
            raise HTTPException(
                status_code=404,
                detail="Examen no encontrado",
            )

        if examen.estatus == "inactivo":
            raise HTTPException(
                status_code=400,
                detail="El examen está inactivo",
            )

        docente = (
            db.query(Docente)
            .filter(Docente.id_usuario == current_user.id_usuario)
            .first()
        )

        if not docente:
            raise HTTPException(
                status_code=403,
                detail="El usuario no es docente",
            )

        if examen.id_docente != docente.id_docente:
            raise HTTPException(
                status_code=403,
                detail="No puedes modificar este examen",
            )

        nueva_pregunta = Pregunta(
            id_examen=data.id_examen,
            pregunta=data.pregunta,
            opcion_a=data.opcion_a,
            opcion_b=data.opcion_b,
            opcion_c=data.opcion_c,
            respuesta_correcta=data.respuesta_correcta,
            estatus=data.estatus,
        )

        # Guardar pregunta
        pregunta = crear_pregunta(db, nueva_pregunta)

        # sincroniza INSERT sin commit
        db.flush()

        # actualizar total reactivos
        examen.total_reactivos = (
            db.query(Pregunta)
            .filter(
                Pregunta.id_examen == examen.id_examen,
                Pregunta.estatus == "activa",
            )
            .count()
        )

        db.commit()
        db.refresh(pregunta)

        return pregunta

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Error al registrar pregunta",
        )


def listar_preguntas_examen(db: Session, id_examen: int):
    try:
        return obtener_preguntas_por_examen(db, id_examen)

    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener preguntas")


def actualizar_pregunta(
    db: Session,
    id_pregunta: int,
    data: PreguntaUpdate,
    current_user: Usuario,
):
    try:
        pregunta = (
            db.query(Pregunta).filter(Pregunta.id_pregunta == id_pregunta).first()
        )

        if not pregunta:
            raise HTTPException(
                status_code=404,
                detail="Pregunta no encontrada",
            )

        examen = db.query(Examen).filter(Examen.id_examen == pregunta.id_examen).first()

        docente = (
            db.query(Docente)
            .filter(Docente.id_usuario == current_user.id_usuario)
            .first()
        )

        if not docente:
            raise HTTPException(
                status_code=403,
                detail="No eres docente",
            )

        if examen.id_docente != docente.id_docente:
            raise HTTPException(
                status_code=403,
                detail="No puedes modificar esta pregunta",
            )

        pregunta.pregunta = data.pregunta
        pregunta.opcion_a = data.opcion_a
        pregunta.opcion_b = data.opcion_b
        pregunta.opcion_c = data.opcion_c
        pregunta.respuesta_correcta = data.respuesta_correcta
        pregunta.estatus = data.estatus

        # sincronizar cambios pendientes
        db.flush()

        # actualizar total reactivos
        examen.total_reactivos = (
            db.query(Pregunta)
            .filter(
                Pregunta.id_examen == examen.id_examen,
                Pregunta.estatus == "activa",
            )
            .count()
        )

        db.commit()
        db.refresh(pregunta)

        return pregunta

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error al actualizar pregunta",
        )
