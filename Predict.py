import ultralytics
from ultralytics import YOLO
import torch
import os 
from IPython import display

display.clear_output()
ultralytics.checks()
torch.cuda.is_available()

# Verificamos se a GPU está disponível para uso (GPUs da Nvidia apenas)
print("CUDA available:", torch.cuda.is_available())
print("Number of GPUs:", torch.cuda.device_count())
if torch.cuda.is_available():
  print("Current GPU:", torch.cuda.get_device_name(0))

# Usamos o modelo que foi treinado, pegando os melhores resultados "best.pt"
model = YOLO ('runs/detect/yolo11nbatch5/train/weights/best.pt')
capturas = ['Capturas/Capturas_hikivision/' , 'Capturas/Capturas_camera/' ] # Lista das pastas que contêm os vídeos a serem analisados

# Rodamos o YOLO a fim de realizar a detcção em fotos ou vídeos 
for captura in capturas : 
  for video in os.listdir(captura) :   
      source_path = captura + video # Só passamos a pasta onde estão os vídeos ou cada vídeo da pasta 
      output_dir = 'runs/detect/predicts' 
      output_name = 'runs/detect/predicts/Predict_' + video[:-4] 
      results = model(source=source_path, stream=True, save=True, max_det=1, save_txt = True, project=output_dir, name=output_name)
      for result in results :
        result # Por algum motivo preciso desse for loop para que funcione