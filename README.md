# 🎮 Análise de Dados de Jogos Steam (2021-2025)

Este projeto tem como objetivo analisar os jogos mais populares da Steam lançados entre 2021 e 2025, utilizando técnicas de análise exploratória de dados e visualização.

## 📚 Fonte de Dados

O dataset utilizado foi retirado do Kaggle:

🔗 [Steam Games Dataset (March 2025) - Kaggle](https://www.kaggle.com/datasets/artermiloff/steam-games-dataset?select=games_march2025_full.csv)

**Observação:**  
Devido às limitações do GitHub (tamanho máximo de arquivos de 100MB), o arquivo `.csv` não está disponível diretamente no repositório.  
Para reproduzir o projeto:
1. Faça o download do dataset no Kaggle.
2. Salve o arquivo em uma pasta chamada `/dataset/` na raiz do projeto.

## 🛠️ Tecnologias utilizadas

- Python 3.x
- Pandas
- Matplotlib
- PyArrow

## 📈 Estrutura do Projeto

```bash
├── analises/        # Gráficos gerados no projeto
├── dataset/         # (Ignorado no Git) - Onde colocar o CSV baixado
├── notebooks/       # Notebooks de limpeza e análise
├── README.md
├── requirements.txt
├── .gitignore
```

## 📊 Gráficos Gerados

### Top 10 Jogos Mais Avaliados (2021-2025)

![Top 10 Jogos Mais Avaliados](análises/top10_mais_avaliados.png)

### Distribuição dos Preços dos Jogos Pagos (até $100) - (2021–2025)

![Distribuição dos Preços dos Jogos Pagos](análises/distribuicao_precos_jogos_pagos_ate_100.png)

### Top 10 Gêneros (2021–2025)

![Top 10 Gêneros](análises/top10_generos.png)
