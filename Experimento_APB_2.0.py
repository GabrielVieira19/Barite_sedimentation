import cv2 as cv
import numpy as np
import os
import ffmpeg
import time

# Configurações da câmera
K = np.array([[7.90595549e+02, 0.00000000e+00, 1.09146315e+03],
              [0.00000000e+00, 7.93205446e+02, 5.09977322e+02],
              [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

dist = np.array([-0.2152493, 0.04892259, 0.00569835, -0.02602686, -0.00692194])

# Configurações da stream e amostragem da imagem
ip_camera = "143.106.170.196"
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;tcp'

rep_exp = len(os.listdir('Imagens_cap/')) - 1

Cv = 3
if rep_exp >= 5 and rep_exp < 9:
    rep_exp = len(os.listdir('Imagens_cap/')) - 5
    Cv = 6
elif rep_exp >= 9 and rep_exp < 13:
    rep_exp = len(os.listdir('Imagens_cap/')) - 9
    Cv = 9
elif rep_exp >= 13 and rep_exp < 17:
    rep_exp = len(os.listdir('Imagens_cap/')) - 13
    Cv = 12

num = len(os.listdir('Imagens_cap')) + 1

def ReadCamera(ip: str):
    endereco = f'rtsp://admin:cepetro1234@{ip}?tcp'
    frame_interval = 1
    frame_count = 0

    try:
        # Inicializa a captura de vídeo
        cap = cv.VideoCapture(endereco)
        if not cap.isOpened():
            print("Erro ao abrir a câmera.")
            return

        # Obtém as dimensões do frame da câmera
        frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        frame_size = frame_width * frame_height * 3  # Assumindo 3 canais (BGR)

        # Abre um processo para escrever o vídeo com ffmpeg
        out_process = (
            ffmpeg
            .input('pipe:', format='rawvideo', pix_fmt='bgr24', s=f'{frame_height}x{frame_width}', framerate=1/frame_interval)
            .output(f'Imagens_cap/Movie_Cv{Cv}_{rep_exp}.avi', codec='mpeg4', qscale=3.0, pix_fmt='yuv420p')
            .run_async(pipe_stdin=True)
        )

        last_cap_time = time.perf_counter()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar frame.")
                break

            frame = cv.undistort(frame, K, dist, None, K)
            
            frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)

            current_time = time.perf_counter()

            if (current_time - last_cap_time) >= frame_interval:
                out_process.stdin.write(frame.tobytes())
                last_cap_time = current_time

            if frame_count % 10 == 0:
                small_frame = cv.resize(frame, (720, 520))
                cv.imshow('Screen', small_frame)

            frame_count += 1

            if cv.waitKey(1) & 0xFF == 27:
                break
    
    finally:
        cap.release()
        cv.destroyAllWindows()
        out_process.stdin.close()
        out_process.wait()

if __name__ == "__main__":
    ReadCamera(ip_camera)
