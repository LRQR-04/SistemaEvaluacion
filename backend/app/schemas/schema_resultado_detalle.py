from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ResultadoDetalleResponse(BaseModel):
    id_resultado: int
    id_estudiante: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    matricula: str
    calificacion: float
    fecha_evaluacion: datetime
    id_examen: int
    nombre_examen: str

    class Config:
        from_attributes = True


class ResultadoExamenResponse(BaseModel):
    id_resultado: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str | None
    matricula: str
    calificacion: float
    fecha_evaluacion: datetime

    model_config = ConfigDict(from_attributes=True)
