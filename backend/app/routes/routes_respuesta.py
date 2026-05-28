from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.schemas.schema_respuesta_detalle import (
    RespuestaDetalleResponse,
)

from app.services.service_respuesta import (
    obtener_respuestas_resultado,
)

router = APIRouter(
    prefix="/respuestas",
    tags=["Respuestas"],
)


@router.get(
    "/resultado/{id_resultado}",
    response_model=list[RespuestaDetalleResponse],
)
def listar_respuestas_resultado(
    id_resultado: int,
    db: Session = Depends(get_db),
):

    return obtener_respuestas_resultado(
        db,
        id_resultado,
    )
