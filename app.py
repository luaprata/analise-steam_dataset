import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import pearsonr
import os

# Configurações iniciais da página
st.set_page_config(page_title="Steam Games Analysis", layout="wide")

# Título principal
st.title("🎮 Steam Games Analysis (2021-2025)")
st.markdown("---")

# Carregar os dados
@st.cache_data
def load_data():
    parquet_path = 'dataset/games_march2025_clean.parquet'

    if not os.path.exists(parquet_path):
        st.error(f"Arquivo {parquet_path} não encontrado no repositório.")
        st.stop()

    df = pd.read_parquet(parquet_path)
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['year'] = df['release_date'].dt.year
    df['month'] = df['release_date'].dt.month
    df['semester'] = df['year'].astype(str) + ' S' + df['release_date'].dt.month.apply(lambda x: '1' if x <= 6 else '2')
    return df

df = load_data()

# Menu lateral
menu = st.sidebar.selectbox(
    "Escolha a Análise",
    [
        "Top 10 Jogos Mais Avaliados",
        "Distribuição dos Preços",
        "Top 10 Gêneros",
        "Evolução dos Lançamentos",
        "Novos Questionamentos"
    ]
)

# 1. Top 10 Jogos Mais Avaliados
if menu == "Top 10 Jogos Mais Avaliados":
    st.header("📊 Top 10 Jogos Mais Avaliados")
    top10 = df.sort_values(by='num_reviews_total', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10,6))
    ax.barh(top10['name'], top10['num_reviews_total'])
    ax.invert_yaxis()
    ax.set_xlabel("Total de Avaliações")
    ax.set_title("Top 10 Jogos Mais Avaliados (2021-2025)")
    st.pyplot(fig)

# 2. Distribuição dos Preços
elif menu == "Distribuição dos Preços":
    st.header("💵 Distribuição dos Preços dos Jogos Pagos")
    max_price = st.slider("Selecione o Preço Máximo:", 0, 100, 50)

    df_paid = df[df['price'] > 0]
    fig, ax = plt.subplots(figsize=(10,6))
    ax.hist(df_paid[df_paid['price'] <= max_price]['price'], bins=30, color='#90caf9', edgecolor='black')
    ax.set_xlabel("Preço ($)")
    ax.set_ylabel("Quantidade de Jogos")
    ax.set_title(f"Distribuição dos Preços (até ${max_price})")
    st.pyplot(fig)

# 3. Top 10 Gêneros
elif menu == "Top 10 Gêneros":
    st.header("🏷️ Top 10 Gêneros Mais Frequentes")
    df['genres_clean'] = df['genres'].str.replace(r"[\[\]']", "", regex=True)
    df['primary_genre'] = df['genres_clean'].str.split(',').str[0]
    top_genres = df['primary_genre'].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10,6))
    top_genres.plot(kind='bar', color='#a5d6a7', edgecolor='black', ax=ax)
    ax.set_ylabel("Quantidade de Jogos")
    ax.set_title("Top 10 Gêneros (2021-2025)")
    st.pyplot(fig)

# 4. Evolução dos Lançamentos
elif menu == "Evolução dos Lançamentos":
    st.header("📈 Evolução dos Lançamentos de Jogos por Semestre")
    launches_per_semester = df['semester'].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(launches_per_semester.index, launches_per_semester.values, marker='o', color='#ab47bc')
    ax.set_xlabel("Semestre")
    ax.set_ylabel("Quantidade de Lançamentos")
    ax.set_title("Evolução dos Lançamentos de Jogos (2021-2025)")
    plt.xticks(rotation=45)
    plt.grid()
    plt.figtext(0.5, -0.05, '*Nota: Os dados de 2025 são parciais.', ha='center', fontsize=9, style='italic')
    st.pyplot(fig)

# 5. Novos Questionamentos
elif menu == "Novos Questionamentos":
    st.header("🔎 Novos Questionamentos e Análises")
    tab1, tab2, tab3 = st.tabs([
        "1. Preço x Avaliações",
        "2. Gêneros + Avaliações",
        "3. Sazonalidade"
    ])

    with tab1:
        st.subheader("1. Correlação entre Preço e Número de Avaliações")
        df_corr = df[df['price'] > 0][['price', 'num_reviews_total']].dropna()
        corr, _ = pearsonr(df_corr['price'], df_corr['num_reviews_total'])
        st.markdown(f"**Correlação de Pearson:** {corr:.2f}")

        fig, ax = plt.subplots(figsize=(10,6))
        sns.regplot(data=df_corr, x='price', y='num_reviews_total', scatter_kws={'alpha':0.3}, line_kws={'color':'red'}, ax=ax)
        ax.set_yscale('log')
        ax.set_xlabel("Preço ($)")
        ax.set_ylabel("Número de Avaliações (escala log)")
        ax.set_title("Relação entre Preço e Número de Avaliações (2021–2025)")
        st.pyplot(fig)

    with tab2:
        st.subheader("2. Gêneros com Melhores Avaliações Positivas")
        df_genres = df.dropna(subset=['genres'])
        df_genres['genres_clean'] = df_genres['genres'].str.replace(r"[\[\]']", "", regex=True)
        df_genres['genres_list'] = df_genres['genres_clean'].str.split(',')
        exploded = df_genres.explode('genres_list')
        exploded = exploded[exploded['num_reviews_total'] > 0]
        exploded['positive_ratio'] = exploded['num_reviews_positive'] / exploded['num_reviews_total']
        genre_scores = exploded.groupby('genres_list')['positive_ratio'].mean().sort_values(ascending=False).head(10)

        fig, ax = plt.subplots(figsize=(10,6))
        genre_scores.plot(kind='barh', color='lightgreen', ax=ax)
        ax.invert_yaxis()
        ax.set_xlabel("% de Avaliações Positivas")
        ax.set_ylabel("Gênero")
        ax.set_title("Top 10 Gêneros com Melhores Avaliações Positivas (2021–2025)\n(considerando todos os gêneros de cada jogo)")
        st.pyplot(fig)

    with tab3:
        st.subheader("3. Sazonalidade dos Lançamentos")
        monthly = df[df['year'] < 2025]['release_date'].dt.month.value_counts().sort_index()
        month_labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

        fig, ax = plt.subplots(figsize=(10,6))
        ax.bar(month_labels, monthly)
        ax.set_title("Lançamentos de Jogos por Mês (2021–2024)")
        ax.set_xlabel("Mês")
        ax.set_ylabel("Quantidade de Jogos Lançados")
        st.pyplot(fig)