from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.resultado_repository import (
    obtener_resultados_estudiantes_tabla_repository,
    obtener_todos_resultados_repository,
    obtener_resultados_estudiante_repository,
    obtener_resultados_examen_repository,
)


def obtener_resultados(
    db: Session,
    page: int,
    limit: int,
    alumno: str,
    examen: str,
    fecha: str,
):
    """
    Obtiene resultados paginados.
    """

    return obtener_todos_resultados_repository(
        db,
        page,
        limit,
        alumno,
        examen,
        fecha,
    )


def obtener_resultados_estudiante(
    db: Session,
    id_estudiante: int,
):
    """
    Obtiene todos los resultados
    de un estudiante.
    """

    resultados = obtener_resultados_estudiante_repository(
        db,
        id_estudiante,
    )

    return resultados


def obtener_resultados_estudiantes_tabla(
    db: Session,
    id_estudiante: int,
    page: int,
    limit: int,
    examen: str,
    fecha: str,
):
    """
    Obtiene resultados paginados
    de un estudiante.
    """

    resultados = obtener_resultados_estudiantes_tabla_repository(
        db,
        id_estudiante,
        page,
        limit,
        examen,
        fecha,
    )

    return resultados


def obtener_resultados_examen(
    db: Session,
    id_examen: int,
):
    """
    Obtiene los resultados
    de un examen.
    """

    resultados = obtener_resultados_examen_repository(
        db,
        id_examen,
    )

    return resultados
