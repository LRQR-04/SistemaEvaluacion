from typing import Optional
from pydantic import BaseModel


class RespuestaDetalleResponse(BaseModel):
    id_respuesta: int
    pregunta: str
    respuesta_alumno: Optional[str] = None
    respuesta_correcta: str
    es_correcta: bool

    class Config:
        from_attributes = True
