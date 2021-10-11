import cv2
import sys
import os
import numpy as np

# para poder dar clic sobre las imagenes y que queden guardados los puntos
points = []
def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))

if __name__ == '__main__':

    # Cargar ruta de carpeta
    path = r'C:\Users\Laura\Desktop\Procesamiento imagenes\stitching'
    files = os.listdir(path)
    count = 0
    # Leer cada uno de las imagenes que se encuentrar en la carpeta para acer stitching
    for file in files:
        image_path = path + "/" + file
        image = cv2.imread(image_path)
        count += 1
        n = file
        cv2.imshow(n, image)
        cv2.waitKey()

    # Mostrar la cantidad de imagenes de la carpeta al usuario
    print("En la carpeta se encuentran:", count, "imagenes")

    # preguntar al usuario cual imagen desea tomar de referencia
    print("de las:", count, "imagenes visualizadas ¿Cual desea usar de referencia?")
    print("digite el valor de N:")
    N = int(input())

    # Verificar si el valor de N esta en la cantidad de imagenes en la carpeta
    print("La imagen seleccionada fue la Número:", N)

    if N > 0 and N <= count:
        print("Correcto")
    else:
        print("No existe la imagen", N)

    # Concatenar las imagenes por pares
    cont = 0
    for file in files:
        image_path = path + "/" + file
        image = cv2.imread(image_path)
        cont = cont + 1
        print(cont)

        if cont == 1:
            image1 = cv2.imread(image_path)
        if cont == 2:
            image2 = cv2.imread(image_path)

    # mostrar las 2 imagenes una al lado de otra en la pantalla
    concat = cv2.hconcat([image1, image2])
    cv2.imshow('concat_horizontal', concat)
    cv2.waitKey(0)

    image =concat
    image_draw = np.copy(image)

    points1 = []
    points2 = []

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", click)

    point_counter = 0
    while True:
        cv2.imshow("Image", image_draw)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("x"):
            points1 = points.copy()
            points = []
            break
        if len(points) > point_counter:
            point_counter = len(points)
            cv2.circle(image_draw, (points[-1][0], points[-1][1]), 3, [0, 0, 255], -1)

    point_counter = 0
    while True:
        cv2.imshow("Image", image_draw)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("x"):
            points2 = points.copy()
            points = []
            break
        if len(points) > point_counter:
            point_counter = len(points)
            cv2.circle(image_draw, (points[-1][0], points[-1][1]), 3, [255, 0, 0], -1)

    N = min(len(points1), len(points2))
    assert N >= 4, 'At least four points are required'

    pts1 = np.array(points1[:N])
    pts2 = np.array(points2[:N])
    if False:
        H, _ = cv2.findHomography(pts1, pts2, method=0)
    else:
        H, _ = cv2.findHomography(pts1, pts2, method=cv2.RANSAC)

    image_warped = cv2.warpPerspective(image, H, (image.shape[1], image.shape[0]))
    cv2.imshow("Image", image)
    cv2.imshow("Image warped", image_warped)
    cv2.waitKey(0)




