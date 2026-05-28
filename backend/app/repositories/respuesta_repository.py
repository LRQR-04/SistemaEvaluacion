from sqlalchemy.orm import Session

from app.models.respuesta import Respuesta
from app.models.pregunta import Pregunta


def obtener_respuestas_resultado_repository(
    db: Session,
    id_resultado: int,
):
    """
    Obtiene todas las respuestas
    de un resultado específico.
    """

    respuestas = (
        db.query(
            Respuesta.id_respuesta,
            Pregunta.pregunta,
            Respuesta.respuesta_alumno,
            Pregunta.respuesta_correcta,
            Respuesta.es_correcta,
        )
        .join(
            Pregunta,
            Respuesta.id_pregunta == Pregunta.id_pregunta,
        )
        .filter(Respuesta.id_resultado == id_resultado)
        .all()
    )

    return [
        {
            "id_respuesta": r.id_respuesta,
            "pregunta": r.pregunta,
            "respuesta_alumno": r.respuesta_alumno,
            "respuesta_correcta": r.respuesta_correcta,
            "es_correcta": r.es_correcta,
        }
        for r in respuestas
    ]


def guardar_respuesta(db, id_resultado, id_pregunta, respuesta, correcta):
    res = Respuesta(
        id_resultado=id_resultado,
        id_pregunta=id_pregunta,
        respuesta_alumno=respuesta,
        es_correcta=correcta,
    )

    db.add(res)
