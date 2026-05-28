from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.respuesta_repository import (
    obtener_respuestas_resultado_repository,
)


def obtener_respuestas_resultado(
    db: Session,
    id_resultado: int,
):
    """
    Obtiene las respuestas
    de un resultado específico.
    """

    respuestas = obtener_respuestas_resultado_repository(
        db,
        id_resultado,
    )

    if not respuestas:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron respuestas",
        )

    return respuestas
