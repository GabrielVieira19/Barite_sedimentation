import cv2 as cv 
import numpy as np
import os

def Extract_Random_frames (video, qtd_frames, vol_cv) : 
    try : 
        os.makedirs(f"Imagens_cap/Frames_Extraidos/Frames_{vol_cv}")
    except : 
        print(f"Pasta dos frames já existe para o Movie_{vol_cv}.avi")
    
    # Abir e setar os parâmetros necessários 
    cap = cv.VideoCapture(video)
    total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    frame_number = 0 
    random_frames = np.random.choice(total_frames, size = qtd_frames, replace = False) # Seleciona X frames aleatórios, dentro do intervalo dos frames totais e sendo X a quantidade requerida de frames
    
    for frame_number in sorted(random_frames) : # Repete X vezes a obtenção do frame aleatório 
        
        cap.set(cv.CAP_PROP_POS_FRAMES, frame_number)  # Posicionar o vídeo no frame aleatório
        ret, frame = cap.read()
        
        if ret:
            img_name = f"Imagens_cap/Frames_Extraidos/Frames_{vol_cv}/{vol_cv}_Frame_{frame_number}.png"
            print(f"Extraindo frame {frame_number}...")
            cv.imwrite(img_name, frame)

    cap.release()
            
if __name__ == "__main__":
    video = "Imagens_cap/Capturas_Hikivision/Movie_Cv3_3.avi"
    qtd_frames = 100
    vol_cv = "Cv3_3" 
    Extract_Random_frames(video, qtd_frames, vol_cv)
