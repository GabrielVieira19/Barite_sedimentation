from ultralytics import YOLO
import os 

# Usamos o modelo que foi treinado, pegando os melhores resultados "best.pt"
model = YOLO ('runs/detect/yolov8nbatch5/train/weights/best.pt')

# Rodamos o YOLO a fim de realizar a detcção em fotos ou vídeos 
source_path = "Imagens_cap\Capturas_Camera\Camera_CV6%_1_Recorte.avi" 
results = model(source=source_path, save=True, max_det=1, save_txt = True)




