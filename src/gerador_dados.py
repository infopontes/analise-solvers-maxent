# Arquivo: src/gerador_dados.py
import numpy as np
import pandas as pd

def gerar_dados_simulados(n_cidades=10):
    """
    Gera uma matriz de fluxo aleatória e constrói as matrizes de restrição G e a.

    Args:
        n_cidades (int): O número de cidades para a simulação.

    Returns:
        tuple: cidades, df_prob_original, G_final, a_final
    """
    print(f"--- Gerando dados simulados para {n_cidades} cidades... ---")

    # Lista de cidades disponíveis
    todas_cidades_piaui = [
        "Teresina", "Parnaíba", "Picos", "Piripiri", "Floriano",
        "Campo Maior", "Barras", "União", "Altos", "Esperantina",
        "José de Freitas", "Pedro II", "Oeiras", "São Raimundo Nonato",
        "Miguel Alves", "Luzilândia", "Batalha", "Corrente", "Bom Jesus",
        "Piracuruca", "Cocal", "Uruçuí", "São João do Piauí", "Jaicós",
        "Paulistana", "Guadalupe", "Castelo do Piauí", "Fronteiras",
        "Inhuma", "Valença do Piauí"
    ]

    # Se n_cidades for maior que a lista, gerar nomes adicionais
    if n_cidades > len(todas_cidades_piaui):
        cidades = todas_cidades_piaui + [f"Cidade_{i}" for i in range(len(todas_cidades_piaui)+1, n_cidades+1)]
    else:
        cidades = todas_cidades_piaui[:n_cidades]

    # Matriz de fluxos aleatória
    fluxos_data = np.random.randint(10, 501, size=(n_cidades, n_cidades))
    np.fill_diagonal(fluxos_data, 0)

    fluxo_total = fluxos_data.sum()
    df_prob_original = pd.DataFrame(fluxos_data / fluxo_total, index=cidades, columns=cidades)

    # Construção das matrizes G e a
    n_variaveis = n_cidades * n_cidades
    prob_saidas = df_prob_original.sum(axis=1)
    prob_entradas = df_prob_original.sum(axis=0)

    n_restricoes_soma = n_cidades + n_cidades
    a_soma = np.concatenate([prob_saidas.values, prob_entradas.values]).reshape(-1, 1)
    G_soma = np.zeros((n_restricoes_soma, n_variaveis))
    for i in range(n_cidades):
        G_soma[i, (i * n_cidades):(i * n_cidades + n_cidades)] = 1
    for j in range(n_cidades):
        G_soma[n_cidades + j, np.arange(j, n_variaveis, n_cidades)] = 1

    # Remover última linha de soma para evitar dependência linear
    indices_para_remover = [n_cidades - 1, n_restricoes_soma - 1]
    G_soma_reduzido = np.delete(G_soma, indices_para_remover, axis=0)
    a_soma_reduzido = np.delete(a_soma, indices_para_remover, axis=0)

    # Restrições de diagonal (p_i,i = 0)
    n_restricoes_diag = n_cidades
    G_diag = np.zeros((n_restricoes_diag, n_variaveis))
    a_diag = np.zeros((n_restricoes_diag, 1))
    for i in range(n_cidades):
        indice_diagonal = i * n_cidades + i
        G_diag[i, indice_diagonal] = 1

    G_final = np.vstack([G_soma_reduzido, G_diag])
    a_final = np.vstack([a_soma_reduzido, a_diag])

    print("Dados gerados com sucesso.")
    return cidades, df_prob_original, G_final, a_final
