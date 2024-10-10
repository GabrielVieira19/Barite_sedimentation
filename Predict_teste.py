from ultralytics import YOLO
import os 

# Usamos o modelo que foi treinado, pegando os melhores resultados "best.pt"
model = YOLO ('runs/detect/yolov8nbatch5/train2/weights/best.pt')

# Rodamos o YOLO a fim de realizar a detcção em fotos ou vídeos 
for video in os.listdir('Imagens_cap/Capturas_Hikivision') :   
    source_path = 'Imagens_cap/Capturas_Hikivision/' + video
    output_dir = 'runs/detect/predict2' 
    output_name = 'Predict_' + video[:-4]
    results = model(source=source_path, save=True, max_det=1, save_txt = True, project=output_dir, name=output_name)




