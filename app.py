import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configurações iniciais da página
st.set_page_config(page_title="Steam Games Analysis", layout="wide")

# Título principal
st.title("🎮 Steam Games Analysis (2021-2025)")
st.markdown("---")

# Carregar os dados
@st.cache_data

def load_data():
    df = pd.read_csv('../dataset/games_march2025_clean.parquet')
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['year'] = df['release_date'].dt.year
    df['semester'] = df['release_date'].dt.year.astype(str) + ' S' + df['release_date'].dt.month.apply(lambda x: '1' if x <= 6 else '2')
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
    st.markdown("- Existe correlação entre preço e quantidade de avaliações?")
    st.markdown("- Quais gêneros têm as melhores médias de avaliações positivas?")
    st.markdown("- Existe sazonalidade nos lançamentos de jogos?")
    
    st.info("**Essas perguntas serão exploradas na Parte 2 do projeto!")
