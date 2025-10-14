# src/main.py
import time
import numpy as np
import pandas as pd
from tqdm import tqdm
import os
import matplotlib
matplotlib.use('Agg')  # garante que o Matplotlib não abra janelas
import sys


from src.gerador_dados import gerar_dados_simulados
from src.solvers import maxent_newton, maxent_bfgs, maxent_lbfgs
from src.visualizacao import plotar_scaling
from src.utils.safe_runner import run_with_timeout

CSV_DIR = "resultados_csv"
GRAF_DIR = "resultados_graficos"
os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(GRAF_DIR, exist_ok=True)

# Parâmetros de teste
SIZES = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100] #[10, 50]       experimentos
TIMEOUT_PER_SOLVER = 30.0  # segundos (aumentado para evitar timeout)
NEWTON_MAX_N = 30         # roda Newton só se n <= 30

def monitor_system():
    try:
        import psutil
        return psutil.cpu_percent(interval=None), psutil.virtual_memory().percent
    except ImportError:
        return None, None

def executar_solver(nome, solver_fn, G, a, timeout_s=5.0):
    """
    Executa solver com timeout via safe_runner e retorna resultados
    """
    res = run_with_timeout(solver_fn, G, a, timeout_s=timeout_s)
    if res["status"] == "timeout":
        return None, 0, "timeout"
    elif res["status"] == "error":
        return None, 0, f"error:{res['error']}"
    else:
        p, iters = res["result"]
        return p, iters, "ok"

def main():
    all_results = []

    for n in SIZES:
        print(f"\n=== Running experiment for n_cidades = {n} ===")
        cidades, df_original, G, a = gerar_dados_simulados(n_cidades=n)

        solvers = []
        if n <= NEWTON_MAX_N:
            solvers.append(("Newton", maxent_newton))
        solvers.append(("BFGS", maxent_bfgs))
        solvers.append(("L-BFGS", maxent_lbfgs))

        # tqdm para mostrar progresso geral
        with tqdm(total=len(solvers), desc=f"Solvers (n={n})") as pbar:
            for nome, fn in solvers:
                start_time = time.perf_counter()
                # executar solver com timeout
                p, n_iter, status = executar_solver(nome, fn, G, a, timeout_s=TIMEOUT_PER_SOLVER)
                elapsed = time.perf_counter() - start_time

                cpu, mem = monitor_system()
                if p is not None:
                    mae = np.mean(np.abs(p - df_original.values.flatten()))
                    rmse = np.sqrt(np.mean((p - df_original.values.flatten())**2))
                else:
                    mae = None
                    rmse = None

                # salvar resultados
                all_results.append({
                    "n_cidades": n,
                    "metodo": nome,
                    "status": status,
                    "tempo_s": elapsed,
                    "iteracoes": n_iter,
                    "erro_mae": mae,
                    "erro_rmse": rmse,
                    "cpu_%": cpu,
                    "mem_%": mem
                })

                pbar.update(1)

    # Salvar CSV
    df_resultados = pd.DataFrame(all_results)
    arquivo_csv = os.path.join(CSV_DIR, "comparativo_maxent.csv")
    df_resultados.to_csv(arquivo_csv, index=False)
    print(f"\nCSV salvo em: {arquivo_csv}")

    # Gerar gráficos de escalabilidade (salvar em disco)
    try:
        plotar_scaling(df_resultados)
        print(f"Gráficos salvos em: {GRAF_DIR}")
    except Exception as e:
        print(f"Falha ao gerar gráficos: {e}")
    finally:
        import matplotlib.pyplot as plt
        plt.close('all')  # força fechamento de todas as figuras
    
    # Encerra o script de forma limpa
    sys.exit(0)

if __name__ == "__main__":
    main()
