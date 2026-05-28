from app.repositories.resultado_repository import crear_resultado
from app.repositories.respuesta_repository import guardar_respuesta
from app.repositories.pregunta_repository import obtener_preguntas_activas


def procesar_evaluacion_omr(db, id_examen, id_estudiante, file):
    """
    Aquí SOLO estructura base.
    Procesamiento de imagen lo agregamos después.
    """

    preguntas = obtener_preguntas_activas(db, id_examen)
    resultado = crear_resultado(db, id_examen, id_estudiante)
    correctas = 0
    total = len(preguntas)

    # -----------------------------
    # PLACEHOLDER OMR (después OpenCV)
    # -----------------------------
    respuestas_detectadas = {}

    # ejemplo temporal
    for i, p in enumerate(preguntas):
        respuestas_detectadas[p.id_pregunta] = "A"

    for p in preguntas:

        respuesta = respuestas_detectadas.get(p.id_pregunta)

        es_correcta = respuesta == p.respuesta_correcta

        if es_correcta:
            correctas += 1

        guardar_respuesta(
            db, resultado.id_resultado, p.id_pregunta, respuesta, es_correcta
        )

    resultado.calificacion = (correctas / total) * 100 if total > 0 else 0

    db.commit()

    return {
        "mensaje": "Evaluación procesada",
        "calificacion": resultado.calificacion,
        "correctas": correctas,
        "total": total,
    }
