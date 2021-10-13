import cv2
import sys
import os
import numpy as np

# para poder dar clic sobre las imagenes y que queden guardados los puntos
points = []

def click(event, x, y,flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x,y))


images = {}


if __name__ == '__main__':

    # Cargar ruta de carpeta
    #path = r'C:\Users\Laura\Desktop\Procesamiento imagenes\stitching'
    path = r'C:\Users\sngh9\OneDrive\Escritorio\Maestria_Semestre_2\Procesamiento_de_imagenes\Taller_5'
    files = os.listdir(path)
    files = [file for file in files if 'png' in file ]
    count = 0
    number = 1
    print(files)
    # Leer cada uno de las imagenes que se encuentrar en la carpeta para hacer stitching
    for file in files:
        image_path = path + "/" + file
        print(image_path)
        image = cv2.imread(image_path)
        images["image%s" % number] = image
        count += 1
        number +=1
        n = file

        #cv2.imshow(n, images["key%s" % number] )
        #cv2.waitKey()
    # print(images['image1'])
    # cv2.imshow('prueba',images['image1'])
    # cv2.waitKey()
    #print(len(images))
    # Mostrar la cantidad de imagenes de la carpeta al usuario
    print("En la carpeta se encuentran:", count, "imagenes")

    # preguntar al usuario cual imagen desea tomar de referencia
    print("de las:", count, "imagenes visualizadas ¿Cual desea usar de referencia?")
    print("digite el valor de N: ")
    N = int(input())

    # Verificar si el valor de N esta en la cantidad de imagenes en la carpeta
    print("La imagen seleccionada fue la Número:", N)

    if N > 0 and N <= count:
        print("Correcto")
    else:
        print("No existe la imagen", N)

    imagen_usuario = images["image%s" % N]
    cv2.imshow('prueba1', imagen_usuario )
    cv2.waitKey()

    image_concat = {}

    N_2 = 1
    for _ in range(len(images)-1):
        N_3 = N_2+1
        image_concat["imageconcat%s" % N_2]  = cv2.hconcat([images["image%s" % N_2],images["image%s" % N_3]])



        cv2.imshow('concat_horizontal', image_concat["imageconcat%s" % N_2])
        cv2.waitKey(0)
        N_2 += 1

    image_draw = np.copy(image)

    points1 = []
    points2 = []

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", click)

    point_counter = 0

    while True:
        cv2.imshow("Image", image_concat["imageconcat1"])
        key = cv2.waitKey(1) & 0xFF
        if key == ord("x"):
            points1 = points.copy()
            points = []
            break
        if len(points) > point_counter:
            point_counter = len(points)
            cv2.circle(image_concat["imageconcat1"], (points[-1][0], points[-1][1]), 3, [0, 0, 255], -1)

    point_counter = 0

    while True:
        cv2.imshow("Image", image_concat["imageconcat1"])
        key = cv2.waitKey(1) & 0xFF
        if key == ord("x"):
            points2 = points.copy()
            points = []
            break
        if len(points) > point_counter:
            point_counter = len(points)
            cv2.circle(image_concat["imageconcat1"], (points[-1][0], points[-1][1]), 3, [255, 0, 0], -1)

    N = min(len(points1), len(points2))
    assert N >= 4, 'At least four points are required'

    pts1 = np.array(points1[:N])
    pts2 = np.array(points2[:N])
    points1 = []
    points2 = []






    point_counter = 0

    while True:
        cv2.imshow("Image", image_concat["imageconcat2"])
        key = cv2.waitKey(1) & 0xFF
        if key == ord("x"):
            points1 = points.copy()
            points = []
            break
        if len(points) > point_counter:
            point_counter = len(points)
            cv2.circle(image_concat["imageconcat2"], (points[-1][0], points[-1][1]), 3, [0, 0, 255], -1)

    point_counter = 0

    while True:
        cv2.imshow("Image", image_concat["imageconcat2"])
        key = cv2.waitKey(1) & 0xFF
        if key == ord("x"):
            points2 = points.copy()
            points = []
            break
        if len(points) > point_counter:
            point_counter = len(points)
            cv2.circle(image_concat["imageconcat2"], (points[-1][0], points[-1][1]), 3, [255, 0, 0], -1)

    N = min(len(points1), len(points2))
    assert N >= 4, 'At least four points are required'

    pts3 = np.array(points1[:N])
    pts4 = np.array(points2[:N])

    H, _ = cv2.findHomography(pts1, pts2, method=cv2.RANSAC)
    H1, _ = cv2.findHomography(pts3, pts4, method=cv2.RANSAC)

    image = images['image1']
    image2 = images['image3']



    image_warped = cv2.warpPerspective(image, H, (image.shape[1], image.shape[0]))
    #image_gray = cv2.cvtColor(image_warped, cv2.COLOR_BGR2GRAY)
    #ret, Ibw_otsu = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #cv2.imshow("Image warped", Ibw_otsu )
    #cv2.waitKey(0)
    image_warped2= cv2.warpPerspective(imagen_usuario, H1, (imagen_usuario.shape[1], imagen_usuario.shape[0]))
    img_final =(np.sum([image_warped,imagen_usuario ,image_warped2],axis=0 ))/3
    img_final = np.uint8(img_final)

    cv2.imshow("Image warped", img_final )
    cv2.waitKey(0)






