import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import get_assets, get_asset_history, get_all_asset_ids
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="Crypto Explorer",
    layout="wide"
)

st.title("📊 Crypto Explorer Dashboard")
st.markdown("Visualize dados históricos de criptomoedas direto da CoinCap API.")

st.sidebar.header("🔎 Filtros")

# SIDEBAR: SELEÇÃO DE ATIVO

ativos_df = get_all_asset_ids()
selected_asset = st.sidebar.selectbox(
    "Escolha um criptoativo", 
    ativos_df["id"],
    format_func=lambda x: ativos_df[ativos_df["id"] == x]["name"].values[0]
)

limit = st.sidebar.slider("Quantidade de ativos no ranking", 5, 50, 10)

# SEÇÃO 1: RANKING GERAL

st.subheader("🏆 Top Criptoativos por Market Cap")

col1, col2 = st.columns(2)

with col1:
    df_assets = get_assets(limit)
    st.dataframe(df_assets[["id", "name", "symbol", "priceUsd", "marketCapUsd"]])

with col2:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(df_assets["name"][::-1], df_assets["marketCapUsd"][::-1])
    ax.set_title("Market Cap dos principais ativos")
    st.pyplot(fig)

# SEÇÃO 2: HISTÓRICO DO ATIVO

st.subheader(f"📈 Histórico de preços: {selected_asset.upper()}")

df_history = get_asset_history(selected_asset)
df_history["time"] = pd.to_datetime(df_history["time"])

col3, col4 = st.columns(2)

with col3:
    st.line_chart(df_history.set_index("time")["priceUsd"], use_container_width=True)

with col4:
    st.line_chart(df_history.set_index("time")["volumeUsd24h"], use_container_width=True)

st.markdown("⬇️ Histórico disponível para exportação em CSV:")
st.download_button("Download CSV", df_history.to_csv(index=False), file_name=f"{selected_asset}_history.csv")
