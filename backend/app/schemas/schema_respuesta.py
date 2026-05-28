from pydantic import BaseModel


class RespuestaBase(BaseModel):
    """
    Esquema base de respuestas.
    """

    id_resultado: int
    id_pregunta: int
    respuesta_alumno: str
    es_correcta: bool = False


class RespuestaCreate(RespuestaBase):
    """
    Esquema para crear respuestas.
    """

    pass


class RespuestaResponse(RespuestaBase):
    """
    Respuesta básica.
    """

    id_respuesta: int

    class Config:
        from_attributes = True
