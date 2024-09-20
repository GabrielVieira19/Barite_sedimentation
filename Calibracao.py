import cv2 as cv
import numpy as np
import os
# Parâmetros do tabuleiro de xadrez
chessboard_size = (9, 6)  # Número de cantos internos no tabuleiro (largura x altura)

# Preparar pontos do objeto 3D
objp = np.zeros((np.prod(chessboard_size), 3), dtype=np.float32)
objp[:, :2] = np.indices(chessboard_size).T.reshape(-1, 2)

# Listas para armazenar pontos do objeto 3D e pontos da imagem 2D
object_points = []
image_points = []
list_of_image_files = os.listdir('Imagens_calibra')

# Carregar e processar cada imagem
for image_file in list_of_image_files:
    image = cv.imread('Imagens_calibra/' + image_file)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # Detectar cantos do tabuleiro de xadrez
    ret, corners = cv.findChessboardCorners(gray, chessboard_size, None)
    # Se os cantos forem encontrados, adicione os pontos do objeto e da imagem
    if ret:
        object_points.append(objp)
        image_points.append(corners)
        # Desenhar e exibir os cantos
        cv.drawChessboardCorners(image, chessboard_size, corners, ret)
        cv.imshow('img', image)
        cv.waitKey(500)
cv.destroyAllWindows()

# Calibrar a câmera
ret, K, dist, rvecs, tvecs = cv.calibrateCamera(
    object_points, image_points, gray.shape[::-1], None, None
)
print("Matriz de calibração K:\n", K)
print("Distorção:", dist.ravel())

# Carregar uma imagem de teste
test_image = cv.imread('./Imagens_calibra/img1.png')
# Corrigir a distorção da imagem
undistorted_image = cv.undistort(test_image, K, dist, None, K)
# Exibir a imagem original e a imagem corrigida lado a lado
combined_image = np.hstack((test_image, undistorted_image))
cv.imshow('Original vs Undistorted', combined_image)
cv.waitKey(0)
cv.destroyAllWindows()