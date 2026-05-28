from pydantic import BaseModel
from typing import Optional, Literal


class PreguntaBase(BaseModel):
    pregunta: str

    opcion_a: str
    opcion_b: str
    opcion_c: str

    respuesta_correcta: Literal["a", "b", "c"]

    estatus: Literal["activa", "inactiva"] = "activa"


class PreguntaCreate(PreguntaBase):
    id_examen: int


class PreguntaUpdate(BaseModel):
    pregunta: Optional[str] = None

    opcion_a: Optional[str] = None
    opcion_b: Optional[str] = None
    opcion_c: Optional[str] = None

    respuesta_correcta: Optional[Literal["a", "b", "c"]] = None

    estatus: Optional[Literal["activa", "inactiva"]] = None


class PreguntaResponse(PreguntaBase):
    id_pregunta: int
    id_examen: int

    class Config:
        from_attributes = True
