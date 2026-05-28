from typing import List, Optional

from fastapi import UploadFile
from pydantic import BaseModel


class EvaluacionOMRRequest(BaseModel):
    id_examen: int
    id_estudiante: int


class RespuestaOMR(BaseModel):
    id_pregunta: int
    respuesta_alumno: Optional[str]
    es_correcta: bool


class EvaluacionOMRResponse(BaseModel):
    mensaje: str
    calificacion: float
    correctas: int
    total: int
    respuestas: List[RespuestaOMR]
