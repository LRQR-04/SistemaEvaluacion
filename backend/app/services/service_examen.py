from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta
from sqlalchemy import func

from app.models.examen import Examen
from app.models.docente import Docente
from app.models.usuario import Usuario

from app.schemas.schema_examen import (
    ExamenCreate,
    ExamenUpdate,
)

from app.repositories.examen_repository import (
    crear_examen,
)


def registrar_examen(
    db: Session,
    data: ExamenCreate,
    current_user: Usuario,
):

    try:
        if current_user.rol != "docente":
            raise HTTPException(
                status_code=403,
                detail="Solo docentes pueden crear exámenes",
            )

        docente = (
            db.query(Docente)
            .filter(Docente.id_usuario == current_user.id_usuario)
            .first()
        )

        if not docente:
            raise HTTPException(
                status_code=404,
                detail="Docente no encontrado",
            )

        nuevo_examen = Examen(
            id_docente=docente.id_docente,
            nombre_examen=data.nombre_examen,
            fecha_aplicacion=data.fecha_aplicacion,
            total_reactivos=0,
            estatus=data.estatus,
        )

        examen = crear_examen(db, nuevo_examen)

        db.commit()
        db.refresh(examen)

        return examen

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Error al registrar examen",
        )


def obtener_examenes(
    db: Session,
    current_user: Usuario,
    nombre_examen: str = "",
    docente: str = "",
    fecha_aplicacion=None,
    estatus: str = "",
    page: int = 1,
    limit: int = 10,
):

    try:
        query = db.query(Examen).options(
            joinedload(Examen.docente).joinedload(Docente.usuario)
        )

        if current_user.rol == "docente":
            docente_actual = (
                db.query(Docente)
                .filter(Docente.id_usuario == current_user.id_usuario)
                .first()
            )

            query = query.filter(Examen.id_docente == docente_actual.id_docente)

        # FILTROS
        if nombre_examen:
            query = query.filter(
                func.lower(Examen.nombre_examen).like(f"{nombre_examen.lower()}%")
            )

        if fecha_aplicacion:
            try:
                fecha = datetime.strptime(fecha_aplicacion, "%Y-%m-%d")

                inicio = datetime(fecha.year, fecha.month, fecha.day)
                fin = inicio + timedelta(days=1)

                query = query.filter(
                    Examen.fecha_aplicacion >= inicio,
                    Examen.fecha_aplicacion < fin,
                )

            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Formato de fecha inválido (YYYY-MM-DD)",
                )

        if estatus:
            query = query.filter(Examen.estatus == estatus)

        total = query.count()

        examenes = (
            query.order_by(Examen.id_examen.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "data": examenes,
            "total": total,
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al obtener exámenes",
        )


def actualizar_examen(
    db: Session,
    examen_id: int,
    data: ExamenUpdate,
    current_user: Usuario,
):
    try:
        examen = db.query(Examen).filter(Examen.id_examen == examen_id).first()

        if not examen:
            raise HTTPException(
                status_code=404,
                detail="Examen no encontrado",
            )

        docente = (
            db.query(Docente)
            .filter(Docente.id_usuario == current_user.id_usuario)
            .first()
        )

        if examen.id_docente != docente.id_docente:
            raise HTTPException(
                status_code=403,
                detail="No puedes editar este examen",
            )

        if data.nombre_examen:
            examen.nombre_examen = data.nombre_examen

        if data.fecha_aplicacion:
            examen.fecha_aplicacion = data.fecha_aplicacion

        if data.estatus is not None:
            examen.estatus = data.estatus

        db.commit()
        db.refresh(examen)

        return examen

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Error al actualizar examen",
        )
