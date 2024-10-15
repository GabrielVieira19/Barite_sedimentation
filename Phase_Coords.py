import numpy as np 
import os 
import re 

# Nessa versão usei 2 diferentes dicionários para separar os dados das capturas, a fim de facilitar o processamento destes posteriormente 

Coords_F = {} # Dicionário para cada tipo de captura  
Coords_V = {} # Dicionário para cada tipo de captura  

paths = ['runs/detect/predicts/Predicts_F/' , 'runs/detect/predicts/Predicts_V/']
   
for path in paths :   
    for predict in os.listdir(path) : # Percorre-se cada pasta predict de cada concentração e repetição   
        i = 0 
        video = predict
        file_count = len(os.listdir(path + predict + "/labels")) #Quantos arquivos temos na pasta analisada 
        print(f"{predict} - Quantidade de arquivos a serem processados = {file_count}")

        def extrair_numero(nome_arquivo): # Ordenar corretamente os arquivos a partir da numeração 
            match = re.search(r'_(\d+)\.txt$', nome_arquivo)
            return int(match.group(1)) if match else float('inf')

        lista = os.listdir(path + predict + "/labels")
        lista_sort = sorted(lista, key=extrair_numero)

        for label in lista_sort : # Dentro de cada pasta labels percorremos por todos os arquivos .txt de label 
            
            if "Predicts_F" in path : 
                Coords = Coords_F
                aux = 'F'
            elif "Predicts_V" in path : 
                Coords = Coords_V
                aux = 'V'
                
            try:
                with open(path + predict + "/labels/" + label) as file : # Abrimos cada arquivo .txt para extrair os valores de alura que serão armazenados no dicionário
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
    class_values = np.array([Coords['Classe'] for Coords in Coords.values()])
    X_center_values = np.array([Coords['X center'] for Coords in Coords.values()])
    Y_center_values = np.array([Coords['Y center'] for Coords in Coords.values()])
    height_values = np.array([Coords['Height'] for Coords in Coords.values()])
    width_values = np.array([Coords['Width'] for Coords in Coords.values()])

    # Salvando em um arquivo .npz
    np.savez(f'Coords_{aux}.npz', labels=labels, classe=class_values, X_center=X_center_values, Y_center=Y_center_values, height=height_values, width=width_values)
    print("Processo finalizado")
            
            
        