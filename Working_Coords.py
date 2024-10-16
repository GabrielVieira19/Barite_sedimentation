import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 
plt.ion()

def encontrar_indices_por_cv(nomes, cv):
    return [i for i, nome in enumerate(nomes) if cv in nome]

def calcular_tempo_acumulado(indices, fps): # Tempo que será usado para o ajuste do eixo X 
    qtd_frames = len(indices)
    tempo_video = (qtd_frames / fps) / 60  # Tempo já é dado em minutos
    return tempo_video
               
def plotar_cv(ax, cv, indices, altura, tempo, titulo):
    ax.scatter(np.linspace(0,tempo,len(indices)), altura[indices], c='black', s=2, edgecolor='black', facecolor='none')
    ax.set_title(titulo)
    if ax in (axs[0, 1], axs[1, 1]):  # Verifica se é na coluna da direita
        ax.set_ylabel('')  # Rótulo vazio para a coluna da direita
    else:
        ax.set_ylabel('Altura do clarificado (mm)')
        
    ax.set_xlabel('Tempo de Captura (min)', fontsize = 8)
    
    ax.minorticks_on()
    
    # Adicionar grids aos plots
    ax.grid(which='both', linestyle='--', linewidth=0.5)  # Grids principais
    ax.grid(which='minor', linestyle=':', linewidth=0.5)  # Grids menores
    
    # Ajustar os "passos" do Eixo X 
    if 'CV12%' in titulo : 
        ax.xaxis.set_major_locator(ticker.MultipleLocator(10)) # Passos de 10 em 10 min para o plot do CV12%
    else : 
        ax.xaxis.set_major_locator(ticker.MultipleLocator(5)) # Passos de 5 em 5 min para os demais plots

    # Aplica-se os minor grids de acordo com a quantidade necessária (10)
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(4))  # minor ticks no eixo X
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(4))  # minor ticks no eixo Y
    
    ax.grid(True)
    
# Dividi os dados em 2 arquivos por conta de problemas de sobreposição e complicação das operações, dessa forma consegui trabalhar bem com os dados 

dados_F = np.load('Coords_F.npz', allow_pickle=True)
dados_V = np.load('Coords_V.npz', allow_pickle=True)

# Separar as informações de acordo com os metodos de captura 
# Dados da câmera fotográfica 
file_names_fotografica = dados_F['labels']
x_center_F = dados_F['X_center']
y_center_F = dados_F['Y_center']
height_F = dados_F['height']

# Dados da câmera de vigilância
file_names_vigilancia = dados_V['labels']
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

# Calcular os tempos acumulados para cada CV fotográfico
tempo_cv3_F = calcular_tempo_acumulado(indices_cv3_F, 60)
tempo_cv6_F = calcular_tempo_acumulado(indices_cv6_F, 30)
tempo_cv9_F = calcular_tempo_acumulado(indices_cv9_F, 30)
tempo_cv12_F = calcular_tempo_acumulado(indices_cv12_F, 30)

# Calular os tempos acumulados para cada CV de vigilância
tempo_cv3_V = calcular_tempo_acumulado(indices_cv3_V, 1)
tempo_cv6_V = calcular_tempo_acumulado(indices_cv6_V, 1)
tempo_cv9_V = calcular_tempo_acumulado(indices_cv9_V, 1)
tempo_cv12_V = calcular_tempo_acumulado(indices_cv12_V, 1)

# Para cada método de aquisição usa-se uma escala de conversão de pixels -> mm 
altura_clareficado_V = y_center_V + (height_V * 1920) / 8.2
altura_clareficado_F = y_center_F + (height_F * 920) / 4.25

# Iniciamos as plotagens 
plt.close('all')
fig, axs = plt.subplots(2, 2, figsize=(6.5, 5), sharey=True)

# Plotando cada CV no seu respectivo gráfico
plotar_cv(axs[0, 0], 'CV3%', indices_cv3_F, altura_clareficado_F,tempo_cv3_F, 'fotográfica CV3%')
plotar_cv(axs[0, 1], 'CV6%', indices_cv6_F, altura_clareficado_F,tempo_cv6_F, 'fotográfica CV6%')
plotar_cv(axs[1, 0], 'CV9%', indices_cv9_F, altura_clareficado_F,tempo_cv9_F, 'fotográfica CV9%')
plotar_cv(axs[1, 1], 'CV12%', indices_cv12_F, altura_clareficado_F,tempo_cv12_F, 'fotográfica CV12%')

# Ajustando o layout
plt.tight_layout()
plt.savefig('Coords_fotográfica.png', dpi=300)
plt.close('all')

# Agora criamos outra imagem de mesmo "formato" para plotar os gráficos respectivos à câmera de vigilância
fig, axs = plt.subplots(2, 2, figsize=(6.5, 5), sharey=True)
plotar_cv(axs[0, 0], 'CV3%', indices_cv3_V, altura_clareficado_V,tempo_cv3_V,'vigilância CV3%')
plotar_cv(axs[0, 1], 'CV6%', indices_cv6_V, altura_clareficado_V,tempo_cv6_V,'vigilância CV6%')
plotar_cv(axs[1, 0], 'CV9%', indices_cv9_V, altura_clareficado_V,tempo_cv9_V,'vigilância CV9%')
plotar_cv(axs[1, 1], 'CV12%', indices_cv12_V, altura_clareficado_V,tempo_cv9_V, 'vigilância CV12%')

plt.tight_layout()
plt.savefig('Coords_vigilância.png', dpi=300)

