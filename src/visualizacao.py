import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set(style="whitegrid")

def plotar_scaling(df_resultados, save_dir="resultados_graficos"):
    """
    Plota escalabilidade em função do número de cidades para todos os solvers.
    Salva gráficos em disco mesmo se alguns solvers falharem.
    """
    if df_resultados.empty:
        print("⚠️ DataFrame vazio, nenhum gráfico gerado.")
        return

    os.makedirs(save_dir, exist_ok=True)

    # Gráfico de Tempo de Execução
    plt.figure(figsize=(10,6))
    for metodo in df_resultados['metodo'].unique():
        subset = df_resultados[(df_resultados['metodo'] == metodo) & (df_resultados['tempo_s'].notnull())]
        if not subset.empty:
            plt.plot(subset['n_cidades'], subset['tempo_s'], marker='o', label=metodo)
    plt.xlabel('Número de Cidades')
    plt.ylabel('Tempo de Execução (s)')
    plt.yscale('log')
    plt.title('Escalabilidade - Tempo de Execução')
    plt.legend()
    plt.tight_layout()
    tempo_file = os.path.join(save_dir, "scaling_tempo.png")
    plt.savefig(tempo_file)
    plt.close()
    print(f"📁 Gráfico de tempo salvo em: {tempo_file}")

    # Gráfico de Erro MAE
    plt.figure(figsize=(10,6))
    for metodo in df_resultados['metodo'].unique():
        subset = df_resultados[(df_resultados['metodo'] == metodo) & (df_resultados['erro_mae'].notnull())]
        if not subset.empty:
            plt.plot(subset['n_cidades'], subset['erro_mae'], marker='o', label=metodo)
    plt.xlabel('Número de Cidades')
    plt.ylabel('Erro MAE')
    plt.title('Escalabilidade - Erro MAE')
    plt.legend()
    plt.tight_layout()
    erro_file = os.path.join(save_dir, "scaling_erro.png")
    plt.savefig(erro_file)
    plt.close()
    print(f"📁 Gráfico de erro salvo em: {erro_file}")
