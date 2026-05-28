from pydantic import BaseModel
from datetime import datetime


class ResultadoBase(BaseModel):
    """
    Esquema base de resultados.
    """

    id_estudiante: int
    id_examen: int
    calificacion: float = 0


class ResultadoCreate(ResultadoBase):
    """
    Esquema para crear resultados.
    """

    pass


class ResultadoResponse(BaseModel):
    id_resultado: int
    nombre_alumno: str
    nombre_examen: str
    calificacion: float
    fecha_evaluacion: datetime

    class Config:
        from_attributes = True


class ResultadoPaginadoResponse(BaseModel):
    data: list[ResultadoResponse]
    total: int


class ResultadoEstudianteTablaResponse(BaseModel):
    id_resultado: int
    nombre_examen: str
    calificacion: float
    fecha_evaluacion: datetime

    class Config:
        from_attributes = True


class ResultadoEstudianteTablaPaginadoResponse(BaseModel):
    data: list[ResultadoEstudianteTablaResponse]
    total: int
