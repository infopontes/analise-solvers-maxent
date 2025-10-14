# Análise Comparativa de Solvers para o Problema de Máxima Entropia

Este projeto implementa e realiza um benchmark comparativo de três métodos de otimização numérica para resolver o problema de estimação de matriz de fluxo (Origem-Destino) usando o princípio da Máxima Entropia (MaxEnt).

O sistema primeiro gera uma matriz de fluxo simulada para um número configurável de cidades (e.g., 10, 20, 30, 40, 50) e, em seguida, utiliza apenas os totais marginais (somas de linhas e colunas) e a restrição de diagonal nula como evidência para estimar a matriz original. O objetivo é comparar a performance, precisão e escalabilidade dos seguintes algoritmos:

1.  **Método de Newton Puro:** Utiliza a matriz Hessiana exata para uma convergência quadrática.
2.  **BFGS:** Um método Quase-Newton que aproxima a Hessiana.
3.  **L-BFGS:** Uma variante do BFGS otimizada para consumir menos memória.

## Estrutura do Projeto

O projeto está organizado em um pacote `src` para separar as responsabilidades, seguindo boas práticas de desenvolvimento em Python.

```
/
├── src/
│   ├── __init__.py
│   ├── gerador_dados.py      # Simula os dados de fluxo e cria as restrições (G e a).
│   ├── solvers.py            # Contém os 3 algoritmos de otimização.
│   ├── visualizacao.py       # Gera os gráficos comparativos.
│   └── main.py               # Orquestra a execução do experimento.
│
├── .gitignore            # Especifica os arquivos e pastas a serem ignorados pelo Git.
├── README.md             # Esta documentação.
└── requirements.txt      # Lista de dependências do projeto.
```

## Análise dos Resultados

A execução do benchmark em diferentes escalas (`n_cidades = [10, 20, 30, 40, 50]`) revelou um claro trade-off entre os métodos:

* **Precisão:** O **Método de Newton** consistentemente alcança a maior precisão (menor erro), na ordem de `1e-16`. Os métodos Quase-Newton (BFGS e L-BFGS) também são muito precisos, com erros estáveis na ordem de `1e-8`.

* **Escalabilidade e Tempo:**
    * Para problemas pequenos (10 cidades), o Newton é o mais rápido.
    * Um **ponto de virada** ocorre em torno de 20 cidades, onde o custo computacional do Newton explode, e o L-BFGS se torna mais eficiente.
    * Para problemas maiores (30+ cidades), o **L-BFGS** demonstra uma escalabilidade muito superior, sendo ordens de magnitude mais rápido que o Newton.

**Conclusão:** O **L-BFGS** é o algoritmo de escolha para este problema em qualquer cenário que não seja de pequena escala, oferecendo o melhor balanço entre velocidade, escalabilidade e alta precisão.

## Pré-requisitos

* Python 3.8+
* Git

## Instalação

1.  Clone este repositório para sua máquina local:
    ```bash
    git clone [https://github.com/infopontes/analise-solvers-maxent.git)
    cd SEU_REPOSITORIO
    ```

2.  Crie e ative um ambiente virtual (altamente recomendado):
    ```bash
    # Criar o ambiente
    python -m venv .venv

    # Ativar no Windows
    .venv\Scripts\activate

    # Ativar no macOS/Linux
    source .venv/bin/activate
    ```

3.  Instale as dependências listadas no `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Como Executar

Com o ambiente virtual ativado e as dependências instaladas, execute o seguinte comando a partir da **pasta raiz do projeto**:

```bash
python -m src.main
```

O script irá imprimir o progresso de cada solver no console e, ao final, salvará os resultados numéricos na pasta `resultados_csv/` e os gráficos comparativos na pasta `resultados_graficos/`.