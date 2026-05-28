from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.resultado import Resultado
from app.models.estudiante import Estudiante
from app.models.usuario import Usuario
from app.models.examen import Examen


def obtener_todos_resultados_repository(
    db: Session,
    page: int,
    limit: int,
    alumno: str,
    examen: str,
    fecha: str,
):
    """
    Obtiene resultados paginados con filtros.
    """

    query = (
        db.query(
            Resultado.id_resultado,
            Resultado.calificacion,
            Resultado.fecha_evaluacion,
            Examen.nombre_examen.label("nombre_examen"),
            func.concat(
                Usuario.nombre,
                " ",
                Usuario.apellido_paterno,
                " ",
                Usuario.apellido_materno,
            ).label("nombre_alumno"),
        )
        .join(Estudiante, Estudiante.id_estudiante == Resultado.id_estudiante)
        .join(Usuario, Usuario.id_usuario == Estudiante.id_usuario)
        .join(Examen, Examen.id_examen == Resultado.id_examen)
    )

    if alumno:
        alumno = alumno.lower()
        query = query.filter(
            or_(
                func.lower(Usuario.nombre).like(f"{alumno}%"),
                func.lower(Usuario.apellido_paterno).like(f"{alumno}%"),
                func.lower(Usuario.apellido_materno).like(f"{alumno}%"),
            )
        )

    if examen:
        query = query.filter(Examen.nombre_examen.ilike(f"{examen}%"))

    if fecha:
        query = query.filter(func.date(Resultado.fecha_evaluacion) == fecha)

    total = query.count()

    resultados = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "data": resultados,
        "total": total,
    }


def obtener_resultados_estudiante_repository(
    db: Session,
    id_estudiante: int,
):
    """
    Obtiene los resultados
    de un estudiante.
    """

    return (
        db.query(
            Resultado.id_resultado.label("id_resultado"),
            Resultado.id_examen.label("id_examen"),
            Resultado.calificacion.label("calificacion"),
            Resultado.fecha_evaluacion.label("fecha_evaluacion"),
            Examen.nombre_examen.label("nombre_examen"),
            Estudiante.id_estudiante.label("id_estudiante"),
            Estudiante.matricula.label("matricula"),
            Usuario.nombre.label("nombre"),
            Usuario.apellido_paterno.label("apellido_paterno"),
            Usuario.apellido_materno.label("apellido_materno"),
        )
        .join(
            Examen,
            Resultado.id_examen == Examen.id_examen,
        )
        .join(
            Estudiante,
            Resultado.id_estudiante == Estudiante.id_estudiante,
        )
        .join(
            Usuario,
            Estudiante.id_usuario == Usuario.id_usuario,
        )
        .filter(
            Resultado.id_estudiante == id_estudiante,
        )
        .all()
    )


def obtener_resultados_estudiantes_tabla_repository(
    db: Session,
    id_estudiante: int,
    page: int,
    limit: int,
    examen: str,
    fecha: str,
):
    """
    Obtiene resultados paginados de un estudiante.
    """

    query = (
        db.query(
            Resultado.id_resultado,
            Resultado.calificacion,
            Resultado.fecha_evaluacion,
            Examen.nombre_examen.label("nombre_examen"),
        )
        .join(
            Examen,
            Examen.id_examen == Resultado.id_examen,
        )
        .filter(Resultado.id_estudiante == id_estudiante)
    )

    if examen:
        query = query.filter(Examen.nombre_examen.ilike(f"%{examen}%"))

    if fecha:
        query = query.filter(func.date(Resultado.fecha_evaluacion) == fecha)

    total = query.count()

    resultados = (
        query.order_by(Resultado.fecha_evaluacion.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "data": resultados,
        "total": total,
    }


def obtener_resultados_examen_repository(
    db: Session,
    id_examen: int,
):
    resultados = (
        db.query(
            Resultado.id_resultado,
            Usuario.nombre,
            Usuario.apellido_paterno,
            Usuario.apellido_materno,
            Estudiante.matricula,
            Resultado.calificacion,
            Resultado.fecha_evaluacion,
        )
        .join(
            Estudiante,
            Resultado.id_estudiante == Estudiante.id_estudiante,
        )
        .join(
            Usuario,
            Estudiante.id_usuario == Usuario.id_usuario,
        )
        .filter(Resultado.id_examen == id_examen)
        .all()
    )

    return [
        {
            "id_resultado": r.id_resultado,
            "nombre": r.nombre,
            "apellido_paterno": r.apellido_paterno,
            "apellido_materno": r.apellido_materno,
            "matricula": r.matricula,
            "calificacion": r.calificacion,
            "fecha_evaluacion": r.fecha_evaluacion,
        }
        for r in resultados
    ]


def crear_resultado(db, id_examen, id_estudiante):
    resultado = Resultado(
        id_examen=id_examen, id_estudiante=id_estudiante, calificacion=0
    )

    db.add(resultado)
    db.commit()
    db.refresh(resultado)

    return resultado
