from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.schemas.schema_resultado import (
    ResultadoEstudianteTablaPaginadoResponse,
    ResultadoPaginadoResponse,
)

from app.schemas.schema_resultado_detalle import (
    ResultadoDetalleResponse,
    ResultadoExamenResponse,
)

from app.services.service_resultado import (
    obtener_resultados,
    obtener_resultados_estudiante,
    obtener_resultados_estudiantes_tabla,
    obtener_resultados_examen,
)

router = APIRouter(
    prefix="/resultados",
    tags=["Resultados"],
)


@router.get(
    "/",
    response_model=ResultadoPaginadoResponse,
)
def listar_resultados(
    page: int = 1,
    limit: int = 10,
    alumno: str = "",
    examen: str = "",
    fecha: str = "",
    db: Session = Depends(get_db),
):
    return obtener_resultados(
        db,
        page,
        limit,
        alumno,
        examen,
        fecha,
    )


@router.get(
    "/estudiante/{id_estudiante}",
    response_model=list[ResultadoDetalleResponse],
)
def listar_resultados_estudiante(
    id_estudiante: int,
    db: Session = Depends(get_db),
):
    return obtener_resultados_estudiante(
        db,
        id_estudiante,
    )


@router.get(
    "/estudiante/{id_estudiante}/tabla",
    response_model=ResultadoEstudianteTablaPaginadoResponse,
)
def listar_resultados_estudiante_tabla(
    id_estudiante: int,
    page: int = 1,
    limit: int = 10,
    examen: str = "",
    fecha: str = "",
    db: Session = Depends(get_db),
):
    return obtener_resultados_estudiantes_tabla(
        db,
        id_estudiante,
        page,
        limit,
        examen,
        fecha,
    )


@router.get(
    "/examen/{id_examen}",
    response_model=list[ResultadoExamenResponse],
)
def listar_resultados_examen(
    id_examen: int,
    db: Session = Depends(get_db),
):
    return obtener_resultados_examen(
        db,
        id_examen,
    )
