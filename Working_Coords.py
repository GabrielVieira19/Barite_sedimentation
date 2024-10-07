import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
plt.ion()

def encontrar_indices_por_cv(nomes, cv):
    return [i for i, nome in enumerate(nomes) if cv in nome]

def separa_arquivos(file_names) : # Usamos para separar entre as capturas feitas pela câmera fotográfica e aquela feitas com a câmera de vigilância, pois a taxa FPS usada nas gravações são diferentes 
    file_names_fotografica = []
    file_names_vigilancia = []
    
    for nome in file_names:
        if 'Camera_' in nome: # Se foi capturada usando a câmera fotográfica, substitui-se Camera por F e teremos algo do tipo 'F_Cv12_1_1'
            nome = nome.replace('Camera', 'F')
            nome = nome.replace('.txt', '')
            file_names_fotografica.append(nome)
            
        elif 'Movie_' in nome: # Se foi capturada usando a câmera de vigilância, substitui-se Movie por V e teremos algo do tipo 'V_Cv12_1_1'
            nome = nome.replace('Movie', 'V')
            nome = nome.replace('.txt', '')
            file_names_vigilancia.append(nome)
    
    return file_names_vigilancia , file_names_fotografica 
               
def plotar_cv(ax, cv, indices, y_center_modified, titulo):
    total_pontos = np.arange(1, len(indices)+1)
    ax.scatter(total_pontos, y_center_modified[indices], c='black', s=2, edgecolor='black', facecolor='none')
    ax.set_title(titulo)
    if ax in (axs[0, 1], axs[1, 1]):  # Verifica se é na coluna da direita
        ax.set_ylabel('')  # Rótulo vazio para a coluna da direita
    else:
        ax.set_ylabel('Altura do clarificado (pixels)')
    ax.grid()
    
    # Ajusta-se o eixo X de acordo com a câmera utilizada 
    if 'vigilância' in titulo :
        ax.xaxis.set_major_formatter(FuncFormatter(formata_eixo_x_Vigilancia))
    elif 'fotográfica' in titulo :
        ax.xaxis.set_major_formatter(FuncFormatter(formata_eixo_x_Fotografica))
        
def formata_eixo_x_Fotografica(valor, pos):
    return f'{valor/1e3:.0f}'

def formata_eixo_x_Vigilancia(valor, pos):
    return f'{valor/5e1:.0f}'

#######################################################

dados = np.load('Coords.npz', allow_pickle=True)
file_names = dados['labels']
file_name_vigilancia , file_name_fotografica = separa_arquivos(file_names)
x_center = dados['X_center']
y_center = dados['Y_center']
height = dados['height']
width = dados['width']

# Encontrando os índices para cada CV específico referente as capturas feitas com a câmera fotográfica
indices_cv3_F = encontrar_indices_por_cv(file_name_fotografica, 'CV3%')
indices_cv6_F = encontrar_indices_por_cv(file_name_fotografica, 'CV6%')
indices_cv9_F = encontrar_indices_por_cv(file_name_fotografica, 'CV9%')
indices_cv12_F = encontrar_indices_por_cv(file_name_fotografica, 'CV12%')

# Encontrando os índices para cada CV específico referente as capturas feitas com a câmera de vigilânica
# notar que o Cv é procurado de outra forma, por conta da nomenclatura diferente dos arquivos 
indices_cv3_V = encontrar_indices_por_cv(file_name_vigilancia, 'Cv3')
indices_cv6_V = encontrar_indices_por_cv(file_name_vigilancia, 'Cv6')
indices_cv9_V = encontrar_indices_por_cv(file_name_vigilancia, 'Cv9')
indices_cv12_V = encontrar_indices_por_cv(file_name_vigilancia, 'Cv12')

y_center_modified = y_center + (height*1080) / 2

#######################################################

plt.close('all')
fig, axs = plt.subplots(2, 2, figsize=(6.5, 5), sharey=True)

# Plotando cada CV no seu respectivo gráfico
plotar_cv(axs[0, 0], 'CV3%', indices_cv3_F, y_center_modified, 'fotográfica CV3%')
plotar_cv(axs[0, 1], 'CV6%', indices_cv6_F, y_center_modified, 'fotográfica CV6%')
plotar_cv(axs[1, 0], 'CV9%', indices_cv9_F, y_center_modified, 'fotográfica CV9%')
plotar_cv(axs[1, 1], 'CV12%', indices_cv12_F, y_center_modified, 'fotográfica CV12%')

# Ajustando o layout
plt.tight_layout()
plt.savefig('Coords_fotográfica.png', dpi=300)
plt.close('all')

# Agora criamos outra imagem de mesmo "formato" para plotar os gráficos respectivos à câmera de vigilância
fig, axs = plt.subplots(2, 2, figsize=(6.5, 5), sharey=True)
plotar_cv(axs[0, 0], 'CV3%', indices_cv3_V, y_center_modified, 'vigilância CV3%')
plotar_cv(axs[0, 1], 'CV6%', indices_cv6_V, y_center_modified, 'vigilância CV6%')
plotar_cv(axs[1, 0], 'CV9%', indices_cv9_V, y_center_modified, 'vigilância CV9%')
plotar_cv(axs[1, 1], 'CV12%', indices_cv12_V, y_center_modified, 'vigilância CV12%')

plt.tight_layout()
plt.savefig('Coords_vigilância.png', dpi=300)

