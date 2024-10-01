import ultralytics 
from ultralytics import YOLO
import torch
import os
from multiprocessing import cpu_count
from IPython import display


if __name__ == '__main__':

    path = os.getcwd().replace("\\", "/")
    

    yolo_names = ['yolov8n.pt']

    batch = 5

    for idx, yolo_name in enumerate(yolo_names):
        os.environ['KMP_DUPLICATE_LIB_OK']='True'
        display.clear_output()
        ultralytics.checks()
        torch.cuda.is_available()
        
        # Verificamos se a GPU está disponível para uso (GPUs da Nvidia apenas)
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {device}")
        
        # Load a model
        model = YOLO(yolo_name)  # load a pretrained model (recommended for training)
        
        # Train the model
        epoch = 100
        history = model.train(data = '3_config.yaml', epochs = epoch, batch = batch, workers = cpu_count(), patience = 25,
                    optimizer = 'auto', seed = 1, lr0 = 0.005, save = True, verbose = True, dropout = 0, save_period = 0,
                    project = path + '/runs/detect/' + yolo_name.split('.pt')[0] + 'batch' + str(batch))