from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.schema_evaluacion import EvaluacionOMRResponse
from app.omr.omr_service import procesar_omr_imagen
from app.repositories.pregunta_repository import obtener_preguntas_activas
from app.repositories.resultado_repository import crear_resultado
from app.repositories.respuesta_repository import guardar_respuesta

router = APIRouter(prefix="/evaluacion", tags=["Evaluación"])


@router.post("/omr", response_model=EvaluacionOMRResponse)
def evaluar_omr(
    id_examen: int = Form(...),
    id_estudiante: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    preguntas = obtener_preguntas_activas(db, id_examen)
    resultado = crear_resultado(db, id_examen, id_estudiante)
    data = procesar_omr_imagen(file, preguntas)

    for r in data["respuestas"]:
        guardar_respuesta(
            db,
            resultado.id_resultado,
            r["id_pregunta"],
            r["respuesta_alumno"],
            r["es_correcta"],
        )

    resultado.calificacion = data["calificacion"]
    db.commit()

    return data
