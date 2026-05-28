import cv2
import numpy as np
from fastapi import HTTPException

from app.omr import utils


def procesar_omr_imagen(
    file,
    preguntas_db,
):
    """
    Procesa una hoja OMR y devuelve respuestas detectadas.
    """

    try:
        # 1. LEER IMAGEN DESDE UPLOAD
        image_data = np.frombuffer(file.file.read(), np.uint8)
        img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Imagen inválida")

        # 2. CONFIG
        heightImg = 700
        widthImg = 700

        questions = len(preguntas_db)
        choices = 3  # A B C

        if questions <= 0:
            raise HTTPException(
                status_code=400,
                detail="El examen no contiene preguntas",
            )

        # 3. PREPROCESAMIENTO
        img = cv2.resize(img, (widthImg, heightImg))
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
        imgCanny = cv2.Canny(imgBlur, 10, 70)

        # 4. CONTORNOS
        contours, _ = cv2.findContours(
            imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        rectCon = utils.rectContour(contours)

        if len(rectCon) < 2:
            raise HTTPException(
                status_code=400, detail="No se detectó la hoja correctamente"
            )

        # 5. PERSPECTIVA (EXAMEN)
        biggestPoints = utils.getCornerPoints(rectCon[0])

        if biggestPoints.size == 0:
            raise HTTPException(
                status_code=400,
                detail="No se pudo detectar la perspectiva de la hoja",
            )

        biggestPoints = utils.reorder(biggestPoints)

        pts1 = np.float32(biggestPoints)
        pts2 = np.float32(
            [[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]]
        )

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarp = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

        # 6. THRESHOLD
        imgWarpGray = cv2.cvtColor(imgWarp, cv2.COLOR_BGR2GRAY)
        imgThresh = cv2.threshold(imgWarpGray, 150, 255, cv2.THRESH_BINARY_INV)[1]

        # 7. SPLIT DE CAJAS
        boxes = utils.splitBoxes(imgThresh, questions, choices)

        expected_boxes = questions * choices

        if len(boxes) != expected_boxes:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"La cantidad de preguntas detectadas no coincide "
                    f"con la hoja esperada. "
                    f"Esperadas: {questions}, "
                    f"Detectadas: {len(boxes) // choices}"
                ),
            )

        myPixelVal = np.zeros((questions, choices))

        countR = 0
        countC = 0

        for image in boxes:
            totalPixels = cv2.countNonZero(image)
            myPixelVal[countR][countC] = totalPixels

            countC += 1
            if countC == choices:
                countC = 0
                countR += 1

        # 8. DETECCIÓN DE RESPUESTAS
        myIndex = []

        threshold_mark = 10000

        for x in range(questions):
            arr = myPixelVal[x]
            print(f"Pregunta {x + 1}: {arr}")
            # Detectar opciones marcadas
            marcadas = []

            for i, valor in enumerate(arr):
                if valor > threshold_mark:
                    marcadas.append(i)

            # ---------------------------------------------
            # REGLAS:
            # 0 marcadas -> NULL
            # 1 marcada -> válida
            # >1 marcadas -> NULL
            # ---------------------------------------------

            if len(marcadas) == 0:
                myIndex.append(None)

            elif len(marcadas) > 1:
                myIndex.append(None)

            else:
                myIndex.append(marcadas[0])

        # 9. COMPARACIÓN CON BD
        correctas = 0
        respuestas_finales = []
        # map: 0=A, 1=B, 2=C
        opciones = ["a", "b", "c"]

        for i, pregunta in enumerate(preguntas_db):
            detectada = myIndex[i]

            respuesta_alumno = opciones[detectada] if detectada is not None else None
            es_correcta = respuesta_alumno == pregunta.respuesta_correcta

            if es_correcta:
                correctas += 1

            respuestas_finales.append(
                {
                    "id_pregunta": pregunta.id_pregunta,
                    "respuesta_alumno": respuesta_alumno,
                    "es_correcta": es_correcta,
                }
            )

        # 10. SCORE
        score = (correctas / questions) * 10 if questions > 0 else 0

        score = round(score, 1)

        return {
            "mensaje": "Evaluación procesada correctamente",
            "calificacion": score,
            "correctas": correctas,
            "total": questions,
            "respuestas": respuestas_finales,
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
