import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from scipy.stats import pearsonr

st.set_page_config(page_title="Steam Games Analysis", layout="wide")
st.title("🎮 Steam Games Analysis (2021-2025)")
st.markdown("---")

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
    df['semester'] = df['release_date'].dt.year.astype(str) + ' S' + df['release_date'].dt.month.apply(lambda x: '1' if x <= 6 else '2')
    return df

df = load_data()

# Menu lateral
menu = st.sidebar.selectbox("Escolha a Análise", [
    "Top 10 Jogos Mais Avaliados",
    "Distribuição dos Preços",
    "Top 10 Gêneros",
    "Evolução dos Lançamentos",
    "Novos Questionamentos"
])

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
    df_genres = df[df['primary_genre'].str.strip() != '']
    top_genres = df_genres['primary_genre'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    top_genres.plot(kind='bar', color='#a5d6a7', edgecolor='black', ax=ax)
    ax.set_ylabel("Quantidade de Jogos")
    ax.set_xlabel("Gênero Principal")
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
    tabs = st.tabs(["Preço x Avaliações", "Gêneros + Avaliações", "Sazonalidade"])

    with tabs[0]:
        st.subheader("1. Correlação entre Preço e Número de Avaliações")
        filtered = df[(df['price'] <= 80) & (df['price'] > 0) & (df['num_reviews_total'] > 0)]
        corr, _ = pearsonr(filtered['price'], filtered['num_reviews_total'])
        st.markdown(f"**Correlação de Pearson:** {corr:.2f}")
        fig, ax = plt.subplots(figsize=(10,6))
        sns.regplot(data=filtered, x='price', y='num_reviews_total', scatter_kws={'alpha':0.3}, line_kws={'color':'red'}, ax=ax)
        ax.set_yscale('log')
        ax.set_xlabel("Preço ($)")
        ax.set_ylabel("Número de Avaliações (escala log)")
        ax.set_title("Relação entre Preço e Número de Avaliações (2021–2025)")
        st.pyplot(fig)

    with tabs[1]:
        st.subheader("2. Gêneros com Melhores Avaliações Positivas")
        df['genres_clean'] = df['genres'].str.replace(r"[\[\]']", "", regex=True)
        df['genres_list'] = df['genres_clean'].str.split(',')
        exploded = df.explode('genres_list')
        exploded = exploded[exploded['genres_list'].notna() & (exploded['genres_list'].str.strip() != '')]

        # Corrigir nomes de colunas conforme o dataset real
        if 'num_reviews_positive' in exploded.columns and 'num_reviews_total' in exploded.columns:
            exploded['positive_ratio'] = exploded['num_reviews_positive'] / exploded['num_reviews_total']
            genre_avg = exploded.groupby('genres_list')['positive_ratio'].mean().sort_values(ascending=False).head(10)
            fig, ax = plt.subplots(figsize=(10,6))
            genre_avg.sort_values().plot(kind='barh', color='#81c784', edgecolor='black', ax=ax)
            ax.set_xlabel("% de Avaliações Positivas")
            ax.set_ylabel("Gênero")
            ax.set_title("Top 10 Gêneros com Melhores Avaliações Positivas (2021–2025)\n(considerando todos os gêneros de cada jogo)")
            st.pyplot(fig)
        else:
            st.error("Colunas 'num_reviews_positive' ou 'num_reviews_total' não encontradas no dataset.")

    with tabs[2]:
        st.subheader("3. Lançamentos por Mês (2021–2024)")
        filtered = df[df['year'] < 2025]
        launches_by_month = filtered['month'].value_counts().sort_index()
        months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        fig, ax = plt.subplots(figsize=(10,6))
        ax.bar(months, launches_by_month)
        ax.set_xlabel("Mês")
        ax.set_ylabel("Quantidade de Jogos Lançados")
        ax.set_title("Lançamentos de Jogos por Mês (2021–2024)")
        st.pyplot(fig)