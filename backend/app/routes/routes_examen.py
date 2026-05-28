from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.middleware.middleware_autenticacion import obtener_usuario_actual

from app.models.usuario import Usuario

from app.schemas.schema_examen import (
    ExamenCreate,
    ExamenUpdate,
    ExamenResponse,
)

from app.services.service_examen import (
    registrar_examen,
    obtener_examenes,
    actualizar_examen,
)

from app.repositories.examen_repository import (
    obtener_examenes_docente,
    obtener_examenes_activos_docente,
)

router = APIRouter(
    prefix="/examenes",
    tags=["Exámenes"],
)


@router.get("/")
def listar_examenes(
    nombre_examen: str = Query(""),
    fecha_aplicacion: str = Query(None),
    estatus: str = Query(""),
    page: int = Query(1),
    limit: int = Query(10),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(obtener_usuario_actual),
):
    return obtener_examenes(
        db=db,
        current_user=current_user,
        nombre_examen=nombre_examen,
        docente="",
        fecha_aplicacion=fecha_aplicacion,
        estatus=estatus,
        page=page,
        limit=limit,
    )


@router.get("/docente/{id_docente}", response_model=list[ExamenResponse])
def listar_examenes_docente(
    id_docente: int,
    db: Session = Depends(get_db),
):
    return obtener_examenes_docente(
        db,
        id_docente,
    )


@router.get("/docente/{id_docente}/activos", response_model=list[ExamenResponse])
def listar_examenes_activos_docente(
    id_docente: int,
    db: Session = Depends(get_db),
):
    return obtener_examenes_activos_docente(
        db,
        id_docente,
    )


@router.post("/", response_model=ExamenResponse)
def crear_examen_route(
    data: ExamenCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(obtener_usuario_actual),
):
    return registrar_examen(db, data, current_user)


@router.put("/{examen_id}", response_model=ExamenResponse)
def editar_examen_route(
    examen_id: int,
    data: ExamenUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(obtener_usuario_actual),
):
    return actualizar_examen(db, examen_id, data, current_user)
