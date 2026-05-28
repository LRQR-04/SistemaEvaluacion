import cv2
import numpy as np


def stackImages(imgArray, scale):
    rows = len(imgArray)

    for x in range(rows):
        for y in range(len(imgArray[x])):
            imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)

            if len(imgArray[x][y].shape) == 2:
                imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)

    hor = [np.hstack(row) for row in imgArray]
    ver = np.vstack(hor)

    return ver


def reorder(points):
    points = points.reshape((4, 2))
    newPoints = np.zeros((4, 1, 2), np.int32)

    add = points.sum(1)
    diff = np.diff(points, axis=1)

    # TOP LEFT
    newPoints[0] = points[np.argmin(add)]

    # TOP RIGHT
    newPoints[1] = points[np.argmin(diff)]

    # BOTTOM LEFT
    newPoints[2] = points[np.argmax(diff)]

    # BOTTOM RIGHT
    newPoints[3] = points[np.argmax(add)]

    return newPoints


def rectContour(contours):
    rectCon = []

    for c in contours:
        area = cv2.contourArea(c)

        if area > 2000:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            if len(approx) == 4:
                rectCon.append(c)

    rectCon = sorted(rectCon, key=cv2.contourArea, reverse=True)

    return rectCon


def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True)
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True)
    return approx


def splitBoxes(img, rows, cols):
    h = img.shape[0] // rows
    w = img.shape[1] // cols

    boxes = []

    for r in range(rows):
        for c in range(cols):

            y1 = r * h
            y2 = (r + 1) * h

            x1 = c * w
            x2 = (c + 1) * w

            box = img[y1:y2, x1:x2]

            # Validar tamaño correcto
            if box.size == 0:
                continue

            boxes.append(box)

    return boxes


def showAnswers(img, myIndex, grading, ans, questions, choices):
    secW = img.shape[1] // choices
    secH = img.shape[0] // questions

    for x in range(questions):
        myAns = myIndex[x]

        if myAns is None:
            continue

        cX = (myAns * secW) + secW // 2
        cY = (x * secH) + secH // 2

        if grading[x] == 1:
            color = (0, 255, 0)
            cv2.circle(img, (cX, cY), 35, color, cv2.FILLED)
        else:
            color = (0, 0, 255)
            cv2.circle(img, (cX, cY), 35, color, cv2.FILLED)

            correct = ans[x]
            cx = (correct * secW) + secW // 2
            cy = cY

            cv2.circle(img, (cx, cy), 20, (0, 255, 0), cv2.FILLED)


def drawGrid(img, questions, choices):
    h = img.shape[0]
    w = img.shape[1]

    secW = w // choices
    secH = h // questions

    for i in range(questions + 1):
        cv2.line(img, (0, secH * i), (w, secH * i), (255, 255, 0), 1)

    for i in range(choices + 1):
        cv2.line(img, (secW * i, 0), (secW * i, h), (255, 255, 0), 1)

    return img
