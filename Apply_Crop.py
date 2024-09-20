import cv2 as cv 
import numpy as np 
import os

# Definições para o recorte da área de interesse e rotação
angulação = 0.88
x = 832
y = 100
crop_width = 200  # Largura do recorte
crop_height = 920 # Altura do recorte

# Novo diretório e possível criação da pasta
output_dir = 'Imagens_cap/Capturas_Camera'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print("Pasta criada!")

# Função de aplicação da correção e rotação da imagem
def Apply_Crop(video): 
    cap = cv.VideoCapture('Capturas_Nikon/' + video)
    
    if not cap.isOpened(): 
        print("Problema em abrir o vídeo, cancelando operação!")
        return

    # Obtém as propriedades do vídeo original
    original_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    ponto_ref = (original_width/2, original_height/2)
    fps = cap.get(cv.CAP_PROP_FPS)
    total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

    print(f'Largura_original = {original_width} ; Altura_original = {original_height}')
    print(f'Total de quadros: {total_frames}')
    
    # Verifica se as dimensões de recorte são válidas
    if x + crop_width > original_width or y + crop_height > original_height:
        print("As dimensões do recorte excedem as dimensões do video.")
        return

    # Cria o objeto VideoWriter para salvar o vídeo processado
    out = cv.VideoWriter('Imagens_Cap/Capturas_Camera/Camera_CV3%_2.MOV_Recorte.avi', cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, (crop_width, crop_height))

    for frame_number in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break
        
        # Aplica o corte de acordo com a área requerida
        rotacao = cv.getRotationMatrix2D (ponto_ref, angulação, 0.85) # os parâmetros são: Ponto de referência, angulo de rotação e proporção usada. 
        frame = cv.warpAffine (frame, rotacao, (original_width, original_height))
        frame = frame[y:y+crop_height, x:x+crop_width]
        out.write(frame)

        # Calcula e imprime o progresso a cada 25%
        if frame_number % (total_frames // 4) == 0:
            percent_complete = (frame_number / total_frames) * 100
            print(f"{percent_complete:.0f}% do video processado")

    cap.release()
    out.release()
    cv.destroyAllWindows()
    print(f'Recorte executado, video salvo como" {video}_Recorte.avi" !!')

if __name__ == "__main__":
    video = "Camera_CV3%_2.MOV"
    Apply_Crop(video)
