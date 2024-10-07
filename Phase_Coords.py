import numpy as np 
import os 
import re 

Coords = {} #Criamos o dicionário que será utilizado 

for predict in os.listdir("runs/detect/predicts") : # Percorre-se cada pasta predict de cada concentração e repetição 
    i = 0 
    video = predict
    file_count = len(os.listdir("runs/detect/predicts/" + predict + "/labels")) #Quantos arquivos temos na pasta analisada 
    print(f"{predict} - Quantidade de arquivos a serem processados = {file_count}")
    
    def extrair_numero(nome_arquivo): # Ordenar corretamente os arquivos a partir da numeração 
        match = re.search(r'_(\d+)\.txt$', nome_arquivo)
        return int(match.group(1)) if match else float('inf')

    lista = os.listdir("runs/detect/predicts/" + predict + "/labels")
    lista_sort = sorted(lista, key=extrair_numero)

    for label in lista_sort : # Dentro de cada pasta labels percorremos por todos os arquivos .txt de label 
        try:
            with open("runs/detect/predicts/" + predict + "/labels/" + label) as file : # Abrimos cada arquivo .txt para extrair os valores de alura que serão armazenados no dicionário
                arq = file.read() 
            
        except Exception as e:
            print(f"Erro ao ler o arquivo {label}: {e}") 
            
        parts = arq.strip().split()
        
        # Retiramos cada informação do arquivo 
        classe = float(parts[0])
        X_center = float(parts[1])
        Y_center = float(parts[2])    
        width = float(parts[3])
        height = float(parts[4]) 
            
        # Criamos um dicionário dentro do dicionário para cada label.txt e colocamos o valor da altura 
        Coords[label] = {
            "Classe" : classe ,
            "X center" : X_center ,
            "Y center" : Y_center ,
            "Width" : width ,
            "Height": height 
        }
       
        if i == round(file_count/100)*25 :
            print(f"{video} 25% concluido")
            
        if i == round(file_count/100)*50 :
            print(f"{video} 50% concluido")
            
        if i == round(file_count/100)*75 :
            print(f"{video} 75% concluido")
            
        if i == file_count-1 : 
            print(f"{video} 100% concluido")
        
        i += 1 
        
# Transformamos o dicionário em uma lista Numpy para exportar como .npz 
labels = list(Coords.keys())
class_values = np.array([coords['Classe'] for coords in Coords.values()])
X_center_values = np.array([coords['X center'] for coords in Coords.values()])
Y_center_values = np.array([coords['Y center'] for coords in Coords.values()])
height_values = np.array([coords['Height'] for coords in Coords.values()])
width_values = np.array([coords['Width'] for coords in Coords.values()])

# Salvando em um arquivo .npz
np.savez('Coords.npz', labels=labels, classe=class_values, X_center=X_center_values, Y_center=Y_center_values, height=height_values, width=width_values)
print("Processo finalizado")
            
            
        