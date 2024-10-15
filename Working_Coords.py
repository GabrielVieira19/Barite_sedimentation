import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
plt.ion()

def encontrar_indices_por_cv(nomes, cv):
    return [i for i, nome in enumerate(nomes) if cv in nome]
               
def plotar_cv(ax, cv, indices, altura, titulo):
    total_pontos = np.arange(1, len(indices)+1)
    ax.scatter(total_pontos, altura[indices], c='black', s=2, edgecolor='black', facecolor='none')
    ax.set_title(titulo)
    if ax in (axs[0, 1], axs[1, 1]):  # Verifica se é na coluna da direita
        ax.set_ylabel('')  # Rótulo vazio para a coluna da direita
    else:
        ax.set_ylabel('Altura do clarificado (mm)')
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

# Dividi os dados em 2 arquivos por conta de problemas de sobreposição e complicação das operações, dessa forma consegui trabalhar bem com os dados 

dados_F = np.load('Coords_F.npz', allow_pickle=True)
dados_V = np.load('Coords_V.npz', allow_pickle=True)

# Separar as informações
file_names_fotografica = dados_F['labels']
file_names_vigilancia = dados_V['labels']

x_center_F = dados_F['X_center']
y_center_F = dados_F['Y_center']
height_F = dados_F['height']

x_center_V = dados_V['X_center']
y_center_V = dados_V['Y_center']
height_V = dados_V['height']

# Encontrando os índices para cada CV específico referente as capturas feitas com a câmera fotográfica
indices_cv3_F = encontrar_indices_por_cv(file_names_fotografica, 'CV3')
indices_cv6_F = encontrar_indices_por_cv(file_names_fotografica, 'CV6')
indices_cv9_F = encontrar_indices_por_cv(file_names_fotografica, 'CV9')
indices_cv12_F = encontrar_indices_por_cv(file_names_fotografica, 'CV12')

# Encontrando os índices para cada CV específico referente as capturas feitas com a câmera de vigilânica
# notar que o Cv é procurado de outra forma, por conta da nomenclatura diferente dos arquivos 
indices_cv3_V = encontrar_indices_por_cv(file_names_vigilancia, 'Cv3')
indices_cv6_V = encontrar_indices_por_cv(file_names_vigilancia, 'Cv6')
indices_cv9_V = encontrar_indices_por_cv(file_names_vigilancia, 'Cv9')
indices_cv12_V = encontrar_indices_por_cv(file_names_vigilancia, 'Cv12')

altura_clareficado_V = y_center_V + (height_V * 1920) / 8.2
altura_clareficado_F = y_center_F + (height_F * 920) / 4.25

#######################################################

plt.close('all')
fig, axs = plt.subplots(2, 2, figsize=(6.5, 5), sharey=True)

# Plotando cada CV no seu respectivo gráfico
plotar_cv(axs[0, 0], 'CV3%', indices_cv3_F, altura_clareficado_F, 'fotográfica CV3%')
plotar_cv(axs[0, 1], 'CV6%', indices_cv6_F, altura_clareficado_F, 'fotográfica CV6%')
plotar_cv(axs[1, 0], 'CV9%', indices_cv9_F, altura_clareficado_F, 'fotográfica CV9%')
plotar_cv(axs[1, 1], 'CV12%', indices_cv12_F, altura_clareficado_F, 'fotográfica CV12%')

# Ajustando o layout
plt.tight_layout()
plt.savefig('Coords_fotográfica.png', dpi=300)
plt.close('all')

# Agora criamos outra imagem de mesmo "formato" para plotar os gráficos respectivos à câmera de vigilância
fig, axs = plt.subplots(2, 2, figsize=(6.5, 5), sharey=True)
plotar_cv(axs[0, 0], 'CV3%', indices_cv3_V, altura_clareficado_V, 'vigilância CV3%')
plotar_cv(axs[0, 1], 'CV6%', indices_cv6_V, altura_clareficado_V, 'vigilância CV6%')
plotar_cv(axs[1, 0], 'CV9%', indices_cv9_V, altura_clareficado_V, 'vigilância CV9%')
plotar_cv(axs[1, 1], 'CV12%', indices_cv12_V, altura_clareficado_V, 'vigilância CV12%')

plt.tight_layout()
plt.savefig('Coords_vigilância.png', dpi=300)

