import cv2

# Carregar o vídeo
video_name = 'Movie_Cv12_4.avi'
video = cv2.VideoCapture('Imagens_cap/' + video_name)

# Verificar se o vídeo foi carregado corretamente
if not video.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()

# Definir o frame inicial e final para o recorte (lembrando que começa em 0)
frame_inicial = 0  # Exemplo: a partir do frame 0
frame_final = 1200 # Exemplo: até o frame X requerido 

# Obter o frame rate do vídeo
fps = video.get(cv2.CAP_PROP_FPS)

# Obter largura e altura do vídeo
largura = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
altura = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Definir o codec e criar o arquivo de saída
quatrocc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para salvar em .mp4
saida = cv2.VideoWriter(video_name, quatrocc, fps, (largura, altura))

# Iterar sobre os frames do vídeo
frame_atual = 0
while True:
    ret, frame = video.read()

    if not ret or frame_atual > frame_final:
        break

    if frame_atual >= frame_inicial:
        # Escrever o frame no vídeo de saída
        saida.write(frame)

    frame_atual += 1

# Liberar os recursos
video.release()
saida.release()
cv2.destroyAllWindows()

print("Trecho do vídeo foi salvo com sucesso!")