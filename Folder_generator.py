import cv2
import os
import random
import shutil

# Função para definir as pastas e alocar as imagens de acordo com o tamanho de cada pasta 
def selectFolder(i, size_train, size_test, size_val, size_run):
    if(i+1 <= size_train):
        folder = 'train'
    elif(i+1 <= size_train + size_test):
        folder = 'test'
    elif(i+1 <=  size_val + size_train + size_test):
        folder = 'val'
    else:
        folder = 'run'

    path = str((os.getcwd()).replace("\\", "/")) + '/datasets'
    if not os.path.exists(path): os.mkdir(path)
    path = path + '/' + folder
    return path

#Carregamento dos arquivos (Imagens e Labels vindos do LabelStudio)
path_folder = str((os.getcwd()).replace("\\", "/"))

#Listagem das iamgens, presentes na pasta images 
path_image = path_folder + '/Coords/images' # Diretório obtido via exportação do label studio e alocado no diretório escolhido
images = os.listdir(path_image)
list_images = [] 

#Listagem dos labels referentes às imagens de mesma numeração, presentes na pasta labels
path_labels = path_folder + '/Coords/labels'
labels = os.listdir(path_labels)
list_labels = []

#Colocando as imagens na lista 
for image in images:
    if (".png" in image): list_images.append(image) #Confirmar que estaremos apenas pegando arquivos de imagem, contendo .png 
images = list_images
random.shuffle(images)

#Pegamos todos os label.txt presentes também  
for label in labels:
    if (".txt" in label): list_labels.append(label)
labels = list_labels

size_train = int(0.35*len(images)) #Define-se como padrão esses tamanhos dos diretórios que serão utilizados no treinamento 
size_test = int(0.15*len(images))
size_val = int(0.15*len(images))
size_run = len(images) - (size_train + size_test + size_val) # Testes nunca vistos antes
if(size_run) <= 0:
    print('Teste deu negativo')

# Separamos as imagens e buscamos o label referente a essa imagem 
for i,image in enumerate(images):
    img = cv2.imread(path_image + '/' + image)
    file_name =  image[:-4] # Retirar .png do nome
    if (file_name + '.txt') in labels :
        file_label =  file_name + '.txt'
    
    #Cria-se os diretórios das pastas se ainda não existirem 
    path_aplication = selectFolder(i, size_train, size_test, size_val, size_run)
    if not os.path.exists(path_aplication): os.mkdir(path_aplication)
    
    #Preenche os diretórios com as imagens, evitando repetições e respeitando a quantidade de imagens imposta pelo "_size"
    path_ap_images = path_aplication + '/images'
    if not os.path.exists(path_ap_images): os.mkdir(path_ap_images)
    shutil.copyfile(path_image + '/' + file_name +'.png', path_ap_images + '/' + file_name +'.png')

    #Repete-se o processo porém agora com os labels, respeitando a equivalência label/image e a quatidade necessária
    path_ap_text = path_aplication + '/labels'
    if not os.path.exists(path_ap_text): os.mkdir(path_ap_text)
    shutil.copyfile(path_labels + '/' + file_label , path_ap_text + '/' + file_name + '.txt')