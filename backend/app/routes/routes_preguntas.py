from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.schema_pregunta import PreguntaCreate, PreguntaResponse, PreguntaUpdate
from app.services.service_pregunta import (
    registrar_pregunta,
    listar_preguntas_examen,
    actualizar_pregunta,
)
from app.middleware.middleware_autenticacion import obtener_usuario_actual

router = APIRouter(prefix="/preguntas", tags=["Preguntas"])


@router.get("/examen/{id_examen}", response_model=list[PreguntaResponse])
def listar(id_examen: int, db: Session = Depends(get_db)):
    return listar_preguntas_examen(db, id_examen)


@router.post("/", response_model=PreguntaResponse)
def crear(
    data: PreguntaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(obtener_usuario_actual),
):
    return registrar_pregunta(db, data, current_user)


@router.put("/{id_pregunta}", response_model=PreguntaResponse)
def actualizar(
    id_pregunta: int,
    data: PreguntaUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(obtener_usuario_actual),
):
    return actualizar_pregunta(db, id_pregunta, data, current_user)
